from decoder import Decode
import time

imei = "000F333536333037303432343431303133"
data = "000000000000003608010000016B40D8EA3001289EBEA2512FA692000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF"
data = imei+data



starttime = time.time()

for x in range(1,1000001):
	decode = Decode(data)
	if not decode.error:
		stoptime = time.time()
		timeused = stoptime - starttime
		print(str(x)+': Done in '+ str(timeused)+' sec')

# 999999: Done in 277.8946976661682
# 3598,468808255115 pr sec
# i5-7600K CPU @ 3.80GHz  