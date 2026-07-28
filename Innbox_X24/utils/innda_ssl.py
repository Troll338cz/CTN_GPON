from __future__ import annotations

import hashlib
import os
import base64
import textwrap
from dataclasses import dataclass
from typing import Optional, Tuple, Type

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


SALT_HEADER = b"Salted__"  # matches the literal used in the C code
SALT_LEN = 8
HEADER_LEN = len(SALT_HEADER) + SALT_LEN  # 16 bytes, same as v47 in the C code
CHUNK_SIZE = 512  # mirrors the 0x200 fread() chunk size in the original code


class CipherError(Exception):
    """Raised for anything that mirrors the C code's `sub_CE0(4, ...)` error logs."""


@dataclass(frozen=True)
class CipherSpec:
    algorithm: Type
    key_len: int
    iv_len: int
    mode_factory: Optional[callable]  # takes iv bytes (or None) -> Mode instance
    block_cipher: bool  # whether PKCS7 padding must be applied


def _cbc(iv: bytes):
    return modes.CBC(iv)


def _cfb(iv: bytes):
    return modes.CFB(iv)


def _ofb(iv: bytes):
    return modes.OFB(iv)


def _ctr(iv: bytes):
    return modes.CTR(iv)


def _ecb(_iv: Optional[bytes]):
    return modes.ECB()


# Equivalent to what EVP_get_cipherbyname("<name>") would resolve to.
# Extend this table if you need more of OpenSSL's cipher names.
_CIPHERS = {
    "aes-128-cbc": CipherSpec(algorithms.AES, 16, 16, _cbc, True),
    "aes-192-cbc": CipherSpec(algorithms.AES, 24, 16, _cbc, True),
    "aes-256-cbc": CipherSpec(algorithms.AES, 32, 16, _cbc, True),
    "aes-128-ecb": CipherSpec(algorithms.AES, 16, 0, _ecb, True),
    "aes-192-ecb": CipherSpec(algorithms.AES, 24, 0, _ecb, True),
    "aes-256-ecb": CipherSpec(algorithms.AES, 32, 0, _ecb, True),
    "aes-128-cfb": CipherSpec(algorithms.AES, 16, 16, _cfb, False),
    "aes-192-cfb": CipherSpec(algorithms.AES, 24, 16, _cfb, False),
    "aes-256-cfb": CipherSpec(algorithms.AES, 32, 16, _cfb, False),
    "aes-128-ofb": CipherSpec(algorithms.AES, 16, 16, _ofb, False),
    "aes-192-ofb": CipherSpec(algorithms.AES, 24, 16, _ofb, False),
    "aes-256-ofb": CipherSpec(algorithms.AES, 32, 16, _ofb, False),
    "aes-128-ctr": CipherSpec(algorithms.AES, 16, 16, _ctr, False),
    "aes-192-ctr": CipherSpec(algorithms.AES, 24, 16, _ctr, False),
    "aes-256-ctr": CipherSpec(algorithms.AES, 32, 16, _ctr, False),
    "des-ede3-cbc": CipherSpec(algorithms.TripleDES, 24, 8, _cbc, True),
    "des-ede3": CipherSpec(algorithms.TripleDES, 24, 0, _ecb, True),
}


def get_cipher_spec(cipher_name: str) -> CipherSpec:
    """Equivalent of EVP_get_cipherbyname(); raises CipherError if unsupported."""
    spec = _CIPHERS.get(cipher_name.lower())
    if spec is None:
        raise CipherError(f"cipher not supported: {cipher_name}")
    return spec


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int,
                      count: int = 1, digest=hashlib.md5) -> Tuple[bytes, bytes]:
    """
    Re-implementation of OpenSSL's EVP_BytesToKey(EVP_md5(), salt, password,
    password_len, count, key_out, iv_out) as used in the original C code.
    """
    derived = b""
    prev = b""
    while len(derived) < key_len + iv_len:
        h = digest(prev + password + salt)
        prev = h.digest()
        for _ in range(count - 1):
            prev = digest(prev).digest()
        derived += prev
    return derived[:key_len], derived[key_len:key_len + iv_len]


