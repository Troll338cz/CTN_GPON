# Test TODO

## HEADER TODO
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