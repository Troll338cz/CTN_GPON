# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | BROADLIGHT BL2338R                                                         |
| DRAM            | 32 MB                                                                      |
| Flash Size      | 16 MB                                                                      |
| CPU             | MIPS 4KEc V6.8 MIPS Goldenrod evaluation board                             |
| CPU Clock       | 200MHz                                                                     |
| Bootloader      | U-Boot 2022.10                                                             |
| System          | Linux version 2.6.15 (root@localhost.localdomain) (gcc version 4.0.2)      |
| Ethernet ports  | 4x 100Base-T                                                               |
| PHY Ethernet    | 88E0645-TAH1                                                               |
| Optics          | SC/APC (OPGP-34-A4B3SL)                                                    |
| IP address      | 192.168.1.154/24 (After mod)                                               |
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
    System Flash Partion Information
Flash Base:         0xbf000000
Flash Size:         0x1000000
System Flash are divided into 5 partitions
0xbf000000-0xbf1fffff : config
0xbf200000-0xbf6fffff : ImageA
0xbf700000-0xbfbfffff : ImageB
0xbfc00000-0xbfc7ffff : bootload
0xbfc80000-0xbfffffff : ImageC

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
[ONT Loader] bdinfo
boot_params = 0x81F2FFB0
memstart    = 0x80000000
memsize     = 0x02000000
flashstart  = 0xBF000000
flashsize   = 0x01000000
flashoffset = 0x00000000
ethaddr     = 00:19:C7:BB:AA:CC
ip_addr     = 192.168.1.251
baudrate    = 115200 bps
flags       = 0x00000003
ramsize     = 0x02000000
relocoff    = 0xC2390000
envaddr     = 0x81F5000C
Programming FPGA ... 
unzip FPGA ...OK!

download Fpga ...75894...OK!
Resetting Fpga and Switch ... OK!
OK!
[ONT Loader] 
[ONT Loader] md.b BF000000 1000000
# Wait few hours...
# Cleanup and convert screenlog.0 with md.b_convert.py

```

# Modify firmware
```
# Take ImageB, delete empty flash
dd if=mtd2_ImageB of=ImageB bs=4530180 count=1
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
# CRC needs to be added to end of file:
# Stock firmware size 4530176, crc append 4 to size 4530180
# If you try to install img with invalid crc it should print the correct one when flashing from linux or booting uboot

#ONT/system/fs>
#ONT/system/fs>upgrade
Starting download 'rootfs.img' from Ftp server'192.168.1.253' ... Done.
Starting save 'rootfs.img' to Flash Partition 2 ...
Check image file CRC ... cal_crc (ed879a5f) ori_crc (aabbccdd) crc check error
# I don't recomend upgrade from OS since you need really old FTP server and its tragicly slow compared to U-Boot
```

# Get shell
```
ONT>enable
#ONT>login
User name:root
Password:huigu309
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
eth0      Link encap:Ethernet  HWaddr 00:19:C7:AA:BB:CC  
          inet addr:192.168.1.251  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)
# or from U-boot
setenv adminen 1

```

# U-Boot hidden commands
```

[ONT Loader] 
[ONT Loader] eeprom set activeimage imageb
activeimage = ImageB
[ONT Loader] eeprom set adminen 1
adminen = 1
[ONT Loader] 


eeprom  - EEPROM sub-system
init
       - initialize eeprom value to factory default
eeprom read addr off cnt
       - read 'cnt' bytes from EEPROM offset 'off' to 'addr'
eeprom write addr off cnt
       - write 'cnt' bytes of 'addr' content to EEPROM offset 'off'
eeprom get item
       - get eeprom item information
       - item
          - activeimage -- active image
          - adminen     -- adminport enable
          - imagename   -- system image name
          - bootpth     -- system boot path
          - eepver      -- get eeprom version
          - ethaddr     -- ethernet port0 mac address
          - eth1addr    -- ethernet port1 mac address
          - ftpuser     -- ftp login user name
          - ftppw       -- ftp login password
          - gateway     -- system gateway address
          - hwdiag      -- hardware diagnostic information
          - ipaddr      -- system local ip address
          - ipmask      -- system local ip mask
          - major       -- system hardware major version
          - minor       -- system hardware minor version
          - serverip    -- remote server ip address
          - upgdstatus  -- upgrade status
          - upgdtest    -- upgrade flag
eeprom set item value
       - set eeprom 'item' with 'value'
       - item
          - activeimage -- active image
           - value
             - imagea -- boot from Image A
             - imageb -- boot from Image B
          - adminen     -- adminport enable
           - value
             - 0  -- admin port disable
             - 1  -- admin port enable
          - imagename   -- system image name
          - bootpth     -- system boot path
            - value
              - tftp  -- boot from tftp
              - flash -- boot from flash
          - ethaddr     -- ethernet port0 mac address
          - eth1addr    -- ethernet port1 mac address
          - ftpuser     -- ftp login user name
          - ftppw       -- ftp login password
          - gateway     -- system gateway address
          - ipaddr      -- system local ip address
          - ipmask      -- system local ip mask
          - major       -- system hardware major version
          - minor       -- system hardware minor version
          - serverip    -- remote server ip address
          - upgdtest    -- upgrade flag
          - upgdstatus  -- upgrade status
eeprom clear hwdiag
       - clear all of the record


upgdimage [place] [filename]
place: upgrade image save to flash, value as follow
        - imagea -- First root file system ImageA
        - imageb -- second root file system ImageB
        - imagec -- factory root file system ImageC
```
