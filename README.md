# Teltonika Codec 8 Decoder
A decoder for the Codec8 packets over TCP sendt from Teltonika devices.

#### Imei hex format
```
000F333536333037303432343431303133
```

#### Sample data used
```
000000000000003608010000016B40D8EA3001289EBEA2512FA692000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF
```

## Testing results

#### Only decoding
100000 requests in 3.1094069480895996 sec  
32160.473578873098 requests pr sec  
i5-7600K CPU @ 3.80GHz  

#### With generating json
100000 requests in 3.410489559173584 sec  
29321.30366182138 requests pr sec  
i5-7600K CPU @ 3.80GHz  

