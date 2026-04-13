
#!/usr/bin/env python3
import sys

infile = sys.argv[1]
outfile = sys.argv[2]

i = open(infile,"r").readlines()
o = open(outfile,"wb")

# TODO:
#	Handle last line being non 16b
#	Automaticly skip to dump start

for aa in i:
 # 80000020: 30 33 34 33 03 00 05 00 9f c1 5e 80 9f c1 5f 00    0343......^..._.
 b = aa.split(" ")
 # ['80000020:', '30', '33', '34', '33', '03', '00', '05', '00', '9f', 'c1', '5e', '80', '9f', 'c1', '5f', '00', '', '', '', '0343......^..._.']
 c = b[1]+b[2]+b[3]+b[4]+b[5]+b[6]+b[7]+b[8]+b[9]+b[10]+b[11]+b[12]+b[13]+b[14]+b[15]+b[16]+b[17]
 # b'30333433030005009fc15e809fc15f00'
 o.write(bytes.fromhex(c))

o.close()
