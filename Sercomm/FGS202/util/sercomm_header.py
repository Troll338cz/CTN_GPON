#!/usr/bin/env python3
"""
sercomm_header.py - Based on header code found in eCos and U-Boot

Build and inspect the 256-byte Sercomm/Falcon SFP image header found at
(image_start - 0x100) in flash.

Confirmed layout (bytes 0x00-0x1F), derived from cross-referencing
bootlog.txt against the decompiled update routine sub_1001CD7C:

    0x00  4 bytes   magic          b"Ser\x00"
    0x04  4 bytes   pid_addr       uint32 LE  = image_start + image_length
    0x08  4 bytes   unknown        uint32 LE  Copied this from my image0, shouldnt be checked anywhere and the value seems radom...
    0x0C  4 bytes   imgnum         uint32 LE  (seen as 1 in bootlog)
    0x10  4 bytes   start_addr     uint32 LE  = image_start (e.g. 0x100000)
    0x14  4 bytes   length         uint32 LE  = image_length
    0x18  4 bytes   crc32          uint32 LE  = zlib.crc32(image_bytes)
    0x1C  4 bytes   reserved       uint32 LE  (0 in the sample)
    0x20-0xFF       unknown        - Does not matter, also no checks in the code

Usage:
  # Inspect / dump a header you extracted from a flash dump
  python3 sercomm_header.py inspect header.bin

  # Build a new header for a new image, keeping unknown template fields
  python3 sercomm_header.py build \
      --template header.bin \
      --image new_image.bin \
      --start 0x100000 \
      --out new_header.bin \
      --full-out new_image_with_header.bin

  # Verify a header against the image it's supposed to describe
  python3 sercomm_header.py verify --header header.bin --image image.bin
"""

import argparse
import struct
import sys
import zlib
from pathlib import Path

HEADER_SIZE = 256
KNOWN_SIZE = 0x20  # first 32 bytes we understand the layout of

MAGIC = b"Ser\x00"

# struct format for the first 8 dwords (32 bytes), all little-endian
STRUCT_FMT = "<4sIIIIIII"
#              magic  pid  unk  imgnum start len  crc  rsvd


def parse_header(data: bytes):
    if len(data) < HEADER_SIZE:
        raise ValueError(f"header is only {len(data)} bytes, expected {HEADER_SIZE}")
    magic, pid_addr, unknown_08, imgnum, start_addr, length, crc32, reserved_1c = \
        struct.unpack_from(STRUCT_FMT, data, 0)
    return {
        "magic": magic,
        "pid_addr": pid_addr,
        "unknown_08": unknown_08,
        "imgnum": imgnum,
        "start_addr": start_addr,
        "length": length,
        "crc32": crc32,
        "reserved_1c": reserved_1c,
        "tail": data[KNOWN_SIZE:HEADER_SIZE],  # opaque 0x20-0xFF region
    }


def print_header(fields: dict, data: bytes):
    print(f"{'offset':<8}{'field':<14}{'value'}")
    print(f"0x00    magic         {fields['magic']!r}")
    print(f"0x04    pid_addr      0x{fields['pid_addr']:08X}")
    print(f"0x08    unknown_08    0x{fields['unknown_08']:08X}")
    print(f"0x0C    imgnum        {fields['imgnum']}")
    print(f"0x10    start_addr    0x{fields['start_addr']:08X}")
    print(f"0x14    length        0x{fields['length']:08X} ({fields['length']} bytes)")
    print(f"0x18    crc32         0x{fields['crc32']:08X}")
    print(f"0x1C    reserved_1c   0x{fields['reserved_1c']:08X}")

    computed_pid = fields["start_addr"] + fields["length"]
    if computed_pid != fields["pid_addr"]:
        print(f"  ! pid_addr (0x{fields['pid_addr']:08X}) != start_addr+length "
              f"(0x{computed_pid:08X})")

    tail = fields["tail"]
    if any(tail):
        print(f"\n0x20-0xFF tail (non-zero bytes present, {len(tail)} bytes total):")
        for i in range(0, len(tail), 16):
            chunk = tail[i:i + 16]
            hexs = " ".join(f"{b:02x}" for b in chunk)
            print(f"  0x{KNOWN_SIZE + i:02X}: {hexs}")
    else:
        print("\n0x20-0xFF tail: all zero")


def cmd_inspect(args):
    data = Path(args.header).read_bytes()
    fields = parse_header(data)
    print_header(fields, data)


def cmd_verify(args):
    header = Path(args.header).read_bytes()
    image = Path(args.image).read_bytes()
    fields = parse_header(header)
    print_header(fields, header)

    print("\n--- verifying against image file ---")
    actual_len = len(image)
    actual_crc = zlib.crc32(image) & 0xFFFFFFFF
    print(f"actual image length : 0x{actual_len:08X} ({actual_len} bytes)")
    print(f"actual image crc32  : 0x{actual_crc:08X}  (zlib.crc32)")

    ok = True
    if actual_len != fields["length"]:
        print("  ! length MISMATCH")
        ok = False
    if actual_crc != fields["crc32"]:
        print("  ! crc32 MISMATCH (or a different CRC32 variant is used - "
              "not confirmed against real bootloader source)")
        ok = False
    print("MATCH" if ok else "MISMATCH")


