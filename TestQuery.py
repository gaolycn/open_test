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

class TestQuery:
    def setUp(self):
        self.txamt = 1        
        self.url = '%s/trade/v1/query' %QT_API

    def _order(self):
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
        return data 
        
    @with_database('qf_trade')
    def _update_order(self,**kwargs):
        where = {}
        where.update(**kwargs)
        values = {
            'status': 0,
            'sysdtm':datetime.datetime.now().strftime('%Y-%m-%d 00:00:01'),
            'txdtm' :datetime.datetime.now().strftime('%Y-%m-%d 00:00:01'),
                }
        self.db.update('record_201604', values, where=where)

    @with_database('qf_trade')
    def _query_order(self,fields="*",**kwargs):
        where = {}
        where.update(**kwargs)
        #table = 'record_'+datetime.datetime.now().strftime('%Y%m')
        table = 'record_201604'
        select_sql = self.db.select_sql(table, where, fields = fields, other = 'order by id desc') 
        s = self.db.select_page(select_sql, 1, 10)
        #print s.todict()
        return len(s.todict())

    def test_query(self):
        '''
        订单查询： 订单查询失败（/trade/v1/query）
        条件： 
        操作： 
        预期：
        '''
        out_trade_sn = self._order().get('out_trade_no')
        param = {
                'out_trade_no': out_trade_sn,
                }
        
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(self.url,req,sign)
        #self.data = pre_create(**param)
        #print 'result',data
        struct = {u'resperr': u'\u8bf7\u6c42\u6210\u529f', u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'800201', u'sysdtm': u'2016-02-18 12:50:24', u'order_type': u'payment', u'txcurrcd': u'CNY', u'txdtm': u'2016-02-18 12:50:24', u'txamt': u'1', u'out_trade_no': u'14557710248461', u'syssn': u'20160218355384', u'cancel': u'0', u'respcd': u'1143', u'errmsg': u'\u4ea4\u6613\u9519\u8bef\uff0c\u8bf7\u8054\u7cfb\u94b1\u65b9\u5ba2\u670d'}], u'page': 1}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回respcd码错误')
        nose.tools.ok_(data['data'][0].get('respcd')=='1143', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')

    
    def test_query_OK(self):
        '''
        订单查询： 订单查询（/trade/v1/query）
        条件： 
        操作： 
        预期：
        '''
        syssn = '20160317800888'
        param = {
                #'out_trade_no': '',
                #'syssn':syssn,
                'start_time':datetime.datetime.now().strftime("%Y-%m-01 00:00:00"),
                'end_time': datetime.datetime.now().strftime("%Y-%m-%d %H:00:00"),
                'page':random.randint(1,10),
                'page_size':random.randint(2,10),
                
                }
            
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(self.url,req,sign)
        #print 'result',data
        #struct = {u'total_num': 1, u'resperr': u'', u'page_num': 1, u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
        struct = {u'resperr': u'',  u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}],u'page':1}
        struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        #print 'struct: \n',struct
        #nose.tools.ok_(data['data'][0].get('pay_type')=='800108', msg='返回码错误')
        #nose.tools.ok_(data['data'][0].get('respcd')=='1143', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回整体结构不一致')
        if data.get('data'):
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct2,data['data'][0]),msg='返回结构不一致')
        
    def test_query_mchnt_OK(self):
        '''
        订单查询： 子商户订单查询（/trade/v1/query）
        条件： 
        操作： 
        预期：
        '''
        syssn = '20160317800888'
        param = {
                'start_time':datetime.datetime.now().strftime("%Y-%m-01 00:00:00"),
                'end_time':datetime.datetime.now().strftime("%Y-%m-%d 23:23:00"),
                'page':1,
                'page_size':2,
                
                }
            
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(self.url,req,sign,mchnt='B7eeimnZ')
        #print 'result',data
        #struct = {u'total_num': 1, u'resperr': u'', u'page_num': 1, u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
        struct = {u'resperr': u'',  u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}],u'page':1}
        struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        #print 'struct: \n',struct
        #nose.tools.ok_(data['data'][0].get('pay_type')=='800108', msg='返回码错误')
        #nose.tools.ok_(data['data'][0].get('respcd')=='1143', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回整体结构不一致')
        if data.get('data'):
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct2,data['data'][0]),msg='返回结构不一致')

    def test_query_other_param(self):
        '''
        订单查询： 非必要参数订单查询（/trade/v1/query）
        条件： 
        操作： 
        预期：
        '''
        start_time = datetime.datetime.now().strftime("%Y-%m-01 00:00:00"),
        end_time = datetime.datetime.now().strftime("%Y-%m-%d 23:23:00"),
        #params = ['syssn','pay_type','start_time','page']
        params = ['pay_type']
        #params = ['start_time']#,'page']
        for p in params:
            param = {}
            if p == 'syssn':
                param['syssn'] = '20160217355317'
            if p == 'pay_type':
                param['pay_type'] = '800101'
            if p == 'start_time':
                param['start_time'] = start_time 
                param['end_time'] = end_time
            if p == 'page':
                param['start_time'] = start_time 
                param['end_time'] = end_time
                param['page'] = 2
                param['page_size'] = 2

            sign = create_sign(param,TEST_APP['key'])
            req = urllib.urlencode(param)
            data = post(self.url,req,sign)
            #print 'result',data
            if p == 'syssn':
                struct = { u'resperr': u'', u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
                struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
                nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
                #print 'source:\n',struct
                #print 'now:\n',struct
                #nose.tools.ok_(data['data'][0].get('pay_type')=='800108', msg='返回码错误')
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
                #nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct2,data['data'][0]),msg='返回结构不一致')
            if p == 'pay_type':
                struct = { u'resperr': u'',  u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
                struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
                nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
                #print 'now:\n',data
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
            if p == 'start_time':
                struct = {u'resperr': u'', u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
                struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
                nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
                #nose.tools.ok_(data['data'][0].get('respcd')=='1144', msg='返回码错误')
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct2,data['data'][0]),msg='返回结构不一致')
                q = {
                    'sysdtm':('between', [start_time, end_time]),
                    'busicd':('in', ('800101','800108','800201','800207','800208','800103','800203')),
                    'userid':'11751',
                    }
                num = self._query_order(**q)
                #print '==================num: ',  num
                #print '==================len: ',  len(data['data'])
                #print num,len(data['data'])
                nose.tools.ok_(len(data['data'])==num, msg='查询结果与实际不一致')
                #print 'source:\n',struct
                #print 'now:\n',struct
            if p == 'page':
                param['page'] = 1
                param['page_size'] = 2
                struct = {u'resperr': u'',  u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
                struct2 = {u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}
                nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
                #nose.tools.ok_(data['data'][0].get('respcd')=='1144', msg='返回码错误')
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
                nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct2,data['data'][0]),msg='返回结构不一致')
                nose.tools.ok_(len(data['data']) == 2,msg='返回页数不一致')
                nose.tools.ok_(data['page'] == 2,msg='返回页数不一致')

    def test_query_fail(self):
        '''
        订单撤销： 测试订单查询失败（/trade/v1/refund）
        条件：不存在的订单 
        操作： 
        预期： 
        '''
        param = {
                'out_trade_no': '2015020212345678',
                }
        
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(self.url,req,sign)
        #print 'result',data
        struct = { u'resperr': u'', u'page_size': 10, u'respmsg': u'', u'respcd': u'0000', u'data': [{u'pay_type': u'', u'sysdtm': u'', u'order_type': u'payment', u'txcurrcd': u'', u'txdtm': u'', u'txamt': u'', u'out_trade_no': u'', u'syssn': u'', u'cancel': u'0', u'respcd': u'', u'errmsg': u''}], u'page': 1}
        nose.tools.ok_(data.get('respcd')=='0000', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
        nose.tools.assert_false(data.get('data'),msg='返回结构不一致')

    def query(self):
        start_time = '2016-02-18 00:50:00' 
        end_time = '2016-02-18 23:50:24' 
        param = {
                'sysdtm':('between', [start_time, end_time]),
                }
        num = self._query_order(**param)
        #print num
        
