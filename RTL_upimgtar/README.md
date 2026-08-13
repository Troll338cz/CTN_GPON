Quick look at Realtek tar file and multicast upgrade.

Will be important to flash supported ONTs without needing serial.

Note that not all devices have this feature enabled and in working state.

Basic files:
```
fwu.sh - Shell script when flashing from linux, depends on board if it has only simple dual boot or with dtb and ubi, ignored in U-Boot.

fwu_ver - Version string that will be written into sw_version0 and sw_version1

hw_ver - Linux update only, HW_HWVER check.

md5.txt - List of md5 sums for fwu.sh, Unix newlines, format md5 and filename seperated by a single space 

rootfs - rootfs image, mainly found squashfs, should work with jffs2 and cramfs aswell.

uImage - uImage kernel file
```

Tar file must be POSIX 1003.1-1990, uncompressed

Take care when repacking rootfs since it needs to fit and follow specific parameters. (Compression & block size)

On UBI devices volumes are written with U-Boot commands from env

Example output from Comtrend GRG-4284:
```
9601D# tftp ${tftp_base} Comtrend.tar
Using LUNA GMAC  device
TFTP from server 192.168.1.7; our IP address is 192.168.1.3
Filename 'Comtrend.tar'.
Load address: 0x81c40000
Loading: #################################################################
         #################################################################
         #################################################################
         #################################################################
         #################################################################
         #################################################################
         #################################################################
         ####
done
Bytes transferred = 6727680 (66a800 hex)
9601D#  upimgtar  ${tftp_base} ${filesize}
img.tar is located at 81c40000 (size = 0x0066a800)
File in Tar: fwu.sh at 0x00000200 (size: 0x000007e8)
File in Tar: fwu_ver at 0x00000c00 (size: 0x0000000c)
File in Tar: hw_ver at 0x00001000 (size: 0x00000005)
File in Tar: kernel at 0x00001400 (size: 0x001d056d)
File in Tar: md5.txt at 0x001d1c00 (size: 0x000000cb)
File in Tar: rootfs at 0x001d2000 (size: 0x00496000)
kernel partition at 0x00080000, size=0x00300000
CMD = sf erase 80000 +300000; sf write 81c40000 80000 0
Erasing 3145728 B from 00080000... 100% ~ 0037ffff/3145728 B
Writing 0 B from 81c40000 to 00080000... EE: unknown error: 0
2nd kernel partition at 0x00840000, size=0x00300000
CMD = sf erase 840000 +300000; sf write 81c40000 840000 0
Erasing 3145728 B from 00840000... 100% ~ 00b3ffff/3145728 B
Writing 0 B from 81c40000 to 00840000... EE: unknown error: 0
rootfs partition at 0x00380000, size=0x004c0000
CMD = sf erase 380000 +4c0000; sf write 81e12000 380000 496000
Erasing 4980736 B from 00380000... 100% ~ 0083ffff/4980736 B
Writing 4808704 B from 81e12000 to 00380000... 100% ~ 00815fff/4808704 B
2nd rootfs partition at 0x00b40000, size=0x004c0000
CMD = sf erase b40000 +4c0000; sf write 81e12000 b40000 496000
Erasing 4980736 B from 00b40000... 100% ~ 00ffffff/4980736 B
Writing 4808704 B from 81e12000 to 00b40000... 100% ~ 00fd5fff/4808704 B
Update SW Version: CTN-1.1.4b6
sw_version0 empty, set CTN-1.1.4b6
sw_version1 empty, set CTN-1.1.4b6
Erasing SPI flash...Erasing 8192 B from 00040000... 100% ~ 00041fff/8192 B
Writing to SPI flash...Writing 8192 B from 81adbb30 to 00040000... 100% ~ 00041fff/8192 B
Writing 1 B from 81addb3c to 00042004... 100% ~ 00042004/1 B
done
Valid environment: 1
Update Image CRC32
old sw_crc0 [fdab829c] is different to new [9ac2bea9], set new crc
old sw_crc1 [fdab829c] is different to new [9ac2bea9], set new crc
Erasing SPI flash...Erasing 8192 B from 00042000... 100% ~ 00043fff/8192 B
Writing to SPI flash...Writing 8192 B from 81adbae8 to 00042000... 100% ~ 00043fff/8192 B
Writing 1 B from 81addaf4 to 00040004... 100% ~ 00040004/1 B
done
Valid environment: 2
Update img.tar Done
```

Warning: flash will be erased to size of file in tar, no checks against partitions are done! 

If you have a copy of Realtek ASDK with U-Boot sources files "cmd_upimgtar.c" and "multicast_upgrade.c" contain all information needed about upgrade process.
