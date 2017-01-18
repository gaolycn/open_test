# coding=utf-8
import base64
import logging
import sys


log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel('DEBUG')

from qfcommon.library.huiyi.huiyi_proto import HuiyiProto

req1 = {'busicd': '820000', 'txdt': '0511111815', 'is_update_key': True, 'clisn': '111815', 'encryptor_flag': '0', 'key_type': '2'}
req2 = {'busicd': '800000'}

s1 = base64.b64decode('LgIwMTEzNjY4MDAwMDAgICAwMDAxMDAwMCAgIDAwMDAwMDAwMDAwMDAwMDAwMDA4MzCCIAAAggAIAAQAAAAAAAAAMDUxMTExMTgxNTExMTgxNTA4NjY4MDAwMDAwMDIwMDAwMDAwMDAwMDAwMDAxMDE=')
s2 = base64.b64decode('LgIwMTI3NjY4MDAwMDAgICAwMDAxMDAwMCAgIDAwMDAwMDAwMDAwMDAwMDAwMDA4MDCCIAAAAAAIAAQAAAEQAAABMDUxMTExMTgxNTMxNDA5NzIwMDAwMDAwMDAwMDAwMDAxMDGFLnvJPiHlZzA4NjY4MDAwMDB66TSvASjYFQ==')


def main():
    p = HuiyiProto()

    p.huiyi2qf(req2, s2)
    # p.huiyi2qf(req1, s1)


if __name__ == '__main__':
    main()
