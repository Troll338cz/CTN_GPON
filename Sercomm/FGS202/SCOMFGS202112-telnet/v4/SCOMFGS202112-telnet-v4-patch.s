    .set noreorder
    .text

# Stack layout (frame size 0x130):
#   sp+0x000..0x0FF  256-byte flash read buffer (dump)
#   sp+0x100..0x10F  16-byte status out-param for sub_10036CF8
#   sp+0x110         s6 (dump: byte index)
#   sp+0x114         s5 (dump: len)
#   sp+0x118         s4 (dump: addr)
#   sp+0x11C         s3 (dump: len_str, or 0 if not given)
#   sp+0x120         s2 (scratch, shared across get/set/dump)
#   sp+0x124         s1 (output ctx, saved for whole call)
#   sp+0x128         s0 (command text, saved for whole call)
#   sp+0x12C         ra

env_handler:
    addiu   $sp, $sp, -0x130
    sw      $ra, 0x12c($sp)
    sw      $s0, 0x128($sp)
    sw      $s1, 0x124($sp)
    sw      $s2, 0x120($sp)
    sw      $s3, 0x11c($sp)
    sw      $s4, 0x118($sp)
    sw      $s5, 0x114($sp)
    sw      $s6, 0x110($sp)
    move    $s0, $a1                # s0 = a2 (command text)
    move    $s1, $a2                # s1 = a3 (output ctx)

check_empty:
    lbu     $t0, 0($s0)
    bnez    $t0, check_get
    nop
    j       do_printenv
    nop

check_get:
    move    $a0, $s0
    la      $a1, str_get
    li      $a2, 4
    jal     sub_10109328
    nop
    bnez    $v0, check_set
    nop

do_get:
    addiu   $a0, $s0, 4
    li      $a1, 0
    jal     sub_1001DBF8
    nop
    move    $s2, $v0
    move    $a0, $s1
    la      $a1, str_pcts
    move    $a2, $s2
    jal     sub_10018884
    nop
    move    $a0, $s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
    j       done_ok
    nop

check_set:
    move    $a0, $s0
    la      $a1, str_set
    li      $a2, 4
    jal     sub_10109328
    nop
    bnez    $v0, check_save
    nop

do_set:
    addiu   $s2, $s0, 4              # rest = a2+4
    move    $a0, $s2
    li      $a1, 0x20                # ' '
    jal     sub_1010908c
    nop
    beqz    $v0, do_fail
    nop
    sb      $zero, 0($v0)
    addiu   $a1, $v0, 1               # value = sp+1
    move    $a0, $s2                  # name = rest
    jal     sub_1001feb4
    li      $a2, 0
    la      $a0, 0x7F0000
    jal     sub_1001dd24
    li      $a1, 0
    move    $a0, $s1
    la      $a1, str_setok
    jal     sub_10018884
    nop
    j       done_ok
    nop

check_save:
    move    $a0, $s0
    la      $a1, str_save
    li      $a2, 4
    jal     sub_10109328
    nop
    bnez    $v0, check_dump
    nop

do_save:
    la      $a0, 0x7F0000
    jal     sub_1001dd24
    li      $a1, 0
    j       done_ok
    nop

check_dump:
    move    $a0, $s0
    la      $a1, str_dump
    li      $a2, 5
    jal     sub_10109328
    nop
    bnez    $v0, do_fail
    nop

do_dump:
    addiu   $s2, $s0, 5               # rest = a2+5 (skip "dump ")
    lbu     $t0, 0($s2)
    beqz    $t0, do_fail              # no address given at all -- bail
    nop

    move    $a0, $s2
    li      $a1, 0x20
    jal     sub_1010908c
    nop
    beqz    $v0, dump_no_len          # no space -> no length given
    nop

    sb      $zero, 0($v0)
    addiu   $s3, $v0, 1               # s3 = len_str
    j       dump_parse_addr
    nop

dump_no_len:
    move    $s3, $zero                # s3 = 0 sentinel -> use default len

