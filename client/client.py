#!/usr/bin/env python
import socket
import sys
import getpass
from Crypto.Cipher import DES
from Crypto import Random

HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#_auth_count = 0

#def _setAuthCount(val):
#	_auth_count = val
#def _getAuthCount()
#	return _auth_count

try:
	#create socket object
	s.connect((HOST, PORT))	#connect to server
except:
	print('Connection error, check the host or port number')
	sys.exit()
	
print('Connecting to ' + str(HOST) + ' on Port ' + str(PORT))
#val = 3
#_setAuthCount(val)

username = input("Username: ")
password = getpass.getpass(prompt = 'Password: ')
userDetails = username + "," + password

#iv = Random.get_random_bytes(8)
#des1 = DES.new(userDetails, DES.MODE_CFB, iv)
#cyper_ud = des1.encrypt(userDetails)

#message = iv + "," + cypher_ud

#print(str(message))

while 1:
	#s.send(message.encode())
	s.send(userDetails.encode())
	print("User Details: " + str(userDetails) + " has been sent.")
	authentication_result = s.recv(1024).decode()
	if(authentication_result != "pass"):
		print('Authentication Failed...')
		#_setAuthCount(val - 1)
		username = input("Username: ")
		password = getpass.getpass(prompt = 'Password: ')
		userDetails = username + "," + password
	else:
		print('Welcome ' + str(username))
		break
	
while 1:
	cmnd = input("Exit | Send File | Access File:\n")
	cmnd = cmnd.lower()
	#print(cmnd)
	if (cmnd == 'exit'):
		print('Exiting Client Application')
		client_exit = 'CEX000'
		s.send(client_exit.encode())
		s.close()
		print('Good-Bye. Thanks for using AJ\'s FTP Client')
		sys.exit()
	elif (cmnd == 'send file'):
		client_send = 'CSF001'
		s.send(client_send.encode())
		while 1:
			filename = input('Provide File Name: ')
			try:
				file = open(filename, 'rb')
				break
			except:
				print('File does not exist.')
		#print('Filename has been sent to the server.')
		#s.send(file)
		file_data = file.readline()
		while (file_data):
			s.send(file_data)
			print('Sent ',repr(file_data))
			file_data = file.readline()
		eof = 'CEOF004'
		s.send(eof.encode())
		file.close()
		print('The file has finished sending')
	elif (cmnd == 'access file'):
		access_file = 'CAF002'
		s.send(access_file.encode())
		while 1:
			filename = input('Provide File Name: ')
			s.send(filename.encode())
			file_status = s.recv(1024).decode()
			if(file_status == 'File does not exist.'):
				print('File does not exist.')
			else:
				break
		print('The filename has been sent')
		file_data = s.recv(1024).decode()
		file = open(filename, "a")
		while 1:
			print('Recieved: ' + file_data)
			if (file_data == 'SEOF004'):
				#print('DEBUG: exit the inner loop')
				break
			else:
				file_data = s.recv(1024).decode()
				file.write(file_data)
	elif (cmnd == 'secret close'):
		secret = 'SECRCL005'
		s.send(secret.encode())
		print('Secret Command accepted. Server and Client Exiting.')
		sys.exit()
	else:
		print('Not a valid command')
