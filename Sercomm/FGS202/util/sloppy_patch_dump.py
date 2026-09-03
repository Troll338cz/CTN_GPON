# Quick script to just rewrite the image0 in flash dump
# Extra data in enviroments, active slot and other settings are NOT checked
qq = open("FGS202.img", "rb").read()
start = qq[0:1048320]
img0_header = open("test-headr.bin", "rb").read()
img0_body = open("SCOMFGS202112-telnet-v2.bin", "rb").read()
end = qq[2755816:8388608]

full = start + img0_header + img0_body + end

if len(full) == 8388608:
   out = open("fw_patch.img", "wb")
   pprint(f"Wrote { out.write(full) } bytes.")
   out.close()
else:
   print(f"Len missmatch {len(full)} != 8388608")

# Rewrite, and yes the SFP has MX25L6405D but chip bellow has same basic read/write, the advance stuff differs but we never use it.
# flashrom -p ch341a_spi -w fw_patch.img  -c "MX25L6436E/MX25L6445E/MX25L6465E"
