#!/usr/bin/env python3
"""
zte_eep.py - dump / verify / patch the ZTE F6005 mtd0 env block.

Layout (MiscMgr mmr_EepCfgLoad2File, mmr_EepApiCheckCrc/UpdateCrc, libvos VOS_ImageSave):
  two redundant 0x600-byte copies in mtd0: eepB @ 0x60000, eepA @ 0x70000
  inner struct  0x000..0x0FF : fields below
      0x0FC..0x0FF  EepChecksum = CRC32/BZIP2 over 0x000..0x0EB   (BE)   [set by MiscMgr 'crc update']
  outer block   0x000..0x5FF
      0x5FC..0x5FF  CRC32/BZIP2 over 0x000..0x5FB                 (BE)   [maintained below MiscMgr]
  CRC32/BZIP2 = poly 0x04C11DB7, init/xorout 0xFFFFFFFF, MSB-first, no reflection.

Input: full flash/mtd0 dump (copies found at 0x60000/0x70000) or a single
64 KiB sector dump (assumed to start at 0x60000; override with --base).

  dump    FILE
  verify  FILE
  set     FILE FIELD=HEX [FIELD=HEX ...] [-o OUT]     FIELD = lanssh | hex offset (<0xEC)
"""
import struct, sys, argparse

BLK, OUT_CRC, IN_CRC, IN_LEN = 0x600, 0x5FC, 0xFC, 0xEC
COPIES = {"eepB": 0x60000, "eepA": 0x70000}
NAMES = {"lanssh": 0xE7}

# (key, offset, length, kind)  kind: s=string, h=hex bytes, ip=ipv4
FIELDS = [
    ("EepMfgProductCode", 0x00, 12, "s"),
    ("EepMfgProductSerial", 0x0C, 12, "s"),
    ("EepMfgHwVersion", 0x18, 2, "s"),
    ("EepMfgLaserSerial", 0x1A, 16, "s"),
    ("EepMfgMac1", 0x2A, 6, "h"),
    ("EepMfgMac2", 0x30, 6, "h"),
    ("EepMfgEepver", 0x36, 2, "h"),
    ("EepHwFunctionMajor", 0x58, 2, "h"),
    ("EepHwFunctionMinor", 0x5A, 1, "h"),
    ("EepHwVersion", 0x5B, 1, "h"),
    ("EepSwProvinceId", 0x5E, 2, "h"),
    ("EepEqVendorID", 0x60, 4, "s"),
    ("EepEqSerialNumber(4s+4h)", 0x64, 8, "s+h"),
    ("EepEqVersionID", 0x6C, 14, "s"),
    ("EepEqID", 0x7A, 20, "s"),
    ("EepSwBootImage", 0x8E, 14, "s"),
    ("EepSwIpAddr", 0x9C, 4, "ip"),
    ("EepSwIpMask", 0xA0, 4, "ip"),
    ("EepSwHostIpAddr", 0xA4, 4, "ip"),
    ("EepSwGWIpAddr", 0xA8, 4, "ip"),
    ("EepSwFtpUser", 0xAC, 8, "s"),
    ("EepSwFtpPass", 0xB4, 8, "s"),
    ("EepSwBootFlag", 0xBC, 2, "h"),
    ("EepSwBootParameter", 0xBE, 1, "h"),
    ("EepSwActiveImage", 0xBF, 1, "h"),
    ("EepSwCommitImage", 0xC0, 1, "h"),
    ("EepAppGponPassword", 0xDA, 10, "h"),
    ("EepLanSsh", 0xE7, 1, "h"),
    ("EepChecksum", 0xFC, 4, "h"),
]


