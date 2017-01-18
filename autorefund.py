#coding: utf-8

import hashlib
import hashids
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
from qfcommon.base import dbpool
from qfcommon.base.dbpool import with_database
dbpool.install(DATABASE)


class refund:
   
    def __init__(self):
        self.dateNow =  datetime.datetime.now()
        self.url = '%s/trade/v1/refund' % QT_API 
   
    @with_database('qf_trade')
    def getcustomer(self):
        where = {
            'status':1,
            'cancel':0,
            'retcd': '0000',
            'busicd':('not in',('800203','800103','800503','800205')),
            'txdtm' : ('>=',self.dateNow.strftime("%Y-%m-%d 00:00:00")),
             }
        ret = self.db.select('record_%s'%self.dateNow.strftime("%Y%m"), where=where, fields='syssn,txamt,userid')
        if ret:
            return ret
        else:
            return None
    
    def refund(self): 
        ret = self.getcustomer()
        
        if ret: 
            for val in ret:
                req = {}
                req['txamt'] = int(val.get('txamt'))
                req['syssn'] = val.get('syssn')
                req['out_trade_no'] = int(time.time()*10000)
                req['txdtm'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #print 'val',str(val.get('userid')) == '11751'


                if str(val.get('userid')) == '11751':
                    sign = create_sign(req,TEST_APP['key'])
                    request = urllib.urlencode(req)
                    data = post(self.url,request,sign)
                else:
                    userid = val.get('userid')
                    submchnt = hashids.Hashids('qfpay').encode(11751,userid)
                    req['mchid'] = submchnt
                    sign = create_sign(req,TEST_APP['key'])
                    request = urllib.urlencode(req)
                    data = post(self.url,request,sign)
                if data.get('respcd') == '0000':
                    #print '0000s'%data
                    print 'order: %s refund success!' %req.get('syssn')
                else:
                    print 'fail%s'%data
                    print 'order: %s  refund fail! retry' % req.get('syssn')
        else:
            print '没有退款的交易！'
     

if __name__=='__main__':
    re = refund()
    re.refund()
