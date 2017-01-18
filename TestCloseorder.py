        
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

class TestClassOrder:
    def setUp(self):
        self.txamt = random.randint(1,10)        

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

    def _create_order(self):
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
        #print 'crete: ', req
        return  post(url,req,sign)

    def test_close_outorder(self):
        '''
        订单关闭： 测试关闭外部订单（/trade/v1/close）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        param = {
                'txamt'   : self.txamt,
                'out_trade_no': self._create_order().get('out_trade_no'), 
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        #print 'out_trade_no',param.get('out_trade_no')
        sign = create_sign(param,TEST_APP['key'])
        req  = urllib.urlencode(param)
        data = post(url,req,sign)
        #self.data = pre_create(**param)
        struct = {u'resperr': u'(1146)', u'respcd': u'1146', u'respmsg': u'', u'syssn': u'20160218355381', u'orig_syssn': u'20160216355248'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_close_syssn(self):
        '''
        订单关闭： 测试使用钱台订单关闭（/trade/v1/close）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        param = {
                'txamt'   : self.txamt,
                'syssn'   : self._create_order().get('syssn'),
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #self.data = pre_create(**param)
        #print 'result',data
        struct = {u'resperr': u'(1146)', u'respcd': u'1146', u'respmsg': u'', u'syssn': u'20160218355381', u'orig_syssn': u'20160216355248'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
    
    def test_close_other(self):
        '''
        订单关闭： 测试使用非必传参数订单关闭（/trade/v1/close）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        param = {
                'txamt'   : self.txamt,
                'syssn'   : self._create_order().get('syssn'),
                'txdtm'   : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'udid'    : 'abcdef', 
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        #self.data = pre_create(**param)
        #print 'result',data
        struct = {u'resperr': u'(1146)', u'respcd': u'1146', u'respmsg': u'', u'syssn': u'20160218355381', u'orig_syssn': u'20160216355248'}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    def test_close_fail(self):
        '''
        订单关闭： 测试关闭订单失败（/trade/v1/close）
        条件：此接口不检查txamt和txdtm 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/close' %QT_API
        param = {
                'txamt'   : 11,
                'syssn'   : '2323432',#self._create_order().get('syssn'),
                'txdtm'   :  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        struct = {u'resperr': u'', u'respcd': u'1136', u'respmsg': u'', u'out_trade_no': u''}
        nose.tools.ok_(data.get('respcd')!='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
   

