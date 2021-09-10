from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import select

class ChatServer:
    def __init__(self):
        self.HEADER_LENGTH = 10
        self.IP = "127.0.0.1"
        self.PORT = 1234
        self.self.server = socket(AF_INET, SOCK_STREAM)
        self.self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.clients = [self.server]
        self.clients_data = {}
    
    def start(self):
        self.self.server.bind((IP, PORT))
        self.self.server.listen()

        while True:
            read_sockets, _, except_sockets = select(self.clients, [], self.clients)
            for notified_socket in read_sockets:
            
                if notified_socket == self.server:
                    client_socket, client_address = self.server.accept()
                    user = _receiveMessage(client_socket)

                    if user is False:
                        continue
                    
                    self.clients.append(client_socket)
                    self.clients_data[client_socket] = user
                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
                else:
                    message = _receiveMessage(notified_socket)

                    if message is False:
                        print(f"Closed connection from {self.clients_data[notified_socket]['data'].decode('utf-8')}")
                        self.clients.remove(notified_socket)
                        del self.clients_data[notified_socket]
                        continue
                    
                    user = self.clients[notified_socket]
                    print(f"{user['data'].decode('utf-8')} >>> {message['data'].decode('utf-8')}")

                    for client in self.clients_data:
                        if client != notified_socket:
                            client.send(user['header'] + user['data'] + message['header'] + message['data'])

            for notified_socket in except_sockets:
                self.clients.remove(notified_socket)
                del self.clients_data[notified_socket]
    
    def _receiveMessage(self, client_socket):
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