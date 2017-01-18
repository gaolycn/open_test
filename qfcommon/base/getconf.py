# coding: utf-8
import os, sys
import time
import socket
import traceback
import json
import logging
import codecs

import qfcommon.conf
from qfcommon.server.client import HttpClient


log = logging.getLogger()

'''
config: /qfconf/service/base         eg: /qfconf/spring/base
        用来表示这个项目的公用配置

        /qfconf/service/host_deploy  eg: /qfconf/spring/BJ-PAY-01_spring.0
        用来表示这个项目的部署配置

name:   /qfname/service/base         eg: /qfconf/spring/base
        用来表示这个手动配置的服务器列表

        /qfname/service/host_deploy  eg: /qfconf/spring/BJ-PAY-01_spring.0
        用来表示这个上报的服务器列表

env:    /qfenv/service/base         eg: /qfconf/spring/base
        用来配置公用的环境规则

        /qfenv/service/host_deploy  eg: /qfconf/spring/BJ-PAY-01_spring.0
        用来配置单个部署的环境规则
'''

ETCD_SERVER = qfcommon.conf.ETCD_CONF
ETCD_SERVICE = os.environ.get('ETCD_SERVICE','')
ETCD_DEPLOY = os.environ.get('ETCD_DEPLOY','')
ETCD_HOST = socket.gethostname()
ETCD_INDEX = {}  # path:index

def install(module = 'config', path='config.json'):
    conf = get_conf()
    config = ConfObj(conf)

    sys.modules[module] = config

    if path:
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(json.dumps(config.data, indent=2, ensure_ascii=False))

    return config

class ConfObj:
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data[key]

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        return str(self.data)

def get_value(path, wait=False, index = 1):
    global ETCD_SERVER,ETCD_INDEX

    value = {}
    try:
        if wait:
            client = HttpClient(ETCD_SERVER, log_except=False)
        else:
            client = HttpClient(ETCD_SERVER)

        # 如果是watch
        if wait:
            ret = client.get(path, {'wait':'true', 'waitIndex':index})
        else:
            ret = client.get(path)

        if ret:
            ret = json.loads(ret)
            #缓存index
            headers = client.client.headers
            ETCD_INDEX[path] = int(headers.get('X-Etcd-Index', 0))
            #如果是目录
            if ret.get('node',{}).get('dir',False):
                nodes = ret.get('node',{}).get('nodes',{})
                for node in nodes:
                    #TODO 忽略目录 忽略多级 理论应该递归处理
                    #如果是节点
                    if not node.get('dir',False) and not node.get('key','').endswith('/base'):
                        value[node.get('key','')] = json.loads(node.get('value','{}'))
            #如果是节点
            else:
                j = ret.get('node',{}).get('value')
                if j:
                    value = json.loads(j)
    except:
        log.warn(traceback.format_exc())
    if not wait:
        log.info('server=etcd|func=get|path=%s|value=%s'%(path,value))
    return value

def set_value(path, value={}, ttl=None):
    global ETCD_SERVER

    data = {}

    if isinstance(value, basestring):
        data['value'] = value
    else:
        data['value'] = json.dumps(value)
    if ttl:
        data['ttl'] = ttl

    log.info('server=etcd|func=set|path=%s|value=%s|ttl=%s'%(path,value,ttl))

    try:
        client = HttpClient(ETCD_SERVER)
        ret = client.put(path, data)
        if ret:
            ret = json.loads(ret)
            value = ret.get('node',{}).get('value')
            if value:
                value = json.loads(value)
                return value
    except:
        log.warn(traceback.format_exc())
    return {}

def watch_value(path, index=0):
    global ETCD_INDEX

    if not index:
        index = ETCD_INDEX.get(path, 1) + 1

    value = get_value(path=path, wait=True, index=index)
    log.info('server=etcd|func=watch|path=%s|index=%s|value=%s'%(path,index,value))
    return value

