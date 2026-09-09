    .set noreorder
    .text

# Stack layout (frame size 0x130):
#   sp+0x000..0x0FF  256-byte flash read buffer (dump)
#   sp+0x100..0x10F  16-byte status out-param for sub_10036CF8
#   sp+0x110         s6 (dump/peek: byte index)
#   sp+0x114         s5 (dump/peek: len)
#   sp+0x118         s4 (dump/peek: addr)
#   sp+0x11C         s3 (scratch: len_str, chunk size, etc.)
#   sp+0x120         s2 (scratch, shared across subcommands)
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
    j       do_help                 # bare "diag" -> help, not printenv anymore
    nop

# ---- get: bare "get" or "get " with nothing after -> print all (u-boot style)
check_get:
    move    $a0, $s0
    la      $a1, str_get            # "get " -- only compare first 3 bytes ("get")
    li      $a2, 3
    jal     sub_10109328
    nop
    bnez    $v0, check_set
    nop
    lbu     $t0, 3($s0)
    beqz    $t0, do_printenv        # bare "get" -> print all
    nop
    addiu   $t1, $t0, -0x20         # must be a space to be a real word boundary
    bnez    $t1, check_set          # e.g. "getfoo" -- not a real match, fall through
    nop

do_get:
    addiu   $s2, $s0, 4              # rest = a2+4 (skip "get ")
    lbu     $t0, 0($s2)
    bnez    $t0, do_get_named
    nop
    j       do_printenv              # "get " with nothing after -> print all
    nop

do_get_named:
    move    $a0, $s2
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

# ---- set: "set <name>" with no value -> delete (set to empty value)
check_set:
    move    $a0, $s0
    la      $a1, str_set            # "set " -- only compare first 3 bytes ("set")
    li      $a2, 3
    jal     sub_10109328
    nop
    bnez    $v0, check_save
    nop
    lbu     $t0, 3($s0)
    beqz    $t0, do_fail            # bare "set", nothing to act on
    nop
    addiu   $t1, $t0, -0x20
    bnez    $t1, check_save         # not a real "set"/"set X" word boundary
    nop

do_set:
    addiu   $s2, $s0, 4              # rest = a2+4 (skip "set ")
    lbu     $t0, 0($s2)
    beqz    $t0, do_fail            # "set " with nothing after -- no name given
    nop

    move    $a0, $s2
    li      $a1, 0x20                # ' '
    jal     sub_1010908c
    nop
    bnez    $v0, do_set_value        # space found -> name+value path
    nop

    # no space found -- bare name only -> delete (set to empty value)
    move    $a0, $s2                  # name = rest
    la      $a1, str_empty            # ""
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

do_set_value:
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
    bnez    $v0, check_selftest
    nop

do_save:
    la      $a0, 0x7F0000
    jal     sub_1001dd24
    li      $a1, 0
    j       done_ok
    nop

# ---- selftest: passthrough to the original "diag" handler (sub_10002D24),
# preserving both bare and "detail" behaviour exactly as it always had it.
check_selftest:
    move    $a0, $s0
    la      $a1, str_selftest        # "selftest"
    li      $a2, 8
    jal     sub_10109328
    nop
    bnez    $v0, check_dump
    nop
    lbu     $t0, 8($s0)
    beqz    $t0, selftest_bare
    nop
    addiu   $t1, $t0, -0x20
    bnez    $t1, check_dump          # not "selftest"/"selftest X" -- not a real match
    nop
    addiu   $s2, $s0, 9              # rest = s0+9 (skip "selftest ")
    j       selftest_forward
    nop

selftest_bare:
    addiu   $s2, $s0, 8              # points at the NUL itself -- empty string

selftest_forward:
    move    $a0, $zero                # original "a1" -- unused by every handler we've
                                       #   traced tonight; passing 0
    move    $a1, $s2                  # a2 = "" or "detail", exactly what sub_10002D24
                                       #   already knows how to handle natively
    jal     sub_10002d24
    move    $a2, $s1                  # a3 = ctx
    j       handler_exit              # preserve its own return value in $v0 as-is
    nop

check_dump:
    move    $a0, $s0
    la      $a1, str_dump
    li      $a2, 5
    jal     sub_10109328
    nop
    bnez    $v0, check_peek
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
    jal     parse_hex                 # addr = raw hex parse, no overflow cap
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

    move    $a0, $s1                  # header line, reused from "guard memory dump:\n"
    la      $a1, str_memdump          #   trimmed to "memory dump:\n"
    jal     sub_10018884
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

check_peek:
    move    $a0, $s0
    la      $a1, str_peek
    li      $a2, 5
    jal     sub_10109328
    nop
    bnez    $v0, do_fail
    nop

