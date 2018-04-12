import socket
import os

MENU_MSG = "########################\n" \
				+ "1. Register a file\n" \
				+ "2. Get the global file list\n" \
				+ "3. Download a file\n" \
				+ "4. Exit\n" \
				+ "########################\n"

print("Welcome")
print("Enter UserID: ")
userID = input()
print("Enter RelayServer IP address: ")
SERVER = input()

PORT = 10800
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.setblocking(0)
client.sendall(bytes(userID,'UTF-8'))
while True:
	try:
		in_data =	client.recv(1024)
		print(in_data.decode())
	except socket.error:
		pass
	opt = input()
	if opt == '0':
		print(MENU_MSG)

	elif opt == '1':
		print("Which file to register? ")
		path = input()
		if os.path.isfile(path):
			try:
				msg = b'/'.join([ b"1", bytes(path, 'UTF-8')])
				client.sendall(msg)
			except:
				print("Error sending request, try again...")

		else:
			print("The file " + path + " doesn't exists!")

	elif opt == '2':
		msg = b'/'.join([ b"2" ])
		client.sendall(msg)
	
	elif opt == '3':
		pass

	elif opt=='4':
		break

	else:
		pass
client.close()