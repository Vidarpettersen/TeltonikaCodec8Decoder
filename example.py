from decoder import Decode

if __name__ == '__main__':
	imei = "000F333536333037303432343431303133"
	data = "000000000000004308020000016B40D57B480100000000000000000000000000000001010101000000000000016B40D5C198010000000000000000000000000000000101010101000000020000252C"
	data = imei + data

	try:
		decode = Decode(data)
		if not decode.error:
			print(decode.getJson())
	except:
		print("Something went wrong")