do_peek:
    addiu   $s2, $s0, 5               # rest = a2+5 (skip "peek ")
    lbu     $t0, 0($s2)
    beqz    $t0, do_fail              # no address given at all -- bail
    nop

    move    $a0, $s2
    li      $a1, 0x20
    jal     sub_1010908c
    nop
    beqz    $v0, peek_no_len
    nop

    sb      $zero, 0($v0)
    addiu   $s3, $v0, 1               # s3 = len_str
    j       peek_parse_addr
    nop

peek_no_len:
    move    $s3, $zero

peek_parse_addr:
    move    $a0, $s2
    jal     parse_hex                 # addr = raw hex parse, no overflow cap
    nop
    move    $s4, $v0

    beqz    $s3, peek_default_len
    nop
    move    $a0, $s3
    move    $a1, $zero
    li      $a2, 16
    jal     sub_1003e490              # len = strtoul(len_str, 0, 16)
    nop
    move    $s5, $v0
    j       peek_clamp_len
    nop

peek_default_len:
    li      $s5, 256

peek_clamp_len:
    sltiu   $v0, $s5, 257
    bnez    $v0, peek_len_ok
    nop
    li      $s5, 256

peek_len_ok:
    beqz    $s5, do_fail
    nop

    move    $a0, $s1                  # header line, same reused string as dump
    la      $a1, str_memdump
    jal     sub_10018884
    nop

    move    $s6, $zero                # i = 0

peek_print_loop:
    slt     $v0, $s6, $s5
    beqz    $v0, done_ok
    nop
    addu    $t0, $s4, $s6             # direct address -- no flash region lookup
    lbu     $a2, 0($t0)
    move    $a0, $s1
    la      $a1, str_pctx
    jal     sub_10018884
    nop
    addiu   $t1, $s6, 1
    andi    $t2, $t1, 0xf
    bnez    $t2, peek_no_newline
    nop
    move    $a0, $s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop

peek_no_newline:
    addiu   $s6, $s6, 1
    j       peek_print_loop
    nop

do_printenv:
    lui     $v0, 0x9f21
    lw      $s2, 0x8c34($v0)         # config env list cursor -- callee-saved,
                                      # must survive the print calls below
pe_loop:
    lw      $t0, 0($s2)
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
    addiu   $s2, $s2, 4
    j       pe_loop
    nop

# ---- help: bare "diag" with no subcommand at all
do_help:
    move    $a0, $s1
    la      $a1, str_help_title       # "CLI commands (misc)"
    jal     sub_10018884
    nop
    move    $a0, $s1
    la      $a1, str_crlf
    jal     sub_10018884
    nop

    move    $a0, $s1
    la      $a1, str_help_list        # one combined write -- many small rapid
    jal     sub_10018884              #   sub_10018884 calls back-to-back were
    nop                               #   getting garbled/reordered on the wire
    j       done_ok
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

# parse_hex: a0 = pointer to a plain hex digit string (no 0x prefix, no sign).
# Returns the raw 32-bit value in v0, with NO overflow capping -- unlike
# sub_1003e490, which clamps to 0x7FFFFFFF for any unsigned value with no
# leading sign, silently corrupting any address with the high bit set
# (e.g. 0x9F21xxxx RAM addresses). Leaf function, no saved registers needed.
parse_hex:
    move    $v0, $zero
ph_loop:
    lbu     $t0, 0($a0)
    beqz    $t0, ph_done
    nop
    sltiu   $t1, $t0, 0x3a            # char < ':' (i.e. <= '9') ?
    beqz    $t1, ph_alpha
    nop
    sltiu   $t2, $t0, 0x30            # char < '0' ?
    bnez    $t2, ph_done
    nop
    addiu   $t3, $t0, -0x30           # '0'-'9' -> 0-9
    j       ph_accum
    nop
ph_alpha:
    ori     $t0, $t0, 0x20            # force lowercase
    sltiu   $t1, $t0, 0x67            # < 'g' ?
    beqz    $t1, ph_done
    nop
    sltiu   $t2, $t0, 0x61            # < 'a' ?
    bnez    $t2, ph_done
    nop
    addiu   $t3, $t0, -0x57           # 'a'-'f' -> 10-15
ph_accum:
    sll     $v0, $v0, 4
    or      $v0, $v0, $t3
    addiu   $a0, $a0, 1
    j       ph_loop
    nop
ph_done:
    jr      $ra
    nop

    .align 2
str_get:      .ascii "get "
str_save:     .ascii "save"
str_dump:     .ascii "dump "
str_peek:     .ascii "peek "
str_selftest: .ascii "selftest"
str_empty:    .byte 0
str_pctx:     .asciiz "%02x "
str_help_list: .asciiz "get \r\nset \r\nsave\r\ndump \r\npeek \r\nselftest\r\n"
