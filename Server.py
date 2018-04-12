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

		userID = self.clientSocket.recv(1024)
		userID = userID.decode()
		self.clientID = userID

		print(self.clientID + " is connected")

		for client in clients:
			client.send(bytes("[Notice] welcome " + self.clientID + "!", 'UTF-8'))
		request = ''

		while True:
			try:
				data = self.clientSocket.recv(2048)
				request = data.decode()
				request = request.split("/")

				if request[0] == '1':
					entry = "/".join([ self.clientID, request[1] ])
					fileList.append(entry)
					for client in clients:
						client.send(bytes("[Notice] The global file list is updated", 'UTF-8'))
					print("The global file list is as follows:")
					for entry in fileList:
						print(entry)


				elif request[0] == '2':
					pass

				elif request[0] == '2':
					pass

				elif request[0] == '4':
					break
				
				else:
					pass
			except:
				pass
			print("aaaaaaaaaaaa")
		print ("Client " + self.clientID + " at ", self.clientAddress , " disconnected...")
		clients.remove(self.clientSocket)
		for client in clients:
			client.send(bytes("[Notice] " + self.clientID + " has left", 'UTF-8'))

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
		clients.append(clientSocket)
		newthread = ClientThread(clientAddress, clientSocket)
		newthread.start()
	except:
		pass
