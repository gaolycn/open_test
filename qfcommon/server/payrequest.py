# coding: utf-8
# pychanneld
import socket
import time
import json
import logging
from copy import deepcopy

log = logging.getLogger()

class PayRequest(object):
    def __init__(self, obj, ip, port, connect_timeout=5000, timeout=10000):
        self.connect_timeout = connect_timeout/1000.0
        self.total_timeout = timeout/1000.0
        self.start_time = None
        self.ip = ip
        self.port = port
        self.sock = None
        self.obj = obj
        self.retobj = None

    def request(self, secret=False):
        str = json.dumps(self.obj)
        send_data = '%04d%s' % (len(str), str)

        try:
            self._connect()
            self._do_send(send_data)
            recv_data = self._do_recv()
            if not recv_data:
                return None
            self.retobj = json.loads(recv_data)
            return self.retobj
        except:
            raise
        finally:
            if self.sock:
                self.sock.close()
                self.sock = None

    def _do_recv(self):
        head = self._recv(4)
        if not head:
            return None
        body_len = int(head)

        log.debug('msg=recv body_len:%d', body_len)
        data = self._recv(body_len)
        return data

    def _do_send(self, data):
        size = self._send(data)

    def _response_error(self, respcd, msg):
        log.warn('_response_error, respcd=%s, msg=%s', respcd, msg)
        self.retobj = deepcopy(self.obj)
        self.retobj['txndir'] = 'A'
        self.retobj['respcd'] = respcd
        self.retobj['respmsg'] = msg

    def _connect(self):
        sock = None
        self.start_time = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.connect_timeout)
            sock.connect((self.ip, self.port))
        except socket.error, e:
            log.warn('server=%s:%d|error=connect_fail', self.ip, self.port)
            raise

        log.debug('server=%s:%d|action=connect|time=%d', self.ip, self.port, int(time.time()-self.start_time))
        self.sock = sock

    def _send(self, data):
        dtime = self.total_timeout - (time.time() - self.start_time)
        while True:
            self.sock.settimeout(dtime)
            try:
                size = self.sock.send(data)
            except socket.error, e:
                if e.args[0] == socket.EINTR:
                   continue
                else:
                    log.warn('server=%s:%d|func=send|error=', self.ip, self.port, str(e))
                    return

            dtime = self.total_timeout - (time.time() - self.start_time)
            if size < len(data):
                data = data[size:]
            else:
                # success
                return
            if dtime <= 0:
                log.warn('server=%s:%d|func=send|error=timeout',self.ip, self.port)
                return

    def _recv(self, size):
        buf = ''
        while True:
            dtime = self.total_timeout - (time.time() - self.start_time)
            if dtime <= 0:
                log.warn('server=%s:%d|func=recv|error=timeout', self.ip, self.port)
                return buf

            self.sock.settimeout(dtime)
            try:
                data = self.sock.recv(size-len(buf))
            except socket.error, e:
                if e.args[0] == socket.EINTR:
                   continue
                else:
                    log.warn('server=%s:%d|func=recv|error=%s', self.ip, self.port, str(e))
                    return buf

            if len(data) == 0:
                log.debug('peer disconnect')
                return buf

            buf += data
            if size == len(buf):
                return buf

    def _do_secret(self):
        '''
            暂时保留，之前更新秘钥使用的
        '''
        log.debug('recv newkey')
        recv_data_newkey = self._do_recv()

        newkey_obj = None
        try:
            newkey_obj = json.loads(recv_data_newkey)
        except:
            log.warn('parse newkey body error')
            self._response_error(RETCD_SYS_ERROR, 'parse newkey body error')
            return

        newkey_obj['respcd'] = '00'
        self.retobj = newkey_obj
        send_data_newkey = json.dumps(newkey_obj)
        send_data_newkey = '%04d%s' % (len(send_data_newkey), send_data_newkey)
        self._do_send(send_data_newkey)
        if self.sock is None:
            log.warn('send newkey response error')
            self._response_error(RETCD_SYS_ERROR, 'send newkey response error')
            return

