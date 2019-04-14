#!/usr/bin/env python
import socket

HOST = '127.0.0.1'
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	#create socket object
    s.connect((HOST, PORT))	#connect to server
    print('Connecting to ' + HOST + ' on Port ' + PORT)
    #s.sendall(b'Hello, world')	#send message, exchange with code to obtain file
								#client ui should loop here and access files
    #data = s.recv(1024)	#read server reply
    s.close()
except:
    print('Connection error')

print('Client should be closed now.')

#print('Received', repr(data))	#print server reply
