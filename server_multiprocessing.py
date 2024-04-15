import multiprocessing
import socket

from typing import Any as Any
from threading import Thread, enumerate, Event

import server_functions
from encryptor import Aes_v
from server_options import conf


global_shutdown_event = multiprocessing.Event()
manager = multiprocessing.Manager


def start() -> None:
    connections_at_ports = manager().dict()
    processes = []
    try:
        for port in conf.multiproc_ports_list:
            process = multiprocessing.Process(target=start_process, args=(port, global_shutdown_event, connections_at_ports))
            processes.append(process)
            process.start()
            connections_at_ports[port] = 0
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        global_shutdown_event.set()


def cleaner(client_connections: dict,
            cleaner_event: Event,
            shutdown_event: Event,
            port: int,
            connections_at_ports: dict) -> None:
    dead_threads = []
    while True:
        cleaner_event.wait()
        if shutdown_event.is_set():
            break
        cleaner_event.clear()
        try:
            for thread_name, thread in client_connections.items():
                if thread.is_alive() is False:
                    thread.join()
                    dead_threads.append(thread_name)
        except RuntimeError:
            pass
        if len(dead_threads) > 0:
            [client_connections.__delitem__(thread_name) for thread_name in dead_threads]
            dead_threads.clear()
            connections_at_ports[port] -= 1


def response(connection: socket.socket, msg: Any) -> None:
    msg = Aes_v.encrypt(msg)
    msg_len_str = Aes_v.encrypt(f"{len(msg):04d}")
    connection.sendall(msg_len_str + msg)


def get_message(connection: socket.socket) -> Any:
    try:
        get_len_message = get_all_data(connection, Aes_v.first_bytes_for_socket)
    except UnicodeDecodeError:
        return
    if not get_len_message:
        return None
    return get_all_data(connection, int(get_len_message))


def get_all_data(connection: socket.socket, n: int) -> Any:
    data = []
    total_received = 0
    while total_received < n:
        packet = connection.recv(n - total_received)
        if not packet:
            return None
        data.append(packet)
        total_received += len(packet)
    return Aes_v.decrypt(b''.join(data))


def handle_client(connection: socket.socket,
                  cleaner_event: Event,
                  connections_at_ports: dict) -> None:
    try:
        while True:
            client_request = get_message(connection)
            try:
                if client_request is None:
                    break
                call_func = client_request[conf.call_func]
                if call_func == '_hello':
                    response(connection, {port: connections for port, connections in connections_at_ports.items()})
                else:
                    response(connection, server_functions.names.get(call_func)(client_request.get(conf.data)))
            except TypeError:
                response(connection, 'incorrect data')
            except KeyError:
                response(connection, 'call_func not found')
    except ConnectionResetError:
        pass
    finally:
        connection.close()
        cleaner_event.set()


def start_process(port: int,
                  glob_shutdown_event: multiprocessing.Event,
                  connections_at_ports: dict) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.settimeout(0.1)
    server_socket.bind((conf.loaded_config[conf.host], port))
    server_socket.listen()

    client_connections = {}
    cleaner_event = Event()
    shutdown_event = Event()

    Thread(name=conf.name_thread_cleaner, target=cleaner, args=[client_connections, cleaner_event, shutdown_event, port, connections_at_ports]).start()
    try:
        while not glob_shutdown_event.is_set():
            try:
                connection, address = server_socket.accept()
                client_thread = Thread(target=handle_client, args=[connection, cleaner_event, connections_at_ports, True])
                client_connections[f'{address[0]}:{address[1]}'] = client_thread
                client_thread.start()
                connections_at_ports[port] += 1
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_event.set()
        cleaner_event.set()
        [thread.join() for thread in client_connections.values() if thread.is_alive()]
        [thread.join() for thread in enumerate() if thread.name == conf.name_thread_cleaner and thread.is_alive() is True]
        server_socket.close()
        del connections_at_ports[port]


if __name__ == '__main__':
    start()
