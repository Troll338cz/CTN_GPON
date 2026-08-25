#
# https://github.com/Anime4000/RTL960x/issues/52#issuecomment-1999838154
#
# CIG SHA256 "Type 1"
#
from hashlib import sha256
# from VOS_CfgParamGetByName("EepEqSerialNumber", a1, 16)
GPON_SN = "ACLCa1b2c3d4"
text = GPON_SN + "-ONTUSER"
print(sha256(text.encode('utf-8')).hexdigest())

