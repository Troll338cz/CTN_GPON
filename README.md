# CTN_GPON
Firmware collection for cheap GPON bridges


|   Device        |  Firmware dump |  Firmware modded | Supports full OMCI editing | XPON |  Secure boot | ISP |
| --------------- | ---------------|------------------|----------------------------|------|------- | -------- |
| Comtrend GRG-4284 	| ✅ | ✅ | ✅ | ✅ | ❌ | Cetin |
| Comtrend GRG-4362 	| ✅ | ✅ | ✅ | ❌ | ❌ | Cetin |
| Iskratel Innbox G23	| ✅ | ✅ | ⚠ | ❓ | ❌ | Cetin |
| Kaon PM1191			| ✅ | ❌ | ❓ | ❌ | ❓ | T-Mobile |
| Orange G-25E			| ✅ | ✅ | ❓ | ❓ | ❌ | Orange.sk |
| Sercomm FG1000R	(WIP)	| ✅ | ❌ | ❓ | ❓ | ✅ | TIM |
| Sercomm RHG3006	(WIP)	| ❓ | ❌ | ❌ | ❓ | ✅ | Vodafone |
| ZTE F6005	(WIP)			| ✅ | ✅ | ✅ | ❌ | ❌ | TIM |
| Frontier FOG421			| ✅ | ❓ | ❓ | ❓ | ❌ | Frontier |

## Notes
Comtrend GRG-4284 - After flash works without issues, GPON/EPON tested, OMCI already patched with firmware unlock.

Innbox G23 - Many hardcoded values in binaries reset on reboot, old 2.6 kernel. Full patch might be possible.

Comtrend GRG-4362 - Info in my other repo, XGS-PON.

Sercomm FG1000R - Secure boot, locked down firmware, probably will only provide dump.

Sercomm RHG3006 (Vodafone Fiber Station) - Secure boot, dont have tools to dump currently.

ZTE F6005 - Writeup and firmware mod by @rgiorgiotech, missing unlocked bootloder files.

G-25E - Old device, not worth looking into OMCI editing.


## TODO
Zyxel CETIN devices - None sold used currently, and EcoNET bleh...

Iskratel Innbox G24 - Expensive and not sold used.

Kaon PM1191 - Currently not intrested in working on this device, (and probably shouldn't since its ISP owned), probably possible.

Flash GRG-4284 firmware into G23 - Crashed for me unsure why, hardware should support it.)

ISP testing - Info on Vodafone custom ONT support, look into CEZNET
