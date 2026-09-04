# Total eCos death

## HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Intel Lantiq PEB98036                                                      |
| DRAM            | 1 MB Inside SoC                                                            |
| Flash Size      | 8 MB MX25L6405D                                                            |
| CPU Arch        | MIPSBE 34Kc                                                                |
| CPU Clock       | 400MHz                                                                     |
| Bootloader      | U-Boot 2011.12-lantiq-gpon-1.2.20.1-svn20 (Aug 10 2015 - 13:49:58)         |
| System          | eCos                                                                       |
| Ethernet ports  | 1x 1000Base-X                                                              |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.2.200/24                                                           |
| Web Gui         | ❌                                                                         |
| SSH             | ❌                                                                         |
| Telnet          | ✅                                                                         |
| FTP             | ❌                                                                         |
| Serial          | ❓                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | Mini ONT SFP                                                               |


## Telnet
Since my OLT is a pice of crap i can't suceessfully setup IPHost to telnet into the stick from there

So the hard way it is....

In function sub_100510D4 we see:
```
        v23 = sub_1001DBF8("ft_flag", 1); // sc_factory_data_get
        if ( sub_1002FA54(v23, "1") )     // strcmp
        {
          for ( i = (_DWORD *)MEMORY[0x9F216C48]; i && sub_1002FA54(*(_BYTE **)(i[9] + 8), "eth0"); i = (_DWORD *)*i )
            ;
          if ( ((i[1] ^ v22[3]) & i[2]) == 0 )
          {
            sub_1002BBA0("TN: Telnet service is blocked by Lan interface, client will be closed!\n");
            v25 = v69;
            goto LABEL_39;
          }
        }
```

eth0 i presume is SFP host interface

ft_flag - Factory Telnet - 4 mentions in the whole file, telnet LAN check, start network stack and telnet on boot and keeping its value upon factory reset.

Looking at the flash dump its set to 0 by default

~~Testing for setting to 1 later...~~ - Too lazy, patched FW instead :) 

## Get GPON paremeters
```
FGS202:/# show device
Returns IPs, GPON SN, Image versions and UPTIME
FGS202:/# show i2c
Hexdump of simulated I2C 0x000-0x1FF
Gpon password *should* be in there

Mikrotik stops reading at 0xFF, external I2C maybe?
I2C will save the GPON Password to its persitent ENV if you write the correct offset 0xB8-0xC2 (see sub_1001A1B8)
You can chance SN and mac with env editor, just make sure to backup encrypt_data first.
OMCI Editing unknown (most likely with embeded mib)
This device was never meant to be reconfigured beyond setting the GPON password, it lacks buildin env editor.
```

## Load into IDA
Grab image0/1 without the 256 byte header

Byteswap the file

Set CPU to MIPSBE

Fill out "Disassembly memory organisation":
```
Create RAM section	unchecked
Create ROM section	checked
ROM start address	0x10000000
Loading address	0x10000000
File offset	0x0
```

Result is firmware loaded and decomiles into readable functions.

