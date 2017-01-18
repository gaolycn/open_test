#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import traceback
import json
import struct

from qfcommon.conf import MSGPASS_CONF
from qfcommon.thriftclient.msgpass import MsgPass
from qfcommon.server.client import ThriftClient

log = logging.getLogger()

RET_OK = struct.pack('I',0)

def recvall(sock, count):
    buf = ''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return buf
        buf += newbuf
        count -= len(newbuf)
    return buf

def unsubscribe(handler_dict, project_name, addr, msgpass_server=None):
    for i in msgpass_server or MSGPASS_CONF:
        client = ThriftClient(i, MsgPass)
        client.unsubscribe(handler_dict.keys(), project_name, addr)
        client.close()

def subscribe_http(msg_list, project_name, addr, msgpass_server=None):
    for i in msgpass_server or MSGPASS_CONF:
        client = ThriftClient(i, MsgPass)
        client.subscribe_http(msg_list, project_name, addr)
        client.close()

def subscribe_thrift(msg_list, project_name, addr, msgpass_server=None):
    for i in msgpass_server or MSGPASS_CONF:
        client = ThriftClient(i, MsgPass)
        client.subscribe_thrift(msg_list, project_name, addr)
        client.close()

def publish(name, content_list, msgpass_server=None):
    '''
    发布消息 content 可以为一个 str list
    '''
    try:
        if not isinstance(content_list, list):
            content_list = [content_list]


        client = ThriftClient(msgpass_server or MSGPASS_CONF, MsgPass)
        for c in content_list:
            client.publish(name, c)

        client.close()
    except:
        log.error('server=MsgPass|func=publish|name=%s|err=%s', name, traceback.format_exc())

__is_running = True

def stop():
    global __is_running

    __is_running = False

def subscribe_gevent(handler_dict, project_name, addr, msgpass_server=None):
    '''
    注册消息接受处理函数
        msg: func(content)
    返回值根据情况处理
        server.stop()

    '''
    import gevent
    from gevent.server import StreamServer
    from gevent import spawn

    def handle(sock, addr):
        global __is_running

        while __is_running:
            try:
                with gevent.Timeout(2):
                    l = recvall(sock, 4)
                    if not l:
                        break
                data = recvall(sock,int(struct.unpack('I', l)[0]))
                if not data:
                    break
                sock.send(RET_OK)

                data = json.loads(data)
                func = handler_dict.get(data.get('msg'))
                if func:
                    spawn(func, data.get('data'))
            except gevent.Timeout:
                continue
            except:
                log.error(traceback.format_exc())
                break

    ip, port = addr.split(':',1)
    port = int(port)
    server = StreamServer(('0.0.0.0', port), handle = handle)
    spawn(server.serve_forever)

    log.info('server=MsgPass|func=listen|port=%d', port)

    for i in msgpass_server or MSGPASS_CONF:
        client = ThriftClient(i, MsgPass)
        client.open()

        client.subscribe(handler_dict.keys(), project_name, addr)
        client.close()

    return server

def subscribe_thread(handler_dict, project_name, addr, pool_size=10, msgpass_server=None):
    '''
    注册消息接受处理函数
        msg: func(content)

    返回值根据情况处理
        server.shutdown()
        server.server_close()
    '''
    from qfcommon.server.threadpool import ThreadPool,Task
    from SocketServer import ThreadingTCPServer, BaseRequestHandler
    import threading

    pool = ThreadPool(pool_size)
    pool.start()

    class SimpleTask(Task):
        def run(self):
            return self._func(*self._args, **self._kwargs)

    class Handler(BaseRequestHandler):

        def handle(self):
            while 1:
                try:
                    l = self.request.recv(4)
                    if not l:
                        break
                    data = self.request.recv(int(struct.unpack('I', l)[0]))
                    if not data:
                        break
                    self.request.send(RET_OK)

                    data = json.loads(data)

                    func = handler_dict.get(data.get('msg'))
                    if func:
                        task = SimpleTask(func, data.get('data'))
                        self.server.pool.add(task)
                except:
                    log.error(traceback.format_exc())
                    break

    ip, port = addr.split(':',1)
    port = int(port)

    server = ThreadingTCPServer(('0.0.0.0', port), Handler)
    server.pool = pool
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    log.info('server=MsgPass|func=listen|port=%d', port)

    for i in msgpass_server or MSGPASS_CONF:
        client = ThriftClient(i, MsgPass)
        client.open()

        client.subscribe(handler_dict.keys(), project_name, addr)
        client.close()

    return server









