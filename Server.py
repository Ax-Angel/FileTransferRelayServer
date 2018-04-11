import os
import socket
import threading

clients = []
 
class ClientThread(threading.Thread):
	def __init__(self, clientAddress, clientSocket, clientID):
		threading.Thread.__init__(self)
		self.clientSocket = clientSocket
		self.clientID = clientID
		print (self.clientID + " is connected")

	def register_file():
		#TODO
		pass

	def download_file():
		#TODO
		pass

	def run(self):
		global clients
		for client in clients:
			client.send(bytes("[Notice] welcome " + self.clientID + "!", 'UTF-8'))
		response = ''

		while True:
			try:
				data = self.clientSocket.recv(2048)
				response = data.decode()

				if response=='4':
					break
				print ("from client " + self.clientID + ": ", response)
				self.clientSocket.send(bytes(response,'UTF-8'))
			except:
				pass
		print ("Client " + self.clientID + " at ", clientAddress , " disconnected...")
		self.clientSocket.send(bytes("Goodbye",'UTF-8'))
		clients.remove(self.clientSocket)
		for client in clients:
			client.send(bytes("[Notice] " + self.clientID + " has left", 'UTF-8'))
		response = ''



LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
server.setblocking(0)
print("Server started")
print("Waiting for client request..")
server.listen(1)
while True:
	try:
		clientSocket, clientAddress = server.accept()
		clients.append(clientSocket)
		data = clientSocket.recv(2048)
		clientID = data.decode()
		newthread = ClientThread(clientAddress, clientSocket, clientID)
		newthread.start()
	except:
		pass