# --- CONF ---

def get_conf_base(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    base_conf_path = '/v2/keys/qfconf/%s/base' % (service)

    return get_value(base_conf_path)

def get_conf_deploy(service=None, host=None, deployname=None):
    global ETCD_SERVER,ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY

    if not service:
        service = ETCD_SERVICE
    if not host:
        host = ETCD_HOST
    if not deployname:
        deployname = ETCD_DEPLOY

    deploy_conf_path = '/v2/keys/qfconf/%s/%s_%s' % (service, host, deployname)

    deploy_conf = get_value(deploy_conf_path)
    return deploy_conf

def get_conf(service=None, host=None, deployname=None):
    global ETCD_SERVER,ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY

    if not service:
        service = ETCD_SERVICE
    if not host:
        host = ETCD_HOST
    if not deployname:
        deployname = ETCD_DEPLOY

    base_conf = get_conf_base(service)
    deploy_conf = get_conf_deploy(service, host, deployname)

    base_conf.update(deploy_conf)
    return base_conf

def watch_conf(service=None, host=None, deployname=None):
    global ETCD_SERVER,ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY

    if not service:
        service = ETCD_SERVICE
    if not host:
        host = ETCD_HOST
    if not deployname:
        deployname = ETCD_DEPLOY

    base_conf_path = '/v2/keys/qfconf/%s/base' % (service)
    deploy_conf_path = '/v2/keys/qfconf/%s/%s_%s' % (service, host, deployname)

    conf = {}

    base_conf = watch_value(base_conf_path)
    deploy_conf = watch_value(deploy_conf_path)

    conf.update(base_conf)
    conf.update(deploy_conf)

    return conf

def set_conf_base(service=None, conf={}):

    base_conf_path = '/v2/keys/qfconf/%s/base' % (service)
    return set_value(base_conf_path, conf)

def set_conf(service=None, host=None, deployname=None, conf={}):

    deploy_conf_path = '/v2/keys/qfconf/%s/%s_%s' % (service, host, deployname)
    return set_value(deploy_conf_path, conf)

# --- NAME ---

def get_name_base(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    base_name_path = '/v2/keys/qfname/%s/base' % (service)

    return get_value(base_name_path)

def get_name(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    name_path = '/v2/keys/qfname/%s/' % (service)

    name = get_value(name_path).values()

    return name

def watch_name_base(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    base_name_path = '/v2/keys/qfname/%s/base' % (service)

    return watch_value(base_name_path)

def watch_name(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    name_path = '/v2/keys/qfname/%s/' % (service)

    return watch_value(name_path).values()

def set_name_base(service=None, value=[]):
    base_name_path = '/v2/keys/qfname/%s/base' % (service)
    return set_value(base_name_path, value)

def set_name(service=None, host=None, deployname=None, value={}, ttl=300):
    name_path = '/v2/keys/qfname/%s/%s_%s' % (service, host, deployname)
    return set_value(name_path, value, ttl)

# --- ENV ---

def get_env_base(service=None):
    global ETCD_SERVICE

    if not service:
        service = ETCD_SERVICE

    base_env_path = '/v2/keys/qfenv/%s/base' % (service)

    return get_value(base_env_path)

def get_env_deploy(service=None, host=None, deployname=None):
    global ETCD_SERVER,ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY

    if not service:
        service = ETCD_SERVICE
    if not host:
        host = ETCD_HOST
    if not deployname:
        deployname = ETCD_DEPLOY

    deploy_env_path = '/v2/keys/qfenv/%s/%s_%s' % (service, host, deployname)

    return get_value(deploy_env_path)

def get_env(service=None, host=None, deployname=None):
    global ETCD_SERVER,ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY

    if not service:
        service = ETCD_SERVICE
    if not host:
        host = ETCD_HOST
    if not deployname:
        deployname = ETCD_DEPLOY

    base_env = get_env_base(service) or []
    deploy_env = get_env_deploy(service, host, deployname) or []

    base_env.extend(deploy_env)
    return base_env

def set_env_base(service=None, env=[]):

    base_env_path = '/v2/keys/qfenv/%s/base' % (service)
    return set_value(base_env_path, env)

def set_env(service=None, host=None, deployname=None, env=[]):

    deploy_env_path = '/v2/keys/qfenv/%s/%s_%s' % (service, host, deployname)
    return set_value(deploy_env_path, env)



def test_conf():
    base_conf = {
        'LOG':'paycore.log',
        'ADDE': ('127.0.0.1',1234),
    }
    deploy_conf = {
        'NAME':'paycore.0'
    }
    log.debug('set conf base')
    set_conf_base('paycore', base_conf)

    ret = get_conf_base('paycore')
    log.debug('get conf base %s'% ret)

    log.debug('set conf')
    set_conf('paycore', 'BJ-01', 'paycore.0', deploy_conf)

    ret = get_conf('paycore', 'BJ-01', 'paycore.0')
    log.debug('get conf %s'% ret)

    raw_input('watch')
    watch_conf('paycore','BJ-01','paycore.0')

def test_name():
    v = [{'addr':('127.0.0.1', 1000), 'timeout':1000}, {'addr':('127.0.0.1', 1001), 'timeout':1000}, {'addr':('127.0.0.1', 1002), 'timeout':1000}]
    v0 = {'addr':('127.0.0.1', 1000), 'timeout':1000}
    v1 = {'addr':('127.0.0.1', 1001), 'timeout':1000}

    set_name_base('paycore', v)
    set_name('paycore', 'BJ-PAY-01', 'paycore.0', v0, ttl=2)
    set_name('paycore', 'BJ-PAY-02', 'paycore.0', v1, ttl=5)

    bnm = get_name_base('paycore')
    print '-'*60
    print bnm

    time.sleep(3)
    print '-'*60, 'sleep 3'
    print get_name('paycore')

    time.sleep(3)
    print '-'*60, 'sleep 3'
    print get_name('paycore')

    print '-'*60, 'base'
    print get_name_base('paycore')

def test_env():
    global ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY
    ETCD_SERVICE= 'paycore'
    ETCD_HOST = 'BJ-01'
    ETCD_DEPLOY = 'paycore.0'

    base_env = [{'env1':'env1'}, {'env2': 'env2'}]

    deploy_env = [{'env3':'env3'}]

    set_env_base(ETCD_SERVICE, base_env)
    set_env(ETCD_SERVICE, ETCD_HOST, ETCD_DEPLOY, deploy_env)

    log.debug('base env %s', get_env_base())
    log.debug('deploy_env env %s', get_env_deploy())
    log.debug('all env %s', get_env())



def test_install():
    global ETCD_SERVICE,ETCD_HOST,ETCD_DEPLOY
    ETCD_SERVICE= 'paycore'
    ETCD_HOST = 'BJ-01'
    ETCD_DEPLOY = 'paycore.0'

    base_conf = {
        'LOG':'paycore.log',
        'ADDE': ('127.0.0.1',1234),
    }
    deploy_conf = {
        'NAME':'paycore.0'
    }
    log.debug('set conf base')
    set_conf_base('paycore', base_conf)

    install()
    import config
    print config.LOG
    print config['LOG']

    from config import LOG
    print LOG

def test():
    envs = [{
        'type': 'input',
        'cookie': 'G',
        'expire': 3,
        'rules': [
            ['a','>',10],
            ['req.path','=','/ping'],
        ],
    }]
    envs = [
        {
            'type': 'weight',
            'cookie': 'G',
            'expire': 3,
            'weight': 50,
        }
    ]
    set_env_base('openapi_trade',envs)

if __name__ == '__main__':
    from qfcommon.base import logger
    logger.install('stdout')
    # test_conf()
    # test_name()
    # test_env()
    # test_install()
    test()


