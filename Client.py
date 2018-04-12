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
		in_data = client.recv(4096)
		in_data = in_data.decode().split('--')
		if in_data[0] == '101':
			file = open(in_data[2], "r+b")
			data = file.read()
			message = b'--'.join([ b"103", bytes(in_data[1], 'UTF-8'), bytes(userID, 'UTF-8'), bytes(in_data[2], 'UTF-8'), data ])
			client.sendall(message)
			file.close()

		elif in_data[0] == '102':
			file = open(in_data[2], "w+b")
			file.write(bytes(in_data[3], 'UTF-8'))
			file.close()
			print(in_data[2] + " has been downloaded")

		elif in_data[0] == '105':
			print(in_data[1])

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
				msg = b'--'.join([ b"1", bytes(path, 'UTF-8')])
				client.sendall(msg)
			except:
				print("Error sending request, try again...")

		else:
			print("The file " + path + " doesn't exists!")

	elif opt == '2':
		msg = b'--'.join([ b"2" ])
		client.sendall(msg)
	
	elif opt == '3':
		print("Which file to download?")
		desiredFile = input()
		desiredFile = desiredFile.split("/")
		request = "3--"+desiredFile[0]+"--"+desiredFile[1]
		client.sendall(bytes(request, 'UTF-8'))

	elif opt=='4':
		break

	else:
		pass
client.close()