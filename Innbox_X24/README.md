# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | EcoNet EN7580 SOC                                                          |
| DRAM            | 256 MB                                                                     |
| Flash Size      | 128 MB WINBOND W25N01G                                                     |
| CPU Arch        | MIPS interAptiv (multi) V2.12 - (2 Core, 4 Threads)                        |
| CPU Clock       | 1.3 GHz                                                                    |
| Bootloader      | Econet free bootbase                                                       |
| System          | Linux version 4.4.115 (gcc version 4.6.3 (Buildroot 2015.08.1-g0b1c64e) )  |
| Ethernet ports  | 1x10G (Supports 2.5Gbase-T and 5Gbase-T) Most likely Airoha PHY            |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.2.1/24                                                             |
| Web Gui         | ✅  After unlock                                                           |
| SSH             | ✅  (Port 55522)                                                           |
| Telnet          | ✅  (Port 55523)                                                           |
| TFTP            | ✅                                                                         |
| Serial          | ✅                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

Probably well capable hardware kept back by how awfull Econet and Iskratel code is.

Bootloader is useless for recovery.

Repeated dissambly weakens low quality plastic screw posts resulting in loose cover.

After unlock default ip changes to 192.168.1.1/24. 

WebUI is now open, SSH and Telnet are disabled by default, enbale them in System -> Access Management -> IPv4

## Flash layout
```
dev:    size   erasesize  name
mtd0: 00040000 00020000 "bootloader"		- Bootbase
mtd1: 00040000 00020000 "romfile"
mtd2: 0027c77b 00020000 "kernel"
mtd3: 01320000 00020000 "rootfs"
mtd4: 03000000 00020000 "tclinux"		- Image A
mtd5: 03f80000 00020000 "kernel_slave"
mtd6: 00000000 00000000 "rootfs_slave"
mtd7: 03000000 00020000 "tclinux_slave"		- Image B
mtd8: 00100000 00020000 "config"		- INNDACFG1
mtd9: 00100000 00020000 "Equip"			- INNDAENV
mtd10: 00100000 00020000 "WlanE2pData"		- Blank
mtd11: 00100000 00020000 "bootEnv"		- INNDABOOT
mtd12: 00100000 00020000 "VoiceLog"		- Blank
mtd13: 00100000 00020000 "SystemLog"		
mtd14: 00200000 00020000 "SaaS"			- /var/SaaS/ jffs2
mtd15: 00240000 00020000 "reservearea"
```

## Unlock v1
- Dump SPI
- Flip a byte in nvram "customer"
- Write back 
- Reset will fallback and rewrite customer=Iskratel

## Unlock v2
- Login as admin / ```c79@NkZ5LJgZ33+Lp6@%``` TODO: UART tested, SSH should work too
- fad config setenv customer_id Iskratel
- Reset to unlock

> ## ⚠️ Important
> Do not write mtd9 with any tools present on device, it will brick the device!
> Crash of main process is not recoverable due to missing login credentials, nand rewrite is needed to fix this!

## Config edit
```
# Readout info
# Many commands have no help to get all options
# fad decompile has alot of helpfull code to learn from
/userfs/bin/tcapi show GPON_ONU
# Set env value
fad config setenv serial_gpon ISKTA1B2C3D4

# XML Edit
csmconf -s /InternetGatewayDevice/ManagementServer/EnableCWMP 0
csmctl savecfg

# Set "manufacturer" user password to admin one (and enable it)
# SYSTEM -> Customization secret menu unlocked :)
# Still does not allow to open all hidden html pages
csmconf -s sys.user.4.password  'U2FsdGVkX18C8hH0ADzGky2BdLI5McGYp/IhqX3jps6XMyFh7kkJhjuPyY8ZO+fo'

```

## Usefull links
[Econet Linux](https://econet-linux.pkt.wiki/en/bootloader)
[Econet GPL code](https://github.com/cjdelisle/EN751221-Linux26/)
