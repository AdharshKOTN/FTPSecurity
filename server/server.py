#!/usr/bin/env python
import socket
import select
import sys
from simplecrypt import encrypt, decrypt
import base64

HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#protected list of passwords
_passwords = {
	"admin":"admin1",
	"user1":"pass1"
}
#protected list of encryption passwords
_encpass = {
	"admin":"password1",
	"user1":"password2"
}

def _confirmAccess(username, password):
	if(_passwords.get(username) == password):
		print('UserAuth Success')
		return True
	else:
		print('UserAuth Fail')
		return False

def _confirmEncryption(username, encPass):
	if(_encpass.get(username) == encPass):
		print('Encryption Auth Success')
		return True
	else:
		print('Encryption Auth Fail')
		return False
		
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
	print('Connected by: ' + str(addr))
	while 1:
		userDetails = connection.recv(1024).decode("utf-8")
		#print(userDetails)
		userDetailsArr = userDetails.split(",")
		username = userDetailsArr[0]
		password = userDetailsArr[1]
		
		print('Obtained details from user: ' + str(username))
		if(_confirmAccess(username,password) == False or username not in _passwords.keys()):
			print('User Authentication Failed')
			passAuth = 'SAF010'
			connection.send(passAuth.encode())
			print('Awaiting next set of user details...')
		else:
			passAuth = 'SAS011'
			connection.send(passAuth.encode("utf-8"))
			print(str(username) + ' is logged in')
			break
	while 1:
		userEncPass = connection.recv(1024).decode("utf-8")
		#print(userEncPass)
		if(_confirmEncryption(username, userEncPass) == False or username not in _encpass.keys()):
			print('Encryption Passcode Fail')
			connection.send('SEAF008'.encode("utf-8"))
			continue
		else:
			print('Encryption Passcode Pass')
			connection.send('SEAS009'.encode("utf-8"))
			break
		
	while 1:
		print('Waiting for Client Command....')
		client_response = connection.recv(1024).decode("utf-8")
		if(client_response):
			print('Client Command: ' + str(client_response))
			if(str(client_response) == 'CEX000'):
				print('Client wants to exit the session')
				connection.close()
				print('Client ' + str(addr) + ' has exited the session')
				break
			elif (str(client_response) == 'CSF001'):
				print('Client is sending a file')
				print('Recieving File...')

				try:
					file_name = str(connection.recv(1024).decode("utf-8"))
					print("Server will write to this file: " +file_name)
					file = open(file_name, "w")
				except:
					print('Unable to recieve the file name.')

				s.shutdown(socket.SHUT_WR)
				file_data = connection.recv(1024)
				print('Data before decrypt: ' + str(file_data))
				file_data = decrypt(_encpass.get(username), file_data).decode("utf-8")
				print("Data after decrypt: " + str(file_data))
				file.write(file_data)
				
			elif (str(client_response) == 'CAF002'):
				print('Sending File...')
				
				file_name = connection.recv(1024).decode("utf-8")
				while 1:
					print('Server will find the file called: ' + str(file_name))
					try:
						file = open(file_name, 'r')
						break
					except:
						file_does_not_exist = 'SFDNE006'
						print('Client is attempting to access file that is not available.')
						connection.send(file_does_not_exist.encode("utf-8"))
						file_name = connection.recv(1024).decode("utf-8")
				file_does_exist = 'SFDE007'
				connection.send(file_does_exist.encode("utf-8"))
				#open the file on the server and send the data to the client
				print('File: ' + file_name + ' has been opened on the server.')
				file_data = file.read()
				print('Data before encryption: ' + str(file_data))
				file_data = encrypt(_encpass.get(username), file_data)
				print('Data after encryption: ' + str(file_data))
				#print(file_data)
				connection.send(file_data)
				
				file.close()
				print('The file has finished sending')
				
			elif (str(client_response) == 'CSECRCL005'):
				print('Secret Command Activated. Turning server off.')
				sys.exit()
		else:
			print('Error: No message sent or message is decoded improperly.')
			break
