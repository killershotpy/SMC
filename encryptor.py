from hashlib import sha256 as sha_256
from typing import Any as Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom as ur, path as pt
from json import loads as ld, dumps as dm


class Aes:
    def __init__(self, key: bytes = None):
        if key:
            self.e_key = sha_256(key).digest()
        else:
            self.e_key = sha_256(load_app_key()).digest()
        self.dump_json = dm
        self.load_json = ld
        self.offset_compression = 16
        self.first_bytes_for_socket = self.offset_compression * 2

    def encrypt(self, obj: Any) -> bytes:
        """Encrypting any object's, that can serialized JSON standard.

        :param obj: Any object, that it's can serialized JSON standard.
        :return: Bytes string encrypt by algorithm AES_256, [obj: bytes].
        """
        enc = Cipher(algorithms.AES(self.e_key), modes.OFB(self.e_key[:self.offset_compression]), default_backend()).encryptor()
        return self.e_key[:self.offset_compression] + enc.update(self.pad(dm(obj)).encode('utf-8')) + enc.finalize()

    def decrypt(self, c_obj: bytes = None) -> Any:
        """Decrypt encrypted object and return serialized JSON standard object.

        :param c_obj: encrypted object
        :return: JSON structured object
        """
        dec = Cipher(algorithms.AES(self.e_key), modes.OFB(c_obj[:self.offset_compression]), default_backend()).decryptor()
        s = (dec.update(c_obj[self.offset_compression:]) + dec.finalize()).decode('utf-8')
        return ld(s[:-ord(s[len(s) - 1:])])

    def pad(self, s: str) -> str:
        padding = (self.offset_compression - (len(s) % self.offset_compression))
        return s + padding * chr(padding)


def generate_app_key(length: int = 256, path_key: str = 'key') -> None:
    """Generate bytes by os.urandom() (default 256) and save on (this) work directory.

    key - is name file because saved.

    :param path_key: absolute path to secret key app
    :param length: key length after generation in bytes
    :return: None
    """
    if not pt.exists(path_key):
        open(path_key, 'wb').write(ur(length))


def load_app_key(path_key: str = 'key') -> bytes:
    """Load secret key app. Return object type bytes.

    :param path_key: absolute path to secret key app
    :return: bytes urandom
    """
    try:
        return open(path_key, 'rb').read()
    except FileNotFoundError:
        generate_app_key(path_key=path_key)
        return open(path_key, 'rb').read()


Aes_v = Aes()
