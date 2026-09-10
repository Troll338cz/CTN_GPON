| ISP             | Infrastruktura |  Technology      | Postup     | Status  | Dokumentace |
| --------------- | ---------------|------------------|------------|---------|---------|
| T-Mobile        | T-Fibre          | GPON           | SN clone[^first] | Funkční+Testováno | [Root.cz](https://forum.root.cz/index.php?topic=31138.15) |
| T-Mobile        | T-Fibre          | XGS-PON        | SN clone[^first] | Funkční+Testováno | [GRG-4362](https://github.com/Troll338cz/Unlock-Comtrend-GRG-4362/blob/main/T-mobile.md) |
| T-Mobile        | Cetin            | GPON           | SN clone | Asi funkční | - |
| Telekom Slovakia | -            | GPON           | SN clone | Asi funkční | - |
| O2.cz           | Cetin            | GPON           | Přes podporu / SN clone        | Working | [O2.cz](https://www.o2.cz/podpora/internet/zapojeni-pevny-internet/nastavit-vlastni-prevodnik-ont) |
| O2.cz           | Cetin            | XGS-GPON       | SN clone        | Funkční | [Writeup](https://gist.github.com/arapov/7eb9d2a1c2186ede049548a8c77b508e) |
| Vodafone.cz     | Cetin            | GPON       | SN Clone         | Asi funkční | -  |
| Vodafone.cz     | Cetin            | XGS-GPON       | SN Clone         | Funkční | [techforum.cz](https://www.techforum.cz/topic/64188-vlastn%C3%AD-ont-na-s%C3%ADti-cetin/) |
| Vodafone.cz     | Vodafone            | GPON       | ?         | ? | Asi full clone |
| Vodafone.cz     | Vodafone            | XGS-GPON       | ?         | ? | - |
| Ceznet     | -            | GPON       | ?         | Mají infra mix na Nokia/Huawei | Asi SN/full clone |

[^first]: Musíte nastavit také "OMCI vendor ID (ME 256)" na 4 první znaky SN, jinak vám OLT ze strany TMO vrátí status fake-O5 kde na ONU nedojde provisioning VLANů.


## GPON
Pro všechny partnery Cetin by mněl být stejný postup.

Při výběru pro GPON doporučuji Realtek, na netu je hromada informací a projeků s custom firmware. Mají hardware v podobě bridge,router i SFP.

V případě že si koupíte starší SFP stick s Lantiq čipem tak některé pokročilé věci to neumí.

Co nebrat: 
- Passive GPON moduly: Jedná se pouze o optickou část SFP, vše co komunukuje na protokolu GPON musí dělat podporované zařízení. Poznáte většinou podle ceny, npř. Huawei HPSP2120.
- Sercomm FGS202: Za podobou cenu si můžete pořídit použitý Huawei MA5671A a odemknout ho, bez custom firmware nejdte telnet a nenastavíte tam nic, navíc je to slabý hardware co ani neumí 2.5G.
- Faraday / Galachip SFP: Není o nich dokumentace. Jen pokud si chcete pohrát s neznámím hardware jako já :-).
- Sercomm / Sagemcom: Vetšina ONT od těchto firem mají secure boot a jsou zamčené, pro naše účely e-waste. 
- Huawei SFU řady OptiXstar (př. HG8010H): Podle toho jaký firmware na zařízení je bude zamčené, nastavíte pouze SN a GPON auth, ostatní ME paramtry mněnit nelze.
- Nokia SFU: Při výběru opatrně podle typu a firmware, jsou mraky druhů pod témněř identických typech  Nokia G-010?-? / Nokia XS-010?-?. Berte pouze pokud 100% víte že jde odemknout, npř. pro některé zatím nejsou login generátory nebo se spravovat nedají. 
- Zyxel: Nové zařízení mají per-device hesla, pokud jej odemknete tak jde mněnit jenom SN. Cetin je taky už klientům nedává.

## XGS-PON
Při výberu SFP raděj zaplate víc, dokumentace na [hack-gpon](https://hack-gpon.org/) a [CA8271x](https://github.com/YuukiJapanTech/CA8271x#ca8271--ca8289-gpon-devices) tam mají pár modulů už zdokumentovaných, a pak zvášt komunita okolo Maxlinear a varianty WAS110.

Pokud chcete pouze jednoduchý bridge tak Comtrend GRG-4362 se dá odemknout přes UART, pak funguje pro Cetin i T-Fibre.

Co nebrat:
- Nokia SFU: Skoro vše je zamčené a pravděpodobně secureboot...
- Huawei OptiXstar S800E: Občas dostupné levně, nikdo zatím nezkoušel jak moc je odemčené.
- Innbox X24: Econet SoC je fuj, budou jen problémy.
