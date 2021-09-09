import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((socket.gethostname(), 1234))
soc.listen(5)

while True:
    clientsocket, address = soc.accept()
    print(f"Connection from {address} has been established")
    for i in range(5):
        clientsocket.send(bytes("Welcome to the server \n", "utf-8"))
    msg = clientsocket.recv(1024)
    print(msg.decode("utf-8"))