import codecs
import struct
from math import ceil
from dataclasses import dataclass, field

@dataclass(slots=True)
class AvlData:
	utcTimeMs: str=""
	utcTime: str=""
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
	bytes: list=field(default_factory=list)
	imei: str = ""
	codecID: str = ""
	noOfData: str = ""
	avlDataPacketFailed: str = ""
	avlDataPackets: list=field(default_factory=list)
	response: str = ""

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
		imeiLenght = toInt(self.bytes[:2])
		self.imei = codecs.decode(''.join(self.bytes[2:][:imeiLenght]),'hex').decode('ascii')
		#added imeiLenght and zero bytes
		nextByte = 10 + imeiLenght

		##############

		self.codecID = self.bytes[nextByte:][:1][0]
		nextByte += 1
		if self.codecID != '08':
			self.error = "This is not codec 8"
			return

		###########

		self.noOfData = toInt(self.bytes[nextByte:][:1])
		nextByte += 1

		#########
		for x in range(self.noOfData):
			avlData = AvlData()

			############################
			utcTimeMs = toInt(self.bytes[nextByte:][:8])
			avlData.utcTime = str(utcTimeMs / 1000)
			avlData.utcTimeMs = str(utcTimeMs)
			nextByte += 8
			########################
			avlData.priority = str(toInt(self.bytes[nextByte:][:1]))
			nextByte += 1
			#############################
			avlData.lat = str(int(''.join(self.bytes[nextByte:][:4]), base=16))
			nextByte += 4
			#############################
			avlData.lng = str(int(''.join(self.bytes[nextByte:][:4]), base=16))
			nextByte += 4
			#############################
			avlData.altitude = str(toInt(self.bytes[nextByte:][:2]))
			nextByte += 2
			#############################
			avlData.angle = str(toInt(self.bytes[nextByte:][:2]))
			nextByte += 2
			#############################
			avlData.visSat = str(toInt(self.bytes[nextByte:][:1]))
			nextByte += 1
			#############################
			avlData.speed = str(toInt(self.bytes[nextByte:][:2]))
			nextByte += 2
			#############################
			avlData.eventID = str(self.bytes[nextByte:][:1])
			nextByte += 1
			#############################
			avlData.nTotal = str(toInt(self.bytes[nextByte:][:1]))
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
		endOfData = self.bytes[nextByte:][:1]
		nextByte += 1
		crc16 = self.bytes[nextByte:][:4]

	def getJson(self):
		first = True

		json = '{'
		json += f'"imei": "{self.imei}",'
		json += f'"dataCount": "{str(self.noOfData)}",'
		json += '"data":['
		for avl in self.avlDataPackets:
			if first:
				first = False
			else:
				json += ','
			json += '{'
			json += f'"ts": "{avl.utcTimeMs}",'
			json += f'"lat": "{avl.lat}",'
			json += f'"lng": "{avl.lng}",'
			json += f'"sp": "{avl.speed}",'
			json += f'"ang": "{avl.angle}",'
			json += f'"sat": "{avl.visSat}",'
			json += f'"alt": "{avl.visSat}",'
			json += '"elements": ['
			first = True
			for element in avl.elements:
				if first:
					first = False
				else:
					json += ','
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