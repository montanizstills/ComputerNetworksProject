from socket import *
import threading


def create_socket():
    socket_out = socket(AF_INET, SOCK_STREAM)
    return socket_out


def client_connect(server_name: str, server_port: int):
    client_socket = create_socket()
    client_socket.connect((server_name, server_port))
    return client_socket


def server_connect(server_name, server_port: int):
    server_socket = create_socket()
    server_socket.bind((server_name, server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    return server_socket


# def server_accept(server_socket):
#     server_socket.accept()


def send_msg(socket, msg: str):
    socket.sendall(msg.encode('utf-8'))


def rcv_msg(socket, buff_size: int = 1024):
    rcvd_msg = (
        socket.
        recv(buff_size).
        decode('utf-8')
    )
    # to broadcast to all users you can "hack" by printing rcvd_msg here
    # print(receive_message(rcvd_msg))
    return rcvd_msg


def run_client(server_name: str, server_port: int):
    with client_connect(server_name,server_port) as client_socket:
        while True:
            message = input("Enter message to send: ")
            send_msg(client_socket, message)
            server_response = rcv_msg(client_socket, 1024)
            print(f"Received from server: {server_response}")



def run_server(server_name: str, server_port: int):
    server_socket = server_connect(server_name, server_port)
    connection_socket, addr = server_socket.accept()

    while True:
        sentence = rcv_msg(connection_socket, 1024)
        print(f'Message from {addr}: ' + sentence)
        sentence = sentence.upper()
        connection_socket.send(sentence.encode('utf-8'))

    # """ listen here  on <host> for <incoming ip request> at <port> """
    # with server_connect(server_name, server_port) as server_socket:
    #     """
    #       Thread: if server accepts a connection:
    #                 then create a new thread to handle the connection
    #                 t1 maintains TCP connection with <client> and sends/receives data
    #
    #                 when client disconnects:
    #                  t1 closes the connection (by killing thread)
    #     """
    #     with server_socket.accept() as (conn, addr):
    #         while True:
    #             sentence = rcv_msg(conn, 1024)
    #             print(f'Message from {addr}: ' + sentence)
    #             sentence = sentence.upper()
    #             send_msg(server_socket, sentence)


def tcp_client(host='127.0.0.1', port=12345):
    thread = threading.Thread(
        target=run_client, args=(host, port)
    )
    thread.start()


def tcp_server(host='0.0.0.0', port=12345):
    thread = threading.Thread(
        target=run_server, args=(host, port)
    )
    thread.start()
