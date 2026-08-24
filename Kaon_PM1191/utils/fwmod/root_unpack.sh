# ubireader_extract_images rootfs1.img
# cp ubifs-root/56367507/squashfs_ubi/img-56367507_vol-squashfs_ubi.ubifs .
# as root...
unsquashfs -d rootfs_extracted/ img-56367507_vol-squashfs_ubi.ubifs

