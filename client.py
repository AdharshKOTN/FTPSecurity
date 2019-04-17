#!/usr/bin/env python
import socket
import sys

HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	#create socket object
    s.connect((HOST, PORT))	#connect to server
except:
	print('Connection error, check the host or port number')
	sys.exit()
	
print('Connecting to ' + str(HOST) + ' on Port ' + str(PORT))
while 1:
	cmnd = input("Exit | Send File| Transfer File:")
	if cmnd == 'Exit':
		print('Exiting Client Application')
		sys.exit()
	elif cmnd == 'Send File':
		print('Provide File Name')
	elif cmnd == 'Transfer File':
		print('Provide File Name')
    #s.sendall(b'Hello, world')	#send message, exchange with code to obtain file
	#client ui should loop here and access files
    #data = s.recv(1024)	#read server reply
s.close()
print('Client should be closed now.')

#print('Received', repr(data))	#print server reply
