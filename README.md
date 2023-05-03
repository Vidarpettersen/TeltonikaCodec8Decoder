# Teltonika Codec 8 Decoder
A decoder for the Codec8 packets over TCP sendt from Teltonika devices.

***Resource***
https://wiki.teltonika-gps.com/view/Codec#Codec_8  

## How to use

1. Mount a new instance of the Decode class and pass in the sample data.
2. convert to json format with toJson() function
3. Se example for more info

```
decode = Decode(data)
if not decode.error:
	print(decode.toJson())
```

## Sample data

#### Imei hex format
```
000F333536333037303432343431303133
```
First 4 chars is hex and its the imei lenght, rest is bytes not hex.

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
			"239": "1",
			"240": "0",
			"21": "5",
			"200": "0",
			"69": "1",
			"181": "16",
			"182": "13",
			"66": "19404",
			"67": "0",
			"68": "0",
			"241": "178441",
			"16": "12913760"
		}
	}
}
```

#### What the numbers in the example represent

```
"239":	"Ignition"
"240": 	"Movement"
"21": 	"GSM Signal"
"200": 	"Sleep Mode"
"69": 	"GNSS Status"
"181": 	"GNSS PDOP"
"182": 	"GNSS HDOP"
"66": 	"External Voltage"
"67": 	"Battery Voltage"
"68": 	"Battery Current"
"241": 	"Active GSM Operator"
"16": 	"Total Odometer"
```

## Testing results

#### Data used
Taken from 1'st example
```
000000000000003608010000016B40D8EA30010000000000000000000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF
```

#### Result
100000 requests in 2.139843225479126 sec  
46732.39553687831 requests pr sec  
i5-7600K CPU @ 3.80GHz
