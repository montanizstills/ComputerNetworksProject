from socket import *


def create_socket():
    socket_out = socket(AF_INET, SOCK_STREAM)
    return socket_out


def client_connect(server_name: str, server_port: str):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))
    return client_socket


def server_connect(server_name, server_port: str):
    server_socket = create_socket()
    server_socket.bind((server_name, server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    return server_socket


# def server_accept(server_socket):
#     server_socket.accept()


def send_msg(socket, msg: str):
    socket.send(msg.encode('utf-8'))


def rcv_msg(socket, buff_size: int = 1024):
    rcvd_msg = (
        socket.
        recv(buff_size).
        decode('utf-8')
    )
    # to broadcast to all users you can "hack" by printing rcvd_msg here
    # print(receive_message(rcvd_msg))
    return rcvd_msg.decode('utf-8')


def run_client(server_name: str, server_port: int):
    while True:
        client_socket = client_connect(server_name, server_port)
        sentence = input('Input lowercase sentence:')
        send_msg(client_socket, sentence)


def run_server(server_name: str, server_port: int):
    server_socket = server_connect(server_name, server_port)
    while True:
        connection_socket, addr = server_socket.accept()
        sentence = connection_socket.recv(1024)
        print('Message from client: ' + sentence.decode('utf-8'))

# if __name__ == '__main__':
#     run_server(11000)
#     run_client('localhost', 11000)
