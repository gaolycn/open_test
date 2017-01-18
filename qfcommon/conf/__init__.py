# coding: utf-8
import os
import yaml

rtenv = os.environ.get("QFRT", 'PRODUCT').lower()
rtenv = rtenv if rtenv in ('debug', 'qa', 'sandbox', 'product') else 'product'

FRAMEWORK = 'tornado'
USER_DB = 'qf_core'
SERVER_CONF_FILE = '/home/qfpay/qfconf/server.yaml'
SERVER_CONF = yaml.load(open(SERVER_CONF_FILE))

SESSION_CONF = SERVER_CONF.get('session', {}).get(rtenv)
MSGPASS_CONF = SERVER_CONF.get('msgpass', {}).get(rtenv)
ETCD_CONF = SERVER_CONF.get('etcd', {}).get(rtenv)

def set_framework(name):
    global FRAMEWORK
    FRAMEWORK = name


def set_userdb(name):
    global USER_DB
    USER_DB = name


def set_server_conf(rtenv):
    global SESSION_CONF
    SESSION_CONF = SERVER_CONF['session'][rtenv]
