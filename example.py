from decoder import Decoder
from lib.FMB import FMB
from lib.converter import convert

if __name__ == '__main__':
	imei = "000F333536333037303432343431303133"
	data = "000f3335303631323037343832333139340000000000000044080100000187dc05469000081e3bdd289fb7150026015a080000000c05ef01f0001505c800450105b50010b6000d424bcc43000044000002f100005e8910000ca330000100001ea9"
	#data = imei + data

	try:
		decoder = Decoder()
		decoder.decode(data)
		if not decoder.error:
			print(decoder.toJson())
			print(decoder.response)
		else: print(decoder.error)
	except:
		print("Something went wrong")

# 081e3bdd
# 289fb715