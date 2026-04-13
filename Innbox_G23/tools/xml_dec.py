import sys

file_path = sys.argv[1]

with open(file_path, 'rb') as f:
    file_bytes = f.read()

print(len(file_bytes))

tmp = []

# Quick look at how this "encryption" works:
# =Dpogjh!Obnf>#SPPU#? - in config
# <Config Name="ROOT"> - plaintext
# '=' = 0x3d (61)
# '<' = 0x3c (60)
# Moving all bytes to left by 0x01 gives us back readble config file


for n in file_bytes:
    qq = n - 1  
    # Newlines in files are inconsistent, some files have correct 0x0A some have 0x0B and some have both with duplicates (0x0B 0x0A 0x0A)
    # Fix new line
    if qq == 9:
        qq = 10
    tmp.append( qq.to_bytes(1,'little') )
f.close()


with open(sys.argv[2], 'wb') as f:
    for m in tmp:
        f.write(m)
    f.close()