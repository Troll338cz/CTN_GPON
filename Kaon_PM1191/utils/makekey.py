import hashlib, sys

if len(sys.argv) != 2:
    print(f"{sys.argv[0]} MAC")
    print("Mac must be seperated by \":\"!")
else:
    # See encrypt script why we do stuff bellow...
    mac = sys.argv[1].lower()
    mackey = hashlib.sha512( f"ethaddr={mac}\x0a".encode('utf-8')).hexdigest()
    mackey = f"{mackey[1:33]}\n"
    print(mackey.strip())
    f = open("kaon_key2", "w")
    f.write(mackey)
    f.close()
