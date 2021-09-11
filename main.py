from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from threading import Thread

# Server constants
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

# Create server
server = socket(AF_INET, SOCK_STREAM)

# Allow to reconnect
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind port and ip
server.bind((IP, PORT))
server.listen()

# Clients socket list
clients = [server]
clients_data = {}

def receiveMessage(client_socket):
    try:
        header_message = client_socket.recv(HEADER_LENGTH)

        if not len(header_message):
            return False
        
        message_length = int(header_message.decode("utf-8").strip())

        return {
            "header": header_message,
            "data": client_socket.recv(message_length)
        }
    except:
        return False

while True:
    read_sockets, _, except_sockets = select(clients, [], clients)
    for notified_socket in read_sockets:

        if notified_socket == server:
            client_socket, client_address = server.accept()
            user = receiveMessage(client_socket)

            if user is False:
                continue
            
            clients.append(client_socket)
            clients_data[client_socket] = user
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
        else:
            message = receiveMessage(notified_socket)
            
            if message is False:
                print(f"Closed connection from {clients_data[notified_socket]['data'].decode('utf-8')}")
                clients.remove(notified_socket)
                del clients_data[notified_socket]
                continue

            user = clients_data[notified_socket]
            print(f"{user['data'].decode('utf-8')} >>> {message['data'].decode('utf-8')}")

            for client in clients_data:
                if client != notified_socket:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in except_sockets:
        clients.remove(notified_socket)
        del clients_data[notified_socket]
