# Teltonika Codec 8 Decoder
A decoder for the Codec8 packets over TCP sendt from Teltonika devices.

Resource  
https://wiki.teltonika-gps.com/view/Codec#Codec_8  



#### Imei hex format
```
000F333536333037303432343431303133
```

#### Sample data used
This is taken from the 3'rd example
```
000000000000004308020000016B40D57B480100000000000000000000000000000001010101000000000000016B40D5C198010000000000000000000000000000000101010101000000020000252C
```

#### Example of return
```
{
	"state": {
		"reported": {
			"ts": "1683023546000",
			"latlng": "68.1555733,13.6199133",
			"alt": "38",
			"ang": "346",
			"sat": "8",
			"sp": "0",
			"Ignition": "1",
			"Movement": "0",
			"GSM Signal": "5",
			"Sleep Mode": "0",
			"GNSS Status": "1",
			"GNSS PDOP": "16",
			"GNSS HDOP": "13",
			"External Voltage": "19404",
			"Battery Voltage": "0",
			"Battery Current": "0",
			"Active GSM Operator": "178441",
			"Total Odometer": "12913760"
		}
	}
}
```

## Testing results

#### Data used
Taken from 1'st example
```
000000000000003608010000016B40D8EA30010000000000000000000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF
```

#### Result
100000 requests in 2.4455857276916504 sec  
40889.99983426809 requests pr sec  
i5-7600K CPU @ 3.80GHz