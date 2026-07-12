|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | MediaTek/EcoNet EN7523OT                                                   |
| DRAM            | 256 MB Winbond W623GU6MB                                                   |
| Flash Size      | 128 MB Macronix W25N01G                                                    |
| CPU Arch        | Dualcore ARMv7 Processor rev 4 (v7l)                                       |
| CPU Clock       | 735MHz                                                                     |
| Bootloader      | U-Boot 2014.04-rc1 (Nov 24 2022 - 09:42:18) + zloader v2.0.6               |
| System          | Linux 4.4.115 #1 SMP Thu Dec 1 14:17:37 CST 2022 armv7l GNU/Linux          |
| Ethernet ports  | 1x 10/100/1000/2500 Base-T                                                 |
| PHY Ethernet    | Realtek RTL8221B                                                           |
| Optics          | SC/APC Econet 7571                                                         |
| IP address      | 192.168.0.1/24                                                             |
| Web Gui         | ✅                                                                         |
| SSH             | ✅                                                                         |
| Telnet          | ✅                                                                         |
| FTP             | ✅                                                                         |
| Serial          | ✅                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |


I hate Zyxel for making me desolder the SPI chip just to unlock this...

Z-Loader now has a password, please just allow users full access instead of clowning with all the locks.

Unlock this evil thing:

## Version 1
```
1. Obtain, decrypt and use the funny credentials from original firmware dump
2. Dump /dev/mtd0 ( Or remove and dump flash )
3. grep -a "supervisor=" mtd0.bin
4. Enter 9 char password into Zloader
5. ATSE PM5100-T0
6. ATENv3 generator go brrr 
7. ATEN 1,RESULT ( Set EngDebugFlag=1 in RAM )
8. ATBT 1 ( Allow nvram write )
9. ATSB ( Write EngDebugFlag=1 + disables password )
10. ATCK ( Get all default passwords )
11. ATUR 192.168.1.XXX,V542ACBF1.1C0.bin
12. Profit!, Zyxel firmware accepts ATCK passwords
```

## Version 2
- Connect modem to a Linux PC
- Clone and build https://github.com/bmork/zyxel-hacks/
- Bring up ethernet interface busybox ifconfig eth0 up
- Start the zyeng tool as root sudo ./zyeng eth0
- Power up the device and wait for the following output:
```
Multiboot server is available for download firmware image!
Be patient, it should be finish in 12 minutes...
No file need to download, stop multiboot service!


Update engineer debug flag!
...TRX 1 : 0x174
TRX 2 : 0x174
```
- NOTE: Some evil ISPs might disable multicast!


Usefull commands:

```
moscli mibdump <id> 	- omcicli mib get 
moscli fakeok on|off	- OMCI_FAKE_OK alternative?
moscli show counter omci - Recived/Send/Error counters
moscli voipinfodump
moscli appconfigdump	- GPON features info
moscli iphostinfodump

Settings probably won't persist reboot

```
U-Boot model id:
```
Other Feature Bits     :
817145ac: 04050f04 00000000 00000000 00000000
817145bc: 00000000 00000000 00000000

0x45f4
```
Some fun stuff you can do:

Patch Z-Loader to be without password by default

Get an OLT to upload modded zyxel firmware with known credentials but no locked LAN access

Not use Zyxel devices

