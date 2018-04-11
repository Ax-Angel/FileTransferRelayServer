import socket
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.setblocking(0)
client.sendall(bytes("NombreCliente1",'UTF-8'))
while True:
	try:
		in_data =	client.recv(1024)
		print(in_data.decode())
	except socket.error:
		pass
	out_data = input()
	client.sendall(bytes(out_data,'UTF-8'))
	if out_data=='4':
		break
client.close()
