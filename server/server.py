#!/usr/bin/env python
import socket
import select
import sys


HOST = ''
PORT = 63430 #number greater than 1023 and less than 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


_passwords = {
	"admin":"admin1",
	"user1":"pass1"
}

def _confirmAccess(username, password):
	if(_passwords.get(username) == password):
		print('UserAuth Success')
		return True
	else:
		print('UserAuth Fail')
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
	userDetails = connection.recv(1024).decode()
	while 1:
		userDetailsArr = userDetails.split(",")
		username = userDetailsArr[0]
		password = userDetailsArr[1]
		print('Obtained details from user: ' + str(username) + ' password provided: ' + str(password))
		if(_confirmAccess(username,password) == False):
			print('User Authentication Failed')
			passAuth = 'fail'
			connection.send(passAuth.encode())
			print('Awaiting next set of user details')
			userDetails = connection.recv(1024).decode()
		else:
			passAuth = 'pass'
			connection.send(passAuth.encode())
			print('Welcome ' + str(username))
			break
		
	while 1:
		print('Waiting for Client Command....')
		client_response = connection.recv(1024).decode()
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
				file_name = connection.recv(1024).decode()
				file = open(file_name, "a")
				file_data = connection.recv(1024).decode()
				while 1:
					print('Recieved: ' + file_data)
					if (file_data == 'CEOF004'):
						#print('DEBUG: exit the inner loop')
						break
					else:
						file_data = connection.recv(1024).decode()
						file.write(file_data)
						#print('Data from file: ' + file_data)
			elif (str(client_response) == 'CAF002'):
				print('Sending File...')
				#check if the file exists on the server
				#if it doesn't let the client know
				file_name = connection.recv(1024).decode()
				while 1:
					print('Server will send the file called: ' + str(file_name))
					try:
						file = open(file_name, 'rb')
						break
					except:
						file_does_not_exist = 'File does not exist.'
						print('Client is attempting to access file that is not available.')
						connection.send(file_does_not_exist.encode())
						file_name = connection.recv(1024).decode()
				#open the file on the server and send the data to the client
				print('File: ' + file_name + ' has been opened on the server.')
				file_data = file.readline()
				while (file_data):
					connection.send(file_data)
					print('Sent ',repr(file_data))
					file_data = file.readline()
				file.close()
				print('The file has finished sending')
				eof = 'SEOF004'
				connection.send(eof.encode())
			elif (str(client_response) == 'SECRCL005'):
				print('Secret Command Activated. Turning server off.')
				sys.exit()
		else:
			print('Error: No message sent or message is decoded improperly.')
			break
