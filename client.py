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
	cmnd = input("Exit | Send File | Transfer File:\n")
	if (cmnd == 'Exit'):
		print('Exiting Client Application')
		sys.exit()
	elif (cmnd == 'Send File'):
		s.send(bytes('Receiving File'))
		# filename = input('Provide File Name: ')
		# file = open(filename, 'rb')
		# print('Filename has been sent to the server.')
		# s.send(file)
		# file_data = bytes(file.readline(string, 'utf-8'))
		# while (file_data):
			# s.send(file_data)
			# print('Sent ',repr(file_data))
			# file_data = bytes(file.readline(string, 'utf-8'))
		# file.close()
		print('The file has finished sending')
	elif (cmnd == 'Access File'):
		filename = input('Provide File Name: ')
		s.send(bytes(filename))
		print('The filename has been sent')
    #s.sendall(b'Hello, world')	#send message, exchange with code to obtain file
	#client ui should loop here and access files
    #data = s.recv(1024)	#read server reply
s.close()
print('Client should be closed now.')

#print('Received', repr(data))	#print server reply
