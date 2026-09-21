# mips-linux-gnu-as -mabi=32 -march=mips32 -EB -o handler_stripped.o handler_stripped.s 
.set noreorder
.text
    addiu   $sp,$sp,-304
    sw      $ra,300($sp)
    sw      $s0,296($sp)
    sw      $s1,292($sp)
    sw      $s2,288($sp)
    sw      $s3,284($sp)
    sw      $s4,280($sp)
    sw      $s5,276($sp)
    sw      $s6,272($sp)
    move    $s0,$a1
    move    $s1,$a2
check_empty:
    lbu     $t0,0($s0)
    bnez    $t0,check_get
    nop
    j       do_help
    nop
check_get:
    move    $a0,$s0
    la      $a1, str_get_i
    li      $a2,3
    jal     sub_10109328
    nop
    bnez    $v0,check_set
    nop
    lbu     $t0,3($s0)
    beqz    $t0,do_printenv
    nop
    addiu   $t1,$t0,-32
    bnez    $t1,check_set
    nop
    addiu   $s2,$s0,4
    lbu     $t0,0($s2)
    bnez    $t0,do_get_named
    nop
    j       do_printenv
    nop
do_get_named:
    move    $a0,$s2
    li      $a1,0
    jal     sub_1001DBF8
    nop
    move    $s2,$v0
    move    $a0,$s1
    la      $a1, str_pcts
    move    $a2,$s2
    jal     sub_10018884
    nop
    move    $a0,$s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
    j       done_ok
    nop
check_set:
    move    $a0,$s0
    la      $a1, str_set
    li      $a2,3
    jal     sub_10109328
    nop
    bnez    $v0,check_save
    nop
    lbu     $t0,3($s0)
    beqz    $t0,do_fail
    nop
    addiu   $t1,$t0,-32
    bnez    $t1,check_save
    nop
    addiu   $s2,$s0,4
    lbu     $t0,0($s2)
    beqz    $t0,do_fail
    nop
    move    $a0,$s2
    li      $a1,32
    jal     sub_1010908c
    nop
    bnez    $v0,do_set_value
    nop
    j       do_unset
    nop
do_set_value:
    sb      $zero,0($v0)
    addiu   $a1,$v0,1
    move    $a0,$s2
    jal     sub_1001feb4
    li      $a2,0
    lui     $a0, 0x7f
    jal     sub_1001dd24
    li      $a1,0
    move    $a0,$s1
    la      $a1, str_setok
    jal     sub_10018884
    nop
    j       done_ok
    nop
do_unset:
    move    $a0,$s2
    jal     sub_1003F200
    nop
    move    $s3,$v0
    lui     $t0, 0x9f21
    lui     $s4, 0x1
    addu    $s4,$s4,$t0
    lw      $s4,-29644($s4)
    move    $s5,$zero
unset_scan:
    sll     $t1,$s5,0x2
    addu    $t1,$s4,$t1
    lw      $s6,0($t1)
    beqz    $s6,do_fail
    nop
    move    $a0,$s6
    move    $a1,$s2
    move    $a2,$s3
    jal     sub_1003F054
    nop
    bnez    $v0,unset_next
    nop
    addu    $t2,$s6,$s3
    lbu     $t3,0($t2)
    li      $t4,61
    beq     $t3,$t4,unset_found
    nop
unset_next:
    addiu   $s5,$s5,1
    j       unset_scan
    nop
unset_found:
    move    $a0,$s6
    jal     sub_1002F748
    nop
    move    $s6,$s5
unset_shift:
    addiu   $t5,$s6,1
    sll     $t6,$t5,0x2
    addu    $t6,$s4,$t6
    lw      $t7,0($t6)
    sll     $t8,$s6,0x2
    addu    $t8,$s4,$t8
    sw      $t7,0($t8)
    beqz    $t7,unset_shifted
    nop
    addiu   $s6,$s6,1
    j       unset_shift
    nop
unset_shifted:
    lui     $t0, 0x9f21
    lw      $t1,21928($t0)
    addiu   $t1,$t1,-1
    sw      $t1,21928($t0)
    lui     $a0, 0x7f
    jal     sub_1001dd24
    li      $a1,0
    move    $a0,$s1
    la      $a1, str_setok
    jal     sub_10018884
    nop
    j       done_ok
    nop
