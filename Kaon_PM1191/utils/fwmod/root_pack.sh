rm -v new_squashfs.img
mksquashfs rootfs_extracted/ new_squashfs.img -comp xz -b 131072 -always-use-fragments -no-recovery -noappend
