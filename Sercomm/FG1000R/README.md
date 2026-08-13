## FG1000R flash dump
- FG1000R_SNANDer_read1_-I.tgz - Read with -I
- FG1000R_SNANDer_read2_-d.tgz - Read with -d

99% sure its not an good idea to flash this back to your device!

## Possible root methods
- Replace /var/protect/scftmgr with a bash script, rename real one and launch it after your commands.
- Add payload to /var/config/run_customized_sdk.sh, works on most Realtek devices, its an feature!

Both need flash desolder and lot of work, just replace this locked ewaste....

## Interesting stuff
- You can download encrypted config from device
- Has special jffs2 mtd mounted at /var/protect/
- BigEndian YAFFS unmountable?
- 128MB Flash is wasted on mips firmware that usualy fits info 16MB even with dualboot
