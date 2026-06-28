#!/bin/sh
#Generate luna firmware upgarde image tar ball

echo $1
use_ubifs=1
if [ "$1" = "-ubifs" ]; then
	use_ubifs=0
fi
if [ "${LINUXDIR}" = "" ];then
LINUXDIR="linux-4.4.x"
fi
echo "-------gen_fwu_img_g3.sh - LINUXDIR: $LINUXDIR   ---------------------"
#if no one export DTB_FILE
if [ "x$DTB_FILE" = "x" ]; then
DTB_FILE="ca7774-engboard.dtb"
fi

up_script="fwu.sh"
fw_list="dtb rootfs kimage fwu_ver hw_ver"

framework_list="framework.img framework.sh"
all_list="$up_script $fw_list $framework_list"
md5_result="md5.txt"
dst_dir="../images/img_tar"
romfs_ver="../romfs/etc/version"
fw_tar_file="img.tar"
fw_tar_file_noOsgi="img_noOsgi.tar"
fw_tar_file_noPreBundle="img_noPreBundle.tar"
fw_tar_file2="img_enc.tar"
openssl_exe="openssl"
openssl_key="realtek"
encrypt_algo="aes-128-cbc"
framework_tar_file="framework.tar"
all_tar_file="fw_framework.tar"
pwddir=`pwd`
rootdir=`dirname $pwddir`
TAR='tar --format=gnu'

hw_check=`cat ../.config | grep CONFIG_HWVER_CHECK | sed s/CONFIG_HWVER_CHECK=//g | sed s/\"//g`
hw_ver_str=`cat ../.config | grep CONFIG_HW_HWVER | sed s/CONFIG_HW_HWVER=\"//g | sed s/\"//g`
is_yueme=`cat ../${LINUXDIR}/.config | grep "CONFIG_YUEME=" | sed s/[^y]//g | sed s/\"//g`
is_cmcc=`cat ../${LINUXDIR}/.config | grep "CONFIG_CMCC=" | sed s/[^y]//g | sed s/\"//g`
is_cu_yueme=`cat ../${LINUXDIR}/.config | grep "CONFIG_CU_BASEON_YUEME=" | sed s/[^y]//g | sed s/\"//g`
is_cu_cmcc=`cat ../${LINUXDIR}/.config | grep "CONFIG_CU_BASEON_CMCC=" | sed s/[^y]//g | sed s/\"//g`
is_jio=`cat ../${LINUXDIR}/.config | grep "CONFIG_JIO=" | sed s/[^y]//g | sed s/\"//g`
cmcc_install_prebundle=`cat ../config/.config | grep "CONFIG_CMCC_OSGI_PREBUNDLE=" | sed s/[^y]//g | sed s/\"//g`

# For FW sigature
sign_fw=`cat ../config/.config | grep "CONFIG_LUNA_FWU_SIGNATURE=" | sed s/[^y]//g | sed s/\"//g`
all_files_to_sign="$fw_tar_file $fw_tar_file_noOsgi $fw_tar_file_noPreBundle $fw_tar_file2 $framework_tar_file $all_tar_file"
unsigned_fw_suffix="orig"
openssl_dgst_algo="-sha256"
openssl_private_key_name="fwu_private.pem"
openssl_private_key_path=$rootdir/tools/security/$openssl_private_key_name

if [ "y" = "$is_cmcc" ]; then
    fw_list_osgi="dtb rootfs kimage osgi.img fwu_ver hw_ver"
    fw_list_osgi_install_prebundle="dtb rootfs kimage osgi.img fwu_ver hw_ver install_prebundle_flag"
    echo "CMCC fw_list=$fw_list_osgi"
fi

if [ "y" = "$is_cu_cmcc" ]; then
    fw_list_osgi="dtb rootfs kimage osgi.img fwu_ver hw_ver"
    fw_list_osgi_install_prebundle="dtb rootfs kimage osgi.img fwu_ver hw_ver install_prebundle_flag"
    echo "CU fw_list=$fw_list_osgi"
fi

test -f hw_ver && rm -rf hw_ver
if [ "$hw_check" = "y" ]; then
    echo $hw_ver_str > hw_ver
else
    echo "skip" > hw_ver
fi

if [ "$use_ubifs" = "0" ]; then
	if [ "$is_cmcc" = "y" ]; then
		cp fwu_ubi_cmcc.sh fwu.sh
	elif [ "$is_cu_cmcc" = "y" ]; then
		cp fwu_ubi_cmcc.sh fwu.sh
	elif [ "$is_jio" = "y" ]; then
		cp fwu_ubi_jio.sh fwu.sh
	elif [ "$is_yueme" = "y" ]; then
		cp fwu_ubi_yueme.sh fwu.sh
	else
		cp fwu_ubi.sh fwu.sh
	fi
else
	if [ "$is_cmcc" = "y" ]; then
		cp fwu_cmcc.sh fwu.sh
	elif [ "$is_cu_cmcc" = "y" ]; then
		cp fwu_cmcc.sh fwu.sh
	elif [ "$is_jio" = "y" ]; then
		cp fwu_jio.sh fwu.sh
	else
		cp fwu_sdk.sh fwu.sh
	fi
fi

if [ "$is_cu_yueme" = "y" ]; then
    cp framework_cu.sh framework.sh
