

class ParametersNames:
    """Parameters names"""

    host = 'host'
    port = 'port'
    call_func = 'call_func'
    data = 'data'
    name_thread_cleaner = 'cleaner'

    try:
        values = {s.split()[0]: s.split()[2] if len(s.split()) == 3 else {} for s in open('options_server', 'r', encoding='utf-8').readlines()}
    except FileNotFoundError:
        raise FileNotFoundError('file \'options_server\' not found')

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


conf = ParametersNames()  # parameters names
