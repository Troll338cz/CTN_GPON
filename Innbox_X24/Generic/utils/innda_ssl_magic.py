from innda_ssl import innda_ssl_dec
import os, sys
#
# Why even encrypt when the keys hardcoded or easy to generate???
#

# Decrypt webserver files
# /etc/config/buildmodel - "InnboxX24"
#buildmodel = "InnboxX24"
#innda_ssl_dec("aes-256-cbc", f"{buildmodel}_ISK", False, "www_ISK.enc", "www_ISK.tgz")
#innda_ssl_dec("aes-256-cbc", f"{buildmodel}_Cetin", False, "www_Cetin.enc", "www_Cetin.tgz")

# Decrypt password
"""
      csm_log(
        &g_fad_module,
        5,
        "[%s:%s(%d)] Change default pwd of TELEKOMSLOVENIJE ...",
        "src.config/config.c",
        "default_pwd_change",
        1567);
      cfg_setstr("U2FsdGVkX18yNGsP5j1/n5/6L6Q/ZTbFr4JFN3cYQk4j2DOjQj0Y/pnh+ZnECZ8Q", "/sys/user:1/password"); -> "U*7#uHYjdVN@nxMu"
      cfg_setstr("U2FsdGVkX194JevnXboYz7oJx6EpWjUes2ynBzKvuc6paptSrl2afN3bCawGoXfL", "/sys/user:2/password"); -> "6*cg9$X7z44shFB8"
      cfg_setint(0, "/sys/user:1/group");
      cfg_setint(1, "/sys/user:2/group");
      cfg_setint(2, "/sys/user:3/group");
      cfg_setint(5, "/sys/default_pwd_change");
"""

q = open("pwd.in", "w")
q.write(sys.argv[1])
q.close()
os.system("rm pwd.out")
innda_ssl_dec("aes-256-cbc", "U2FsdGVkX19uKaaqovStQb+jck413jzQ7Gw130JcYi8=U2FsdGVkX1+ahtAAdY331XsPULpQunVZUxpxwRBBOW8=U2FsdGVkX1/dSwJIUZ3dIeYhHLF3WmYhP1S0WFZkGFo=U2FsdGVkX18bPvlpdCTMy1TFL7q6kulMFNyzdXyNn6k=U2FsdGVkX1/atqLrkJjRsYk445ZUrwFWWP/s32zYpu4=", True,"pwd.in", "pwd.out")
os.system("cat pwd.out")

# Decrypt default config
"""
hw_id = nvram "hw_id" .split("_")[0]
customer = nvram "customer"
buildrev = /etc/config/buildrev

sprintf "%s_%s_%s" hw_id customer buildrev

"""

# same for datamodel_
#qqq = "841f5f5bb6b84ba463bf461f1af48b800ded462d"
#q = ["Cetin", "CSpire", "Hyperoptics", "Iskratel", "Windstream", "Wire3", "Zzoomm" ]
#for qq in q:
#  innda_ssl_dec("aes-256-cbc", f"InnboxX24_{qq}_{qqq}", False, f"defaultvalue_InnboxX24_{qq}.enc", f"defaultvalue_InnboxX24_{qq}.gz")
#  os.system(f"gzip -d defaultvalue_InnboxX24_{qq}.gz")
