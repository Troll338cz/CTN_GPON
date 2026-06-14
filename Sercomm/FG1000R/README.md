## FG1000R flash dump
- FG1000R_SNANDer_read1_-I.tgz - Read with -I
- FG1000R_SNANDer_read2_-d.tgz - Read with -d
99% sure its not an good idea to flash thise

## Possible root methods
- Replace /var/protect/scftmgr with a bash script
- Add payload to /var/config/run_customized_sdk.sh

## Interesting stuff
- You can download encrypted config from device
- Has special jffs mtd mounted at /var/protect/ 
- No clue on how to mount yaffs from dump
