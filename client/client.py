#!/usr/bin/env python
import socket
import sys
import getpass
from simplecrypt import encrypt, decrypt
import time

HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#_auth_count = 0

#def _setAuthCount(val):
#	_auth_count = val
#def _getAuthCount()
#	return _auth_count
class enc:
	def __init__(self, val):
		self.__encryption_pass = val
	def setEncryptPass(self, val):
		self.__encryption_pass = val
	def getEncryptPass(self):
		return self.__encryption_pass

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
enc1 = enc('temp')

while 1:
	enc1.setEncryptPass(getpass.getpass(prompt='Encryption Pass: '))
	#print('Encrypted Pass: ' + enc1.getEncryptPass() + p)
	s.send(enc1.getEncryptPass().encode())
	time.sleep(1)
	#print('enc pass sent')
	s.send(userDetails.encode())
	#print('user details sent')
	encAuth = s.recv(1024).decode()
	#print('recieved enc auth code')
	if(encAuth != 'pass'):
		print('Encryption passcode incorrect')
		continue
	print('Encryption Pass Accepted')
	#cipher_text = encrypt(_getEncryptPass(),userDetails)
	#s.send(cipher_text.encode())
	print("User Details: " + str(userDetails) + " has been sent.")
	authentication_result = s.recv(1024).decode()
	if(authentication_result != "pass"):
		print('Authentication Failed...')
		
		username = input("Username: ")
		password = getpass.getpass(prompt = 'Password: ')
		userDetails = username + "," + password
	else:
		print('Welcome ' + str(username))
		break
	
while 1:
	cmnd = input("Exit | Send File | Access File:\n")
	cmnd = cmnd.lower()
	
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
				file = open(filename, 'r')
				break
			except:
				print('File does not exist.')
		
		print('Sending File Name: ' + str(filename))
		s.send(filename.encode())

		file_data = file.read()
		file_data = encrypt(enc1.getEncryptPass(), file_data)
		s.send(file_data)
		
		file.close()
		print('The file has finished sending')
	elif (cmnd == 'access file'):
		access_file = 'CAF002'
		s.send(access_file.encode())
		while 1:
			file_name = input('Provide File Name: ')
			s.send(file_name.encode())
			file_status = s.recv(1024).decode()
			print(file_status)
			if(file_status == 'File does not exist.'):
				print('File does not exist.')
			else:
				break

		print('Recieving File...')

		try:
			#file_name = str(connection.recv(1024).decode("utf-8"))
			print("Server will send this file: " + file_name)
			file = open(file_name, "w")
		except:
			print('Unable to write to the file.')
		
		try:
			file_data = s.recv(1024)
			file_data = decrypt(enc1.getEncryptPass(), file_data).decode("utf-8")
		except:
			print("Unable to recieve/decrypt file")

		print("this is from the file: " + str(file_data))
		file.write(file_data)
		print('File has been created')
		file.close()
		
	elif (cmnd == 'secret close'):
		secret = 'SECRCL005'
		s.send(secret.encode())
		print('Secret Command accepted. Server and Client Exiting.')
		sys.exit()
	else:
		print('Not a valid command')
