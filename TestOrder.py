        
# coding: utf-8
'''订单测试'''

import json
import time
import datetime
import urllib
from qiantai_config import *
from qiantai_util import *
import random 
import nose
import cmp_struct
from qfcommon.base import dbpool
from qfcommon.base.dbpool import with_database
dbpool.install(DATABASE)

class TestOrder:
    def setUp(self):
        self.txamt = 11        
        
    def test_order_saoma(self):
        '''
        钱台订单： 测试微信扫码预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800201,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        print data
        struct = {u'cardcd': u'',u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_order_add_trade_name(self):
        '''
        钱台订单： 测试交易增加trade_name字段（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800201,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'trade_name': 'kaer_Y',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print data
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')

    def test_order_app(self):
        '''
        钱台订单： 测试微信扫码预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800210,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        submchnt=''
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=submchnt)
        #print data
        struct = {u'cardcd': u'',u'pay_type': u'', u'sysdtm': u'', u'cardcd': u'', u'resperr': u'', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14633944799951', u'syssn': u'20160516124500020005341807', u'pay_params': {u'package': u'Sign=WXPay', u'timestamp': u'1463394480', u'sign': u'49357F2C967ED1DB05718D486B199882', u'partnerid': u'1298257101', u'appid': u'wx087a3fc3f3757766', u'prepayid': u'wx20160516182800851177b3350003221281', u'noncestr': u'71662d73503b4cd297eddebb685bfaa4'}, u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
    
    def test_order_micropay(self):
        '''
        钱台订单： 测试微信刷卡支付（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        #auth_code = str(int(time.time() *1000000)) + str(random.randrange(10,99))
        auth_code = '130132752777533864'
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800208,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'auth_code': auth_code,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result \n',data
        struct = {u'pay_type': u'800208', u'resperr': u'\u4ea4\u6613\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\uff0c\u6216\u8054\u7cfb\u94b1\u65b9\u5ba2\u670d(1101)', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 17:18:18', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556142982734', u'syssn': u'20160216355271', u'respcd': u'1101'}
        
        nose.tools.ok_(data.get('respcd')=='1202', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_order_h5(self):
        '''
        钱台订单： 测试微信公众账号预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800207,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #'sub_openid':'oo3Lss4RHF6LNDv2iYt3YUn50Zsg',
                }
        if DEBUG_MODE != 'offline':
            param['sub_openid']='oo3Lss4RHF6LNDv2iYt3YUn50Zsg'
        else:
            param['sub_openid']='oYkCztyemzMxwKHFYXlKrH1M4m3c'
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result\n',data
        struct = {u'pay_type': u'800207', u'sysdtm': u'2016-02-17 14:13:51', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-17 14:13:50', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556896309805', u'syssn': u'20160217355282', u'pay_params': {u'package': u'prepay_id=wx20160217141351f9afbe18f90426146429', u'timeStamp': u'1455689631', u'signType': u'MD5', u'paySign': u'F36C1706B2C92F496E4977093E02363E', u'appId': u'wx370e5f2f9001f90b', u'nonceStr': u'523ca46a375e4b5f8bf7bd231c6045dd'}, u'respcd': u'0000'} 
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        #print 'struct\n',struct
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_submchnt_wx(self):
        '''
        钱台订单： 测试微信子商户下单（/trade/v1/payment）
        条件：子商户id 11754  // 10205 账户使用中信账号不能交易 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800207,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #'openid':'oMGYCj7dkqBDjry172r83XgD-t3s',
                'sub_openid':'oo3Lss4RHF6LNDv2iYt3YUn50Zsg',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt='la33S8k8')
        print data
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        struct = {u'cardcd': u'',u'pay_type': u'800207', u'sysdtm': u'2016-03-23 20:25:11', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-03-23 20:25:11', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14587359113311', u'syssn': u'20160323801075', u'pay_params': {u'package': u'prepay_id=wx201603232025111667d839410381315372', u'timeStamp': u'1458735911', u'signType': u'MD5', u'paySign': u'698378C5D0A953F0140715B991F631AF', u'appId': u'wx370e5f2f9001f90b', u'nonceStr': u'95c8a15cae02421489f23f13eee65e6c'}, u'respcd': u'0000'}
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def ttest_order_alipay_saoma(self):
        '''
        钱台订单： 测试支付宝扫码预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800101,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result',data
        struct = {u'pay_type': u'800108', u'resperr': u'', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 17:18:18', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556142982734', u'syssn': u'20160216355271', u'respcd': u'1101'}
        #struct = {u'pay_type': u'800108', u'resperr': u'',  u'txdtm': u'2016-02-16 17:18:18', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556142982734', u'syssn': u'20160216355271', u'respcd': u'1101'}
        
        #print 'old: ', struct
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def ttest_order_alipay_fansao(self):
        '''
        钱台订单： 测试支付宝刷卡下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800108,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'auth_code':'284184993278765276',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        # print 'result',data
        struct = {u'pay_type': u'800108', u'resperr': u'', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 17:18:18', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556142982734', u'syssn': u'20160216355271', u'respcd': u'1101'}
        nose.tools.ok_(data.get('respcd')=='1145', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def ttest_order_alipay_h5(self):
        '''
        钱台订单： 测试支付宝h5预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期：暂不支持 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                'txcurrcd': 'CNY',
                'pay_type': 800107,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #'openid':'oMGYCj7dkqBDjry172r83XgD-t3s',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result\n',data
        struct = {u'pay_type': u'800207', u'sysdtm': u'2016-02-17 14:13:51', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-17 14:13:50', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556896309805', u'syssn': u'20160217355282', u'pay_params': {u'package': u'prepay_id=wx20160217141351f9afbe18f90426146429', u'timeStamp': u'1455689631', u'signType': u'MD5', u'paySign': u'F36C1706B2C92F496E4977093E02363E', u'appId': u'wx370e5f2f9001f90b', u'nonceStr': u'523ca46a375e4b5f8bf7bd231c6045dd'}, u'respcd': u'0000'} 
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        #print 'struct\n',struct
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
    def test_order_other_param(self):
        '''
        钱台订单： 测试增加其他参数预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        param_list = ['goods_name','goods_info','pay_limit','udid','mchntid'] 
        for p in param_list: 
            out_trade_sn = int(time.time()*10000)
            param = {
                    'txamt'   : self.txamt,
                    'txcurrcd': 'CNY',
                    'pay_type': 800201,
                    'out_trade_no': out_trade_sn,
                    'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
            if p == "goods_name":
                param['goods_name'] = 'goods'

            if p == "goods_info":
                param['goods_info'] = 'goods_info'

            if p == "pay_limit":
                param['pay_limit'] = "no_credit"
            
            if p == "udid":
                param['udid'] = "abcdef"
            
            if p == "mchntid":
                param['mchntid'] = "abc123"

            sign = create_sign(param,TEST_APP['key'])
            req = urllib.urlencode(param)
            data = post(url,req,sign)
            #print 'result: %s'%p,"===",param
            #print 'result: %s'%p,"===",data
            struct = {u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
            nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_order_submchnt(self):
        '''
        钱台订单： 测试下单时使用子商户且商户信息在消息体中（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        if DEBUG_MODE == 'offline':
            mchid = 'B7eeimnZ'
        else:
            mchid = 'ZOkq8uOqdP'
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'          : self.txamt,
                'txcurrcd'       : 'CNY',
                'pay_type'       : 800201,
                'out_trade_no'   : out_trade_sn,
                'mchid'          : mchid,
                'txdtm'          : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result: ',data
        struct = {u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_order_paylimit(self):
        '''
        钱台订单： 测试微信下单限制信用卡（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                   'txamt'   : self.txamt,
                   'txcurrcd': 'CNY',
                   'pay_type': 800201,
                   'out_trade_no': out_trade_sn,
                   'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'limit_pay': 'no_credit',
                   }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result: %s'%p,"===",param
        struct = {u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
    
    def test_order_paylimit_h5(self):
        '''
        钱台订单： 测试微信下单H5限制信用卡（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                   'txamt'   : self.txamt,
                   'txcurrcd': 'CNY',
                   'pay_type': 800207,
                   'out_trade_no': out_trade_sn,
                   'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'limit_pay': 'no_credit',
                   'sub_openid': 'oYkCztwXJe86LKgVmoEAll3eU9sY',
                   }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result: %s'%p,"===",param
        #print 'result: ',data
        struct = {u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        #nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')


    def test_order_txcurrcd(self):
        '''
        钱台订单： 测试商户港币预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        self.txamt = 10
        param = {
                   'txamt'          : self.txamt,
                   'txcurrcd'       : 'HKD',
                   'pay_type'       : 800201,
                   'out_trade_no'   : out_trade_sn,
                   'txdtm'          : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #print 'result: %s'%p,"===",param
        #print 'result: ',data
        struct = {u'pay_type': u'800201', u'sysdtm': u'2016-02-16 16:03:20', u'resperr': u'\u4ea4\u6613\u6210\u529f', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-16 16:03:20', u'txamt': u'1', u'respmsg': u'', u'out_trade_no': u'14556098000975', u'syssn': u'20160216355258', u'qrcode': u'weixin://wxpay/bizpayurl?pr=wd71tMi', u'respcd': u'0000'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def other_check(self):
        '''
        钱台订单： 测试子商户模式微信增加其他参数预下单（/trade/v1/payment）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        for a in range(0,2):
            param = {
                   'txamt'   : self.txamt,
                   'txcurrcd': 'CNY',
                   'pay_type': 800201,
                   'out_trade_no': out_trade_sn,
                   'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                   'pay_limit': 'no_credit',
                   }
            sign = create_sign(param,TEST_APP['key'])
            req = urllib.urlencode(param)
            data = post(url,req,sign)
            #print 'result: ',data


    @with_database('qf_trade')
    def _update_order(self,**kwargs):
        where = {}
        where.update(**kwargs)
        values = {
            'status': 0,
            'sysdtm':datetime.datetime.now().strftime('%Y-%m-%d 00:00:01'),
            'txdtm' :datetime.datetime.now().strftime('%Y-%m-%d 00:00:01'),
                }
        self.db.update('record_201602', values, where=where)

    def ttest_close_out_trade(self):
        '''
        订单关闭： 测试关闭订单（/trade/v1/close）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        out_trade_no = '14555915664200'
        order_status = {
                'out_trade_no':out_trade_no, 
                }
        self._update_order(**order_status)
        param = {
                'txamt'   : self.txamt,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req  = urllib.urlencode(param)
        data = post(url,req,sign)
        #self.data = pre_create(**param)
        struct = {u'resperr': u'(1146)', u'respcd': u'1146', u'respmsg': u'', u'syssn': u'20160218355381', u'orig_syssn': u'20160216355248'}
        nose.tools.ok_(data.get('respcd')=='1146', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')


def re_notify(order_no=None):
    url='%s/order/notify?out_trade_no=%s'%(WXCHAT,order_no)
    req = urllib2.Request(url)
    print urllib2.urlopen(req).read()
    return url



