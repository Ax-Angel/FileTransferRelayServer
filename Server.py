import os
import socket
import threading

clients = []
fileList = []

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# Doesn't matter if its unreachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.1.1'
	finally:
		s.close()
	return IP
 
class ClientThread(threading.Thread):
	def __init__(self, clientAddress, clientSocket):
		threading.Thread.__init__(self)
		self.clientAddress = clientAddress
		self.clientSocket = clientSocket
		self._clientID = None

	@property
	def clientID(self):
		return self._clientID

	@clientID.setter
	def clientID(self, clientID):
		self._clientID = clientID

	@clientID.deleter
	def clientID(self, clientID):
		del self._clientID

	def run(self):
		global clients

		userID = self.clientSocket.recv(1054)
		userID = userID.decode()
		self.clientID = userID
		clients.append([self.clientSocket, self.clientID])

		print(self.clientID + " is connected")

		for client in clients:
			client[0].send(bytes("105--[Notice] welcome " + self.clientID + "!\n", 'UTF-8'))
		request = ''

		while True:
			try:
				data = self.clientSocket.recv(4096)
				request = data.decode()
				request = request.split("--")

				if request[0] == '1':
					entry = "/".join([ self.clientID, request[1] ])
					fileList.append(entry)
					for client in clients:
						client[0].send(bytes("105--[Notice] The global file list is updated", 'UTF-8'))
					print("The global file list is as follows:")
					for entry in fileList:
						print(entry)

				elif request[0] == '2':
					fileListMessage = "105--The global file list is as follows:\n"
					for entry in fileList:
						fileListMessage = fileListMessage + entry + "\n"
					self.clientSocket.send(bytes(fileListMessage, 'UTF-8'))

				elif request[0] == '3':
					print("Received the file download request from " + self.clientID + " for " + request[1] + "/" + request[2])
					for client in clients:
						if client[1] == request[1]:
							request = b'--'.join([ b"101", bytes(self.clientID, 'UTF-8'), bytes(request[2], 'UTF-8') ])
							client[0].sendall(request)
							break
						

				elif request[0] == '4':
					break

				elif request[0] == '103':
					print("Retrieved " + request[2] + " from " + request[1])
					response = b'--'.join([ b"102", bytes(request[2], 'UTF-8'), bytes(request[3], 'UTF-8'), bytes(request[4], 'UTF-8') ])
					print(request)
					for client in clients:
						if client[1] == request[1]:
							client[0].sendall(response)
							break
					print("The transfer of " + request[3] + " to " + request[1] + " has been completed")
					entry = "/".join([ request[1], request[3] ])
					fileList.append(entry)
					print("The global file list is as follows:")
					for entry in fileList:
						print(entry)
					for client in clients:
						client[0].send(bytes("105--[Notice] The global file list is updated", 'UTF-8'))
				
				else:
					pass
			except:
				pass
		print ("Client " + self.clientID + " at ", self.clientAddress , " disconnected...")
		clients.remove(self.clientSocket)
		for client in clients:
			client[0].send(bytes("105--[Notice] " + self.clientID + " has left", 'UTF-8'))

LOCALHOST = get_ip()
PORT = 10800
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
server.setblocking(0)
print("Server started at " + LOCALHOST + " in port " + str(PORT))
print("Waiting for client request..")
server.listen(5)
while True:
	try:
		clientSocket, clientAddress = server.accept()
		newthread = ClientThread(clientAddress, clientSocket)
		newthread.start()
	except:
		pass
