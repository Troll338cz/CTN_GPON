# HW Info
|                 |                                                                            |
| --------------- | -------------------------------------------------------------------------- |
| CPU             | Econet EN7580                                                              |
| DRAM            | 256 MB                                                                     |
| Flash Size      | 128 MB WINBOND W25N01G                                                     |
| CPU Arch        | MIPS                                                       |
| CPU Clock       | ? MHz                                                                      |
| Bootloader      | Econet free bootbase                                                       |
| System          | Linux 4.4.115                                                              |
| Ethernet ports  | 1x10G (Supports 2.5Gbase-T and 5Gbase-T) Most likely Airoha PHY            |
| Optics          | SC/APC                                                                     |
| IP address      | 192.168.2.1/24                                                             |
| Web Gui         | ❓  Present in firmware, maybe locked?                                     |
| SSH             | ✅  (Port 55522)                                                           |
| Telnet          | ✅  (Port 55523)                                                           |
| FTP             | ❌                                                                         |
| Serial          | ✅                                                                         |
| Serial baud     | 115200                                                                     |
| Serial encoding | 8-N-1                                                                      | 
| Form Factor     | ONT                                                                        |

Probably well capable hardware kept back by how awfull Econet and Iskatrel code is.
Bootloader is useless.

## Unlock v1
- Dump SPI
- Flip a byte in nvram "customer" ( todo look in fad for checksum )
- Reset will fallback and rewrite customer=Iskatrel 
- Write back 
