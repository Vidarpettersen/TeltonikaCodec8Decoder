from decoder import Decode
import time

imei = "000F333536333037303432343431303133"
data = "000000000000003608010000016B40D8EA30010000000000000000000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF"
data = imei+data


numberOfTimes = 100000
startNumber = 1
endNumber = startNumber + numberOfTimes
startTime = time.time()
lastStopTime = time.time()

for x in range(startNumber,endNumber):
	decode = Decode(data)
	if not decode.error:
		json = decode.toApi()
		lastStopTime = time.time()
		del decode

timePassed = lastStopTime - startTime
requestsPrSec = numberOfTimes / timePassed
print(f"{numberOfTimes} requests in {timePassed} sec")
print(f"{requestsPrSec} requests pr sec")

# 100000 requests in 3.2860710620880127 sec
# 30431.478233601767 requests pr sec
# i5-7600K CPU @ 3.80GHz  