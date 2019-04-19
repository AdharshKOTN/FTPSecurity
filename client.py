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
	cmnd = input("Exit | Send File | Access File:\n")
	if (cmnd == 'Exit'):
		print('Exiting Client Application')
		client_repsonse = 'EX000'
		s.send(client_repsonse.encode())
		s.close()
		print('Client should be closed now.')
		sys.exit()
	elif (cmnd == 'Send File'):
		client_response = 'SF001'
		s.send(client_response.encode())
		filename = input('Provide File Name: ')
		file = open(filename, 'rb')
		print('Filename has been sent to the server.')
		#s.send(file)
		file_data = file.readline(string, 'utf-8')
		while (file_data):
			s.send(file_data.encode())
			print('Sent ',repr(file_data))
			file_data = bytes(file.readline(string, 'utf-8'))
		file.close()
		print('The file has finished sending')
	elif (cmnd == 'Access File'):
		access_file = 'AF002'
		s.send(access_file.encode())
		filename = input('Provide File Name: ')
		s.send(filename.encode())
		print('The filename has been sent')
		while 1:
			file_data = connection.recv(1024).decode("utf-8")
			if(file_data):
				print(file_data)
			else:
				print('File has been fully transferred')
				break
	else:
		print('Not a valid command')
    #s.sendall(b'Hello, world')	#send message, exchange with code to obtain file
	#client ui should loop here and access files
    #data = s.recv(1024)	#read server reply

#print('Received', repr(data))	#print server reply
