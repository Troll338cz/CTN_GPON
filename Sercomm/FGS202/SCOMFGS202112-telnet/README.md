# Tested in a Mikrotik RB5009

![pic](TELNET_MOD.png)

## v0 - ENV method
set ft_flag=1 Factory info, does same as bellow, will survive config resets

but you need to desolder the flash, fw can be loeaded with tftp or OMCI ( if your OLT works ) but you can't edit envs.



## v1 - SCOMFGS202112-telnet-v1.bin
Simple patch to remove LAN check, you still need telnet and mgmt interface to be UP
```
# Hex patch, start at offset 0x0005140c
+0xC	3C 04 10 12 ->	3C 04 10 18
+0x10	24 84 08 9C ->	24 84 8D 74
+0x18	0C 00 76 FE ->	00 00 00 00
+0x20	00 40 20 21 ->	00 00 00 00

# Decompiled Pseudocode:
Original:
        sub_1002BBEC(*(_BYTE **)(a1 + 4), v62, 0x308u);
        v22[1] = v20;
        v23 = sub_1001DBF8("ft_flag", 1);
        if ( sub_1002FA54(v23, "1") )
        {

Patched:
        sub_1002BBEC(*(_BYTE **)(a1 + 4), v61, 0x308u);
        v22[1] = v20;
        if ( sub_1002FA54("1", "1") )
        {
```

## v2 - SCOMFGS202112-telnet-v2.bin
Starts the network on boot, combined with the v1 check
Unless OMCI disables the network again it should boot up and be accesible

```
# Hex patch, start at offset 0x100526B0
+08-11  00 00 00 00
+14	00 40 20 21 ->	24 A5 8D 74
+1C	24 A5 8D 74 ->	00 A0 20 21

# Decompiled Pseudocode:
Original:
    v34 = sub_1001DBF8("ft_flag", 1);
    if ( !sub_1002FA54(v34, "1") )
    {
      if ( sub_1004EF94(*(_BYTE *)(v3 + 12)) )
      {
        sub_10108140("Network initialization failed!\n");
        sub_1002250C("Network initialization failed!\n");
        goto LABEL_66;
      }
      MEMORY[0x9F214DE8] = 1;
      MEMORY[0x9F214DE4] = 1;
      MEMORY[0x9F214DE0] = 3;
    }

Patched:
    if ( !sub_1002FA54("1", "1") )
    {
      if ( sub_1004EF94(*(_BYTE *)(v3 + 12)) )
      {
        sub_10108140("Network initialization failed!\n");
        sub_1002250C("Network initialization failed!\n");
        goto LABEL_66;
      }
      MEMORY[0x9F214DE8] = 1;
      MEMORY[0x9F214DE4] = 1;
      MEMORY[0x9F214DE0] = 3;
    }

```

This patch acts as if factory flag was set...

## v3 - SCOMFGS202112-telnet-v3.bin

```
# Replace 6 calls, clean and simple
# leaves us about 60 instruction window in the old function
0x0C0080b9 -> 0x0C0076fe

and

# Nuke the encrypt code, if check and strlen are left to preserve register states...

ROM:1001FF1C                 move    $a3, $s0
ROM:1001FF20                 jal     sub_10107984
ROM:1001FF24                 move    $a0, $s1
ROM:1001FF28                 jal     sub_1003F200
ROM:1001FF2C                 move    $a0, $s3
ROM:1001FF30                 lui     $a1, 0x1012
ROM:1001FF34                 move    $a0, $s3
ROM:1001FF38                 li      $a1, aNpassword  # "nPassword"
ROM:1001FF3C                 jal     sub_1002FA54
ROM:1001FF40                 move    $s2, $v0
ROM:1001FF44                 beqz    $v0, loc_1001FF60
ROM:1001FF48                 lui     $a1, 0x1012
ROM:1001FF4C                 move    $a0, $s3
ROM:1001FF50                 jal     sub_1002FA54
ROM:1001FF54                 li      $a1, aPassword_0  # "password"
ROM:1001FF58                 bnez    $v0, loc_10020050
ROM:1001FF5C                 li      $v0, 1
ROM:1001FF60
ROM:1001FF60 loc_1001FF60:                            # CODE XREF: sub_1001FEB4+90â†‘j
ROM:1001FF60                 li      $v0, 1
ROM:1001FF64                 j       loc_10020050
ROM:1001FF68                 nop
ROM:1001FF6C                 nop
ROM:1001FF70                 nop
ROM:1001FF74                 nop
ROM:1001FF78                 nop
ROM:1001FF7C                 nop
ROM:1001FF80                 nop
ROM:1001FF84                 nop
.....
ROM:10020046                 nop

# This is middle version between telnet enable and adding env editor


```

## v4 - SCOMFGS202112-telnet-v4.bin
TEST version with ENV editor. Used mainly to test quick patching by jumping behind the image into flash.
```
# Why this works:
ecos_vaddr=0x10000000
image0_addr=0xB0100000
boot_image0=tlb map ${ecos_vaddr} ${image0_addr} ${max_image_size} && go ${ecos_vaddr}
# Entire image0 range mapped...

For testing patch code was placed after original firmware ending
diag command was hijacked to point at 
sub_10008270(a1, 0, " ", "diag", (int)sub_10002D24); <-- swaped here to 0x101A2000

This test version has the following:
diag dump ADDR LEN - Dump RAM, limited to 256 bytes. WARNING: output at 0x8 to 0xF is corrupt, you must read this range again to get real value!
diag get key - Get value from config env
diag set key - Set value to key in config env, empty does not delete the key like U-Boot (todo)
diag - Dump full env. WARNING: Crashes device :)
```

## v5 - SCOMFGS202112-telnet-v5.bin
Final version for now, commands have been cleaned up and original diag restored.
```
Patch is now injected before image footer, 

get — get prints all, get <name> returns key value
set — set <name> deletes (empty "" value), set <name> <value> sets normally like U-Boot.  WARNING: You cannot fully delete 
save — commit changes to flash
selftest / selftest detail — original diag/diag detail command
dump / peek — Hexdump of flash and RAM, dump <hex addr> <hex len>. WARNING: output at 0x8 to 0xF is still corrupt, not worth fixing, just re-read it with second command.


```
