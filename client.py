import socket

from typing import Any as Any

from encryptor import Aes_v


def send_msg(connection: socket.socket, msg: Any) -> None:
    msg = Aes_v.encrypt(msg)
    msg_len_str = Aes_v.encrypt(f"{len(msg):04d}")
    connection.sendall(msg_len_str + msg)


def get_message(connection: socket.socket):
    get_len_message = get_all_data(connection, Aes_v.first_bytes_for_socket)
    if not get_len_message:
        connection.close()
        return 'ConnectionResetError'
    return get_all_data(connection, int(get_len_message))


def get_all_data(connection: socket.socket, n: int) -> Any:
    data = []
    total_received = 0
    while total_received < n:
        try:
            packet = connection.recv(n - total_received)
        except ConnectionResetError:
            connection.close()
            return None
        if not packet:
            return None
        data.append(packet)
        total_received += len(packet)
    return Aes_v.decrypt(b''.join(data))


def _hello(host: str, port: int) -> int:
    """Send a greeting to the server, get an up-to-date list of ports
        and connections, get the port that has the minimum number of connections."""
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    active_ports = request(connection, {'call_func': '_hello'})
    connection.close()
    return int(min(active_ports, key=active_ports.get))


def get_connect(host: str, port: int) -> socket.socket:
    """Obtain a list of used ports on the remote host and create
    a connection through the port with the least number of connections (load balancing).

    :param host: remote IPv4 address host
    :param port: port remote host
    :return: socket connection object
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, _hello(host, port)))
    return connection


def request(connection: socket.socket, data: Any, _hello: bool = None) -> Any:
    """Send request in server and get response.

    :param connection: socket connection
    :param data: any object than can be serialized JSON standard
    :param _hello: first connect to the server and take list actual active ports for connection
    :return: response server
    """
    send_msg(connection, data)
    return get_message(connection)
