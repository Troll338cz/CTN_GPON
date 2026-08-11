import sys
from struct import pack, unpack

#
#
# mtdblock11
# 0000000: 494e 4e44 4142 4f4f 5400 0000 0000 0000
# 0000010: 1c00 0000 1c00 0000 8501 0000
# 494e 4e44 4145 4e56 - INNDABOOT magic 
# 1c - magic
# 1c - magic
# 8501 - Envlen LE
#
#
# mtdblock9
# 00000000: 494e 4e44 4145 4e56 0000 0000 0000 0000
# 00000010: 1c00 0000 1c00 0000 d200 0000
# 494e 4e44 4145 4e56 - INNDAENV magic 
# 1c - magic
# 1c - magic
# d200 - Envlen LE
#
#
HEADER_LEN = 28

if len(sys.argv) != 4:
        print(f"{sys.argv[0]} encode|decode infile outfile")
        print(f"{sys.argv[0]} verify infile null")
        sys.exit(1)

ops = ["encode", "decode", "verify"]
if sys.argv[1] not in ops:
        print(f'First argument must be {', '.join(ops)}.')
        sys.exit(1)


if sys.argv[2] == sys.argv[3]:
        print('Infile cant be same as outfile!')
        sys.exit(1)

if sys.argv[1] == "verify":
    fin = open(sys.argv[2], "rb")
    dats = fin.read()
    dlen = ( unpack('H', dats[24:26] )[0] + HEADER_LEN )
    dats = dats.strip(b'\xff') # Dumped MTD padd
    if len(dats) == dlen:
        print(f"{sys.argv[2]} Test OK!")
    else:
        print(f"{sys.argv[2]} Test FAIL! {dlen} != {len(dats)}")

if sys.argv[1] == "decode":
    fin = open(sys.argv[2], "rb")
    fout = open(sys.argv[3], "wb")
    dats = fin.read()
    dlen = unpack('H', dats[24:26] )[0]
    fout.write( dats[HEADER_LEN:dlen+HEADER_LEN] )
    fout.close()
    fin.close()

if sys.argv[1] == "encode":
    fin = open(sys.argv[2], "rb")
    fout = open(sys.argv[3], "wb")
    dats = fin.read()
    dlen = pack('H', ( len(dats) ))
    header = b'INNDAENV' + b'\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x1c\x00\x00\x00' + dlen + b'\x00\x00'
    fout.write( header+dats )
    fout.close()
    fin.close()


