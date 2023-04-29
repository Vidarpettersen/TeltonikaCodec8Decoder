from decoder import Decode

if __name__ == '__main__':
	imei = "000F333536333037303432343431303133"
	data = "000000000000003608010000016B40D8EA3001289EBEA2512FA692000000000000000105021503010101425E0F01F10000601A014E0000000000000000010000C7CF"
	data = imei + data

	try:
		decode = Decode(data)
		if not decode.error:
			print(decode.getJson())
	except:
		print("Something went wrong")