## Flash dump and layout
Huge thanks to OpenWRT forum user @centaur for [digging into this device](https://forum.openwrt.org/t/support-for-gpon-sfp-fgs202/42641) and providing a second flash dump
 
```
0x000000-0x03FFFF  0000000-0262143  # U-Boot/ magic number=0xFFDD0022
0x040000-0x04FFFF  0262144-0327679  # uboot_env
0x050000-0x05FFFF  0327680-0393215  # Factory info/ at 0x50000 CRC32 for (0x050005-0x05FFFF)
0x060000-0x06FFFF  0393216-0458751  # Config storage  / at 0x60000 CRC32 for (0x060005-0x06FFFF)
0x070000-0x07FFFF  0458752-0524287  # syslog storage
0x080000-0x08FFFF  0524288-0589823  # uboot_env(redund) /at 0x80000 CRC32 for (0x080005-0x08FFFF)
0x0FFF00-0x0FFFFF  1048320-1048575  # 256 bytes image0 header/CRC32 at 0x0FFF18(reversed) for(0x100000-0x2A0CE7)
0x100000-0x2A0CE7  1048576-2755815  # Image0/magic number=0x2100FF03
0x47FF00-0x47FFFF  4718336-4718591  # 256 bytes image1 header/CRC32 at 0x47FF18(reversed) for(0x480000-0x620CE7)
0x480000-0x620CE7  4718592-6425831  # Image1/magic number=0x2100FF03
0x7D0000-0x7DFFFF  8192000-8257535  # syslog storage(redund)
0x7F0000-0x7FFFFF  8323072-8388607  # Config storage  / at 0x7F0000 CRC32 for (0x7F0005-0x7FFFFF)

image0 pid_addr 0x2a0ce8
image1 pid_addr 0x620ce8
64 bytes long encrypted gpon password at 0x7F0168 - Cracked, see util/decrypt_encrypt_data.py 

Byteswap Image, run again to swap back:
xxd -e -g4 img0.bin | xxd -r > img0.byteswap

The empty areas between images are usualy 0xFF sometimes Sercomm stuff (ex. U-Boot 0x3FFB0-0x3FFF0)

There is 2 null bytes after each image, after the version, its not checked by CRC or probably the code but i worth a mention.

```

environ values mentioned in code
```
Config   - ['ethaddr', 'nSerial', 'image0_version', 'image1_version', 'user', 'qos_reservation', 'hua_vlan_sort', 'LOG_CURRENT_START_BLOCK', 'nPassword', 'mib_file']
Factory  - ['ethaddr', 'nSerial', 'date_code', 'bosa_type', 'pcbasn', 'ft_flag', 'nSerial', 'ipaddr', 'nPassword']
uboot??? - ['c_img', 'sc_dl', 'committed_image']

# sub_10063398
mib_file=HWTC or ALCL
# Huawei and Nokia OLT specific mode??
# Other OLT types should be unset probably (may explain issue with VSOL)

```

## Firmware Upgrade
From the decompile it looks like:

When upgradeing from TFTP or OMCI do not include the 256 header, it is accualy built in code after file is recived.

If SPI editing then rewrite both header and image

## U-Boot network flash
> ## ⚠️ Important
> DO NOT RUN THISE COMMANDS!! Not recoverable if you dont have the tools!

Hidden command "sercomm_download", sets sc_dl=1 and reboots device.

Drops you to Sercomm download mode, then you can upload new flash using sercomm-recovery rewrite both images and empty flash between.

```
DEBUG_INF:===================================================
DEBUG_INF:Sercomm Upgrade(Module Ver 2.14.02.24) Start!
DEBUG_INF:===================================================
SF: Detected MX25L6405D with page size 64 KiB, total 8 MiB

0x0000: 00  c0  02  XX  XX  XX
SERDES: Link Speed is 1000 Mbps - FULL duplex connection
DEBUG_INF:ecc bytes 0
PCBASN = R.BNN72O048E
DEBUG_INF:normal upgrade.
DEBUG_INF:Erase Done.
DEBUG_INF:Program Starting.
DEBUG_INF:Verify Starting.
DEBUG_INF:===================================================
DEBUG_INF:=   Stats of this Sercomm Upgrade is as below:    =
DEBUG_INF:===================================================
DEBUG_INF:Following Partitions NOT Erased,
DEBUG_INF: Index Name                Offset    Length
DEBUG_INF:     0 u-boot              0         40000
DEBUG_INF:     1 u-boot-env          40000     10000
DEBUG_INF:     2 factory_data        50000     10000
DEBUG_INF:     3 fw_config           60000     10000
DEBUG_INF:     4 sercomm_log         70000     10000
DEBUG_INF:     5 u-boot-env-second   80000     10000
DEBUG_INF:    10 image1_reserve      7f0000    10000
DEBUG_INF:---------------------------------------------------
DEBUG_INF:Following Partitions Updated,
DEBUG_INF: Index Name                Bad Cnt   Dropped
DEBUG_INF:     6, reserved_area       0         0
DEBUG_INF:     7, image0              0         0
DEBUG_INF:     8, image0_reserve      0         0
DEBUG_INF:     9, image1              0         0
DEBUG_INF:===================================================
```

Note the difference between @centaur's flash laylout and Sercomm's

Redundant env and log are not mentioned, instead they are part of reserve areas.

This custom protocol is undocumented, its pretty basic and wants the full 8Mb (8388608 bytes) dump, thankfully skips anything that is needed for device to boot back into recovery upon fails, its the device decides what areas to write.

Note that you need a dumb SFP to RJ45 converter, U-Boot leaves i2c blank and anything that reads it will just ignore the module.

Unsure what other secrets Sercomm's U-Boot holds, so far no results in trying to decompile or mod it...
