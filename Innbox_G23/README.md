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
| Ethernet ports  | 1x 1000Base-T                                                              |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.150.1/24                                                           |
| Web Gui         | ✅                                                                         |
| SSH             | ✅                                                                         |
| Telnet          | ✅                                                                         |
| FTP             | ✅                                                                         |
| Serial          | ✅                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

Unless more work is put into patching MIPS binaries system will reset most of OMCI info on reboot.

It should be possible to use /var/config/run_customized_sdk.sh to set values back on startup as a temporary fix.

GRG-4284 and G23 is idential device, Comtrend software uses newer SDK and isnt locked but i haven't got crossflash to boot properly.

Unsure if this is due to U-Boot version or issue with hardware but Comtrend firmware will hang on boot and shorty after crash with OOM error.

