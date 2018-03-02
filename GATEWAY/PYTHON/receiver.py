#! /usr/bin/python
#coding: utf-8

#FIXME: Cambiar los nombres: 
#-Receptor -> EPController
#-Gateway_vx -> Receiver
#-Endpoint -> EPVirtual

#import modules
import serial
from xbee import DigiMesh
import time
import threading
from Queue import Queue
import os.path
import socket
import signal
import os
import sys

#Open serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)
#Open socket
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#Objeto para manejar xbee
global xbee

#---VARIABLES---
xbee_wake = False
myAddress = ''#b'\xFF\xFF' #Broadcast por defecto
broadcastAddress = b'\x00\x00\x00\x00\x00\x00\xFF\xFF'
sendLock = threading.Lock()
sendQueue = Queue() #Cola de envio para el protocolo de descubrimiento
sendSynchronyzedQueue = Queue() #Cola de envio sincronizada con modo sleep
global sh
global sl

#---CONSTANTES---
#-Maximos-
MAX_LISTEN_SOCKET = 5
MAX_LENGTH_RCV = 1024
#-Protocolo de descubrimiento:
DISCOVERY = b'\x01'
ASSIGN = b'\x02'
CONFIRM = b'\x03'
ACCEPT = b'\x04'
#-Códigos ACCEPT
ACCEPT_OK = b'\x00'
ACCEPT_NOTOK = b'\x01'
#-Envío de datos:
DATA = b'\x11'
NEW_SP = b'\x12'
RESET = b'\x13'
START_GW = b'\x14'
#-Protocolo EPVirtual-Gateway
EPDATA = b'\x00'
EPCREATE = b'\x01'
EPEXISTS = b'\x02'
#-Códigos EPCREATE
EPCREATE_OK = b'\x00'
EPCREATE_ERR = b'\x01'
#-Códigos EPEXISTS
EPEXISTS_OK = b'\x00'
EPEXISTS_ERR = b'\x01'

DIR = './tmp/'
SERVSOCKET = DIR + 'receiver'
SENDSOCKET = DIR + 'sender'

#==========================================================================================
class sendData(threading.Thread):
	def __init__(self, data):
		threading.Thread.__init__(self)
		self.data = data
		self.start()

	def run(self):
		
		global myAddress
		
		#Separar la trama obtenida
		frameId = self.data[0] #Para esta implementación siempre será NEW_SP
		address = self.data[1:9]
		frameLength = int(self.data[9].encode('hex'), base=16)
		frameLengthByte = self.data[9]
		data = self.data[10:10+frameLength] if frameLength > 0 else None #en este caso siempre sera SamplePeriod
		
		#Armar la respuesta
		response = NEW_SP + myAddress + frameLengthByte + data
		
		#Enviar los datos a las xbee correspondiente
		sendQueue.put( (1, xbee.send, 'tx', {'frame_id':b'\x01', 'dest_addr':address, 'data':response}) )

