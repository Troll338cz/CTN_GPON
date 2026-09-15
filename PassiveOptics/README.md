A quick list of junk hardware I accidentally got.

Modules without MAC are only the optical part of a normal ONU, they behave like a normal SFP module with specific laser wavelenths.

Although it is theoretically possible to find the necessary bits in a supported router firmware, it is unlikely that full functionality will even work on other devices (dependency on hardware features, closed binaries or kernel modules, and other possible incompatibilities).

It's unlikely that we will ever see the day when Linux can accept a SFP module and just run entire GPON stack without dedicated ONU hardware.

Don't be fooled by sellers claiming this as a "Mini ONU, SFP Stick or GPON Module", this does not work the same as "smart" devices like the Hauwei MA5671A.

The purchase is a 100% waste of money as they can't even run normal ethernet traffic even with the appropriate matching pair of modules.

## Sercomm CS50001
Sold as "SFP-EOLE XGSPON" or "10GB gpon onu CS50001 mini ont"

Used in: "Sunrise Internet Box Fiber (Zyxel AX7501-B0)", "Bouygues Telecom Bbox Ultym", "Sagemcom F@st5688ax", "TIM Hub"

```
                      name: sfp-sfpplus1                                                             
                    status: no-link                                                                  
          auto-negotiation: done                                                                     
                 supported: 10M-baseT-half                                                           
                            10M-baseT-full                                                           
                            100M-baseT-half                                                          
                            100M-baseT-full                                                          
                            1G-baseT-half                                                            
                            1G-baseT-full                                                            
                            1G-baseX                                                                 
                            2.5G-baseT                                                               
                            2.5G-baseX                                                               
                            5G-baseT                                                                 
                            10G-baseT                                                                
                            10G-baseSR-LR                                                            
                            10G-baseCR                                                               
             sfp-supported: 1G-baseX                                                                 
                            10G-baseSR-LR                                                            
               advertising: 1G-baseX                                                                 
                            10G-baseSR-LR                                                            
  link-partner-advertising:                                                                          
        sfp-module-present: yes                                                                      
               sfp-rx-loss: no                                                                       
              sfp-tx-fault: no                                                                       
                  sfp-type: SFP/SFP+/SFP28/SFP56                                                     
        sfp-connector-type: SC                                                                       
              sfp-encoding: nrz                                                                      
        sfp-link-length-sm: 20km                                                                     
           sfp-vendor-name: TSUHAN LTD.                                                              
    sfp-vendor-part-number: THMPRA-2677-GXA                                                          
       sfp-vendor-revision: 10                                                                       
         sfp-vendor-serial: 802670138206693                                                          
    sfp-manufacturing-date: 22-09-28                                                                 
            sfp-wavelength: 1270nm                                                                   
           sfp-temperature: 30C                                                                      
        sfp-supply-voltage: 3.26V                                                                    
       sfp-tx-bias-current: 0mA                                                                      
              sfp-rx-power: -40dBm                                                                   
           eeprom-checksum: good                                                                     
                    eeprom: 0000: 03 04 01 00 00 00 00 00  00 00 00 03 64 64 14 c8  ........ ....dd..
                            0010: 00 00 00 00 54 53 55 48  41 4e 20 4c 54 44 2e 20  ....TSUH AN LTD. 
                            0020: 20 20 20 20 00 00 00 00  54 48 4d 50 52 41 2d 32      .... THMPRA-2
                            0030: 36 37 37 2d 47 58 41 20  31 30 20 20 04 f6 00 eb  677-GXA  10  ....
                            0040: 00 1a 00 00 38 30 32 36  37 30 31 33 38 32 30 36  ....8026 70138206
                            0050: 36 39 33 20 32 32 30 39  32 38 20 20 68 f0 08 1e  693 2209 28  h...
                            0060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ........ ........
                            *                                                                        
                            0080: 5a 00 f1 00 55 00 f6 00  8d cc 74 04 87 28 7a a8  Z...U... ..t..(z.
                            0090: af c8 00 00 88 b8 00 00  ff ff 45 77 ff ff 6e 18  ........ ..Ew..n.
                            00a0: 07 cb 00 09 04 eb 00 0e  00 00 00 00 00 00 00 00  ........ ........
                            00b0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ........ ........
                            00c0: 00 00 00 00 3f 80 00 00  00 00 00 00 01 00 00 00  ....?... ........
                            00d0: 01 00 00 00 01 00 00 00  01 00 00 00 00 00 00 c8  ........ ........
                            00e0: 1e a4 7f 58 00 00 00 00  00 01 00 00 00 00 82 00  ...X.... ........
                            00f0: 01 40 00 00 01 40 00 ff  ff ff ff ff ff ff ff 00  .@...@.. ........
```

