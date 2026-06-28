#!/bin/sh

# luna firmware upgrade  script
# $1 image destination (0 or 1)
# $2 image path
# Kernel and root file system images are assumed to be located at the same directory named uImage and rootfs respectively
# ToDo: use arugements to refer to kernel/rootfs location.

########### G3 ##########################################################
### dtb    : ca7774-engboard.dtb or ca8276 Device Tree Binary ###########
### kimage : Image or Image.lzma
### rootfs : rootfs_G3_1.ubi
#########################################################################
d_img="dtb"
k_img="kimage"
r_img="rootfs"
img_ver="fwu_ver"
md5_cmp="md5.txt"
md5_cmd="/bin/md5sum"
#md5 run-time result
md5_tmp="md5_tmp"
md5_rt_result="md5_rt_result.txt"
new_fw_ver="new_fw_ver.txt"
cur_fw_ver="cur_fw_ver.txt"
env_sw_ver="env_sw_ver.txt"
hw_ver_file="hw_ver"
skip_hwver_check="/tmp/skip_hwver_check"

# For CMCC
o_img="osgi.img"
osgi_upgraded=0
osgi_mmc_name=osgi

# For YueMe framework
framework_img="framework.img"
framework_sh="framework.sh"
framework_upgraded=0

arg1="$1"
arg2="$2"

set +x

check_osgi() {
	if [ "`tar -tf $2 $o_img`" = "$o_img" ]; then
		osgi_upgraded=1
	fi
}

update_framework() {

	if [ "`tar -tf $2 $framework_sh`" = "$framework_sh" ] && [ "`tar -tf $2 $framework_img`" = "$framework_img" ]; then
			echo "Updaing framework from $2"
			tar -xf $2 $framework_sh
			grep $framework_sh $md5_cmp > $md5_tmp
			$md5_cmd $framework_sh > $md5_rt_result
			diff $md5_rt_result $md5_tmp

			if [ $? != 0 ]; then 
					echo "$framework_sh md5_sum inconsistent, aborted image updating !"
					exit 1
			fi

			# Run firmware upgrade script extracted from image tar ball
			sh $framework_sh $2
			framework_upgraded=1
	fi

	if [ "`tar -tf $2 $k_img`" = '' ] && [ $framework_upgraded = 1 ]; then
			echo "No uImage for upgrading, skip"
			exit 2
	fi
}

do_hwver_check() {
	if [ -f $skip_hwver_check ]; then
			echo "Skip HW_VER check!!"
	else
			img_hw_ver=`tar -xf $2 $hw_ver_file -O`
			mib_hw_ver=`mib get HW_HWVER | sed s/HW_HWVER=//g`
			if [ "$img_hw_ver" = "skip" ]; then
					echo "skip HW_VER check!!"
			else
					echo "img_hw_ver=$img_hw_ver mib_hw_ver=$mib_hw_ver"
					if [ "$img_hw_ver" != "$mib_hw_ver" ]; then
							echo "HW_VER $img_hw_ver inconsistent, aborted image updating !"
							exit 1
					fi
			fi
	fi
}

do_extract_img_md5() {
	# Extract DTB image
	tar -xf $2 $d_img -O | md5sum | sed 's/-/'$d_img'/g' > $md5_rt_result
	# Check integrity
	grep $d_img $md5_cmp > $md5_tmp
	diff $md5_rt_result $md5_tmp

	if [ $? != 0 ]; then
			echo "$d_img""md5_sum inconsistent, aborted image updating !"
			exit 1
	fi

	# Extract kernel image
	tar -xf $2 $k_img -O | md5sum | sed 's/-/'$k_img'/g' > $md5_rt_result
	# Check integrity
	grep $k_img $md5_cmp > $md5_tmp
	diff $md5_rt_result $md5_tmp

	if [ $? != 0 ]; then
			echo "$k_img""md5_sum inconsistent, aborted image updating !"
			exit 1
	fi

	# Extract rootfs image
	tar -xf $2 $r_img -O | md5sum | sed 's/-/'$r_img'/g' > $md5_rt_result
	# Check integrity
	grep $r_img $md5_cmp > $md5_tmp
	diff $md5_rt_result $md5_tmp

	if [ $? != 0 ]; then
			# rm $r_img
			echo "$r_img""md5_sum inconsistent, aborted image updating !"
			exit 1
	fi

	if [ $osgi_upgraded = 1 ]; then
		# Extract osgi image
		tar -xf $2 $o_img -O | md5sum | sed 's/-/'$o_img'/g' > $md5_rt_result
		# Check integrity
		grep $o_img $md5_cmp > $md5_tmp
		diff $md5_rt_result $md5_tmp

		if [ $? != 0 ]; then
			# rm $o_img
			echo "$o_img""md5_sum inconsistent, aborted image updating !"
			exit 1
		fi
	fi

	echo "Integrity of $k_img & $r_img is okay."
}