dump_parse_addr:
    move    $a0, $s2
    move    $a1, $zero
    li      $a2, 16
    jal     sub_1003e490              # addr = strtoul(addr_str, 0, 16)
    nop
    move    $s4, $v0

    beqz    $s3, dump_default_len
    nop
    move    $a0, $s3
    move    $a1, $zero
    li      $a2, 16
    jal     sub_1003e490              # len = strtoul(len_str, 0, 16)
    nop
    move    $s5, $v0
    j       dump_clamp_len
    nop

dump_default_len:
    li      $s5, 256

dump_clamp_len:
    sltiu   $v0, $s5, 257             # len <= 256 ?
    bnez    $v0, dump_len_ok
    nop
    li      $s5, 256                  # clamp -- buffer is exactly 256 bytes

dump_len_ok:
    beqz    $s5, do_fail              # len==0 -> nothing to read, bail

    move    $s6, $zero                # s6 = bytes read so far

dump_read_chunk:
    li      $t0, 8
    subu    $t1, $s5, $s6             # remaining = len - read_so_far
    slt     $v0, $t1, $t0
    movn    $t0, $t1, $v0             # chunk = min(8, remaining)
    move    $s3, $t0                  # save chunk size in a CALLEE-SAVED reg --
                                       # $t0 is not guaranteed to survive the call

    addu    $a0, $s4, $s6             # addr + offset
    addu    $a1, $sp, $s6             # buf + offset
    move    $a2, $s3
    addiu   $a3, $sp, 0x100           # status out-param (16 bytes reserved)
    sw      $zero, 0x100($sp)         # clear it every call -- must never look
    sw      $zero, 0x104($sp)         #   like valid cached region state from
    sw      $zero, 0x108($sp)         #   a previous iteration
    sw      $zero, 0x10c($sp)
    jal     sub_10036cf8
    nop
    bnez    $v0, do_fail              # read failed -> bail safely
    nop

    addu    $s6, $s6, $s3             # use the saved chunk size, not $t0
    slt     $v0, $s6, $s5
    bnez    $v0, dump_read_chunk
    nop

    move    $s6, $zero                # i = 0 -- restart index for printing

dump_print_loop:
    slt     $v0, $s6, $s5
    beqz    $v0, done_ok
    nop
    addu    $t0, $sp, $s6
    lbu     $a2, 0($t0)
    move    $a0, $s1
    la      $a1, str_pctx
    jal     sub_10018884
    nop
    addiu   $t1, $s6, 1
    andi    $t2, $t1, 0xf
    bnez    $t2, dump_no_newline
    nop
    move    $a0, $s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop

dump_no_newline:
    addiu   $s6, $s6, 1
    j       dump_print_loop
    nop

do_printenv:
    lui     $v0, 0x9f21
    lw      $v0, 0x8c34($v0)         # config env list base pointer
pe_loop:
    lw      $t0, 0($v0)
    beqz    $t0, done_ok
    nop
    move    $a0, $s1
    la      $a1, str_pcts
    jal     sub_10018884
    move    $a2, $t0
    move    $a0, $s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop
    addiu   $v0, $v0, 4
    j       pe_loop
    nop

do_fail:
    move    $a0, $s1
    la      $a1, str_setfailed
    jal     sub_10018884
    nop
    li      $v0, -1
    j       handler_exit
    nop

done_ok:
    li      $v0, 0

handler_exit:
    lw      $ra, 0x12c($sp)
    lw      $s0, 0x128($sp)
    lw      $s1, 0x124($sp)
    lw      $s2, 0x120($sp)
    lw      $s3, 0x11c($sp)
    lw      $s4, 0x118($sp)
    lw      $s5, 0x114($sp)
    lw      $s6, 0x110($sp)
    jr      $ra
    addiu   $sp, $sp, 0x130

    .align 2
str_get:  .ascii "get "
str_save: .ascii "save"
str_dump: .ascii "dump "
str_pctx: .asciiz "%02x "