def crc32_bzip2(data: bytes) -> int:
    c = 0xFFFFFFFF
    for b in data:
        c ^= b << 24
        for _ in range(8):
            c = ((c << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if c & 0x80000000 else (c << 1) & 0xFFFFFFFF
    return c ^ 0xFFFFFFFF


def locate(buf, base):
    if base is not None:
        r = {n: (a - base, a) for n, a in COPIES.items() if 0 <= a - base and a - base + BLK <= len(buf)}
    elif len(buf) <= 0x10000:
        r = {"eepB": (0, 0x60000)}
    else:
        r = {n: (a, a) for n, a in COPIES.items() if a + BLK <= len(buf)}
    return r


def crcs(buf, fo):
    ist, ic = struct.unpack(">I", buf[fo + IN_CRC: fo + IN_CRC + 4])[0], crc32_bzip2(bytes(buf[fo: fo + IN_LEN]))
    ost, oc = struct.unpack(">I", buf[fo + OUT_CRC: fo + BLK])[0], crc32_bzip2(bytes(buf[fo: fo + OUT_CRC]))
    return ist, ic, ost, oc


def fmt(raw, kind):
    if kind == "ip":
        return ".".join(str(x) for x in raw)
    if kind == "h":
        return raw.hex()
    if kind == "s+h":
        return raw[:4].decode("latin1") + raw[4:].hex().upper()
    if 0xFF in raw:
        return ""
    return raw.split(b"\0")[0].decode("latin1", "replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["dump", "verify", "set"])
    ap.add_argument("file")
    ap.add_argument("patches", nargs="*")
    ap.add_argument("-o", "--out")
    ap.add_argument("--base", type=lambda x: int(x, 0))
    a = ap.parse_args()

    buf = bytearray(open(a.file, "rb").read())
    copies = locate(buf, a.base)
    if not copies:
        sys.exit("no env copy found (file size %#x)" % len(buf))

    if a.cmd == "dump":
        n, (fo, _) = next(iter(copies.items()))
        print(f"# {n}")
        for k, o, l, kind in FIELDS:
            print(f"{o:#06x}  {k}={fmt(bytes(buf[fo+o: fo+o+l]), kind)}")
        return

    if a.cmd == "verify":
        ok = True
        for n, (fo, addr) in copies.items():
            ist, ic, ost, oc = crcs(buf, fo)
            ok &= (ist == ic and ost == oc)
            print(f"{n} @{addr:#x}: inner(0xFC) stored {ist:08x} calc {ic:08x} {'OK' if ist == ic else 'BAD'}"
                  f" | outer(0x5FC) stored {ost:08x} calc {oc:08x} {'OK' if ost == oc else 'BAD'}")
        sys.exit(0 if ok else 1)

    if not a.patches:
        sys.exit("set needs FIELD=HEX")
    patches = []
    for p in a.patches:
        k, v = p.split("=")
        o = NAMES.get(k.lower()) if k.lower() in NAMES else int(k, 16)
        v = int(v, 16)
        if not (0 <= o < IN_LEN and 0 <= v <= 0xFF):
            sys.exit(f"bad patch {p}: offset must be < {IN_LEN:#x}, one byte value")
        patches.append((o, v))

    cli = []
    for n, (fo, addr) in copies.items():
        old = bytes(buf[fo: fo + BLK])
        for o, v in patches:
            buf[fo + o] = v
        buf[fo + IN_CRC: fo + IN_CRC + 4] = struct.pack(">I", crc32_bzip2(bytes(buf[fo: fo + IN_LEN])))
        buf[fo + OUT_CRC: fo + BLK] = struct.pack(">I", crc32_bzip2(bytes(buf[fo: fo + OUT_CRC])))
        new = bytes(buf[fo: fo + BLK])
        for i in range(BLK):
            if old[i] != new[i]:
                cli.append((n, addr + i, new[i], i))
    out = a.out or a.file + ".patched"
    open(out, "wb").write(buf)
    print("wrote", out)
    print("\n# raw flash writes (ONT/system/fs/write <addr> <byte>), copy by copy, payload -> inner CRC -> outer CRC:")
    for n, ad, v, i in cli:
        tag = "payload" if i < IN_CRC else ("inner CRC" if i < 0x100 else "outer CRC")
        print(f"write {ad:x} {v:02x}    # {n} {tag}")


if __name__ == "__main__":
    main()
