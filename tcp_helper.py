from socket import *


def create_tcp_socket():
    socket_out = socket(AF_INET, SOCK_STREAM)
    return socket_out


def create_udp_socket():
    return socket(AF_INET, SOCK_DGRAM)


def udp_client(server_name, server_port):
    client_socket = create_udp_socket()
    while True:
        message = input("Enter message to send:")
        client_socket.sendto(message.encode('utf-8'), (server_name, server_port))
        server_msg, server_address = client_socket.recvfrom(2048)
        print(f'{server_msg.decode("utf-8")}')
    client_socket.close()


def udp_server(server_name, server_port):
    server_socket = create_udp_socket()
    server_socket.bind((server_name, server_port))
    print("The server is ready to receive!")

    CONNECTED_CLIENTS = {}
    while True:
        message, client_address = server_socket.recvfrom(2048)
        if client_address not in CONNECTED_CLIENTS:
            print(f'Connection from {client_address}')
        CONNECTED_CLIENTS[client_address] = server_socket

        # for client_address, server_socket in CONNECTED_CLIENTS.items():
        #     server_socket.sendto(message, client_address)

        message = message.decode('utf-8')
        print(f'{client_address}: {message}')

    server_socket.close()