def cmd_build(args):
    template = Path(args.template).read_bytes()
    if len(template) < HEADER_SIZE:
        sys.exit(f"template header must be >= {HEADER_SIZE} bytes, "
                  f"got {len(template)}")

    image = Path(args.image).read_bytes()
    start_addr = int(args.start, 0)

    tmpl_fields = parse_header(template)

    if tmpl_fields["start_addr"] not in (0, start_addr):
        print(f"WARNING: template header's start_addr (0x{tmpl_fields['start_addr']:08X}) "
              f"does not match --start (0x{start_addr:08X}).")
        print("  unknown_08 (offset 0x08) has been confirmed to be *slot-specific* - it "
              "differs between the image0 and image1 headers on the one device checked "
              "so far, even though those two images have identical content/crc.")
        print("  Using a template from a different slot/address for this field is NOT "
              "confirmed safe - prefer a template pulled from the SAME slot you're "
              "writing to.")
        if not args.force:
            sys.exit("  refusing to continue (pass --force to override)")

    length = len(image)
    pid_addr = start_addr + length
    crc32 = zlib.crc32(image) & 0xFFFFFFFF

    magic = tmpl_fields["magic"] if not args.magic else args.magic.encode()
    if len(magic) != 4:
        sys.exit("magic must be exactly 4 bytes")

    unknown_08 = tmpl_fields["unknown_08"]  # carried over, not regenerated
    imgnum = tmpl_fields["imgnum"] if args.imgnum is None else int(args.imgnum, 0)
    reserved_1c = tmpl_fields["reserved_1c"]  # carried over
    tail = tmpl_fields["tail"]                # carried over, opaque region

    new_header = struct.pack(
        STRUCT_FMT,
        magic, pid_addr, unknown_08, imgnum, start_addr, length, crc32, reserved_1c,
    ) + tail

    assert len(new_header) == HEADER_SIZE

    Path(args.out).write_bytes(new_header)
    print(f"wrote {args.out} ({HEADER_SIZE} bytes)")
    print_header(parse_header(new_header), new_header)

    print("\nFields taken from template unchanged (not verified/regenerated):")
    print(f"  unknown_08  = 0x{unknown_08:08X}")
    print(f"  reserved_1c = 0x{reserved_1c:08X}")
    print(f"  tail (0x20-0xFF) copied verbatim from template")

    if args.full_out:
        Path(args.full_out).write_bytes(new_header + image)
        print(f"\nwrote {args.full_out} "
              f"({HEADER_SIZE + len(image)} bytes = header + image)")
        print("NOTE: this is header-then-image. Confirm your flash layout actually "
              "expects the header immediately before the image at (start-0x100) "
              "before writing this to flash - don't assume, check the dump.")


def cmd_diff(args):
    a = Path(args.header_a).read_bytes()
    b = Path(args.header_b).read_bytes()
    fa = parse_header(a)
    fb = parse_header(b)

    print(f"{'field':<14}{'A':<14}{'B':<14}same?")
    for key in ("magic", "pid_addr", "unknown_08", "imgnum",
                "start_addr", "length", "crc32", "reserved_1c"):
        va, vb = fa[key], fb[key]
        same = "same" if va == vb else "DIFFERS"
        if isinstance(va, bytes):
            print(f"{key:<14}{va!r:<14}{vb!r:<14}{same}")
        else:
            print(f"{key:<14}0x{va:08X}    0x{vb:08X}    {same}")

    ta, tb = fa["tail"], fb["tail"]
    if ta == tb:
        print("\ntail (0x20-0xFF): identical")
    else:
        print("\ntail (0x20-0xFF): DIFFERS at these offsets:")
        for i in range(len(ta)):
            if ta[i] != tb[i]:
                print(f"  0x{KNOWN_SIZE + i:02X}: A={ta[i]:02x}  B={tb[i]:02x}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_inspect = sub.add_parser("inspect", help="parse and print a 256-byte header file")
    p_inspect.add_argument("header")
    p_inspect.set_defaults(func=cmd_inspect)

    p_verify = sub.add_parser("verify", help="check a header's length/crc against an image file")
    p_verify.add_argument("--header", required=True)
    p_verify.add_argument("--image", required=True)
    p_verify.set_defaults(func=cmd_verify)

    p_build = sub.add_parser("build", help="build a new header for a new image, keeping unknown template fields")
    p_build.add_argument("--template", required=True, help="known-good 256-byte header from YOUR device's flash dump")
    p_build.add_argument("--image", required=True, help="the new image body (no header)")
    p_build.add_argument("--start", default="0x100000", help="image start address, e.g. 0x100000 or 0x480000")
    p_build.add_argument("--imgnum", default=None, help="override imgnum field (default: keep template's value)")
    p_build.add_argument("--magic", default=None, help="override 4-byte magic (default: keep template's value)")
    p_build.add_argument("--out", required=True, help="output path for the 256-byte header")
    p_build.add_argument("--full-out", default=None, help="optional: also write header+image concatenated")
    p_build.add_argument("--force", action="store_true", help="override the slot-address mismatch safety check")
    p_build.set_defaults(func=cmd_build)

    p_diff = sub.add_parser("diff", help="compare two 256-byte headers field by field (e.g. image0 vs image1)")
    p_diff.add_argument("header_a")
    p_diff.add_argument("header_b")
    p_diff.set_defaults(func=cmd_diff)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
