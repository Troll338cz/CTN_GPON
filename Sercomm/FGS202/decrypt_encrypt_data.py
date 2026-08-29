import hashlib
from Crypto.Cipher import AES

# from Factory environ
ethaddr = "78:94:B4:27:5F:2A"
nSerial = "SCOM21040A14"
# from Config environ
encrypt_data = bytes.fromhex("23cc5d5da799673708e443594e06272ffde3f449061bff7604c32cd50a186e19")

alphabet = "93axcdz25efhiv87ykmuj46stpbw"
digest = hashlib.md5(f"{ethaddr}{nSerial}".encode()).digest().hex()
out = bytes(ord(c) % 28 for c in digest)
mapped = bytes(ord(alphabet[b]) for b in out)

cipher = AES.new(mapped[:16], AES.MODE_CBC, iv=b'\x00'*16)
print( cipher.decrypt(encrypt_data) )
