#!/usr/bin/env python3
import sys
import struct
import zlib
import argparse

BLOCK_SIZE = 65536
HEADER_LEN = 5  # 4 bytes CRC + 1 flag byte
PAD_BYTE = b"\xFF"


def crc_of_payload(payload: bytes) -> int:
    return zlib.crc32(payload) & 0xFFFFFFFF


def do_export(env_path, out_path):
    data = open(env_path, "rb").read()
    if len(data) != BLOCK_SIZE:
        print(f"Warning: expected {BLOCK_SIZE} bytes, got {len(data)}", file=sys.stderr)

    stored_crc = struct.unpack(">I", data[0:4])[0]  # big-endian, per detected format
    flag = data[4]
    payload = data[HEADER_LEN:]

    calc_crc = crc_of_payload(payload)
    ok = "OK" if calc_crc == stored_crc else "MISMATCH"
    print(f"Stored CRC:     0x{stored_crc:08x}")
    print(f"Calculated CRC: 0x{calc_crc:08x}  [{ok}]")
    print(f"Flag byte:      0x{flag:02x}")

    # cut off at first 0xFF padding run (start of padding),
    # keeping only the actual key=value text
    pad_start = len(payload)
    for i, b in enumerate(payload):
        if b == 0xFF:
            pad_start = i
            break
    text = payload[:pad_start]

    variables = [v.decode("utf-8", errors="replace") for v in text.split(b"\x00") if v]

    with open(out_path, "w") as f:
        # store flag + padded length as metadata comments so import can rebuild exactly
        f.write(f"# flag=0x{flag:02x}\n")
        f.write(f"# padded_length={len(payload)}\n")
        for v in variables:
            f.write(v + "\n")

    print(f"\nExported {len(variables)} variable(s) to {out_path}")


def do_import(vars_path, out_path, flag_override=None):
    flag = None
    padded_length = None
    variables = []

    with open(vars_path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("# flag="):
                flag = int(line.split("=", 1)[1], 16)
            elif line.startswith("# padded_length="):
                padded_length = int(line.split("=", 1)[1])
            elif line.strip() == "" or line.startswith("#"):
                continue
            else:
                variables.append(line)

    if flag_override is not None:
        flag = flag_override
    if flag is None:
        flag = 0x01  # sane default seen in the sample
    if padded_length is None:
        padded_length = BLOCK_SIZE - HEADER_LEN  # 65531, matches sample

    text = b"\x00".join(v.encode("utf-8") for v in variables) + b"\x00"

    if len(text) > padded_length:
        raise SystemExit(
            f"Variables too long: {len(text)} bytes, only {padded_length} available. "
            "Shorten a value or the block will overflow."
        )

    payload = text + PAD_BYTE * (padded_length - len(text))
    crc = crc_of_payload(payload)

    block = struct.pack(">I", crc) + bytes([flag]) + payload

    if len(block) != BLOCK_SIZE:
        # pad/truncate defensively to guarantee exactly 64KB on disk
        if len(block) < BLOCK_SIZE:
            block += PAD_BYTE * (BLOCK_SIZE - len(block))
        else:
            block = block[:BLOCK_SIZE]

    with open(out_path, "wb") as f:
        f.write(block)

    print(f"Wrote {out_path}: {len(block)} bytes")
    print(f"  CRC32 (big-endian): 0x{crc:08x}")
    print(f"  Flag byte:          0x{flag:02x}")
    print(f"  Variables:          {len(variables)}")


def do_verify(env_path):
    data = open(env_path, "rb").read()
    if len(data) != BLOCK_SIZE:
        print(f"Warning: expected {BLOCK_SIZE} bytes, got {len(data)}", file=sys.stderr)
    stored_crc = struct.unpack(">I", data[0:4])[0]
    payload = data[HEADER_LEN:]
    calc_crc = crc_of_payload(payload)
    if calc_crc == stored_crc:
        print(f"OK: CRC matches (0x{calc_crc:08x})")
    else:
        print(f"MISMATCH: stored=0x{stored_crc:08x} calculated=0x{calc_crc:08x}")
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("export", help="Extract variables from a 64KB env block to a text file")
    pe.add_argument("env_file")
    pe.add_argument("out_file")

    pi = sub.add_parser("import", help="Rebuild a 64KB env block from an edited text file")
    pi.add_argument("vars_file")
    pi.add_argument("out_file")
    pi.add_argument("--flag", type=lambda x: int(x, 0), default=None,
                     help="Override flag byte, e.g. --flag 0x01")

    pv = sub.add_parser("verify", help="Check a block's stored CRC against a recalculated one")
    pv.add_argument("env_file")

    args = p.parse_args()

    if args.cmd == "export":
        do_export(args.env_file, args.out_file)
    elif args.cmd == "import":
        do_import(args.vars_file, args.out_file, args.flag)
    elif args.cmd == "verify":
        do_verify(args.env_file)


if __name__ == "__main__":
    main()
