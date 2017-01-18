        
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

class TestRefund:
    def setUp(self):
        self.txamt = 11        

    def test_refund_wx(self):
        '''
        订单撤销： 测试微信订单退款（/trade/v1/refund）
        条件： 
        操作： 
        预期： 
        '''
        url = '%s/trade/v1/refund' %QT_API
        
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : self.txamt,
                #'syssn'   : '20160414124500020003833701', 
                'syssn'   : '20160825536565', 
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
        print 'result',data
	struct = {u'resperr': u'\u4ea4\u6613\u4e0d\u5b58\u5728\u6216\u4e0d\u5728\u53ef\u64cd\u4f5c\u65f6\u95f4\u5185', u'respcd': u'1136', u'respmsg': u'', u'out_trade_no': u'14606316974781'}
        #nose.tools.ok_(data.get('respcd')=='1143', msg='返回码错误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,data),msg='返回结构不一致')
