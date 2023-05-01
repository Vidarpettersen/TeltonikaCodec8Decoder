import codecs
import struct
from dataclasses import dataclass, field

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
	bytes: list = field(default_factory=list)
	imei: str = ""
	codecID: str = ""
	noOfData: str = ""
	avlDataPacketFailed: str = ""
	avlDataPackets: list=field(default_factory=list)
	response: str = hex(0)

	def __post_init__(self):

		# Create byte array from hex string
		self.getBytes()

		# Start the decode prossess
		try:
			self.decode()
		except:
			return self.error

	def getBytes(self):
		self.bytes = [self.data[i:i+2] for i in range(0,len(self.data), 2)]

	def decode(self):
		# Get the imei length
		imeiLenght = toInt(self.bytes[:2])

		# Check if the imei is 15 long
		if imeiLenght == 15:
			self.imei = codecs.decode(''.join(self.bytes[2:][:imeiLenght]),'hex').decode('ascii')
			imeiLenght += 2

		zerobytes = 4 			# Lenght of the zero bytes at the start
		dataFieldLength = 4		# Dont care about the data field lenght

		# Adding the start byte lenght to start at the top of the packet
		nextByte = imeiLenght + zerobytes + dataFieldLength

		############## 

		self.codecID = self.bytes[nextByte:][:1][0]
		nextByte += 1
		if self.codecID != '08':
			self.error = "This is not codec 8"
			return

		###########

		self.noOfData = toInt(self.bytes[nextByte:][:1])
		nextByte += 1

		if self.noOfData == 0:
			self.error = "This sending has no packets"
			return

		#########
		for x in range(self.noOfData):
			avlData = AvlData()

			############################
			avlData.utcTimeMs = toInt(self.bytes[nextByte:][:8])
			nextByte += 8
			########################
			avlData.priority = toInt(self.bytes[nextByte:][:1])
			nextByte += 1
			#############################
			avlData.lat = hex_to_float(''.join(self.bytes[nextByte:][:4]))
			nextByte += 4
			#############################
			avlData.lng = hex_to_float(''.join(self.bytes[nextByte:][:4]))
			nextByte += 4
			#############################
			avlData.altitude = toInt(self.bytes[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.angle = toInt(self.bytes[nextByte:][:2])
			nextByte += 2
			if(avlData.angle > 360):
				self.error = "Angle can't be over 360"
				return
			#############################
			avlData.visSat = toInt(self.bytes[nextByte:][:1])
			nextByte += 1
			#############################
			avlData.speed = toInt(self.bytes[nextByte:][:2])
			nextByte += 2
			#############################
			avlData.eventID = self.bytes[nextByte:][:1][0]
			nextByte += 1
			#############################
			avlData.nTotal = self.bytes[nextByte:][:1][0]
			nextByte += 1

			for x in range(1,5):
				ioSize = toInt(self.bytes[nextByte:][:1])
				nextByte += 1
				if x == 1: valueSize = 1
				if x != 1: valueSize = pow(2, (x-1))

				for io in range(1,ioSize+1):
					element = Element()
					###
					element.ioid = toInt(self.bytes[nextByte:][:1])
					nextByte += 1
					###
					element.value = toInt(self.bytes[nextByte:][:valueSize])
					nextByte += valueSize

					# Add element to avl data
					avlData.elements.append(element)
			#save the data
			self.avlDataPackets.append(avlData)
		endOfData = toInt(self.bytes[nextByte:][:1])
		nextByte += 1
		if endOfData != self.noOfData:
			self.error = "The end of data count is different"
			return
		crc16 = self.bytes[nextByte:][:4]
		self.response = hex(self.noOfData)

	def getJson(self):
		first = True

		json = '{'
		json += f'"imei": "{self.imei}",'
		json += f'"dataCount": "{str(self.noOfData)}",'
		json += '"data":['
		for avl in self.avlDataPackets:
			if not first:
				json += ','
			else:
				first = False
				
			json += '{'
			json += f'"ts": "{avl.utcTimeMs}",'
			json += f'"lat": "{avl.lat}",'
			json += f'"lng": "{avl.lng}",'
			json += f'"alt": "{avl.altitude}",'
			json += f'"ang": "{avl.angle}",'
			json += f'"sat": "{avl.visSat}",'
			json += f'"sp": "{avl.speed}",'
			json += '"elements": ['
			first = True
			for element in avl.elements:
				if not first:
					json += ','
				else:
					first = False
				json += '{'
				json += f'"id": "{element.ioid}",'
				json += f'"value": "{element.value}"'
				json += '}'
			json += ']'
			json += '}'
		json = json+']}'
		return json

def toInt(data):
	return int(''.join(data), 16)

def hex_to_float(h):
    return struct.unpack('<f', struct.pack('<I', int(h, 16)))[0]
