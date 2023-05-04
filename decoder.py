from dataclasses import dataclass, field
from lib.FMB import FMB
from lib.converter import convert

@dataclass(slots=True)
class AvlData:
	utcTimeMs: str=""
	priority: str=""
	lat: str=""
	lng: str=""
	altitude: str=""
	angle: str=""
	visSat: str=""
	speed: str=""
	eventID: str=""
	nTotal: str=""
	elements: list=field(default_factory=list)

@dataclass(slots=True)
class Element:
	ioid: str=""
	value: str=""

@dataclass(slots=True)
class Decode:
	data: str
	json: str = ""
	error: str = ""
	imei: str = ""
	codecID: str = ""
	noOfData: str = ""
	avlDataPacketFailed: str = ""
	avlDataPackets: list=field(default_factory=list)
	response: str = hex(0)

	def __post_init__(self):
		# Start the decode prossess
		self.decode()


	def decode(self):
		# Get the imei length
		imeiLenght = toInt(self.data[:4])
		# Check if the imei is 15 long
		if imeiLenght == 15 or imeiLenght == 16:
			self.imei = bytes.fromhex(self.data[4:][:(imeiLenght*2)]).decode('utf-8')
			imeiLenght = imeiLenght*2+4
		zerodata = 8			# Lenght of the zero data at the start
		dataFieldLength = 8		# Dont care about the data field lenght

		# Adding the start byte lenght to start at the top of the packet
		nextByte = imeiLenght + zerodata + dataFieldLength

		############## 
		self.codecID = self.data[nextByte:][:2]
		nextByte += 2
		if self.codecID != '08':
			self.error = "This is not codec 8"
			return

		###########

		self.noOfData = toInt(self.data[nextByte:][:2])
		nextByte += 2

		if self.noOfData == 0:
			self.error = "This sending has no packets"
			return

		#########
		for x in range(self.noOfData):
			avlData = AvlData()

			############################
			avlData.utcTimeMs = toInt(self.data[nextByte:][:16])
			nextByte += 16
			########################
			avlData.priority = toInt(self.data[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.lng = hex_to_float(''.join(self.data[nextByte:][:8]))
			nextByte += 8
			#############################
			avlData.lat = hex_to_float(''.join(self.data[nextByte:][:8]))
			nextByte += 8
			#############################
			avlData.altitude = toInt(self.data[nextByte:][:4])
			nextByte += 4
			#############################
			avlData.angle = toInt(self.data[nextByte:][:4])
			nextByte += 4
			if(avlData.angle > 360):
				self.error = "Angle can't be over 360"
				return
			#############################
			avlData.visSat = toInt(self.data[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.speed = toInt(self.data[nextByte:][:4])
			nextByte += 4
			#############################
			avlData.eventID = self.data[nextByte:][:2]
			nextByte += 2
			#############################
			avlData.nTotal = self.data[nextByte:][:2]
			nextByte += 2

			for x in range(1,5):
				ioSize = toInt(self.data[nextByte:][:2])
				nextByte += 2
				if x == 1: valueSize = 1
				if x != 1: valueSize = pow(2, (x-1))

				for io in range(1,ioSize+1):
					element = Element()
					###
					element.ioid = toInt(str(self.data[nextByte:][:2]))
					nextByte += 2
					###
					element.value = self.data[nextByte:][:valueSize*2]
					nextByte += valueSize*2

					# Add element to avl data
					avlData.elements.append(element)
			#save the data
			self.avlDataPackets.append(avlData)
		endOfData = toInt(self.data[nextByte:][:2])
		nextByte += 2
		if endOfData != self.noOfData:
			self.error = "The end of data count is different"
			return
		crc16 = self.data[nextByte:][:8]
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
				False if first else ','
				try:
					conversion = FMB[str(element.ioid)]['FinalConversion']
					value = str(convert(element.value, conversion))
				except:
					value = element.value

				json += f'"{element.ioid}":"{value}"'
				#print(FMB[str(element.ioid)]['PropertyName'])
			json += '}}}'
			jsonArray.append(json)
		return jsonArray


def toInt(data):
	return int(data, 16)

def hex_to_float(h):
    return int(h, 16)/10000000
