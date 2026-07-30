from innda_ssl import innda_ssl_dec

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

innda_ssl_dec("aes-256-cbc", "U2FsdGVkX19uKaaqovStQb+jck413jzQ7Gw130JcYi8=U2FsdGVkX1+ahtAAdY331XsPULpQunVZUxpxwRBBOW8=U2FsdGVkX1/dSwJIUZ3dIeYhHLF3WmYhP1S0WFZkGFo=U2FsdGVkX18bPvlpdCTMy1TFL7q6kulMFNyzdXyNn6k=U2FsdGVkX1/atqLrkJjRsYk445ZUrwFWWP/s32zYpu4=", True,"pwd.in", "pwd.out")


# Decrypt default config
"""
hw_id = nvram "hw_id" .split("_")[0]
customer = nvram "customer"
buildrev = /etc/config/buildrev

sprintf "%s_%s_%s" hw_id customer buildrev

"""

# same for datamodel_
innda_ssl_dec("aes-256-cbc", "InnboxX24_Cetin_cdadf94603b0d7ecb346064b502c74b3b295a0c6", False, "defaultvalue_InnboxX24_Cetin.enc", "defaultvalue_InnboxX24_Cetin.gz")

innda_ssl_dec("aes-256-cbc", "InnboxX24_Hyperoptics_cdadf94603b0d7ecb346064b502c74b3b295a0c6", False, "defaultvalue_InnboxX24_Hyperoptics.enc", "defaultvalue_InnboxX24_Hyperoptics.gz")