#==========================================================================================
class dataSender(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.start()

	def run(self):

		global xbee_wake
		
		while True:
			if xbee_wake:
				items = sendQueue.get()
				function = items[1]
				command = items[2]
				kwargs = items[3]
				function(command, **kwargs)
				print '---SEND SYNCHRONYZED DATA----'
				print 'Command: ' + command
				print 'Data: ' + str(kwargs)
				print '-FIN SEND SYNCHRONYZED DATA--'
				sendQueue.task_done()

#==========================================================================================
class processAtCommand(threading.Thread):
	def __init__(self, at_response):
		threading.Thread.__init__(self)
		self.at_response = at_response
		self.start()

	def run(self):

		global myAddress
		global sh
		global sl

		status = self.at_response['status']
		command = self.at_response['command']
		parameter = self.at_response['parameter']
		print '----------AT_RESPONSE----------'

		if status == b'\x00': #OK
			print 'Status: OK'
			if command == 'SH':
				sh = 1
				myAddress = parameter
		 	elif command == 'SL':
		 		sl = 1
				myAddress += parameter
		else: #0x01 - ERROR, 0x02 - Invalid command, 0x03 Invalid parameter, 0x04 Tx failure
			print 'Status: ' + status.encode('hex') + '-ERROR'

		print 'Command: ' + command
		print 'Parameter: ' + parameter.encode('hex')
		print '--------FIN AT_RESPONSE--------'

#==========================================================================================
class processPacket(threading.Thread):
	#constructor
	def __init__(self, packet):
		threading.Thread.__init__(self) #or super(processPacket, self).__init__()
		self.packet = packet
		self.start()

	#RUN when START method is invoked
	def run(self):
		print '-----------RX_PACKET-----------'

		veces = 2
		#Obtener encabezados y datos del paquete
		packetId = self.packet[0]
		packetMAC = self.packet[1:9]
		packetLength = int(self.packet[9].encode('hex'), base=16)
		packetLengthByte = self.packet[9]
		packetData = None if packetLength == 0 else self.packet[10:10+packetLength]
		#Datos de la respuesta
		response = None
		address = packetMAC

		if packetId == DISCOVERY:
			print 'Tipo: DISCOVERY'
			print 'MAC: ' + packetMAC.encode('hex')
			print 'Largo: ' + str(packetLength)
			#Respuesta [ID + MAC(gateway) + LARGO]
			response = ASSIGN + myAddress + b'\x00'

		elif packetId == CONFIRM:
			print 'Tipo: CONFIRM'
			print 'MAC: ' + packetMAC.encode('hex')
			print 'Largo: ' + str(packetLength)
			response = ACCEPT + myAddress + b'\x01'
			#Creacion del EP virtual
			#FIXME: Está bien controlar por el archivo, o llevar registro en el EPCONTROLLER?
			if os.path.exists(DIR + str(packetMAC.encode('hex'))):
				print 'EP Virtual: ya existe'		
				response += ACCEPT_OK + b'\x00' + b'\x00' + b'\x00' + b'\x0A' #TODO: Recibirlo desde EPV
			else:
				print 'EP Virtual: se debe crear'
				#Conexión con el proceso RECEPTOR, envía MAC
				s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
				s.connect(SERVSOCKET)
				time.sleep(1) #Esperar por creación de EPVIRTUAL
				epResponse = s.recv(1024)
				print '[DEBUG] Antes del if, llega respuesta: ' + str(epResponse.encode('hex'))
				if epResponse[0] == EPCREATE and epResponse[1] == EPCREATE_OK:
					print '[DEBUG] Entró al if'
					s.sendall(str(packetMAC.encode('hex'))) #TODO: Pasar configuración inicial de sensores
					epResponse = s.recv(1024)
					s.close()
					if epResponse[0] == EPEXISTS and epResponse[1] == EPEXISTS_OK:
						print 'EP creado: OK'
						response = response + ACCEPT_OK + b'\x00' + b'\x00' + b'\x00' + b'\x0A'			
					elif epResponse[0] == EPEXISTS and epResponse[1] == EPEXISTS_ERR:
						print 'EP creado: Problemas con el socket'
						response += ACCEPT_NOTOK #No se pudo crear el socket del EP
					else:
						print 'EP creado: error'
						response += ACCEPT_NOTOK #Error no reconocido
				else:
					print 'EP creado: No se pudo crear'
					response += ACCEPT_NOTOK #No se pudo crear el proceso del EP	

		elif packetId == DATA:
			print 'Tipo: DATA'
			print 'Address: ' + str(packetMAC.encode('hex'))
			print 'Largo: ' + str(packetLength)
			print 'Datos: ' + ( '--' if packetLength == 0 else str(packetData.encode('hex')) )

			SOCKET = DIR + str(packetMAC.encode('hex'))

			if os.path.exists(SOCKET):
				s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
				s.connect(SOCKET)

				s.sendall(EPDATA)
				s.sendall(packetLengthByte)
				s.sendall(packetData)

				s.close()
			else:
				#Solicitar reinicio de EP para reiniciar protocolo de descubrimiento
				print 'Los datos recibidos no pudieron ser enviados al EPV'
				response = RESET
		else:
			print'Tipo: Desconocido'

		if response is not None:
			print 'Respuesta: si'
			sendQueue.put( (2, xbee.send, 'tx', {'frame_id':b'\x01', 'dest_addr':address, 'data':response}) )
		else:
			print 'Respuesta: no'
		print '---------FIN RX_PACKET---------'

#==========================================================================================
def showStatus(data):
		print '-----------TX_STATUS-----------'
		estado = 'OTHER/ERROR'
		if data['deliver_status'] == b'\x00':
			estado = 'SUCCESS'
		print 'Status: ' + estado
		print '---------FIN TX_STATUS---------'

#==========================================================================================
#THREAD waiting for DigiMesh packets.
def receiveData(data):

	global xbee_wake

	#Start new threads according to DigiMesh packets.
	if data['id'] == 'rx':
		#Execute new 'processPacket' thread for each RX_PACKET
		processPacket(data['data'])

	elif data['id'] == 'status':
		#Obtain sleep status (OB - Woke up / 0C - Went to sleep)
		print '--------SLEEP_STATUS-----------'
		if data['status'] == b'\x0B':
			xbee_wake = True
			print 'Status: Xbee network woke up'
		else:
			xbee_wake = False
			print 'Status: Xbee network went to sleep'
		print '-----FIN SLEEP_STATUS----------'

	elif data['id'] == 'tx_status':
		#Show TX_STATUS for each packet sent
		showStatus(data)

	elif data['id'] == 'at_response':
		#Execute new 'processAtCommand' thread for each AT_RESPONSE
		processAtCommand(data)
	else:
		print '---------NOT SUPPORTED---------'
		print ('Type: ' + data['id'])
		print '--------------FIN--------------'

#==========================================================================================
#Manejar las interrupciones
def sign_hand(signum, frame):
	print 'Señal captada: ', signum
	global ser
	global s
	global xbee

	xbee.halt()
	ser.close()
	s.close()

	sys.exit(0)

#==========================================================================================
#Crear el objeto API, en este caso utilizamos DigiMesh
xbee = DigiMesh(ser, callback=receiveData)

print 'Comenzar programa...'

#Manejar interrupciones
signal.signal(signal.SIGTERM, sign_hand)
signal.signal(signal.SIGINT, sign_hand)

#Iniciar proceso de envíos
dataSender()

sh = 0
sl = 0
#Conocer parámetros propios
while sh < 1:
	xbee.send('at', frame_id= 'A', command='SH')
	print('mandar sh')
	time.sleep(1)

while sl < 1:
	xbee.send('at', frame_id= 'B', command='SL')
	print('mandar sl')
	time.sleep(1)

#xbee.send('at', frame_id= b'\x01', command='SH')
#xbee.send('at', frame_id= b'\x01', command='SL')

#Resetear todos los EP para que reinicien el protocolo de descubrimiento en caso de estar funcionando
sendQueue.put( (1, xbee.send, 'tx', {'frame_id':b'\x01', 'dest_addr':broadcastAddress, 'data':START_GW}) )


#recibir tramas
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.bind(SENDSOCKET)
s.listen(MAX_LISTEN_SOCKET)
while True:
	try:
		print 'hi!'
		conn, addr = s.accept()
		#Recibir trama desde EPV_i para entregar a EP_i
		data = conn.recv(MAX_LENGTH_RCV)
		sendData(data)
		conn.close()
	except KeyboardInterrupt:
		break

s.close()
sendQueue.join()
sendSynchronyzedQueue.join()
xbee.halt()
ser.close()

print 'Finalizar programa...'
    
