#!/usr/bin/env python3
import socket, struct, sys, time, zlib

MCAST_IP		= "224.1.2.3"	# Default, can be anything in 224.0.0.0/4
MCAST_IPv6		= "ff02::16:"	# Comtrend GRG-4362
USE_V6			= True
MCAST_PORT		= 1234			# Default, can be anything, ignored in U-Boot
FRAME_LEN		= 1024			# MUTLICAST_FRAME_LENGTH
INTERVAL		= 0.01			# Realtek tool has: 1 / 5 / 10 / 20 / 50 / 100 / 200 ms, Default is 10ms

MUP_DATATYPE_NORM = 0x1
MUP_DATATYPE_LAST = 0x2
MUP_DATATYPE_INFO = 0x4

def hl(datatype, datalen=FRAME_LEN):
	# hl = datatype(3 bits)<<29 | datalen(29 bits)  -- matches MUP_DATATYPE_MASK<<29 check
	return (datatype << 29) | (datalen & 0x1FFFFFFF)

def build_packet(datatype, seqnum, image_data, img_len, img_crc):
	data = image_data.ljust(FRAME_LEN, b"\x00")[:FRAME_LEN]
	data_crc = zlib.crc32(data) & 0xFFFFFFFF
	pkt  = struct.pack(">I", hl(datatype))
	pkt += struct.pack(">I", seqnum)
	pkt += struct.pack(">I", data_crc)
	pkt += struct.pack(">I", img_len)
	pkt += struct.pack(">I", img_crc)
	pkt += b"\x00" * 22		# package_id
	pkt += b"\x00" * 20		# product_id
	pkt += data				# image_data[1024]
	return pkt

def build_partition_hdr(name=b"kernel", addrstart=0, addrend=0, cover_flag=0):
	name20 = name.ljust(20, b"\x00")[:20]
	return struct.pack(">20sIIB3x", name20, addrstart, addrend, cover_flag)

def main():
	if len(sys.argv) != 3:
		print(f"Usage: {sys.argv[0]} <firmware file> <interface>")
		sys.exit(1)

	with open(sys.argv[1], "rb") as f:
		fw = f.read()

	img_len = len(fw)
	# "image size should not over 64MB, one packet size if 1024"
	if(img_len > (51200 * 1024)):
		print(f"File {sys.argv[1]} is larger then multicast protocol maximum {51200 * 1024} bytes, unsupported.")
		sys.exit(1)

	img_crc = zlib.crc32(fw) & 0xFFFFFFFF

	if USE_V6:
		sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)
		scope_id = socket.if_nametoindex(sys.argv[2])
		dst = (MCAST_IPv6, MCAST_PORT, 0, scope_id)
	else:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, bytes(sys.argv[2]+"\0", "utf8"))
		dst = (MCAST_IP, MCAST_PORT)


	
	# Force "partiton_info_array[i].type == PARTI_TYPE_IMG", it will try upimgtar and upvmimg
	part_hdr = build_partition_hdr(b"kernel", 0, img_len, 0)
	info_data = part_hdr.ljust(FRAME_LEN, b"\x00")
	pkt = build_packet(MUP_DATATYPE_INFO, 0, info_data, img_len, img_crc)
	sock.sendto(pkt, dst)
	time.sleep(INTERVAL)

	# 2) Data packets
	total_frames = (img_len + FRAME_LEN - 1) // FRAME_LEN
	for i in range(total_frames):
		seq = i + 1
		chunk = fw[i * FRAME_LEN:(i + 1) * FRAME_LEN]
		dtype = MUP_DATATYPE_LAST if seq == total_frames else MUP_DATATYPE_NORM
		pkt = build_packet(dtype, seq, chunk, img_len, img_crc)
		sock.sendto(pkt, dst)
		time.sleep(INTERVAL)
		if seq % 50 == 0 or seq == total_frames:
			print(f"sent {seq}/{total_frames}")

	# 3) Resend INFO packet once more to trigger "same packet" finish detection
	pkt = build_packet(MUP_DATATYPE_INFO, 0, info_data, img_len, img_crc)
	sock.sendto(pkt, dst)

	print(f"Done. total_len={img_len} total_crc32=0x{img_crc:08x} frames={total_frames}")

if __name__ == "__main__":
	main()