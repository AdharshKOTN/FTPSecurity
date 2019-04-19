#!/usr/bin/env python
import socket

HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	#bind the address and port
	s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code: ' + str(msg[0]) + ' Message ' +msg[1])

print('Awaiting connection....')
s.listen(1) #enables server to be available connection
#print('Socket is listening')

while 1:
	connection, addr = s.accept() #waits for connection from client
	#returns socket object for connection and client address
	print('connected by', addr)
	while 1:
		print('Waiting for Client Command')
		client_response = connection.recv(1024).decode("utf-8")
		if(client_response):
			print('Client Command: ' + str(client_response))
			if(str(client_response) == 'EX000'):
				print('Client wants to exit the session')
				connection.close()
				print('Client ' + addr + 'has exited the session')
			elif (str(client_response) == 'SF001'):
				print('Client is sending a file')
				print('Recieving File...')
				while 1:
					file_data = connection.recv(1024).decode("utf-8")
					if(file_data):
						print(file_data)
					else:
						print('File has been fully transferred')
						break
			elif (str(client_response) == 'AF002'):
				print('Sending File...')
				file_name = connection.recv(1024).decode("utf-8")
				print('Server will send the file called: ' + file_name)
				file = open(filename, 'rb')
				print('File: ' + filename + ' has been opened on the server.')
				#s.send(file)
				file_data = file.readline()
				while (file_data):
					s.send(file_data.encode())
					print('Sent ',repr(file_data))
					file_data = file.readline()
				file.close()
				print('The file has finished sending')
		else:
			print('Error: No message sent or message is decoded improperly.')
			break