#
# https://github.com/hack-gpon/hack-gpon.github.io/issues/444
# https://github.com/Anime4000/RTL960x/issues/380
#
# CIG SHA256 "Type 2"
#
import hashlib
# from VOS_CfgParamGetByName("EepEqSerialNumber", a1, 16)
# If the info is right this is case sensitive! - AAAAbbbbbb
# Sadly untested
GPON_SN = "ACLCa1b2c3d4"
text = GPON_SN + "-ONTUSER"
# from /usr/lib/libvos.so.0.0.0 - hmac_sha256_pwd
charset = "ACDEFGHJKLMNPQRSTUVWXYZ2345679abcdefghijkmnpqrstuvwxyz"
rawdigest = hashlib.sha256(text.encode("utf-8")).digest()
output = []
#  From /bin/Console - sub_4017F8
#  sprintf(v2, "%s-%s", v1, "ONTUSER");
#  hmac_sha256_pwd(v2, &cli_password, 16);
for i in range(16):
   byte_val = rawdigest[i]
   char_index = byte_val % 0x36
   output.append(charset[char_index])

print("".join(output))
