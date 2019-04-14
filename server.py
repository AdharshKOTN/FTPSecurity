#!/usr/bin/env python
import socket

HOST = '127.0.0.1'
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code: ' + str(msg[0]) + ' Message ' +msg[1])

print('Awaiting connection....')
s.listen(1) #enables server to be available connection
print('Socket is listening')

while 1:
    conn, addr = s.accept() #waits for connection from client
							#returns socket object for connection and client address
    print('connected by', addr)

s.close()
