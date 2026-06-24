
I hate Zyxel for making me desolder the SPI chip just to unlock this...

Z-Loader now has a password, please just allow users full access instead of clowing with all the locks.

Unlock this evil thing:

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

Some fun stuff you can do:

Patch Z-Loader to be without password by default

Get an OLT to upload modded zyxel firmware with known credentials but no locked LAN access

Not use Zyxel devices

