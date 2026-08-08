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

Probably well capable hardware kept back by how awfull Econet and Iskatrel code is.
Bootloader is useless.

Repeated dissambly weakens low quality plastic screw posts resulting in loose cover.

After unlock default ip changes to 192.168.1.1/24. 

WebUI is now open, SSH and Telnet are disabled by default, enbale them in System -> Access Management -> IPv4

## Flash layout
```
dev:    size   erasesize  name
mtd0: 00040000 00020000 "bootloader"
mtd1: 00040000 00020000 "romfile"
mtd2: 0027c77b 00020000 "kernel"
mtd3: 01320000 00020000 "rootfs"
mtd4: 03000000 00020000 "tclinux"
mtd5: 03f80000 00020000 "kernel_slave"
mtd6: 00000000 00000000 "rootfs_slave"
mtd7: 03000000 00020000 "tclinux_slave"
mtd8: 00100000 00020000 "config"
mtd9: 00100000 00020000 "Equip"
mtd10: 00100000 00020000 "WlanE2pData"
mtd11: 00100000 00020000 "bootEnv"
mtd12: 00100000 00020000 "VoiceLog"
mtd13: 00100000 00020000 "SystemLog"
mtd14: 00200000 00020000 "SaaS"
mtd15: 00240000 00020000 "reservearea"
```

## Unlock v1
- Dump SPI
- Flip a byte in nvram "customer"
- Write back 
- Reset will fallback and rewrite customer=Iskatrel

## Unlock v2
- Login as admin / ```c79@NkZ5LJgZ33+Lp6@%``` TODO:UART tested, SSH should work too
- Edit nvram tool TODO
- Reset to unlock

> ## ⚠️ Important
> Do not write mtd9 with any tools present on device, it will brick the device!
> Crash of main process is not recoverable due to missing login credentials, nand rewrite is needed to fix this!

## Config edit
```
# Resets after reboot
/userfs/bin/tcapi show GPON_ONU
/userfs/bin/tcapi set GPON_ONU SerialNumber "AAAABBBBBBB"
/userfs/bin/tcapi set GPON_ONU VendorId "KAON"

# Cant save file
/userfs/bin/cfg show root.GPON.ONU
/userfs/bin/cfg set root.GPON.ONU SerialNumber ISKTABCD1234

# Saves
csmconf -s /InternetGatewayDevice/ManagementServer/EnableCWMP 0
# Resets after reboot
csmconf -s /InternetGatewayDevice/X_INNBOX_GPON/ONU/SerialNumber ISKTABCD1234
csmctl savecfg

```
