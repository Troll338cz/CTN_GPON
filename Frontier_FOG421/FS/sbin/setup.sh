#!/bin/sh

/bin/echo /sbin/mdev > /proc/sys/kernel/hotplug
/bin/mount -t tmpfs mdev /dev
mdev -s

mkdir -p /dev/pts
/bin/mount -t devpts devpts /dev/pts

mkdir -p /dev/voip
mknod /dev/dsp_console 	  c 252 0
mknod /dev/voip/dtmfdet0  c 243 76
mknod /dev/voip/dtmfdet1  c 243 77
mknod /dev/voip/ipc       c 243 66
mknod /dev/voip/ivr8k     c 243 16
mknod /dev/voip/log_ioctl c 243 40
mknod /dev/voip/mgr       c 243 1
mknod /dev/voip/pcmrx0    c 243 65
mknod /dev/voip/pcmrx1    c 243 74
mknod /dev/voip/pcmtx0    c 243 64
mknod /dev/voip/pcmtx1    c 243 73

mount -t jffs2 /dev/mtdblock1 /mnt/rwdir > /dev/null 2>&1

#function request in issue 10391
if [ $? -eq 0 ] ; then
	echo "" #mount rwdir (ont.mib) ok "
	
	if [ $(grep -c "startup" /mnt/rwdir/.startup) -ge 5000 ] ; then
		rm -rf /mnt/rwdir/.startup
		echo continue > /mnt/rwdir/.startup
	fi
	
	if [ -e /mnt/rwdir/.startup ] ; then
		if [ $(grep -c "#" /mnt/rwdir/.startup) -eq 10 ] ; then
			echo -e "# num is 10,nothing need to do" 
		else
			echo -e "#" >> /mnt/rwdir/.startup
		fi
	else
		echo normal > /mnt/rwdir/.startup
	fi 
else
	flash_eraseall /dev/mtd1
	mount -t jffs2 /dev/mtdblock1 /mnt/rwdir > /dev/null 2>&1
	echo format > /mnt/rwdir/.startup
fi

	
#cp -f /etc/resolv.conf.rwdir /mnt/rwdir/resolv.conf
touch /tmp/voip_resolv.conf
touch /tmp/rg_resolv.conf

#for cramfs debug interface, you can do all like this:
#1. copy /sbin/setup.sh to /mnt/rwdir 
#then modify /mnt/rwdir/setup.sh
#2. delete flash_erase /dev/mtd1
#3. delete [ -f /mnt/rwdir/setup.sh ] && /mnt/rwdir/setup.sh && exit
[ -f /mnt/rwdir/setup.sh ] && /mnt/rwdir/setup.sh && exit

FSTYPE=cramfs
DEVICE=/dev/mtdblock2
USERFS=/dev/mtdblock5

#if grep -i mtdblock2 /proc/cmdline > /dev/null; then
#	DEVICE=/dev/mtdblock3
#	USERFS=/dev/mtdblock4
#fi

#mount -t cramfs $DEVICE /mnt/backupdir > /dev/null 2>&1
#if [ $? -eq 0 ] ; then
#	echo "mount cramfs (backupdir) ok "
#else
#	mount -t jffs2 $DEVICE /mnt/backupdir > /dev/null 2>&1
#	FSTYPE=jffs2
#fi
export FSTYPE DEVICE USERFS

[ -f /mnt/backupdir/etc/sys.cfg ] && cp /mnt/backupdir/etc/sys.cfg /tmp/backup_sys.cfg	
########

#tar xzvf /etc/ramdisk.tgz -C /tmp > /dev/null
#mount -o loop /tmp/ramdisk /mnt/ramdisk

#/tmp/log/messages for syslogd
mkdir -p /tmp/run
mkdir -p /tmp/log
syslogd

#ftp server use this directory to save firmware Image file
#mkdir -p  /tmp/home/root
#bftpd -d

dmesg -n 2

#install your modules here

insmod /lib/modules/2.6.30/kernel/drivers/kvos.ko
insmod /lib/modules/2.6.30/kernel/drivers/klog.ko
insmod /lib/modules/2.6.30/kernel/drivers/misc_mod.ko
#need remove follow lines after all mgr is ok
#insmod /lib/modules/2.6.30/kernel/drivers/eth_drv.ko
#/bin/sleep 1
#/bin/ifconfig eth0 192.168.1.254 netmask 255.255.255.0
#/bin/ifconfig eth0 up
####

if [ -f /lib/modules/2.6.30/kernel/drivers/aipc.ko ]; then
    echo "loading voip drivers...aipc"
    insmod /lib/modules/2.6.30/kernel/drivers/aipc.ko
    echo "loading voip drivers...voip_manager"
    insmod /lib/modules/2.6.30/kernel/drivers/voip_manager.ko
    
    DSP_BOOT_DELAY=1
    if [ -x "/etc/rc_boot_dsp" ]; then
    	echo "run dsp set script..."
      /etc/rc_boot_dsp
    	
    	if [ -x "/bin/wait_dsp" ]; then
    		wait_dsp
    	else
    		echo "no wait_dsp, so force to sleep $DSP_BOOT_DELAY seconds..."
    		sleep $DSP_BOOT_DELAY
    	fi
    fi
fi

#set the max number of message queue
echo 32 >  /proc/sys/kernel/msgmni
echo 65536 >  /proc/sys/kernel/msgmnb
echo 65536 >  /proc/sys/kernel/msgmax

/bin/Console &
/bin/telnetd
#/bin/dropbear 1>/dev/null 2>&1
/bin/GponCLI --script &
/bin/GponCLI --hook &
Ssp

#/bin/sh
