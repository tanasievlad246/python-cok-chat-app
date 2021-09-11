from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from sys import argv, exit
import errno
from threading import Thread

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Enter your username >>> ")
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

def listenForMessages():
    while True:
        # Receive things
        username_header = client_socket.recv(HEADER_LENGTH)
        
        if not len(username_header):
            print("connection closed by the server")
            exit()
        username_length = int(username_header.decode("utf-8").strip())
        username = client_socket.recv(username_length).decode("utf-8")
        
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(float(message_header.decode('utf-8').strip()))
        message = client_socket.recv(message_length).decode("utf-8")
        
        print(f"{username} >>> {message}")

def sendMessages():
    while True:
        message = input(f"{my_username} >>> ")

        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)

while True:

    sendMessages()

    try:

        Thread(target=listenForMessages).start()

    except IOError as e:
        if e.errno != errno.EAGAIN or e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            exit()

    except Exception as e:
        print('General error', str(e))
        exit()