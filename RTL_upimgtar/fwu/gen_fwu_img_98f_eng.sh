#!/bin/sh
#Generate luna firmware upgarde image tar ball

COMPRESS_UP_SH=1

up_script="fwu.sh"
fw_list="dtb rootfs kimage fwu_ver hw_ver"
framework_list="framework.img framework.sh"
all_list="$up_script $fw_list $framework_list"
md5_result="md5.txt"
dst_dir="../images/img_tar"
romfs_ver="../romfs/etc/version"
fw_tar_file="img.tar"
framework_tar_file="framework.tar"
all_tar_file="fw_framework.tar"
TAR='tar --format=gnu'

hw_check=`cat ../.config | grep CONFIG_HWVER_CHECK | sed s/CONFIG_HWVER_CHECK=//g | sed s/\"//g`
hw_ver_str=`cat ../.config | grep CONFIG_HW_HWVER | sed s/CONFIG_HW_HWVER=\"//g | sed s/\"//g`
is_yueme=`cat ../linux-4.4.x/.config | grep "CONFIG_YUEME=" | sed s/[^y]//g | sed s/\"//g`
is_cmcc=`cat ../linux-4.4.x/.config | grep "CONFIG_CMCC=" | sed s/[^y]//g | sed s/\"//g`
is_cu_yueme=`cat ../linux-4.4.x/.config | grep "CONFIG_CU_BASEON_YUEME=" | sed s/[^y]//g | sed s/\"//g`
is_cu_cmcc=`cat ../linux-4.4.x/.config | grep "CONFIG_CU_BASEON_CMCC=" | sed s/[^y]//g | sed s/\"//g`
is_rootfs_ubifs=`cat ../linux-4.4.x/.config | grep "CONFIG_UBIFS_FS=" | sed s/[^y]//g | sed s/\"//g`
is_ubi_dev=`cat ../linux-4.4.x/.config | grep "CONFIG_MTD_UBI=" | sed s/[^y]//g | sed s/\"//g`

test -f hw_ver && rm -rf hw_ver
if [ "$hw_check" = "y" ]; then
    echo $hw_ver_str > hw_ver
else
    echo "skip" > hw_ver
fi

if [ "$is_cmcc" = "y" ]; then
    cp fwu_cmcc.sh fwu.sh
elif [ "$is_cu_cmcc" = "y" ]; then
    cp fwu_cmcc.sh fwu.sh
elif [ "$is_ubi_dev" = "y" ]; then
    cp fwu_luna_98f_ubi.sh fwu.sh
else
    cp fwu_sdk.sh fwu.sh
fi

if [ "$is_cu_yueme" = "y" ]; then
    cp framework_cu.sh framework.sh
else
    cp framework_yueme.sh framework.sh
fi

if [ ! -d $dst_dir ];then
    mkdir -p $dst_dir
fi

# remove old data
rm $dst_dir/*

#g3_eng
#cp ../images/ca7774-engboard.dtb  $dst_dir/dtb
#cp ../images/rootfs_G3_1.ubi      $dst_dir/rootfs
#cp ../images/Image.gz             $dst_dir/kimage

#98f_eng
cp ../images/rtl8198f-engboard.dtb $dst_dir/dtb
cp ../images/uImage $dst_dir/kimage
#if [ "$is_rootfs_ubifs" = "y" ]; then
#cp ../images/ubifs.rootfs $dst_dir/rootfs
#else
cp ../images/squashfs.rootfs $dst_dir/rootfs
#fi

cp fwu.sh $dst_dir
cp ../linux-4.4.x/fwu_ver $dst_dir

# If /romfs/etc/version is exist, replace it to /images/fwu_ver 
# then parse&store by nv setenv in fwu.sh
cat $romfs_ver
if [ $? = 0 ]; then 
    cat $romfs_ver > $dst_dir/fwu_ver
fi

cp hw_ver $dst_dir
cd $dst_dir
md5sum $fw_list $up_script > $md5_result
if [ $COMPRESS_UP_SH = 1 ]; then
gzip $up_script
up_script="fwu.sh.gz"
fi
${TAR} -cf $fw_tar_file $up_script $fw_list $md5_result

if [ "$is_yueme" = "y" ] && [ -f ../framework.img ]; then
    cd -
    echo Aligning framework.img to 2k/page boundary for NAND platform
    sz=`stat --printf="%s" ../framework.img`
    pagecnt=$(( (sz+2047) / 2048 ))
    dd if=../framework.img ibs=2k count=$pagecnt of=$dst_dir/framework.img conv=sync
    ls -l ../images/framework.img
    cp framework.sh $dst_dir

    cd $dst_dir
    md5sum $framework_list $up_script > $md5_result
    ${TAR} -cf $framework_tar_file $up_script $framework_list $md5_result
    md5sum $all_list > $md5_result
    ${TAR} -cf $all_tar_file $all_list $md5_result
fi
if [ "$is_cu_yueme" = "y" ] && [ -f ../framework.img ]; then
    cd -
    echo Aligning framework.img to 2k/page boundary for NAND platform
    sz=`stat --printf="%s" ../framework.img`
    pagecnt=$(( (sz+2047) / 2048 ))
    dd if=../framework.img ibs=2k count=$pagecnt of=$dst_dir/framework.img conv=sync
    ls -l ../images/framework.img
    cp framework.sh $dst_dir

    cd $dst_dir
    md5sum $framework_list $up_script > $md5_result
    tar -cf $framework_tar_file $up_script $framework_list $md5_result
    md5sum $all_list > $md5_result
    tar -cf $all_tar_file $all_list $md5_result
fi
ls -l $fw_tar_file
cp *.tar ../

