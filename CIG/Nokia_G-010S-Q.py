#
# https://github.com/Anime4000/RTL960x/issues/52#issuecomment-1999838154
#
# CIG SHA256 "Type 1"
#
from hashlib import sha256
# Found out that ONTUSER needs to be used on second management IP 192.168.188.1/24 
# Thanks to @yahelgr for verifying the full process.
# you can also use CIG backdoor (https://github.com/YuukiJapanTech/CA8271x/blob/main/doc/rootShell.md#nokia-xs-010x-r)
#
# Must be in format 4 Uppercase and 8 lowercase AAAAbbbbbbbb
# from VOS_CfgParamGetByName("EepEqSerialNumber", a1, 16)
GPON_SN = "ALCLa1b2c3d4"
text = GPON_SN # + "-ONTUSER" - not used, telnetd runs sprintf but only runs sha256 on SN itself, also leaking it into active session
print(sha256(text.encode('utf-8')).hexdigest())

