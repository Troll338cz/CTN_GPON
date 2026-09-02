# Quick script to just rewrite the image0 in flash dump
# Extra data in enviroments, active slot and other settings are NOT checked
qq = open("FGS202.img", "rb").read()
start = qq[0:1048320]
qqq = open("test-headr.bin", "rb").read()
qqqq = open("SCOMFGS202112-telnet-v2.bin", "rb").read()
end = qq[2755816:8388608]

full = start + qqq + qqqq + end

out = open("fw_patch.img", "wb")
out.write(full)
out.close()