do_firware_ver_chk() {
	# Check upgrade firmware's version with current firmware version
	tar -xf $2 $img_ver
	if [ $? != 0 ]; then
		echo "1" > /var/firmware_upgrade_status
		echo "Firmware version incorrect: no fwu_ver in img.tar !"
		exit 1
	fi

	cat $img_ver > $new_fw_ver
	cat /etc/version > $cur_fw_ver

	cat $new_fw_ver | grep -n '^V[0-9]*.[0-9]*.[0-9]*[-_][0-9][0-9]*'
	if [ $? != 0 ]; then
		echo "1" > /var/firmware_upgrade_status
		echo "Firmware version incorrect: `cat $new_fw_ver` !"
		exit 1
	fi

	echo "Try to upgrade firmware version from `cat $cur_fw_ver`"
	echo "                                  to `cat $new_fw_ver`"

	if [ "`cat $new_fw_ver`" == "`cat $cur_fw_ver`" ]; then
		echo "4" > /var/firmware_upgrade_status
			echo "Current firmware version already is `cat $cur_fw_ver` !"
			exit 1
	fi

	echo "Firware version check okay."
}

get_mmc_blkp_from_part_name(){
	dev_num="$1"
	part_name="$2"
	info=$(parted --script /dev/mmcblk${dev_num} p | grep -w "$part_name")
	set $info
	echo "/dev/mmcblk${dev_num}p$1"
}

do_extract_and_update_img() {
	img_num=$1
	tar_name=$2
	vdimg=$(get_mmc_blkp_from_part_name "0" "DTB${img_num}")
	vkimg=$(get_mmc_blkp_from_part_name "0" "k${img_num}")
	vrimg=$(get_mmc_blkp_from_part_name "0" "r${img_num}")


	tar -xf "${tar_name}" $d_img
	cp "$d_img" "$vdimg"
	echo cp "$d_img" "$vdimg"

	tar -xf "${tar_name}" $k_img
	cp "$k_img" "$vkimg"
	echo cp "$k_img" "$vkimg"

	tar -xf "${tar_name}" $r_img
	cp "$r_img" "$vrimg"
	echo cp "$r_img" "$vrimg"

	if [ $osgi_upgraded = 1 ]; then
		tar -xf "${tar_name}" $o_img
		vosgi=$(get_mmc_blkp_from_part_name "0" "${osgi_mmc_name}")
		cp "$vosgi" "$o_img"
	fi


}

write_ver_record_and_clean() {
	cat $new_fw_ver | grep CST
	if [ $? = 0 ]; then
		echo `cat $new_fw_ver` | sed 's/ *--.*$//g' > $env_sw_ver
	else
		cat $new_fw_ver > $env_sw_ver
	fi
	# Write image version information 
	nv setenv sw_version"$1" "`cat $env_sw_ver`"

	# Clean up temporary files
	rm -f $md5_cmp $md5_tmp $md5_rt_result $img_ver $new_fw_ver $cur_fw_ver $env_sw_ver  $d_img $k_img $r_img $2

	# Post processing (for future extension consideration)

	echo "Successfully updated image $1!!"
}

main() {
	check_osgi "$arg1" "$arg2"
	update_framework "$arg1" "$arg2"
	do_hwver_check "$arg1" "$arg2"
	do_extract_img_md5 "$arg1" "$arg2"
	do_firware_ver_chk "$arg1" "$arg2"
	do_extract_and_update_img "$arg1" "$arg2"
	write_ver_record_and_clean "$arg1" "$arg2"
}

main

# Stop this script upon any error
# set -e

