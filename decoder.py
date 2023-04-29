import codecs
import struct
from math import ceil

class AvlData:
	def __init__(self):
		self.utcTimeMs = 0
		self.utcTime = 0
		self.priority = 0
		self.lat = 0
		self.lng = 0
		self.altitude = 0
		self.angle = 0
		self.visSat = 0
		self.speed = 0
		self.eventID = 0
		self.nTotal = 0
		self.elements = [] 

class Element:
	def __init__(self):
		self.IOID = 0
		self.value = 0

class Decode:
	def __init__(self, data):
		# Store the data for later use
		self.data = data
		self.json = ""
		self.error = ""
		self.bytes = []

		# Contents of the data header
		self.imei = 0
		self.codecID = 0
		self.noOfData = 0
		self.avlDataPacketFailed = 0
		self.avlDataPackets = []
		self.response = []

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
			avlData.utcTimeMs = toInt(self.bytes[nextByte:][:8])
			avlData.utcTime = str(avlData.utcTimeMs / 1000)
			avlData.utcTimeMs = str(avlData.utcTimeMs)
			nextByte += 8
			########################
			avlData.priority = toInt(self.bytes[nextByte:][:1])
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
			avlData.eventID = self.bytes[nextByte:][:1]
			nextByte += 1
			#############################
			avlData.nTotal = toInt(self.bytes[nextByte:][:1])
			nextByte += 1

			for x in range(1,5):
				ioSize = toInt(self.bytes[nextByte:][:1])
				nextByte += 1
				if x == 1: valueSize = 1
				if x != 1: valueSize = pow(2, (x-1))

				for io in range(1,ioSize+1):
					element = Element()
					###
					element.IOID = toInt(self.bytes[nextByte:][:1])
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
		json += '"imei": "'+self.imei+'",'
		json += '"dataCount": "'+str(self.noOfData)+'",'
		json += '"data":['
		for avl in self.avlDataPackets:
			if first:
				first = False
			else:
				json += ','
			json += '{'
			json += '"ts": "'+avl.utcTimeMs+'",'
			json += '"lat": "'+avl.lat+'",'
			json += '"lng": "'+avl.lng+'",'
			json += '"sp": "'+avl.speed+'",'
			json += '"ang": "'+avl.angle+'",'
			json += '"sat": "'+avl.visSat+'",'
			json += '"alt": "'+avl.visSat+'",'
			json += '"elements": ['
			first = True
			for element in avl.elements:
				if first:
					first = False
				else:
					json += ','
				json += '{'
				json += '"id": "'+str(element.IOID)+'",'
				json += '"value": "'+str(element.value)+'"'
				json += '}'
			json += ']'
			json += '}'
		json = json+']}'
		return json

def toInt(data):
	return int(''.join(map(str, data)), 32)

def toStr(data):
	return str(''.join(map(str, data)))