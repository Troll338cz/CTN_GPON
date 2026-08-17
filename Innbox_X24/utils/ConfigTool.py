#!/usr/bin/env python3
import argparse
import gzip
import hashlib
import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

def generate_hash_enc_pass(model_name: str, customer_name: str):
    model_bytes = model_name.encode('latin1')
    cust_bytes = customer_name.encode('latin1')
    buf = bytearray(256)

    len_model = len(model_bytes)
    len_cust = len(cust_bytes)
    for i in range(256):
        v7 = (i & 0x0F) + 49
        if i < len_model:
            buf[i] = (v7 + model_bytes[i]) & 0xFF
        elif i >= 256 - len_cust:
            buf[i] = (v7 + cust_bytes[i - (256 - len_cust)]) & 0xFF
        else:
            buf[i] = v7 & 0xFF
    return bytes(buf)

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16):
    derived = b""
    prev = b""
    while len(derived) < key_len + iv_len:
        h = hashlib.md5(prev + password + salt)
        prev = h.digest()
        derived += prev
    return derived[:key_len], derived[key_len:key_len + iv_len]

def compute_v17_checksum(openssl_stream):
    """Calculates 2-byte hex XOR checksum (sub_2E00) across the OpenSSL stream."""
    xor_val = 0
    for b in openssl_stream:
        xor_val ^= b
    return f"{xor_val:02x}".encode('ascii')

def parse_header(raw_data):
    salted_idx = raw_data.find(b"Salted__")
    if salted_idx == -1:
        raise ValueError("Salted__ magic header not found in binary.")

    v17 = raw_data[:2]
    v21 = raw_data[2:salted_idx]
    return v17, v21, salted_idx

def decrypt_bin(raw_data: bytes, model_name: str, customer_name: str) -> bytes:
    v17, _, salted_idx = parse_header(raw_data)
    len_v17 = len(v17)

    clean_stream = bytearray()
    pos = salted_idx

    for chunk_size in (1024, 2048, 3072, 4096, 5120):
        if pos + chunk_size + len_v17 <= len(raw_data):
            if raw_data[pos + chunk_size : pos + chunk_size + len_v17] == v17:
                clean_stream.extend(raw_data[pos : pos + chunk_size])
                pos += chunk_size + len_v17
                continue
        break

    clean_stream.extend(raw_data[pos:])

    salt = clean_stream[8:16]
    ciphertext = bytes(clean_stream[16:])

    password = generate_hash_enc_pass(model_name, customer_name)
    key, iv = evp_bytes_to_key(password, salt, key_len=32, iv_len=16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(128).unpadder()
    compressed_data = unpadder.update(padded_plaintext) + unpadder.finalize()

    return gzip.decompress(compressed_data)

def encrypt_xml(xml_bytes: bytes, model_name: str, customer_name: str, image_sign: str) -> bytes:
    compressed = gzip.compress(xml_bytes)
    salt = os.urandom(8)
    password = generate_hash_enc_pass(model_name, customer_name)
    key, iv = evp_bytes_to_key(password, salt, key_len=32, iv_len=16)

    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(compressed) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    openssl_stream = b"Salted__" + salt + ciphertext

    v17 = compute_v17_checksum(openssl_stream)
    v21 = image_sign.encode('ascii')

    out = bytearray()
    out.extend(v17)
    out.extend(v21)

    pos = 0
    rem = len(openssl_stream)

    for chunk_size in (1024, 2048, 3072, 4096, 5120):
        if chunk_size >= rem:
            break
        out.extend(openssl_stream[pos : pos + chunk_size])
        pos += chunk_size
        rem -= chunk_size
        out.extend(v17)

    out.extend(openssl_stream[pos:])
    return bytes(out)

# customer = from nvram "fad config getenv customer_id" = "Iskratel"
# model = cfg_getstr(v11, 16, "/InternetGatewayDevice/DeviceInfo/ModelName"); = InnboxX24
# signature = /etc/config/image_sign = "Iskratel_InnboxX24" -- This is also in header of backup file itself...

def main():
    parser = argparse.ArgumentParser(description="Iskratel Innbox Configuration Tool")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    dec_parser = subparsers.add_parser("decrypt", help="Decrypt .bin to .xml")
    dec_parser.add_argument("-i", "--input", required=True, help="Input config.bin")
    dec_parser.add_argument("-o", "--output", required=True, help="Output config.xml")
    dec_parser.add_argument("-m", "--model", default="InnboxX24", help="Model Name")
    dec_parser.add_argument("-c", "--customer", default="Iskratel", help="Customer Name")

    enc_parser = subparsers.add_parser("encrypt", help="Encrypt .xml to .bin")
    enc_parser.add_argument("-i", "--input", required=True, help="Input config.xml")
    enc_parser.add_argument("-o", "--output", required=True, help="Output config.bin")
    enc_parser.add_argument("-s", "--signature", default="Iskratel_InnboxX24", help="Image Signature (v21)")
    enc_parser.add_argument("-m", "--model", default="InnboxX24", help="Model Name")
    enc_parser.add_argument("-c", "--customer", default="Iskratel", help="Customer Name")

    args = parser.parse_args()

    try:
        bytenr = 0
        if args.mode == "decrypt":
            with open(args.input, "rb") as f:
                raw = f.read()
            xml_data = decrypt_bin(raw, args.model, args.customer)
            with open(args.output, "wb") as f:
                bytenr = f.write(xml_data)
            print(f"Decrypted successfully {bytenr} bytes -> {args.output}")

        elif args.mode == "encrypt":
            with open(args.input, "rb") as f:
                xml_bytes = f.read()
            bin_data = encrypt_xml(xml_bytes, args.model, args.customer, args.signature)
            with open(args.output, "wb") as f:
                bytenr = f.write(bin_data)
            print(f"Encrypted successfully {bytenr} bytes -> {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
