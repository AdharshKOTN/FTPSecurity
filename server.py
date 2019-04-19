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
print('Socket is listening')

while 1:
	connection, addr = s.accept() #waits for connection from client
	#returns socket object for connection and client address
	print('connected by', addr)
	client_response = connection.recv(1024).decode
	if(client_response):
		print('Client Response: ' + str(client_response))
	else:
		print('Client response has finished reveiving')
	# file = open('recieved_file', 'wb')
	# print ('file opened')
	# while 1:
		# print('receiving data...')
		# data = s.recv(1024)
		# print('data=%s', (data))
		# if not data:
			# break
			# write data to a file
		# file.write(data)
	# file.close()
connection.close()
