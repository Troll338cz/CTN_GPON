
# Thakns to CA8271x project by YuukiJapanTech for hosting a full mtd dump
# Sample sourced from https://github.com/YuukiJapanTech/CA8271x/blob/main/mtd/NOKIA_XS-010X-R/mtd10.bin
# Funny CIG trolling anyone trying to RE their config CRC is only done over 236 bytes
# The code that handles nand is in cig-misc.ko not ca-ne.ko
# Function we want is nvram_nand_eeprom_valid_check
import struct

mfginfo0_256 = bytes.fromhex("314b342d30303030312d313330363235323030383034343330314853463036413231383136324700000094f7175d5ce494f7175d5ce700010000000000000000000000000000000000000000000000000000000000000000011a010200000000414c434c414c434cfdb614a433544e303036363641424141303142564d50443030425241585330313058520000006f6e742e7a000000000000000000c0a86401ffffff00c0a86401000000006f6e7400000000006f6e74000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000fdd62392")
crc_expected = struct.unpack("I", mfginfo0_256[252:])[0]

def crc32_bzip2(data, poly, init, xorout):
    crc = init & 0xFFFFFFFF
    for byte in data:
        crc ^= (byte << 24) & 0xFFFFFFFF
        for _ in range(8):
            if crc & 0x80000000:
                crc = ((crc << 1) ^ poly) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
    return crc ^ xorout

crc_out = crc32_bzip2(mfginfo0_256[0:236], 0x04C11DB7, 0xFFFFFFFF, 0xFFFFFFFF)

print(f"From file: {crc_expected} | Calculated: {crc_out} | Match: {crc_expected == crc_out}")

