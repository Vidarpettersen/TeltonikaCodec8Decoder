from dataclasses import dataclass, field
from lib.FMB import FMB
from lib.converter import convert

@dataclass(slots=True)
class AvlData:
	utcTimeMs: str=""
	lat: str=""
	lng: str=""
	altitude: str=""
	angle: str=""
	visSat: str=""
	speed: str=""
	elements: list=field(default_factory=list)

@dataclass(slots=True)
class Element:
	ioid: str=""
	value: str=""

@dataclass(slots=True)
class Decoder:
	json: str = ""
	error: str = ""
	imei: str = ""
	codecID: str = ""
	noOfData: str = ""
	avlDataPacketFailed: str = ""
	avlDataPackets: list=field(default_factory=list)
	response: str = hex(0)

	def decode(self, data):
		data = data.upper()
		# Get the imei length
		imeiLenght = toInt(data[:4])
		# Check if the imei is 15 long
		if imeiLenght == 15 or imeiLenght == 16:
			self.imei = bytes.fromhex(data[4:][:(imeiLenght*2)]).decode('utf-8')
			imeiLenght = imeiLenght*2+4
		zerodata = 8			# Lenght of the zero data at the start
		dataFieldLength = 8		# Dont care about the data field lenght

		# Adding the start byte lenght to start at the top of the packet
		nextByte = imeiLenght + zerodata + dataFieldLength

		############## 
		self.codecID = data[nextByte:][:2]
		nextByte += 2
		if self.codecID != '08' and self.codecID != '8E':
			self.error = "This is not codec 8 or 8 extended"
			return

		###########

		self.noOfData = toInt(data[nextByte:][:2])
		nextByte += 2

		if self.noOfData == 0:
			self.error = "This sending has no packets"
			return

		#########
		for x in range(self.noOfData):
			avlData = AvlData()

			############################
			avlData.utcTimeMs = toInt(data[nextByte:][:16])
			nextByte += 16
			########################
			# priority = toInt(data[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.lng = hex_to_float(''.join(data[nextByte:][:8]))
			nextByte += 8
			#############################
			avlData.lat = hex_to_float(''.join(data[nextByte:][:8]))
			nextByte += 8
			#############################
			avlData.altitude = toInt(data[nextByte:][:4])
			nextByte += 4
			#############################
			avlData.angle = toInt(data[nextByte:][:4])
			nextByte += 4
			if(avlData.angle > 360):
				self.error = "Angle can't be over 360"
				return
			
			#############################
			avlData.visSat = toInt(data[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.speed = toInt(data[nextByte:][:4])
			nextByte += 4

			if self.codecID == '08':
				#############################
				# eventID = data[nextByte:][:2]
				nextByte += 2
				#############################
				# nTotal = data[nextByte:][:2]
				nextByte += 2

				for x in range(1,5):
					ioSize = toInt(data[nextByte:][:2])
					nextByte += 2
					if x == 1: valueSize = 1
					if x != 1: valueSize = pow(2, (x-1))

					for io in range(1,ioSize+1):
						element = Element()
						###
						element.ioid = toInt(data[nextByte:][:2])
						nextByte += 2
						###
						element.value = data[nextByte:][:valueSize*2]
						nextByte += valueSize*2

						# Add element to avl data
						avlData.elements.append(element)
			else:
				#############################
				# eventID = data[nextByte:][:2]
				nextByte += 4
				#############################
				# nTotal = data[nextByte:][:2]
				nextByte += 4

				for x in range(1,5):
					ioSize = toInt(data[nextByte:][:4])
					nextByte += 4
					if x == 1: valueSize = 1
					if x != 1: valueSize = pow(2, (x-1))

					for io in range(1,ioSize+1):
						element = Element()
						###
						element.ioid = toInt(data[nextByte:][:4])
						nextByte += 4
						###
						element.value = data[nextByte:][:valueSize*2]
						nextByte += valueSize*2
						# Add element to avl data
						avlData.elements.append(element)

				nxOfXbyte = toInt(data[nextByte:][:4])
				nextByte += 4
				for x in range(nxOfXbyte):
					element = Element()
					element.ioid = toInt(data[nextByte:][:4])
					nextByte += 4
					nthLenght = toInt(data[nextByte:][:4])
					nextByte += 4
					element.value = data[nextByte:][:nthLenght*2]
					nextByte += nthLenght*2
					avlData.elements.append(element)
			#save the data
			self.avlDataPackets.append(avlData)
		endOfData = toInt(data[nextByte:][:2])
		nextByte += 2
		if endOfData != self.noOfData:
			self.error = "The end of data count is different"
			return
		# crc16 = data[nextByte:][:8]
		self.response = hex(self.noOfData)
	
	def toJson(self):
		jsonArray = []
		for avl in self.avlDataPackets:
			json = '{"state":{"reported":{'
			json += f'"ts":"{avl.utcTimeMs}",'
			json += f'"latlng":"{avl.lat},{avl.lng}",'
			json += f'"alt":"{avl.altitude}",'
			json += f'"ang":"{avl.angle}",'
			json += f'"sat":"{avl.visSat}",'
			json += f'"sp":"{avl.speed}",'
			first = True
			for element in avl.elements:
				if first:
					first = False
				else: 
					json += ','
				try:
					io = element.ioid
					conversion = FMB[str(element.ioid)]['FinalConversion']
					value = str(convert(element.value, conversion))
				except:
					io = element.ioid
					value = element.value

				json += f'"{io}":"{value}"'
				#print(FMB[str(element.ioid)]['PropertyName'])
			json += '}}}'
			jsonArray.append(json)
		return jsonArray


def toInt(data):
	return int(data, 16)

def hex_to_float(h):
    return int(h, 16)/10000000
