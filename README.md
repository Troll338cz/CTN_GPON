# CTN_GPON
Firmware collection for cheap GPON bridges


|   Device        |  Firmware dump |  Firmware modded | Supports full OMCI editing | XPON |  Secure boot | ISP |
| --------------- | ---------------|------------------|----------------------------|------|------- | -------- |
| Comtrend GRG-4284 	| ✅ | ✅ | ✅ | ✅ | ❌ | Cetin |
| Comtrend GRG-4362 	| ✅ | ✅ | ✅ | ❌ | ❌ | Cetin |
| Iskratel Innbox G23	| ✅ | ✅ | ✅ | ❓ | ❌ | Cetin |
| Kaon PM1191			| ✅ | ✅ | ❓ | ❌ | ❌ | T-Mobile |
| Orange G-25E			| ✅ | ✅ | ❓ | ❓ | ❌ | Orange.sk |
| Sercomm FG1000R	(WIP)	| ✅ | ❌ | ❓ | ❓ | ✅ | - |
| Sercomm RHG3006	(WIP)	| ❓ | ❌ | ❌ | ❓ | ✅ | - |
| ZTE F6005	(WIP)			| ✅ | ✅ | ✅ | ❌ | ❌ | - |
| Frontier FOG421			| ✅ | ❓ | ❓ | ❓ | ❌ | - |
| Tenda HG1     			| ✅ | ✅ | ✅ | ✅ | ❌ | - |
| Zyxel PM5100-T0 			| ✅ | ❓ | ❓ | ❓ | ❌ | Cetin |
| Iskratel Innbox X24	| ✅ | ❓| ❌ | ❌ | ❓ | Cetin |

## Notes
Comtrend GRG-4284 - After flash works without issues, GPON/EPON tested, OMCI already patched with firmware unlock.

Innbox G23 - Most hardcoded MIBs removed, old 2.6 kernel.

CIG G-25E - Old device, not worth looking into OMCI editing.

Comtrend GRG-4362 - Info in my other repo, XGS-PON.

Sercomm FG1000R - Secure boot, locked down firmware, probably will only provide dump.

Sercomm RHG3006 (Vodafone Fiber Station) - Secure boot, don't have tools to dump currently.

ZTE F6005 - Writeup and firmware mod by @rgiorgiotech, missing unlocked bootloder files.

Zyxel PM5100-T0 - For easy unlock zyeng, SPI dump or known login is needed, has per device password for bootloader and users.

Innbox X24 - Limited by software and SDK, no good documentation.

Kaon PM1191 - XGS-PON, firmware mod removes ISP branding.

## TODO
Flash GRG-4284 firmware into G23 - Crashed for me unsure why, hardware should support it.

ISP testing - Info on Vodafone custom ONT support, look into CEZNET

Make archive with all Zyxel firmwares -  ✅  [Firmware files](https://files.qqwee.net/Zyxel/)

Vodafone PM7500
