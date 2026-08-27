# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Cortina CA8271A                                                            |
| DRAM            | 256 MB                                                                     |
| Flash Size      | 128 MB MICRON MT29F1G01ABAFD                                               |
| CPU Arch        | MIPSel with DSP                                                            |
| CPU Clock       | 666 MHz                                                                    |
| Bootloader      | U-Boot 2020.04                                                             |
| System          | Linux 4.14.275.saturn2-sfu-r2.2 + RTOS "Zephyr" for HW offload             |
| Ethernet ports  | 1x 10/100/1000/2.5G/5G/10G Base-T                                          |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.1.1/24                                                             |
| Web Gui         | ✅ (_eng builds only)                                                      |
| SSH             | ✅                                                                         |
| Telnet          | ❌ (Cortina cli on localhost:2323)                                         |
| FTP             | ❌                                                                         |
| Serial          | ✅ (_eng builds only, U-Boot always)                                       |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

> ## ⚠️ Important
> The encryption key for each device is bound to the MAC address in the U-Boot ENV.
> This includes the administrator password and the scfg.txt file, a backup is recommended.
> If the key is regenerated after changing the MAC address, permanent data loss may occur!

## Firware commands
Boot from image0
```
# fw_setenv img_active 1
# fw_setenv img_commit 1

dev:    size   erasesize  name
mtd0: 00400000 00020000 "ssb"
mtd1: 00200000 00020000 "uboot-env"
mtd2: 00100000 00020000 "dtb0"
mtd3: 00600000 00020000 "kernel0"
mtd4: 02800000 00020000 "rootfs0"
mtd5: 00100000 00020000 "dtb1"
mtd6: 00600000 00020000 "kernel1"
mtd7: 02800000 00020000 "rootfs1"
mtd8: 01400000 00020000 "userdata"
mtd9: 00800000 00020000 "logdata"
mtd10: 01129000 0001f000 "squashfs_ubi"
mtd11: 01078000 0001f000 "userdata"
```

Boot from image1
```
# fw_setenv img_active 2
# fw_setenv img_commit 2

dev:    size   erasesize  name
mtd0: 00400000 00020000 "ssb"
mtd1: 00200000 00020000 "uboot-env"
mtd2: 00100000 00020000 "dtb1"
mtd3: 00600000 00020000 "kernel1"
mtd4: 02800000 00020000 "rootfs1"
mtd5: 00100000 00020000 "dtb0"
mtd6: 00600000 00020000 "kernel0"
mtd7: 02800000 00020000 "rootfs0"
mtd8: 01400000 00020000 "userdata"
mtd9: 00800000 00020000 "logdata"
mtd10: 01129000 0001f000 "squashfs_ubi"
mtd11: 01078000 0001f000 "userdata"
```

Update firmware
```
# cd /tmp
# wget 192.168.1.XXX:8080/new_rootfs1.img
# flash_eraseall /dev/mtdX
# flashcp -v new_rootfs1.img /dev/mtdX
```

Change PON settings
```
/sbin/fw_setenv gpon_passwd KAONA1B2C3D4
/sbin/fw_setenv loid LoidUSer
/sbin/fw_setenv loid_passwd LoidPass
```

## Extra info
Make sure to check what image is active, switching doesn't change the mtd number only its name.

Non _eng builds don't start getty on serial and have deleted webserver binary.

On _eng builds getty waits for all init services, lighttpd takes a while to start.

U-Boot has non-working networking

