import os

from json import loads as ld


name_file_config = 'options_server'
default_host = 'host = \"127.0.0.1\"'
default_port = 'port = 20001'
default_host_port = [default_host, default_port]


try:
    loaded_config = {s.split()[0]: ld(s.split()[2]) if len(s.split()) == 3 else {} for s in open(name_file_config, 'r', encoding='utf-8').readlines()}
except FileNotFoundError:
    open(name_file_config, 'w', encoding='utf-8').write('\n'.join(default_host_port))
    loaded_config = {s.split()[0]: ld(s.split()[2]) if len(s.split()) == 3 else {} for s in open(name_file_config, 'r', encoding='utf-8').readlines()}


class ParametersNames:
    """Parameters names"""

    host = 'host'
    port = 'port'
    call_func = 'call_func'
    data = 'data'
    name_thread_cleaner = 'cleaner'
    timeout = 'timeout'
    loaded_config = loaded_config
    multiproc_ports_list = [loaded_config['port'] + x for x in range(os.cpu_count() * 2)]

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


conf = ParametersNames()  # parameters names
