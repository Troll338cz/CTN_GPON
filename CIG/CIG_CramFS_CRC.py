def crc32_be(data: bytes,
                 poly: int = 0x04C11DB7, # CRCPOLY_BE - see u-boot/drivers/mtd/ubi/crc32defs.h
                 init: int = 0xFFFFFFFF,
                 xorout: int = 0xFFFFFFFF) -> int:
    crc = init & 0xFFFFFFFF
    for byte in data:
        crc ^= (byte << 24) & 0xFFFFFFFF
        for _ in range(8):
            if crc & 0x80000000:
                crc = ((crc << 1) ^ poly) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
    return crc ^ xorout

firmware_data = open("newrootfs.img", "rb").read()
cramfs_magic = b'\x28\xcd\x3d\x45'
print(f"Loaded file with lenth {len(firmware_data)} bytes")
print(f"Is CramFS magic valid: {firmware_data[0:4] == cramfs_magic}")
print(f"Current CRC32 (if present): \n0x{firmware_data[len(firmware_data)-4:].hex()}\n")
print(f"CRC32 for whole file: \n0x{crc32_be(firmware_data):08x}\n")
print(f"CRC32 for file without last 4 bytes (if you included old CRC): \n0x{crc32_be(firmware_data[:-4]):08x}\n")
