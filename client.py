import socket

from encryptor import Aes_v


def send_msg(connection, msg):
    msg = Aes_v.encrypt(msg)
    msg_len_str = Aes_v.encrypt(f"{len(msg):04d}")
    connection.sendall(msg_len_str + msg)


def get_message(connection):
    get_len_message = get_all_data(connection, Aes_v.first_bytes_for_socket)
    if not get_len_message:
        return 'ConnectionResetError'
    return get_all_data(connection, int(get_len_message))


def get_all_data(connection, n):
    data = []
    total_received = 0
    while total_received < n:
        try:
            packet = connection.recv(n - total_received)
        except ConnectionResetError:
            return None
        if not packet:
            return None
        data.append(packet)
        total_received += len(packet)
    return Aes_v.decrypt(b''.join(data))


def get_connect(host: str, port: int):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection


def request(connection: socket, data: object) -> object:
    """send request in server and get response

    :param connection: socket connection
    :param data: any object than can be serialized JSON standard
    :return: response server
    """
    send_msg(connection, data)
    return get_message(connection)
