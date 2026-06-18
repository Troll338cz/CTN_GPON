
## Patch FW
- Add /var/config/skip_version to disable /etc/version.sh
- Patch /bin/startup to not reset HW VER and HW REV
- Enable telnet on LAN by default
- Disable http/telnet on WAN by default
- Set OMCI_OLT_MODE=3 by default
- Set OMCI_FAKE_OK=1 by default
- Make sure to change WAN User
```
<Value Name="WAN_USER_NAME" Value="tendaxpon"/>
<Value Name="WAN_USER_PASSWORD" Value="XPON#TDWLD"/>
```
- OMCI Need telnet edit
- SSH and HTTPS support not in firmware, xml change cant affect it