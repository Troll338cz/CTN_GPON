import hashlib

#
# Cleaned up disassembly fed to Claude for cleaner python rewrite
# Supports generation of classic CIG algorithm and new one
# While it is possible to get a clean implementation in C with minimal effort, i couldn't be bothered this time for CIG stuff.
# Zyxel's algorithms are fun, this is not...
#
# JS version is available at https://hack-gpon.org/assets/js/cigpassword.js
#

# Hardcoded
HM_KEY1 = bytes([0x01, 0x03, 0x0A, 0x10, 0x13, 0x05, 0x17, 0x64, 0xC8, 0x06, 0x14, 0x19, 0xB4, 0x9D, 0x05])
HM_KEY2 = bytes([0x05, 0x11, 0x3A, 0x60, 0x7B, 0xFB, 0x0F, 0x43, 0x5C, 0x21, 0xBE, 0x86, 0x41, 0x32, 0x1C])
PASSWORD_CHARS = "2345679abcdefghijkmnpqrstuvwxyzACDEFGHJKLMNPQRSTUVWXYZ"


def vos_md5_encode(data: str, key: bytes) -> bytes:
    """HMAC-MD5 as implemented in the C code (ipad=0x36, opad=0x5C, block=64)."""
    key_bytes = key
    # If key >= 65 bytes, pre-hash it
    if len(key_bytes) >= 65:
        key_bytes = hashlib.md5(key_bytes).digest()

    # Pad key to 64 bytes
    k_ipad = bytearray(64)
    k_opad = bytearray(64)
    k_ipad[:len(key_bytes)] = key_bytes
    k_opad[:len(key_bytes)] = key_bytes

    # XOR with ipad (0x36) and opad (0x5C)
    for i in range(64):
        k_ipad[i] ^= 0x36
        k_opad[i] ^= 0x5C

    # Inner hash: MD5(k_ipad || data)
    inner = hashlib.md5(bytes(k_ipad) + data.encode()).digest()

    # Outer hash: MD5(k_opad || inner)
    outer = hashlib.md5(bytes(k_opad) + inner).digest()

    return outer

def vos_hmac_md5_ssh(input_str: str, out_len: int = 16) -> str:
    result = [''] * out_len
    use_len = min(16, out_len)

    # out_len == 8 makes C unhappy and appends null byte to end of both keys....
    key1, key2 = HM_KEY1, HM_KEY2
    if out_len == 8:
        key1 = HM_KEY1 + bytes([out_len])
        key2 = HM_KEY2 + bytes([out_len])

    # First half using HM_KEY1
    digest1 = vos_md5_encode(input_str, key1)
    for i in range(use_len):
        result[i] = PASSWORD_CHARS[digest1[i] % 0x36]

    if out_len >= 17:
        # Second half using HM_KEY2
        digest2 = vos_md5_encode(input_str, key2)
        for j in range(out_len - 16):
            result[16 + j] = PASSWORD_CHARS[digest2[j] % 0x36]

    return ''.join(result)



