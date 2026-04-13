import sys
file_path = sys.argv[1]

with open(file_path, 'rb') as f:
    file_bytes = f.read()

print(len(file_bytes))

tmp = []
for n in file_bytes:
    qq = n + 1
    if qq == 10: # Undo newline fix
        qq = 11
    tmp.append( qq.to_bytes(1,'little') )
f.close()


with open(sys.argv[2], 'wb') as f:
    for m in tmp:
        f.write(m)
    f.close()