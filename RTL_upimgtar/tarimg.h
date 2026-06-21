
#if 0
#define TAR_KERNEL_NAME		"uImage"
#define TAR_KERNEL_NAME_SIZE	6

#define TAR_ROOTFS_NAME		"rootfs"
#define TAR_ROOTFS_NAME_SIZE	6

#define TAR_FWUVER_NAME		"fwu_ver"
#define TAR_FWUVER_NAME_SIZE	6
#define TAR_FWUVER_FILE_SIZE	32
#else  //G3
/*****************G3 ***********
fw_list="dtb rootfs kimage fwu_ver hw_ver"
********************************/
#define TAR_DTB_NAME        "dtb"
#define TAR_DTB_NAME_SIZE   3

#define TAR_KERNEL_NAME		"kimage"
#define TAR_KERNEL_NAME_SIZE	6

#define TAR_ROOTFS_NAME		"rootfs"
#define TAR_ROOTFS_NAME_SIZE	6

#define TAR_OSGI_NAME		"osgi.img"
#define TAR_OSGI_NAME_SIZE	8

#define TAR_FWUVER_NAME		"fwu_ver"
#define TAR_FWUVER_NAME_SIZE	6
#define TAR_FWUVER_FILE_SIZE	32

#define TAR_ENV_NAME "uboot-env.bin"
#define TAR_ENV_NAME_SIZE sizeof(TAR_ENV_NAME)

#endif

#if CONFIG_RTK_USE_ONE_UBI_DEVICE
#define UBI_MAIN_DEVICE_NAME "ubi_device"
#define UBI_DTB0_NAME "ubi_DTB0"
#define UBI_DTB1_NAME "ubi_DTB1"
#define UBI_K0_NAME "ubi_k0"
#define UBI_K1_NAME "ubi_k1"
#define UBI_R0_NAME "ubi_r0"
#define UBI_R1_NAME "ubi_r1"
#define UBI_OSGI_NAME "ubi_osgi"
#endif


// Dont think i can share more then this....

// SPI need fwu_ver+kernel+rootfs
// Ubi need dtb+kernel+rootfs+fwu_ver 
// tarimg flash both image0 and image1 with same file

/*
For ubi U-Boot also need have env set with partition sizes (set to ur specific device specs)
pf1_apps_sz=0x3000000
pfl_boot_sz=0x200000
pfl_env_size=0x40000
pfl_fdt1_sz=0x40000
pfl_fdt2_sz=0x40000
pfl_fip_sz=0xC0000
pfl_kernel1_sz=0x600000
pfl_kernel2_sz=0x600000
pfl_rootfs1_sz=0x4600000
pfl_rootfs2_sz=0x4600000
*/