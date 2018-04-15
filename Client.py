import socket
import os
import select
import sys

MENU_MSG = "########################\n" \
				+ "1. Register a file\n" \
				+ "2. Get the global file list\n" \
				+ "3. Download a file\n" \
				+ "4. Exit\n" \
				+ "########################\n"

def input_with_timeout(timeout):
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    raise TimeoutExpired

print("Welcome")
print("Enter UserID: ")
userID = input()
sys.stdout.flush()
print("Enter RelayServer IP address: ")
SERVER = input()
sys.stdout.flush()

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
			sys.stdout.flush()

		elif in_data[0] == '105':
			print(in_data[1])
			sys.stdout.flush()

	except socket.error:
		try:
			opt = input_with_timeout(0.3)
			if opt == '0':
				print(MENU_MSG)

			elif opt == '1':
				print("Which file to register? ")
				path = input()
				sys.stdout.flush()
				if os.path.isfile(path):
					try:
						msg = b'--'.join([ b"1", bytes(path, 'UTF-8')])
						client.sendall(msg)
					except:
						print("Error sending request, try again...")
						sys.stdout.flush()

				else:
					print("The file " + path + " doesn't exists!")
					sys.stdout.flush()

			elif opt == '2':
				msg = b'--'.join([ b"2" ])
				client.sendall(msg)
			
			elif opt == '3':
				print("Which file to download?")
				desiredFile = input()
				sys.stdout.flush()
				desiredFile = desiredFile.split("/")
				request = "3--"+desiredFile[0]+"--"+desiredFile[1]
				client.sendall(bytes(request, 'UTF-8'))

			elif opt=='4':
				response = b'4'
				client.sendall(response)
				print("Notified RelayServer\nGoodbye!")
				break

			else:
				pass

		except:
			pass
	
client.close()