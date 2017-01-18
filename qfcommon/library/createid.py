# coding:utf-8
# 各种id生成算法
import os, sys
import time
import struct
import binascii
import uuid
import base64
import threading
import datetime

_inc = 1

# 4B(time) + 3B(hostid) + 2B(pid) + 3B(inc)
def new_id(hostid=None, enc='bcd'):
    if not hostid:
        hostid = os.environ.get('HOSTNAME','localhost')
    hostid = hash(hostid) % 16777216
    pid = os.getpid()
    global _inc
    n = _inc % 16777216
    _inc += 1
    p3 = ((pid & 0xff)<<24)|n
    p2 = (hostid << 8) | (pid >> 8)
    s = struct.pack('III',int(time.time()), p2, p3)
    #print repr(s)
    if enc == 'b32':
        return base64.b32encode(s).strip('=')
    elif enc == 'b64':
        return base64.b64encode(s).strip('=')
    return binascii.hexlify(s)

def unpack_time_id(s, enc='bcd'):
    x = ''
    if enc == 'b32':
        x = base64.b32decode(s+'====')
    elif enc == 'b64':
        x = base64.b64decode(s+'======')
    else:
        x = binascii.unhexlify(s)
    #print repr(x)
    ret = struct.unpack('III', x)[0]
    return ret


def new_id2(enc='b32'):
    if enc == 'b32':
        return base64.b32encode(uuid.uuid4().bytes).strip('=')
    elif enc == 'b64':
        return base64.b64encode(uuid.uuid4().bytes).strip('=')
    else:
        return uuid.uuid4().hex
    x = uuid.uuid4()
    t = time.localtime()
    s = '%d%02d' % (t[0], t[1])
    if enc == 'b32':
        return s[2:] + base64.b32encode(x.bytes).strip('=')
    elif enc == 'b64':
        return s[2:] + base64.b64encode(x.bytes).strip('=')
    else:
        return s[2:] + x.hex

new_id_str = new_id2


seq = 0
_seq_locker = threading.Lock()
# msec(42b) + server_id(10b) + seq(12b) 
def new_id_long(server_id=None, **kwargs):
    msec = int(time.time()*1000)
    if server_id is None:
        host = os.environ.get('HOSTNAME','hostname')
        server_id = hash(host) % 1024
    global seq, _seq_locker
    _seq_locker.acquire() 
    seq += 1
    _seq_locker.release()
    return (msec << 22) + (server_id << 12) + seq

def unpack_id_long(xid):
    msec = (xid >> 22)
    server_id = (xid >> 12) & 0x02ff
    return msec, server_id


def new_id_mysql_uuid(conn):
    ret = conn.get("select uuid_short()", isdict=False)
    return ret[0]

def unpack_id_mysql_uuid(mid):
    sec = (mid >> 24) & 0xffffffff
    server_id = mid >> 56
    return sec, server_id


# msec(42b) + server_id(6b) + seq(16b) 
def new_id64(**kwargs):
    conn = kwargs['conn']
    msec = int(time.time()*1000)
    ret  = conn.get("select uuid_short()", isdict=False)
    uuid = ret[0]
    seq  = uuid % 65535;
    return (msec << 22) + (conn.server_id << 16) + seq

def unpack_id64(xid):
    msec = (xid >> 22)
    server_id = (xid >> 16) & 0xffff
    return msec, server_id

def unpack_time_id64(xid):
    msec = (xid >> 22)
    return datetime.datetime.fromtimestamp(int(msec/1000.0))

def test():
    print 'new_id b32'
    for i in range(0, 10):
        ret =  new_id(enc='b32')
        print len(ret), ret, unpack_time_id(ret, enc='b32'), time.time()

    print 'new_id b64'
    for i in range(0, 10):
        ret =  new_id(enc='b64')
        print len(ret), ret, unpack_time_id(ret, enc='b64'), time.time()


    print 'new_id'
    for i in range(0, 10):
        ret =  new_id()
        print len(ret), ret, unpack_time_id(ret), time.time()

    print 'new_id2 b32'
    for i in range(0, 10):
        ret =  new_id2()
        print len(ret), ret

    print 'new_id2 b64'
    for i in range(0, 10):
        ret =  new_id2('b64')
        print len(ret), ret


    #for i in range(0, 10):
    #    ret =  new_id3()
    #    print len(ret), ret

    #for i in range(0, 10):
    #    ret =  new_id3('b64')
    #    print len(ret), ret

    start = time.time()
    n = 10
    idset = set() 
    for i in range(0, n):
        ret = new_id_long()
        #print ret, unpack_id_long(ret)
        idset.add(ret)
        #time.sleep(0.1)
    print 'n=%d, idset=%d' % (n, len(idset))
    print 'use:', time.time()-start

    sec,sid = unpack_id_mysql_uuid(167878339694689191)
    print sec, sid, datetime.datetime.fromtimestamp(sec)

def test2():
    from qfcommon.base import logger, dbpool
    logger.install('stdout')
    DATABASE = {'test': # connection name, used for getting connection from pool
                {'engine':'mysql',   # db type, eg: mysql, sqlite
                 'db':'test',        # db name
                 'host':'127.0.0.1', # db host
                 'port':3306,        # db port
                 'user':'qf',      # db user
                 'passwd':'123456',  # db password
                 'charset':'utf8',   # db charset
                 'conn':2}          # db connections in pool
           }

    dbpool.install(DATABASE)

    with dbpool.get_connection('test') as conn:
        for i in range(0, 10):
            myid = new_id64(conn=conn)
            print time.time(), time.localtime()[:]
            print myid,
            unpack_id64(myid)
            print unpack_time_id64(myid)

if __name__ == '__main__':
    #test()
    test2()



