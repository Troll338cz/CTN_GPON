#!/bin/sh
#Generate luna firmware upgarde image tar ball

f_list="fwu.sh rootfs uImage fwu_ver"
md5_result="md5.txt"
img_tar_file="img.tar"

cp ../tools/xdsl/fwu.sh $IMAGEDIR
cp fwu_ver $IMAGEDIR
cd $IMAGEDIR
md5sum $f_list > $md5_result
tar -cf $img_tar_file $f_list $md5_result
ls -l $img_tar_file