## Huawei HPSP2120
Used in: Huawei SmartAX MA5620/MA5626, Huawei GPON OLT/ONU

```
                      name: sfp-sfpplus1                                                             
                    status: no-link                                                                  
          auto-negotiation: done                                                                     
                 supported: 10M-baseT-half                                                           
                            10M-baseT-full                                                           
                            100M-baseT-half                                                          
                            100M-baseT-full                                                          
                            1G-baseT-half                                                            
                            1G-baseT-full                                                            
                            1G-baseX                                                                 
                            2.5G-baseT                                                               
                            2.5G-baseX                                                               
                            5G-baseT                                                                 
                            10G-baseT                                                                
                            10G-baseSR-LR                                                            
                            10G-baseCR                                                               
             sfp-supported: 1G-baseX                                                                 
               advertising: 1G-baseX                                                                 
  link-partner-advertising:                                                                          
        sfp-module-present: yes                                                                      
               sfp-rx-loss: no                                                                       
              sfp-tx-fault: no                                                                       
                  sfp-type: SFP/SFP+/SFP28/SFP56                                                     
        sfp-connector-type: SC                                                                       
              sfp-encoding: nrz                                                                      
        sfp-link-length-sm: 20km                                                                     
           sfp-vendor-name: HUAWEI                                                                   
    sfp-vendor-part-number: HPSP2120                                                                 
         sfp-vendor-serial: 030KMF6TB4524820                                                         
    sfp-manufacturing-date: 11041403                                                                 
            sfp-wavelength: 1310nm                                                                   
           sfp-temperature: -24C                                                                     
        sfp-supply-voltage: 3.391V                                                                   
       sfp-tx-bias-current: 0mA                                                                      
              sfp-tx-power: 2.499dBm                                                                 
           eeprom-checksum: good                                                                     
                    eeprom: 0000: 03 04 01 00 00 00 00 00  00 00 00 03 0d 00 14 c8  ........ ........
                            0010: 00 00 00 00 48 55 41 57  45 49 20 20 20 20 20 20  ....HUAW EI      
                            0020: 20 20 20 20 00 00 00 00  48 50 53 50 32 31 32 30      .... HPSP2120
                            0030: 20 20 20 20 20 20 20 20  00 00 00 00 05 1e 00 1a           ........
                            0040: 00 1c 00 00 30 33 30 4b  4d 46 36 54 42 34 35 32  ....030K MF6TB452
                            0050: 34 38 32 30 31 31 30 34  31 34 30 33 58 80 03 2b  48201104 1403X..+
                            0060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ........ ........
                            *                                                                        
                            0080: 00 ef 00 80 00 ef 00 80  02 f2 02 6b 02 d0 02 8d  ........ ...k....
                            0090: 14 08 00 cd 14 08 00 cd  ff ff 00 00 ff ff 00 00  ........ ........
                            00a0: 01 f6 00 0b 01 f6 00 0b  00 00 00 00 00 00 00 00  ........ ........
                            00b0: 00 00 00 00 00 00 00 00  32 01 14 f5 b6 f4 79 6d  ........ 2.....ym
                            00c0: 3b 7c 3a cf 3f bb 3a 59  bf 32 73 91 09 c0 00 00  ;|:.?.:Y .2s.....
                            00d0: 01 00 00 00 dc b7 91 35  30 a6 fe 5a 00 00 00 d1  .......5 0..Z....
                            00e0: 00 ac 02 b4 00 1b 45 76  00 00 00 00 00 00 00 00  ......Ev ........
                            00f0: 04 40 00 00 04 40 00 00  00 00 00 00 00 00 00 00  .@...@.. ........
```