def _build_cipher(spec: CipherSpec, key: bytes, iv: bytes):
    mode = spec.mode_factory(iv if spec.iv_len else None)
    return Cipher(spec.algorithm(key), mode)


def _wrap_base64(data: bytes, line_len: int = 64) -> bytes:
    encoded = base64.b64encode(data).decode("ascii")
    return ("\n".join(textwrap.wrap(encoded, line_len)) + "\n").encode("ascii")


# ---------------------------------------------------------------------------
# innda_ssl_enc
# ---------------------------------------------------------------------------
def innda_ssl_enc(cipher_name: str, password: str, use_base64: bool,
                   src_path: str, dst_path: str) -> int:
    """
    Encrypt `src_path` into `dst_path` using `cipher_name` (e.g. "aes-256-cbc")
    with a password-derived key, mirroring the C `innda_ssl_enc` function.

    Returns 0 on success, -1 on failure (logging the reason), matching the
    original function's return convention.
    """
    if not password:
        print("innda_ssl_enc: no password")
        return -1

    try:
        spec = get_cipher_spec(cipher_name)
    except CipherError as e:
        print(f"innda_ssl_enc: {e}")
        return -1

    try:
        with open(src_path, "rb") as fin:
            plaintext = fin.read()
    except OSError as e:
        print(f"innda_ssl_enc: fopen error: {e}")
        return -1

    salt = os.urandom(SALT_LEN)
    header = SALT_HEADER + salt

    key, iv = evp_bytes_to_key(password.encode(), salt, spec.key_len, spec.iv_len)

    cipher = _build_cipher(spec, key, iv)
    encryptor = cipher.encryptor()

    data = plaintext
    if spec.block_cipher:
        block_bits = spec.algorithm.block_size
        padder = sym_padding.PKCS7(block_bits).padder()
        data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(data) + encryptor.finalize()

    try:
        with open(dst_path, "wb") as fout:
            if use_base64:
                fout.write(_wrap_base64(header + ciphertext))
            else:
                fout.write(header)
                fout.write(ciphertext)
    except OSError as e:
        print(f"innda_ssl_enc: fwrite error: {e}")
        return -1

    return 0


# ---------------------------------------------------------------------------
# innda_ssl_dec
# ---------------------------------------------------------------------------
def innda_ssl_dec(cipher_name: str, password: str, use_base64: bool,
                   src_path: str, dst_path: str) -> int:
    """
    Decrypt `src_path` into `dst_path`, mirroring the C `innda_ssl_dec`
    function. Returns 0 on success, -1 on failure.
    """
    if not password:
        print("innda_ssl_dec: no password")
        return -1

    try:
        spec = get_cipher_spec(cipher_name)
    except CipherError as e:
        print(f"innda_ssl_dec: {e}")
        return -1

    try:
        with open(src_path, "rb") as fin:
            raw = fin.read()
    except OSError as e:
        print(f"innda_ssl_dec: fopen error: {e}")
        return -1

    if use_base64:
        try:
            raw = base64.b64decode(raw, validate=False)
        except Exception as e:
            print(f"innda_ssl_dec: base64 decode failed: {e}")
            return -1

    if len(raw) < HEADER_LEN or raw[:len(SALT_HEADER)] != SALT_HEADER:
        print("innda_ssl_dec: no salt head found.")
        return -1

    salt = raw[len(SALT_HEADER):HEADER_LEN]
    ciphertext = raw[HEADER_LEN:]

    key, iv = evp_bytes_to_key(password.encode(), salt, spec.key_len, spec.iv_len)

    cipher = _build_cipher(spec, key, iv)
    decryptor = cipher.decryptor()

    try:
        data = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        print(f"innda_ssl_dec: EVP_CipherFinal_ex failed: {e}")
        return -1

    if spec.block_cipher:
        try:
            block_bits = spec.algorithm.block_size
            unpadder = sym_padding.PKCS7(block_bits).unpadder()
            data = unpadder.update(data) + unpadder.finalize()
        except Exception as e:
            print(f"innda_ssl_dec: bad padding (wrong password/cipher?): {e}")
            return -1

    try:
        with open(dst_path, "wb") as fout:
            fout.write(data)
    except OSError as e:
        print(f"innda_ssl_dec: fwrite error: {e}")
        return -1

    return 0

