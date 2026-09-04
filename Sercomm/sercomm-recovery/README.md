This tool allows you to flash firmware into a Sercomm router after it
was put into download mode, e.g. if the original firmware was destroyed.
It runs under Linux only, you must be root to execute it.

## 1. Compile


make


## 2. Enter Download Mode

 1. Power off the device
 2. Press the RESET or WPS button (this depends on the router model)
 3. Power on while holding the button
 4. Wait 5 seconds or more until the LEDs blink in a special pattern depending on the router model.


## 3. Run the Tool

Connect a LAN port to a NIC of the host, e.g. to eth1.

### 3.1. Probe the Device
`./sercomm-recovery eth1`

This should list some info about all device found in download mode.


### 3.2. Flash


`./sercomm-recovery eth1 flash_burn.bin`

This probes for devices in download mode. If more than one found, it
prompts for the one to flash. Afterwards the firmware file is checked
(matching hardware id etc.) and flashed. A reboot is executed afterwards.


## 4. Troubleshooting

If anything goes wrong with probing or flashing, please execute the command
again with "-v", e.g:

`./sercomm-recovery -v eth1 flash_burn.bin`

This adds a lot of debug output to stdout.


## 5. Status

Currently works with:  

* Sercomm AD1018
* Sercomm FGS202
* Sercomm H500-s (untested)
* Sercomm Vox 2.5 (untested)

If you plan to use this tool on a device not listed here, be sure to create a full backup of your flash contents!

Just because device is detected does not mean the protocol is 100% supported, many devices could have architecture specific quirks.
