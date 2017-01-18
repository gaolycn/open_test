# coding=utf-8

from Crypto.Cipher import AES
from Crypto import Random


class AESHelper(object):
    def __init__(self, key):
        """

        :param key:
        :type key: str
        """

        self._key = key

    def enc(self, raw_data):
        """

        :param raw_data:
        :type raw_data: str
        :return:
        :rtype: str
        """

        pad_data = self._pad(raw_data)
        iv = Random.new().read(AES.block_size)

        cipher = AES.new(self._key, mode=AES.MODE_CBC, IV=iv)
        enc_data = cipher.encrypt(pad_data)
        data = iv + enc_data

        return data

    def dec(self, data):
        """

        :param data:
        :type data: str
        :return:
        :rtype: str
        """

        iv = data[:AES.block_size]
        enc_data = data[AES.block_size:]

        cipher = AES.new(self._key, mode=AES.MODE_CBC, IV=iv)
        pad_data = cipher.decrypt(enc_data)
        raw_data = self._unpad(pad_data)

        return raw_data

    def _pad(self, raw_data):
        """

        :param raw_data:
        :type raw_data: str
        :return:
        :rtype: str
        """

        pad_len = AES.block_size - (len(raw_data) % AES.block_size)
        pad_str = chr(pad_len) * pad_len
        pad_data = raw_data + pad_str

        return pad_data

    def _unpad(self, pad_data):
        """

        :param pad_data:
        :type pad_data: str
        :return:
        :rtype: str
        """

        pad_len = ord(pad_data[-1])
        raw_data = pad_data[0:-pad_len]

        return raw_data