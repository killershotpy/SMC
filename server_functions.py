from sys import _getframe as frame


def test1(data: object = None):
    return 'test1 name'


def test2(data: object = None):
    return 'test2 name'


# get names functions and links to functions for import
names = {name: obj for name, obj in frame().f_locals.items() if callable(obj) and obj.__module__ == __name__}
