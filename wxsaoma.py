#coding: utf-8

import hashlib
import urllib, urllib2
import json
import time
import datetime
import types
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from qiantai_config import *
from qiantai_util import *

class WxSaoma:
    request_url = "%s/trade/v1/payment"%QT_API
        
    def trade(self,submchnt=''):
        print "----------------swipe trade-------------------------"
        out_trade_sn = int(time.time()*10000)
        req = {}
        code  = str(raw_input('jdpay(1) or weixin(2):'))
        if code == "1":
            busicd = '800501'
        else:
            busicd = '800201'
        #800201 统一预下单，800207 h5下单
        req['txamt'] = 10 
        req['out_trade_no'] = out_trade_sn
        req['pay_type'] = busicd
        req['txcurrcd'] = 'CNY'
        req['txdtm'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        req['mchid'] = submchnt 
        sign = create_sign(req,TEST_APP['key'])
        request  = urllib.urlencode(req)
        print 'self.req: ', self.request_url
        #result = post(self.request_url,request,sign,submchnt)
        result = post(self.request_url,request,sign)
        return result

    
def query(order_id,submchnt=''):
    request_url = "%s/trade/v1/query"%QT_API
    submchnt='B7eeimnZ'
    req = {}
    req['syssn'] = order_id
    req['mchid'] = submchnt 
    sign = create_sign(req,TEST_APP['key'])
    result = post(request_url,urllib.urlencode(req),sign)
    print result
    return result
    
def refund(payamt,order_id,submchnt=''):
    import time
    print 'test refund,please wait ......'
    time.sleep(1)
    url = '%s/trade/v1/refund' % QT_API 
    req = {}
    req['txamt'] = payamt
    req['syssn'] = order_id
    req['out_trade_no'] = int(time.time()*10000)
    req['txdtm'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sign = create_sign(req,TEST_APP['key'])
    request = urllib.urlencode(req)
    data = post(url,request,sign,submchnt)
    print 'refund: ',data
    return data

def test():
    submchnt='B7eeimnZ'
    #submchnt=''
    pay = WxSaoma()
    ret = pay.trade(submchnt)
    print 'pay result:', ret
    print 'pay syssn:',ret.get('syssn')
    #close()
    return ret.get('syssn'),ret.get('txamt')

def test2(payamt,order_id):
    #submchnt='B7eeimnZ'
    submchnt=''
    print 'test refund,please wait ......'
    time.sleep(1)
    url = '%s/trade/v1/refund' % QT_API 
    req = {}
    req['txamt'] = payamt
    req['syssn'] = order_id
    req['out_trade_no'] = int(time.time()*10000)
    req['txdtm'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sign = create_sign(req,TEST_APP['key'])
    request = urllib.urlencode(req)
    data = post(url,request,sign,mchnt=submchnt)

    print 'result',data
  
def close():
        '''
        订单关闭： 测试使用钱台订单关闭（/trade/v1/close）
        '''
	order_id,txamt = test()
        url = '%s/trade/v1/close' %QT_API
        param = {
                'txamt'   : txamt,
                'syssn'   : order_id,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign)
    	print data 

if __name__=='__main__':
    #close()
    test()
    #query('20160629124500020008065775')
