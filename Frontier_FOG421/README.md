# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Realtek RTL8696                                                            |
| DRAM            | 128 MB                                                                     |
| Flash Size      | 128 MB                                                                     |
| CPU Arch        | MIPSBE Realtek Lexra                                                       |
| CPU Clock       | 700MHz                                                                     |
| Bootloader      | U-Boot CIG custom RSDK 2011                                                |
| System          | Linux 2.6.30.9-cig-sfu-1 (gcc version 4.4.6 (Realtek RSDK-1.5.6p2) )       |
| Ethernet ports  | 4x 1000Base-T                                                              |
| PHY Ethernet    | RTL8696GMAC                                                                |
| Optics          | SEMTECH 25L95 SC/APC                                                       |
| IP address      | 192.168.100.1/24                                                           |
| Web Gui         | ❌                                                                         |
| SSH             | ❌                                                                         |
| Telnet          | ✅                                                                         |
| FTP             | ✅(Basic ftpput/ftpget)                                                    |
| Serial          | ✅                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

# Flash layout in ram
```
#ONT/system/fs>show flash
    System Flash Partition Information
dev:    size   erasesize  name
mtd0: 000c0000 00020000 "Boot1"
mtd1: 00200000 00020000 "Config1"
mtd2: 01c00000 00020000 "ImageA"
mtd3: 01c00000 00020000 "ImageB"
mtd4: 00300000 00020000 "KernelA"
mtd5: 000c0000 00020000 "Boot2"
mtd6: 00200000 00020000 "Config2"
mtd7: 00e00000 00020000 "Imagec1"
mtd8: 00e00000 00020000 "Imagec2"
mtd9: 00100000 00020000 "eeprom1"
mtd10: 00100000 00020000 "eeprom2"
mtd11: 00300000 00020000 "KernelB"
mtd12: 01600000 00020000 "rsv"
mtd13: 00800000 00020000 "MidWare"
```

# Access U-Boot
```
# When you see:
**************************************
*                                    *
*  KEY -- Enter console terminal     *
*                                    *
**************************************
waiting for your select ...

# Spam this on your host system
echo -en "\x1B\x1D\x0F\x0B" > /dev/ttyUSB0
```

# Dump flash
```
RTL8696# bdinfo
boot_params = 0x87CF3F98
memstart    = 0x80000000
memsize     = 0x08000000
flashstart  = 0xBD000000
flashsize   = 0x10090828
flashoffset = 0x00000000
ethaddr     = E4:8E:10:AA:BB:CC
ip_addr     = 192.168.100.1
baudrate    = 115200 bps

md.b shown empty bytes, maybe nand command needed to copy to ram.

```

# Modify firmware
```
# Byte swap BE->LE
cramfsswap ImageB ImageB.le
# Unpack to folder as root
pycramfs extract -d ImageB_out ImageB.le
# Repack as root
mkfs.cramfs -N big ImageB_out ImageB.mod
# From U-Boot load with TFTP
upgdimage imageX
# Swap active image
eeprom set activeimage imageX

# Use imagea for testing, imageb for running
# CRC 4 bytes needs to be added to end of file
# If you try to install img with invalid crc it should print the correct one when flashing from linux or booting uboot

#ONT/system/fs>
#ONT/system/fs>upgrade
Starting download 'rootfs.img' from Ftp server'192.168.100.253' ... Done.
Starting save 'rootfs.img' to Flash Partition 2 ...
Check image file CRC ... cal_crc (ed879a5f) ori_crc (aabbccdd) crc check error
# I don't recomend upgrade from OS since you need really old FTP server and its tragicly slow compared to U-Boot
```

# Get shell on UART
```
# No password on this device??
ONT>enable
#ONT>?
  Description: CLI Root
    +traffic             Service CLI menu    
    +system              System CLI menu     
#ONT>sys
#ONT/system>
#ONT/system>shell
#ONT/system/shell>
```

# Enable LAN access
```
#ONT/system/misc>admin_en set 1
# Reboot

#ONT/system/shell>ifconfig
lan0      Link encap:Ethernet  HWaddr E4:8E:10:AA:BB:CC
          inet addr:192.168.100.1  Bcast:192.168.100.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:4507 errors:0 dropped:0 overruns:0 frame:0
          TX packets:16298 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:278489 (271.9 KiB)  TX bytes:19017457 (18.1 MiB)
# or from U-boot
eeprom set adminen 1

TLF_TELNET_ENABLE=1 can be set by adding sys.cfg into /mnt/rwdir but unlock tool still needed
TODO: CLI debug submenu menu creds

```


