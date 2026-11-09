# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Realtek RTL9601D                                                           |
| DRAM            | 32 MB                                                                      |
| Flash Size      | 16 MB                                                                      |
| CPU Arch        | MIPSBE Realtek Lexra                                                       |
| CPU Clock       | 300MHz                                                                     |
| Bootloader      | U-Boot RSDK 2011                                                           |
| System          | Linux 2.6                                                                  |
| Ethernet ports  | 1x 2500Base-T                                                              |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.1.1/24                                                             |
| Web Gui         | ✅ - Limited, depends on firmware type.                                    |
| SSH             | ✅ - Needs to be enabled by hand.                                          |
| Telnet          | ✅ - After mod.                                                            |
| FTP             | ❌                                                                         |
| Serial          | ❌                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |


Flash Layout:
| dev | size     | erasesize |  name    |
| --- | -------- | --------- | -------- |
| mtd0| 00080000 | 00001000  | "Boot"   | 
| mtd1| 00180000 | 00001000  | "Config" |
| mtd2| 00700000 | 00001000  | "ImageA" |
| mtd3| 00700000 | 00001000  | "ImageB" |


# SSH

SSH is present in firmware but it doesnt start sucessfully when enabled from /sbin/setup.sh

setup.sh doesn't work since /bin/MecMgr reads config variables on startup and kills it.

MecMgr also hides a large number of settings that can be adjusted by sending custom OMCI messages from a ZTE OLT unit, sadly i cannot look into this one.


GOOGLE_ENGINEERING_BUILD needs to be set, unset = disable

"yes" starts it without second check,

"no" it reads "EepLanSsh", if its set to 2 dropbear is enabled.

First flag is "no" on my unit, EepLanSsh can be set from telnet with "echo EepLanSsh=2 >> /mnt/rwdir/sys.cfg" and after reboot SSH is enabled.

SSH user is root and password needs to be generated from SN with a [tool](https://tools.qqwee.net/CIG-Pass/) - Username: "ont", type: 16 chars


# UART

Unless your bootloader is "blessed" there wont be any serial console. 

It might be possible to combine unlocked pre-loader and existing second stage U-Boot to get it working but i didn't succeed.

/bin/Console would enable CLI on serial headers but without blessed bootloader it maxes the cpu to 100% trying to open non-existent tty.


# CIG Backdoor and why no telnet enable

Standard CIG backdoor is present but limited:
apollo_enet_rx_hook recives the packet and consumes it, checks for 00000001 and forwards it to NetMgr

It also has extra required filends: 
Type byte	Field	Max length	Destination 
0x01	IPv4 address	4 bytes	gbgmTip     - /sys/ont/l2d/bgm/tip
0x02	Username	16 bytes	gbgmTuser   - /sys/ont/l2d/bgm/tuser 
0x03	Password	32 bytes	gbgmTpasswd - /sys/ont/l2d/bgm/tpasswd

Sadly telnetd is stopped by GOOGLE_ENGINEERING_BUILD=="yes", so you can only push LOID,LOID Password and reset the device using it.