else
    cp framework_yueme.sh framework.sh
fi

if [ ! -d $dst_dir ];then
	mkdir -p $dst_dir
fi

#g3_eng
cp ../images/${DTB_FILE}  $dst_dir/dtb
if [ "$use_ubifs" = "1" ]; then
cp ../images/rootfs_G3_1.ubi      $dst_dir/rootfs
else
cp ../images/rootfs      $dst_dir/rootfs
fi
cp ../images/Image.lzma            $dst_dir/kimage

cp fwu.sh $dst_dir
cp ../${LINUXDIR}/fwu_ver $dst_dir

#[ -f ../images/osgi/osgi.img ] && cp ../images/osgi.img $dst_dir

# If /romfs/etc/version is exist, replace it to /images/fwu_ver 
# then parse&store by nv setenv in fwu.sh
cat $romfs_ver
if [ $? = 0 ]; then
if [ "y" = "$is_yueme" ]; then
	echo `cat $romfs_ver` | sed 's/ *--.*$//g' > $dst_dir/fwu_ver
else
if [ "y" = "$is_cu_yueme" ]; then
	echo `cat $romfs_ver` | sed 's/ *--.*$//g' > $dst_dir/fwu_ver
else
	cat $romfs_ver > $dst_dir/fwu_ver
fi
fi	
fi

cp hw_ver $dst_dir
cd $dst_dir


if [ "y" = "$is_cmcc" ] || [ "y" = "$is_cu_cmcc" ]; then
#img.tar: fwu.sh rootfs uImage osgi.img fwu_ver hw_ver md5.txt
#img_noOsgi.tar: fwu.sh rootfs uImage fwu_ver hw_ver md5.txt
cp ../osgi/osgi_noPreBundle.img ./osgi.img
md5sum $fw_list_osgi $up_script > $md5_result
${TAR} -cf $fw_tar_file_noPreBundle $up_script $fw_list_osgi $md5_result
rm -rf ./osgi.img
cp ../osgi/osgi.img ./osgi.img

if [ "y" = "$cmcc_install_prebundle" ]; then 
touch install_prebundle_flag
md5sum $fw_list_osgi_install_prebundle $up_script > $md5_result
${TAR} -cf $fw_tar_file $up_script $fw_list_osgi_install_prebundle $md5_result
cat $fw_tar_file | $openssl_exe $encrypt_algo -e -out $fw_tar_file2  -k $openssl_key
else
md5sum $fw_list_osgi $up_script > $md5_result
${TAR} -cf $fw_tar_file $up_script $fw_list_osgi $md5_result
cat $fw_tar_file | $openssl_exe $encrypt_algo -e -out $fw_tar_file2  -k $openssl_key
fi
md5sum $fw_list $up_script > $md5_result
${TAR} -cf $fw_tar_file_noOsgi $up_script $fw_list $md5_result
else
md5sum $fw_list $up_script > $md5_result
${TAR} -cf $fw_tar_file $up_script $fw_list $md5_result
fi

#### work in images/img_tar

if [ "$is_yueme" = "y" ] && [ -f $rootdir/framework.img ]; then
	cp  $rootdir/framework.img .
	echo Aligning framework.img to 2k/page boundary for NAND platform
	sz=`stat --printf="%s" $rootdir/framework.img`
	pagecnt=$(( (sz+2047) / 2048 ))
	dd if=${rootdir}/framework.img ibs=2k count=$pagecnt of=./framework.img conv=sync
	ls -l ./framework.img
	cp $rootdir/tools/framework.sh .

	md5sum $framework_list $up_script > $md5_result
	${TAR} -cf $framework_tar_file $up_script $framework_list $md5_result
	md5sum $all_list > $md5_result
	${TAR} -cf $all_tar_file $all_list $md5_result
fi
if [ "$is_cu_yueme" = "y" ] && [ -f $rootdir/framework.img ]; then
	cp  $rootdir/framework.img .
	echo Aligning framework.img to 2k/page boundary for NAND platform
	sz=`stat --printf="%s" $rootdir/framework.img`
	pagecnt=$(( (sz+2047) / 2048 ))
	dd if=${rootdir}/framework.img ibs=2k count=$pagecnt of=./framework.img conv=sync
	ls -l ./framework.img
	cp $rootdir/tools/framework.sh .

	md5sum $framework_list $up_script > $md5_result
	tar -cf $framework_tar_file $up_script $framework_list $md5_result
	md5sum $all_list > $md5_result
	tar -cf $all_tar_file $all_list $md5_result
fi

echo all files list: $all_files_to_sign
for file in $all_files_to_sign
do
	if [ -f $file ]; then
		echo "Signing $file...."
		mv $file $file.$unsigned_fw_suffix
		if [ "$sign_fw" = "y" ]; then
			$openssl_exe dgst $openssl_dgst_algo -sign $openssl_private_key_path -out $file.sig $file.$unsigned_fw_suffix
		else
			$openssl_exe dgst $openssl_dgst_algo -binary -out $file.sig $file.$unsigned_fw_suffix
		fi
		cat $file.$unsigned_fw_suffix $file.sig > $file
	fi
done

cp *.tar.$unsigned_fw_suffix ../

ls -l $fw_tar_file
cp *.tar ../
