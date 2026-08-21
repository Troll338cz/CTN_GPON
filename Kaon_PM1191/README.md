# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Cortina CA8271A                                                            |
| DRAM            | 256 MB                                                                     |
| Flash Size      | 128 MB MICRON MT29F1G01ABAFD                                               |
| CPU Arch        | MIPSBE Dualcore + DSP                                                      |
| CPU Clock       | 666 MHz                                                                    |
| Bootloader      | U-Boot 2020.04                                                             |
| System          | Linux 4.14.275.saturn2-sfu-r2.2 + RTOS "Zephyr" for HW offload             |
| Ethernet ports  | 1x 10/100/1000/2.5G/5G/10G Base-T                                          |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.1.1/24                                                             |
| Web Gui         | ❓ (Depends on version, not many features)                                 |
| SSH             | ✅                                                                         |
| Telnet          | ❌ (Cortina cli on localhost:2332)                                         |
| FTP             | ❌                                                                         |
| Serial          | ❌ (U-Boot only, no shell)                                                 |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

> ## ⚠️ Important
> The encryption key for each device is bound to the MAC address in the U-Boot ENV.
> This includes the administrator password and the scfg.txt file, a backup is recommended.
> If the key is regenerated after changing the MAC address, permanent data loss may occur!

## FW Warning
T-Mobile version with hardcoded TR-069!

Backup your current one and only flash one image at once to prevent brick in case of incompatibility.

Currently not modified.
