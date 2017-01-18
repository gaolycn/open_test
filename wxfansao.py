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
import hashids

class Swipe:
    request_url = "%s/trade/v1/payment"%QT_API
        
    def trade(self,submchnt=''):
        print "----------------swipe trade-------------------------"
        out_trade_sn = int(time.time()*10000)
        req = {}
        code  = 2 #raw_input('alipay(1) or weixin(2):')
        userid  = raw_input('userid(default 11751):')
        if userid:
            submchnt = hashids.Hashids('qfpay').encode(11751,int(userid))
        if code == "1":
            busicd = '800108'
        else:
            busicd = '800208'
        req['txamt'] = raw_input('pay_amt:')
        req['auth_code'] = raw_input('auth_code:')
        req['out_trade_no'] = out_trade_sn
        req['pay_type'] = busicd
        req['txcurrcd'] = 'CNY'
        req['trade_name'] = '点餐收款xxxxxxxxxxxxxxxxx======'
        req['txdtm'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if submchnt:
            req['mchid'] = submchnt
        sign = create_sign(req,TEST_APP['key'])
        request  = urllib.urlencode(req)
        #print 'self.req: ', self.request_url
        result = post(self.request_url,request,sign)
        return result

    
def query(order_id,submchnt=''):
    request_url = "%s/trade/v1/query"%QT_API
    req = {}
    req['syssn'] = order_id
    if submchnt:
        req['mchid'] = submchnt
    sign = create_sign(req,TEST_APP['key'])
    result = post(request_url,urllib.urlencode(req),sign)
    print result
    return result
    
def refund(payamt,order_id,submchnt=''):
    import time
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

def trade():
    #submchnt='B7eeimnZ'
    #submchnt='MNbbIQp0ge'
    #submchnt='ZOkq8uOqdP'
    submchnt = ''
    swipe = Swipe()
    ret = swipe.trade(submchnt)
    #org_order = ret.get
    print 'swipe result:', ret
    if ret['respcd'] == '1145':
        while True:
            r = query(ret.get('syssn'),submchnt)
            print 'query_result: ', r
            if r['data'][0].get('respcd') == '0000':
                print 'order payed'
                break
            time.sleep(1)
    #print 'test refund,please wait ......'
    #time.sleep(5)
    #refund(ret.get('txamt'),ret.get('syssn'),submchnt)

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
    
     

if __name__=='__main__':
    #trade()
    #query('20161008124500020000001510')
    refund('100','20161128016100020000031296')

    #pay_amt,order_id = test() 
    #test2(1,'20161008124500020000001510') 
    #fundlist = [('1','20160425124500020004606143'),
    #        ] 
    #for k,v in fundlist:
    # test2(k,v) 
    #test2('1','20160425124500020004606143') 