check_save:
    move    $a0,$s0
    la      $a1, str_save_i
    li      $a2,4
    jal     sub_10109328
    nop
    bnez    $v0,check_selftest
    nop
    lbu     $t0,4($s0)                # word-boundary check -- without this, "saveu"
    beqz    $t0,do_save               #   matches this 4-byte prefix and silently
    nop                               #   runs a plain save before check_saveu is
    addiu   $t1,$t0,-0x20             #   ever reached
    bnez    $t1,check_selftest
    nop
do_save:
    lui     $a0, 0x7f
    jal     sub_1001dd24
    li      $a1,0
    j       done_ok
    nop
check_selftest:
    move    $a0,$s0
    la      $a1, str_selftest_i
    li      $a2,8
    jal     sub_10109328
    nop
    bnez    $v0,check_dump
    nop
    lbu     $t0,8($s0)
    beqz    $t0,selftest_bare
    nop
    addiu   $t1,$t0,-32
    bnez    $t1,check_dump
    nop
selftest_named:
    addiu   $s2,$s0,9
    j       selftest_forward
    nop
selftest_bare:
    addiu   $s2,$s0,8
selftest_forward:
    move    $a0,$zero
    move    $a1,$s2
    jal     sub_10002d24
    move    $a2,$s1
    j       handler_exit
    nop
check_dump:
    move    $a0,$s0
    la      $a1, str_dump_i
    li      $a2,5
    jal     sub_10109328
    nop
    bnez    $v0,check_peek
    nop
    addiu   $s2,$s0,5
    lbu     $t0,0($s2)
    beqz    $t0,do_fail
    nop
    move    $a0,$s2
    li      $a1,32
    jal     sub_1010908c
    nop
    beqz    $v0,dump_deflen
    nop
    sb      $zero,0($v0)
    addiu   $s3,$v0,1
    j       dump_parseaddr
    nop
dump_deflen:
    move    $s3,$zero
dump_parseaddr:
    move    $a0,$s2
    jal     parse_hex
    nop
    move    $s4,$v0
    beqz    $s3,dump_default256
    nop
    move    $a0,$s3
    move    $a1,$zero
    li      $a2,16
    jal     sub_1003e490
    nop
    move    $s5,$v0
    j       dump_clamp
    nop
dump_default256:
    li      $s5,256
dump_clamp:
    sltiu   $v0,$s5,257
    bnez    $v0,dump_checkzero
    nop
    li      $s5,256
dump_checkzero:
    beqz    $s5,do_fail
dump_loop_init:
    move    $s6,$zero
dump_loop:
    li      $t0,8
    subu    $t1,$s5,$s6
    slt     $v0,$t1,$t0
    movn    $t0,$t1,$v0
    move    $s3,$t0
    addu    $a0,$s4,$s6
    addu    $a1,$sp,$s6
    move    $a2,$s3
    addiu   $a3,$sp,256
    sw      $zero,256($sp)
    sw      $zero,260($sp)
    sw      $zero,264($sp)
    sw      $zero,268($sp)
    jal     sub_10036cf8
    nop
    bnez    $v0,do_fail
    nop
    addu    $s6,$s6,$s3
    slt     $v0,$s6,$s5
    bnez    $v0,dump_loop
    nop
dump_print_header:
    move    $a0,$s1
    la      $a1, str_memdump
    jal     sub_10018884
    nop
dump_print_loop:
    move    $s6,$zero
dump_print_loop2:
    slt     $v0,$s6,$s5
    beqz    $v0,done_ok
    nop
    addu    $t0,$sp,$s6
    lbu     $a2,0($t0)
    move    $a0,$s1
    la      $a1, str_pctx_i
    jal     sub_10018884
    nop
    addiu   $t1,$s6,1
    andi    $t2,$t1,0xf
    bnez    $t2,dump_print_next
    nop
    move    $a0,$s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
dump_print_next:
    addiu   $s6,$s6,1
    j       dump_print_loop2
    nop
check_peek:
    move    $a0,$s0
    la      $a1, str_peek_i
    li      $a2,5
    jal     sub_10109328
    nop
    bnez    $v0,do_fail
    nop
    addiu   $s2,$s0,5
    lbu     $t0,0($s2)
    beqz    $t0,do_fail
    nop
    move    $a0,$s2
    li      $a1,32
    jal     sub_1010908c
    nop
    beqz    $v0,peek_deflen
    nop
    sb      $zero,0($v0)
    addiu   $s3,$v0,1
    j       peek_parseaddr
    nop
