# coding: utf-8
'''订单测试'''

import json
import time
import urllib
from qiantai_config import *
from qiantai_util import *
import random 
import nose
import settings
from nose.tools import with_setup,timed

class TestOrder:
    def setUp(self):
        self.url = '%s/trade/v1/query' %QT_API
    

    def test_close(self):
        '''
        订单关闭： 测试冲正订单（/trade/v1/close）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        import hashids
        userid = 10205
        submchnt = hashids.Hashids('qfpay').encode(11751,userid)
        param = {
                'txamt'   : 10,
                'mchid'   : submchnt,
                'syssn':'20160803998485',
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req  = urllib.urlencode(param)
        data = post(url,req,sign)
        print data
        '''

        a =  {'pay_type': '800208', 'goods_name': '\xe6\xb0\xb8\xe8\x83\x9c\xe8\xbe\x89\xe7\x94\x9f\xe6
        \xb4\xbb\xe6\x98\x93\xe8\xb4\xad', 'udid': '18100796959-a001', 'txcurrcd': 'CNY', 'txdtm': '2016-08-25 13:09:55', 'mchid': 'qAIN7SJLWW', 'txamt': '100', 'out_trade_no': '181007969592016082501000002', 'auth_code': '130149874644554100'}|{"resperr": "MCHCODE\u975e\u6cd5", "respcd": "1108", "respmsg": ""}
        '''
    def test_order(self):
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : 10,
                'txcurrcd': 'CNY',
                'pay_type': 800208,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'auth_code':'130083501481097212',
                'mchid' : 'qAlN7SJLWW', 
                }
        sign = create_sign(param,'2BB23268288F469CAB3CB9BA83D50562')
        req = urllib2.Request(url,urllib.urlencode(param))
        req.add_header("X-QF-SIGN", sign)
        req.add_header("X-QF-APPCODE", '8F644D7307D84F1296C524BF006BEFE8')
        res = urllib2.urlopen(req).read()
        data = json.loads(res)
        print data
    def test_refund(self):
        url = '%s/trade/v1/refund' %QT_API
        
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : 101,
                'syssn'   : '20161026423378', 
                #'syssn'   : '20161026388255', 
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #'mchid' : '', 
                }
        #sign = create_sign(param,TEST_APP['key'])
        sign = create_sign(param,TEST_APP['key'])
        request = urllib.urlencode(param)
        data = post(url,request,sign)
        print data
