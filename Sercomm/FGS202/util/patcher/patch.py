import struct
import zlib

HEADER_FMT = "<4sIIIIIII"
HEADER_KNOWN = 32
HEADER_SIZE = 256

# The splice point and padding, as specified: insert at the offset where the
# marker+zeros+version-string block currently begins, landing the handler
# exactly at file-offset (slot_start + SPLICE_OFFSET + PAD_BEFORE).
SPLICE_OFFSET = 0x1A0C80        # offset into the image body, relative to start_addr
PAD_BEFORE = 128
PAD_AFTER = 128

# The 16-byte "short pid" footer tail that always sits immediately after
# pid_addr -- confirmed unconditionally copied forward by the real firmware
# update path (sub_1001CD7C), never recomputed. Same for both slots.
FOOTER_TAIL = bytes.fromhex("0000007F100090F76552634F6D4D0000")

OLD_LENGTH = 0x1A0CE8            # expected original (pre-splice) v4.bin length


def build_header(template_header, start_addr, image_body):
    magic, _pid, unknown_08, imgnum, _start, _len, _crc, reserved_1c = \
        struct.unpack_from(HEADER_FMT, template_header, 0)
    tail = template_header[HEADER_KNOWN:HEADER_SIZE]

    length = len(image_body)
    pid_addr = start_addr + length
    crc32 = zlib.crc32(image_body) & 0xFFFFFFFF

    header = struct.pack(HEADER_FMT, magic, pid_addr, unknown_08, imgnum,
                          start_addr, length, crc32, reserved_1c) + tail
    assert len(header) == HEADER_SIZE
    return header, pid_addr


def splice_body(v4_body, handler_bytes):
    """Insert [128xFF][handler][128xFF] at SPLICE_OFFSET, relocating the
    original marker+zeros+version-string block (whatever sat from
    SPLICE_OFFSET to the old end of v4_body) to right after it."""
    if len(v4_body) != OLD_LENGTH:
        raise ValueError(f"v4_body is {len(v4_body)} bytes, expected "
                          f"{OLD_LENGTH} -- splice offsets assume the "
                          f"original, unpatched-past-this-point length")

    prefix = v4_body[:SPLICE_OFFSET]
    displaced = v4_body[SPLICE_OFFSET:]   # marker + zeros + version string

    new_body = (prefix
                + b"\xff" * PAD_BEFORE
                + handler_bytes
                + b"\xff" * PAD_AFTER
                + displaced)
    return new_body


def build_slot(flashorig, start_addr, header_offset, v4_body, handler_bytes):
    template = flashorig[header_offset:header_offset + HEADER_SIZE]
    new_body = splice_body(v4_body, handler_bytes)
    header, pid_addr = build_header(template, start_addr, new_body)
    return header, new_body, pid_addr


# ---------------- load inputs ----------------
flashorig = open("FGS202_1.img", "rb").read()
# 
# You need to patch v3 yourself 
# sub_10008270(a1, 0, " ", "diag", (int)sub_10002D24); <-- swap here to jump to 0x101A0D00 
#
v4_body = open("SCOMFGS202112-telnet-v4.bin", "rb").read()
handler_bytes = open("patch.bin", "rb").read()

IMAGE0_START = 0x100000
IMAGE0_HEADER_OFF = IMAGE0_START - HEADER_SIZE     # 0x0FFF00
IMAGE1_START = 0x480000
IMAGE1_HEADER_OFF = 0x47FF00

start = flashorig[0:IMAGE0_HEADER_OFF]

image0_header, image0_body, image0_pid_addr = build_slot(
    flashorig, IMAGE0_START, IMAGE0_HEADER_OFF, v4_body, handler_bytes)

image1_header, image1_body, image1_pid_addr = build_slot(
    flashorig, IMAGE1_START, IMAGE1_HEADER_OFF, v4_body, handler_bytes)

# gap between end of image0's footer tail and start of image1's header --
# pulled from the clean dump, not assumed, in case anything unexpected is
# actually sitting in there
gap0 = flashorig[IMAGE0_START + len(image0_body) + len(FOOTER_TAIL):IMAGE1_HEADER_OFF]

# everything after image1's footer tail through the end of the chip
gap1 = flashorig[IMAGE1_START + len(image1_body) + len(FOOTER_TAIL):8388608]

flash_full = (
    start
    + image0_header + image0_body + FOOTER_TAIL + gap0
    + image1_header + image1_body + FOOTER_TAIL + gap1
)

out = open("fw_patch.img", "wb")
if len(flash_full) == 8388608:
    out.write(flash_full)
    out.close()
    print("wrote fw_patch.img (8388608 bytes)")
    print(f"image0: header@0x{IMAGE0_HEADER_OFF:06X} "
          f"length=0x{len(image0_body):06X} pid_addr=0x{image0_pid_addr:06X}")
    print(f"image1: header@0x{IMAGE1_HEADER_OFF:06X} "
          f"length=0x{len(image1_body):06X} pid_addr=0x{image1_pid_addr:06X}")
    print(f"handler lands at file offset 0x{IMAGE0_START + SPLICE_OFFSET + PAD_BEFORE:06X} "
          f"(image0) / 0x{IMAGE1_START + SPLICE_OFFSET + PAD_BEFORE:06X} (image1)")
    print("both should equal virtual 0x101A0D00 once mapped (start_addr cancels "
          "out under the shared ecos_vaddr TLB mapping)")
else:
    print(f"Len mismatch {len(flash_full)} != 8388608")
