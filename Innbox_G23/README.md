Unless more work is put into patching MIPS binaries system will reset most of OMCI info on reboot.

It should be possible to use /var/config/run_customized_sdk.sh to set values back on startup as a temporary fix.

GRG-4284 and G23 is idential device, Comtrend software uses newer SDK and isnt locked but i haven't got crossflash to boot properly.

Unsure if this is due to U-Boot version or issue with hardware but Comtrend firmware will hang on boot and shorty after crash with OOM error.

Again, unless you have to keep this just replace this device...


