import queue
import random
import socket as mySock
import threading
from socket import *

from cryptography.fernet import Fernet


def create_tcp_socket():
    socket_out = socket(AF_INET, SOCK_STREAM)
    return socket_out


def create_udp_socket():
    return socket(AF_INET, SOCK_DGRAM)


def udp_client(server_name, server_port):
    client_socket = create_udp_socket()
    MULTICAST_GROUP = ('224.0.0.0', server_port)
    client_socket.setsockopt(
        mySock.IPPROTO_IP, mySock.IP_ADD_MEMBERSHIP,
        mySock.inet_aton(MULTICAST_GROUP[0]) + mySock.inet_aton('0.0.0.0')
    )
    while True:
        message = input("Enter message to send:")
        server_msg, server_address = client_socket.recvfrom(2048)
        client_socket.sendto(message.encode('utf-8'), MULTICAST_GROUP)
        print(f'{server_msg.decode("utf-8")}')
    # client_socket.close()


def udp_server(server_name, server_port):
    AVAILABLE_PORTS = [p for p in range(20000, 65535)]
    CONNECTED_CLIENTS = {}

    server_socket = create_udp_socket()

    MULTICAST_GROUP = ("224.0.0.1", 21211)
    server_socket.setsockopt(
        mySock.IPPROTO_IP,
        mySock.IP_ADD_MEMBERSHIP,
        mySock.inet_aton(MULTICAST_GROUP[0]) + mySock.inet_aton('0.0.0.0')
    )

    server_socket.bind((server_name, server_port))
    print("The server is ready to receive!")

    while True:
        message, client_address = server_socket.recvfrom(2048)
        print(f'Connection from {client_address}')
        # server_socket.sendto(message, MULTICAST_GROUP)
        message = message.decode('utf-8')
        print(f'{client_address}: {message}')

        # if client_address not in CONNECTED_CLIENTS:
        #     print(f'Connection from {client_address}')
        # CONNECTED_CLIENTS[client_address] = server_socket
        # for client_address, server_socket in CONNECTED_CLIENTS.items():
        #     server_socket.sendto(message, client_address)

    server_socket.close()



def udp_client_2(key):

    # Create a UDP socket for the client
    client = mySock.socket(mySock.AF_INET, mySock.SOCK_DGRAM)

    # Bind the client to a random port in the range 8000-9000
    client.bind(("localhost", random.randint(8000, 9000)))

    # Get the user's nickname as input
    name = input("Alias: ")

    # Function to receive messages from the server
    def receive():
        while True:
            try:
                # Receive a message from the server
                message, server_address = client.recvfrom(1024)

                # Print the decoded message
                print(decrypt(key,message.decode()))
                print(message.decode())
            except:
                pass

    # Create a thread for receiving messages
    t = threading.Thread(target=receive)
    t.start()

    # Send a signup message to the server with the user's nickname
    client.sendto(f"Alias: {name}".encode(), ("localhost", 9999))

    # Main loop for sending messages to the server
    while True:
        # Get user input for a message
        message = input("")

        # Check if the user wants to quit
        if message == "!q":
            exit()
        else:
            # Send the user's message to the server
            client.sendto(f"{name}: {encrypt(key,message)}".encode(), ("localhost", 9999))



def upd_server_2():
    # Initialize a queue to store client messages
    messages = queue.Queue()

    # List to track connected clients
    clients = []

    # Create a UDP socket for the server
    server = mySock.socket(mySock.AF_INET, mySock.SOCK_DGRAM)

    # Bind the server to the specified address and port
    server.bind(("localhost", 9999))

    key = generate_key()

    # Function to handle incoming messages from clients
    def receive():
        while True:  # Continuously listen for messages
            try:
                # Receive a message and the sender's address
                message, addr = server.recvfrom(1024)


                # Add the message and address to the queue
                messages.put((message, addr))
            except:
                pass

    # Function to broadcast messages to all connected clients
    def broadcast():
        while True:
            # Check if there are messages in the queue
            while not messages.empty():
                # Get the message and sender's address from the queue
                message, addr = messages.get()

                # Decode and display the message
                print(message.decode())

                # If the client is new, add them to the clients list
                if addr not in clients:
                    clients.append(addr)

                # Send the message to all connected clients
                for client in clients:
                    try:
                        # Check if the message starts with a specific tag indicating signup
                        if message.decode().startswith("ALIAS:"):
                            # Extract and notify about the new client's name
                            name = message.decode()[message.decode().index(":") + 1:]
                            server.sendto(f"{name} joined!", client)
                        else:
                            server.sendto(encrypt(key,message), client)
                    except:
                        # Remove unreachable clients
                        clients.remove(client)

    # Start threads for receiving and broadcasting messages
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=broadcast)

    t1.start()  # Start the receiver thread
    t2.start()  # Start the broadcaster thread

    return key.decode()


def generate_key():
    return Fernet.generate_key()


def decrypt(key, text):
    # Fernet requires the key to be in bytes
    key = key.encode()
    f = Fernet(key)
    decrypted_message = f.decrypt(text.encode())
    return decrypted_message.decode()


def encrypt(key, text):
    # Fernet requires the key to be in bytes
    key = key.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(text.encode())
    return encrypted_message.decode()
