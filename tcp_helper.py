from socket import *
import threading
import queue
from multiprocessing import Queue, shared_memory, Semaphore


def create_socket():
    socket_out = socket(AF_INET, SOCK_STREAM)
    return socket_out


def client_connect(server_name: str, server_port: int):
    client_socket = create_socket()
    client_socket.connect((server_name, server_port))
    return client_socket


def server_listen_at(server_name, server_port: int):
    server_socket = create_socket()
    server_socket.bind((server_name, server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    return server_socket


def send_msg(socket, msg: str):
    socket.sendall(msg.encode('utf-8'))


def rcv_msg(socket, buff_size: int = 1024):
    rcvd_msg = (
        socket.
        recv(buff_size).
        decode('utf-8')
    )
    return rcvd_msg


def handle_server_side_connection(conn, addr, queue):
    while True:
        if not rcv_msg(conn, 1024): continue  # prevent spurious empty messages/bits from being added to queue
        queue.append(rcv_msg(conn, 1024))
        # print(f'Message from {addr}: ' + sentence)
        # sentence = sentence.upper()
        # send_msg(conn, sentence)
        print(len(queue))


def handle_client_side_connection(server_socket):
    while True:
        message = input("Enter message to send: ")
        if message == 'exit':
            break
        send_msg(server_socket, message)
        server_response = rcv_msg(server_socket, 1024)
        print(f"Received from server: {server_response}")


def run_client(server_name: str, server_port: int):
    """ connect to <host> on <port> """
    # client_socket = client_connect(server_name, server_port)
    with client_connect(server_name, server_port) as client_socket:
        print("Connected to server!")
        handle_client_side_connection(client_socket)
        client_socket.close()


def run_server(server_name: str, server_port: int):
    """ listen here  on <host> for <incoming ip request> at <port> """
    # with server_listen_at(server_name, server_port) as server_socket:
    server_socket = server_listen_at(server_name, server_port)
    conn, addr = server_socket.accept()
    handle_server_side_connection(conn, addr, [])  # start server with empty queue
    conn.close()


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
