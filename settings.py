#encoding:utf8
from qiantai_config import *
from qiantai_util import *
import urllib

'''
设置钱台相关信息
set_bankinfo  设置清算信息
'''

def set_bankinfo(method='post',**kwargs):
    url = '%s/setting/v1/bankinfo'%QT_API
    if method == "post":
        param = {
            'caller':'server',
            'app_code':TEST_APP['app_code'],
            #'bank_type':1,
            'head_bank_name':u'中国民生银行',
            'bank_user': u'刘四泉',
            'bank_account': '6226220104400865',
                }
        param.update(kwargs)
        create_sign(param,TEST_APP['server_key'])
        senddata = urllib.urlencode(param)
        data = post(url,senddata)
        return data
    else:
        param = {
            'caller':'server',
            'app_code':TEST_APP['app_code'],
            }
        param.update(kwargs)
        create_sign(param,TEST_APP['server_key'])
        sendurl= url + '?' + urllib.urlencode(param)
        data = get(sendurl)
        return data