peek_deflen:
    move    $s3,$zero
peek_parseaddr:
    move    $a0,$s2
    jal     parse_hex
    nop
    move    $s4,$v0
    beqz    $s3,peek_default256
    nop
    move    $a0,$s3
    move    $a1,$zero
    li      $a2,16
    jal     sub_1003e490
    nop
    move    $s5,$v0
    j       peek_clamp2
    nop
peek_default256:
    li      $s5,256
peek_clamp2:
    sltiu   $v0,$s5,257
    bnez    $v0,peek_clamp
    nop
    li      $s5,256
peek_clamp:
    beqz    $s5,do_fail
    nop
peek_print_header:
    move    $a0,$s1
    la      $a1, str_memdump
    jal     sub_10018884
    nop
peek_print_loop:
    move    $s6,$zero
peek_print_loop2:
    slt     $v0,$s6,$s5
    beqz    $v0,done_ok
    nop
    addu    $t0,$s4,$s6
    lbu     $a2,0($t0)
    move    $a0,$s1
    la      $a1, str_pctx_i
    jal     sub_10018884
    nop
    addiu   $t1,$s6,1
    andi    $t2,$t1,0xf
    bnez    $t2,peek_print_next
    nop
    move    $a0,$s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
peek_print_next:
    addiu   $s6,$s6,1
    j       peek_print_loop2
    nop
do_printenv:
    lui     $v0, 0x9f21
    lui     $s2, 0x1
    addu    $s2,$s2,$v0
    lw      $s2,-29644($s2)
printenv_loop:
    lw      $t0,0($s2)
    beqz    $t0,done_ok
    nop
    move    $a0,$s1
    la      $a1, str_pcts
    jal     sub_10018884
    move    $a2,$t0
    move    $a0,$s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
    addiu   $s2,$s2,4
    j       printenv_loop
    nop
do_help:
    move    $a0,$s1
    la      $a1, str_help_title
    jal     sub_10018884
    nop
    move    $a0,$s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
    move    $a0,$s1
    la      $a1, str_help_list_i
    jal     sub_10018884
    nop
    j       done_ok
    nop
do_fail:
    move    $a0,$s1
    la      $a1, str_setfailed
    jal     sub_10018884
    nop
    li      $v0,-1
    j       handler_exit
    nop
done_ok:
    li      $v0,0
handler_exit:
    lw      $ra,300($sp)
    lw      $s0,296($sp)
    lw      $s1,292($sp)
    lw      $s2,288($sp)
    lw      $s3,284($sp)
    lw      $s4,280($sp)
    lw      $s5,276($sp)
    lw      $s6,272($sp)
    jr      $ra
    addiu   $sp,$sp,304
parse_hex:
    move    $v0,$zero
parse_hex_loop:
    lbu     $t0,0($a0)
    beqz    $t0,parse_hex_end
    nop
    sltiu   $t1,$t0,58
    beqz    $t1,parse_hex_alpha
    nop
    sltiu   $t2,$t0,48
    bnez    $t2,parse_hex_end
    nop
    addiu   $t3,$t0,-48
    j       parse_hex_combine
    nop
parse_hex_alpha:
    ori     $t0,$t0,0x20
    sltiu   $t1,$t0,103
    beqz    $t1,parse_hex_end
    nop
    sltiu   $t2,$t0,97
    bnez    $t2,parse_hex_end
    nop
    addiu   $t3,$t0,-87
parse_hex_combine:
    sll     $v0,$v0,0x4
    or      $v0,$v0,$t3
    addiu   $a0,$a0,1
    j       parse_hex_loop
    nop
parse_hex_end:
    jr      $ra
    nop
    .align 2
str_get_i:      .ascii "get "
str_save_i:     .ascii "save"
str_dump_i:     .ascii "dump "
str_peek_i:     .ascii "peek "
str_selftest_i: .ascii "selftest"
str_pctx_i:     .asciiz "%02x "
str_help_list_i: .asciiz "get \r\nset \r\nsave\r\ndump \r\npeek \r\nselftest\r\n"
    .byte 0,0,0,0
