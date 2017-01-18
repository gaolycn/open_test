#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import types
import datetime
import urllib
import urllib2
import logging

from qfcommon.base.tools import smart_utf8

ALIPAY_WAP_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm'
ALIPAY_WAP_SERVICE_CREATE_DIRECY = 'alipay.wap.trade.create.direct'
ALIPAY_WAP_SERVICE_AUTH_AND_EXECUTE = 'alipay.wap.auth.authAndExecute'

log = logging.getLogger()

def str2dict(s):
    b = s.split('&')
    para = {}
    for i in b:
        c = i.split('=',1)
        para[c[0]] = c[1]
    return para

class AlipayWap(object):
    def __init__(self, pid, key, account, callback_url='', notify_url = '', merchant_url=''):
        self.pid = pid
        self.key = smart_utf8(key)
        self.account = account
        self.callback_url = callback_url
        self.notify_url = notify_url
        self.merchant_url = merchant_url
        self.charset = 'utf-8'
        self.sign_type = 'MD5'
        self.format = 'xml'
        self.v = '2.0'

    def serialize_xml(self, root, sep=''):
        '''sep 可以为 \n'''
        xml = ''
        for key in root.keys():
            if type(key) == types.StringType:
                u_key = key.decode('utf-8')
            else:
                u_key = unicode(key)
            if type(root[key]) == types.DictType:
                xml = '%s<%s>%s%s</%s>%s' % (xml, u_key, sep, self.serialize_xml(root[key], sep), u_key, sep)
            elif type(root[key]) == types.ListType:
                xml = '%s<%s>' % (xml, u_key)
                for item in root[key]:
                    xml = '%s%s' % (xml, self.serialize_xml(item,sep))
                xml = '%s</%s>' % (xml, u_key)
            else:
                value = root[key]
                if type(value) == types.StringType:
                    value = value.decode('utf-8')
                xml = '%s<%s>%s</%s>%s' % (xml, u_key, value, u_key, sep)
        return xml

    @staticmethod
    def check_sign(params, alikey, charset='utf-8'):
        if 'sign' in params:
            keys = params.keys()
            keys.sort()
            query = []
            for key in keys:
                if key not in ('sign', 'sign_type'):
                    query.append('%s=%s' % (key, params[key]))

            data = '&'.join(query) + alikey
            if not isinstance(data, types.UnicodeType):
                data = data.decode('utf-8')

            md5 = hashlib.md5()
            md5.update(data.encode(charset))
            return params['sign'] == md5.hexdigest()
        return False

    @staticmethod
    def add_sign(params, alikey, charset='utf-8'):
        keys = params.keys()
        keys.sort()

        unsigned_data = ''
        for key in keys:
            unsigned_data += smart_utf8(key) + '=' + smart_utf8(params[key])
            if key != keys[-1]:
                unsigned_data += '&'
        unsigned_data += smart_utf8(alikey)
        md5 = hashlib.md5()
        md5.update(unsigned_data.decode('utf-8').encode(charset))
        sign = md5.hexdigest()

        params['sign'] = sign

        return params

    def create_direct(self, subject, out_trade_no, total_fee, out_user = ''):
        '''预下单获取令牌'''
        if not isinstance(subject, types.UnicodeType):
            subject = subject.decode('utf-8')

        req_data_dict = {
            'direct_trade_create_req':{
                'subject':subject,
                'out_trade_no':out_trade_no,
                'total_fee':total_fee,
                'seller_account_name':self.account,
                'call_back_url':self.callback_url,
                'notify_url':self.notify_url,
                'out_user':out_user,
                'merchant_url':self.merchant_url,
                'pay_expire':'3600',
                #'agent_id':'',
            }
        }
        req_data = self.serialize_xml(req_data_dict)

        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        param = {
            'service':ALIPAY_WAP_SERVICE_CREATE_DIRECY,
            'format':self.format,
            'v':self.v,
            'partner':self.pid,
            'req_id':out_trade_no +'_'+ time_str,
            'sec_id':self.sign_type,
            'req_data':smart_utf8(req_data),
            '_input_charset':self.charset,
        }
        param = AlipayWap.add_sign(param, self.key)
        return param

    def auth_and_execute(self, request_token):
        '''令牌生成url'''
        req_data_dict = {
            'auth_and_execute_req':{
                'request_token':request_token,
            }
        }
        req_data = self.serialize_xml(req_data_dict)

        param = {
            'service':ALIPAY_WAP_SERVICE_AUTH_AND_EXECUTE,
            'format':self.format,
            'v':self.v,
            'partner':self.pid,
            'sec_id':self.sign_type,
            'req_data':smart_utf8(req_data),
            '_input_charset':self.charset,
        }
        param = AlipayWap.add_sign(param, self.key)
        return param


#-----------test----------------


def test_create_direct():
    partner = '2088711407753777'
    alipay_key = 'kfy8iitaqvki7wlsvu9p4tb9bp54goke'
    seller_email = 'mmhz@qfpay.com'
    a = AlipayWap(partner,alipay_key,seller_email)
    data = a.create_direct(u'测试商品','123','0.01')
    print data
    data = urllib.urlencode(data, 'utf-8')
    res =  urllib2.urlopen(ALIPAY_WAP_GATEWAY,data)

    ret = urllib.unquote_plus(res.read())
    print ret

def test_auth():
    partner = '2088711407753777'
    alipay_key = 'kfy8iitaqvki7wlsvu9p4tb9bp54goke'
    seller_email = 'mmhz@qfpay.com'
    a = AlipayWap(partner,alipay_key,seller_email)
    data = a.auth_and_execute('2015032540c69a7f7ba106b7d8f8569b07a30a91')
    data = urllib.urlencode(data)
    print data

def test_all_in_one():
    partner = '2088711407753777'
    alipay_key = 'kfy8iitaqvki7wlsvu9p4tb9bp54goke'
    seller_email = 'mmhz@qfpay.com'
    a = AlipayWap(partner,alipay_key,seller_email,'http://1.qfpay.com/','http://1.qfpay.com','http://1.qfpay.com')
    data = a.all_in_one('测试商品','yushijun123','0.01')
    print data

if __name__ == '__main__':
    #test_all_in_one()
    test_create_direct()
    #test_auth()






