# coding: utf-8
import os, sys

#DEBUG_MODE = 'onlinesandbox'
DEBUG_MODE = 'offline'
if DEBUG_MODE == 'online':
    #线上正式
    QT_API   = 'https://openapi.qfpay.com'
    TEST_APP = {
    'app_code' : '17390DF8EA4446029D8F10AFB0C7FC35',
    'key'      : 'F11F1A116172464C9896253B8A4CDC09',
        }
elif DEBUG_MODE == 'offline':
    #线下测试
    #QT_API   = 'http://172.100.101.107:6200'
    QT_API   = 'https://openapi.qa.qfpay.net'
    WXCHAT   = 'http://172.100.101.106:8910'
    TEST_APP = {
    'app_code':'8085381F5F2F1C726C8232E61C96302D',
    'key'     :'5E37CAD08F0E7387D40825B37524B566',
        }
else:
    #线上沙盒
    QT_API   = 'https://openapi-test.qfpay.com'
    TEST_APP = {
    'app_code' : '17390DF8EA4446029D8F10AFB0C7FC35',
    'key'      : 'F11F1A116172464C9896253B8A4CDC09',
        }

DATABASE = { 
    "qf_trade": {
        'engine'  :  "mysql",
        'db'      :  "qf_trade",
        'user'    :  "qf",  
        'passwd'  :  "123456",
        'host'    :  "172.100.101.107", 
        'port'    :  3306, 
        'charset' :  "utf8",
        'conn'    :  2,
    },  
    "qf_open": {
        'engine'  :  "mysql",
        'db'      :  "qf_open",
        'user'    :  "qf",  
        'passwd'  :  "123456",
        'host'    :  "172.100.101.107", 
        'port'    :  3306, 
        'charset' :  "utf8",
        'conn'    :  2,
    },  

}



