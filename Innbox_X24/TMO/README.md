## Test Results
- Cloned my GPON SN+Vendor ID with ```fad config setenv serial_gpon ISKTA1B2C3D4```
- After boot it took about 15 seconds to reach O5
- VLANs were sucessfully set from OMCI settings
- Filling in VLAN id 2510 with pbit 0 resulted in PPPoE untaged?? on LAN1 interface, reached speeds 960/380 Mb/s and packet loss of 1.3%
- Filling in -1 for both values on "Connected bridge" resulted in PPPoE untaged?? on LAN1 interface, reached speeds 960/890 Mb/s with no packet loss
- Device works but doesn't reach stable speeds, my configuration was probably sub-optimal due to lack of proper documentation.
