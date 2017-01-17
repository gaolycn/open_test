# encoding: utf-8

import hashlib
import types,json
import time
import urllib
import urllib2
from urllib2 import HTTPError
import datetime
from qiantai_config import *
#此处解决中文签名失败的问题
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

'''
create_sign  创建签名
get   http get方法
post  http post方法
get_token 获取APP token
create_order 创建订单
get_customer_info 获取用户信息
pre_create 预下单
activity_create  创建活动
coupon_create 创建优惠券
activity_share 分享活动
create_balance_rule 创建充值规则
order_recharge 订单充值
set_result 更新订单
balance_rule_query APP充值余额规则查询
order_query 订单查询
close_order 关闭订单
merchant_set 设置商户信息
'''

def create_sign(params, server_key, charset='utf-8'):
    keys = params.keys()
    keys.sort()
    query = []
    for k in keys:
        if k not in ('sign', 'sign_type') and params[k]:
            query.append('%s=%s' % (k, params[k]))

    data = '&'.join(query) + server_key
    if not isinstance(data, types.UnicodeType):
        data = data.decode(charset)

    md5 = hashlib.md5()
    md5.update(data.encode(charset))
    return md5.hexdigest().upper()


def get(requrl,sign='',header='',appcode=''):
    #req.add_header('User-Agent', 'fake-client')
    #req.add_header('X-QTSIGN', '')
    req = urllib2.Request(requrl)
    if sign:
        req.add_header("X-QF-SIGN", sign)
    if header:
        req.add_header("Cookie", header)
    if appcode:
        req.add_header("X-QF-APPCODE", appcode)
    else:
        req.add_header("X-QF-APPCODE", TEST_APP['app_code'])
    try:
        res = urllib2.urlopen(req).read()
        data = json.loads(res)
        return data
    except HTTPError:
        return 'error'


def post(requrl,data,sign='',mchnt='',appcode=''):
    
    req = urllib2.Request(requrl,data)
    if sign:
        req.add_header("X-QF-SIGN", sign)
    if mchnt:
        req.add_header("X_QF_MCHCODE",mchnt)
    if appcode:
        req.add_header("X-QF-APPCODE", appcode)
    else:
        req.add_header("X-QF-APPCODE", TEST_APP['app_code'])
    try:
        res = urllib2.urlopen(req).read()
        data = json.loads(res)
        return data
    except HTTPError:
        return 'error'

def post_img(requrl,data,sign='',headers=''):
    
    req = urllib2.Request(requrl,data,headers)
    req.add_header("X-QF-SIGN", sign)
    req.add_header("X-QF-APPCODE", TEST_APP['app_code'])
    try:
        res = urllib2.urlopen(req).read()
        data = json.loads(res)
        return data
    except HTTPError:
        return 'error'
def post_cookie(requrl,data,header=''):

    import cookielib
    ck = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
    req = urllib2.Request(requrl,data)

    try:
        #req_data = urllib2.urlopen(req)
        res = opener.open(req).read()
        data = json.loads(res)
        if ck:
            return data,ck
        return data,'error'
    except HTTPError:
        return 'error'

def get_token(**kwargs):
    url = 'http://172.100.101.169:6600/auth/v1/token' #% QT_API
    param = {
            'app_code':TEST_APP['app_code'],
            'out_user':'13812345678',
            'mobile':'13812345678',
            'caller':'server',
            }
    param.update(kwargs)
    if kwargs.get('server_key'):
        tmp = kwargs.get('server_key')
        param.pop('server_key')
        create_sign(param,tmp)
    else:
        create_sign(param,TEST_APP['server_key'])
    senddata = urllib.urlencode(param)
    #ret = post(url,senddata)
    return post(url,senddata)['data'].get('token')

def create_order(**kwargs):
    url = '%s/order/v1/create' % QT_API
    param = {
                'app_code':TEST_APP['app_code'],
                'caller':'app',
                'token':'xxx',
                'order_token':'xxx',
                'total_amt':5,
                'pay_amt':5,
                'pay_type':1,
                'pay_source':1,
                'goods_name':'笔记本',                            
            }
    param.update(kwargs)     
    if param['caller'] == 'server':
        create_sign(param,TEST_APP['server_key'])
    senddata = urllib.urlencode(param)
    #print senddata
    data = post(url,senddata)
    time.sleep(1)
    #print data
    order_id = data['data'].get('order_id')
    return order_id

def get_customer_info(**kwargs):
    url = '%s/customer/v1/info?'%QT_API
    param = {
            'token':'xx',
            'caller':'app',
            'app_code':TEST_APP['app_code'],
            'sign':"xxx",
                }
    param.update(kwargs)
    reurl = url + urllib.urlencode(param)
    return  get(reurl)

#预下单
def pre_create(**kwargs):
    url = '%s/order/v1/pre_create' %QT_API
    out_sn = int(time.time()*10000)
    param = {
        'app_code':TEST_APP['app_code'],
        'caller':'server',
        'total_amt':1,
        'out_sn': out_sn,
        }
    param.update(kwargs)
    create_sign(param,TEST_APP['server_key'])
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    #print '预下单',data
    order_token = data['data'].get('order_token')
    time.sleep(1)
    return order_token,out_sn

def set_result(**kwargs):
    url = '%s/order/v1/set_result' %QT_API
    param = {
            'app_code':TEST_APP['app_code'],
            'caller':'app',
            }
    #create_sign(param,TEST_APP['server_key'])
    param.update(kwargs)
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    return data

def activity_share(**kwargs):
    url = '%s/activity/v1/share?'%QT_API
    param = {
                'caller':'app',
                'token':'xxx',
                'sign':'xx',
                } 
    param.update(kwargs)
    url = url + urllib.urlencode(param)
    data = get(url)
    return data

def order_refund(**kwargs):
    url = '%s/order/v1/refund' % QT_API
    param = {
            'app_code':TEST_APP['app_code'],
            'caller':'app',
            }
    param.update(kwargs)
    create_sign(param,TEST_APP['server_key'])
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    return data

def close_order(**kwargs):
    url = '%s/order/v1/close'%QT_API
    param = {
                'app_code':TEST_APP['app_code'],
                'caller':'server',
                }
    param.update(kwargs)
    if param['caller'] == 'server':
        create_sign(param,TEST_APP['server_key'])
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    return data

#设置商户信息

def merchant_set(method='post',**kwargs):
    url = '%s/merchant/v1/setting'%QT_API
    param  = {
        'caller':'server',
        'app_code':TEST_APP['app_code'],
        }
    param.update(kwargs)
    if param['caller'] == 'server':
        create_sign(param,TEST_APP['server_key'])
    if param['caller'] == 'mis':
        url = 'http://172.100.101.169:6600/merchant/v1/setting'
    if method == 'post':
        param = urllib.urlencode(param)
        #print 'param',param
        data = post(url,param)
        return data
    else:
        param = url + '?' + urllib.urlencode(param)
        #print 'param',param
        data = get(param)
        return data


#def coupon_create(**kwargs):
#    url = '%s/coupon/v1/create'%QT_COUPON_API
#    status = 2 # 1，创建， 2， 启动， 3. 关闭        
#    starttime = datetime.datetime.now()
#    expiretime = starttime + datetime.timedelta(days = 1) 
#    param = {
#                'caller':'mis',
#                'app_code':TEST_APP['app_code'],
#                'title':'title',
#                'type':1,
#                'amt_max':5,#amt_max 与amt_min相同生成固定金额的优惠券
#                'amt_min':5,
#                'status':status,
#                'start_time':starttime.strftime('%Y-%m-%d %H:%M:%S'),
#                'expire_time':expiretime.strftime('%Y-%m-%d %H:%M:%S'),
#                'use_rule':json.dumps({"result":["succ"],"rate":1.0,"rule":[['amt','>=',5],['begin_time','>=',0],['end_time','<=',86400]]}),
#                'content':'测试优惠券',
#                }
#    param.update(kwargs)
#    senddata = urllib.urlencode(param)
#    data = post(url,senddata)
#    return data
#
#def activity_create(**kwargs):
#    url = '%s/activity/v1/create'%QT_COUPON_API
#    starttime = datetime.datetime.now()
#    expiretime = datetime.datetime.now() + datetime.timedelta(seconds = 10) 
#    param = {
#                'app_code':TEST_APP['app_code'],
#                'caller':'mis',
#                'type':1,
#                'title':'test',
#                'total_amt':10,
#                'obtain_num':10,
#                'sponsor_award_num':0,
#                'status':2,
#                'xx_type':1,
#                'rule':json.dumps({'obtain_rule':[["amt", ">=", 5], ["begin_time",">=",0], ["end_time", "<=", 86400]], "sponsor_rule": [["award_time", "=", 1]]}),
#                'start_time':starttime.strftime('%Y-%m-%d %H:%M:%S'),
#                'expire_time':expiretime.strftime('%Y-%m-%d %H:%M:%S'),
#                'content':'测试活动',
#                }
#    param.update(kwargs)
#    senddata = urllib.urlencode(param)
#    data = post(url,senddata)
#    print data
#    return data
#
#def coupon_obtain(**kwargs):
#    mobile = kwargs.get('mobile')
#    share_id = kwargs.get('share_url').split('?')[1]
#    url = kwargs.get('url') + '/coupon/v1/obtain?' + share_id + '&mobile=' + mobile + '&caller=web'
#    data = get(url)
#    return data
#
#def create_balance_rule(**kwargs):
#
#    url = '%s/balance/v1/create'%QT_API
#    param = {
#                'app_code':TEST_APP['app_code'],
#                'title':'规则'+str(int(time.time())),
#                'start_time':datetime.datetime.now().strftime('%F %T'),
#                'expire_time':(datetime.datetime.now() + datetime.timedelta(days =5)).strftime('%F %T'),
#                'amt':10,
#                'award':20,
#                'type':1,
#                'status':2,
#                'content':'10to20',
#                'caller':'mis',
#                }
#    param.update(kwargs) 
#    create_sign(param,TEST_APP['server_key'])
#    senddata = urllib.urlencode(param)
#    data = post(url,senddata)
#    return data

def order_recharge(**kwargs):

    url = '%s/order/v1/recharge' %QT_API
    param = {
                    'app_code':TEST_APP['app_code'],
                    'pay_amt':1,
                    'pay_type':1,
                    'pay_source':1,
                    'goods_name':'可乐',
                    'goods_info':'good',
                    'sign':'xxx',
                    'caller':'app',
            }
    param.update(kwargs)
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    return data


#def balance_rule_query(**kwargs):
#    url = '%s/balance/v1/query_rule?'%QT_API
#    param = {
#            'token':'xx',
#            #'balance_id':充值规则ID 
#            'app_code':TEST_APP['app_code'],
#            'caller':'app',
#            }
#    param.update(kwargs)
#    url = url + urllib.urlencode(param)
#    data = get(url)
#    return data

def modify_recharge_rule(**kwargs):
    url = '%s/balance/v1/change'%QT_API
    param = {
            'balance_id':'xx',
            'caller':'mis',
            'app_code':TEST_APP['app_code'],
            }
    param.update(kwargs)
    senddata = urllib.urlencode(param)
    data = post(url,senddata)
    return data

#def balance_rule_match(**kwargs):
#    url = '%s/balance/v1/match_rule?'%QT_API
#    param = {
#            'token':'xxx',
#            'amt':1,
#            'caller':'app',
#            'app_code':TEST_APP['app_code'],
#            }
#    param.update(kwargs)
#    url = url + urllib.urlencode(param)
#    data = get(url)
#    return data
#
#def activity_change(**kwargs):
#    url = '%s/activity/v1/change'%QT_COUPON_API
#    param = {
#            'app_code':TEST_APP['app_code'],
#            'type':1,
#            'title':'changed',
#            'total_amt':10000,
#            'obtain_num':10,
#            'sponsor_award_num':0,
#            'status':2,
#            'xx_type':1,
#            'xx_id':'xxx',
#            'sponsor_xx_id':'xxx',
#            'rule':'xx',
#            'rule':json.dumps({'obtain_rule':[["amt", ">=", 5], ["begin_time",">=",0], ["end_time", "<=", 86400]], "sponsor_rule": [["award_time", "=", 1]]}),
#            'start_time':starttime.strftime('%Y-%m-%d %H:%M:%S'),
#            'expire_time':expiretime.strftime('%Y-%m-%d %H:%M:%S'),
#            'content':'测试活动',
#            }
#    param.update(kwargs)
#    senddata = urllib.urlencode(param)
#    data = post(url,senddata)
#    return data 

#def coupon_query_rule(**kwargs):
#    url = '%s/coupon/v1/query_rule?'%QT_COUPON_API
#    param = {
#            'app_code':TEST_APP['app_code'],
#            #'caller':'server',
#            'caller':'mis',
#            }
#
#
#    param.update(kwargs)
#    create_sign(param,TEST_APP['server_key'])
#    url = url + urllib.urlencode(param)
#    data = get(url)
#    return data

#def server_coupon_dispatch(**kwargs):
#    url = '%s/coupon/v1/dispatch'%QT_COUPON_API
#    param = {
#            'app_code':TEST_APP['app_code'],
#            'activity_id':'xxx',
#            'customers':[{'mobile':'13812345680'},{'mobile':'13812345681'},{'out_user':'13812385683'}],
#            'num':2,
#            }
#    param.update(kwargs)
#    senddata = urllib.urlencode(param)
#    data = post(url,senddata)
#    return data 
#
#def coupon_query_bind(**kwargs):
#    url = '%s/coupon/v1/query_bind?'%QT_COUPON_API
#    param = {
#            'app_code':TEST_APP['app_code'],
#            'caller':'server',
#            }
#    param.update(kwargs)
#    create_sign(param,TEST_APP['server_key'])
#    url = url + urllib.urlencode(param)
#    data = get(url)
#    return data

def order_query(**kwargs):
    url = '%s/order/v1/query?'%QT_API
    param = {
            "app_code":TEST_APP['app_code'],
            "caller":'server',
            }
    param.update(kwargs)
    create_sign(param,TEST_APP['server_key'])
    url = url + urllib.urlencode(param)
    data = get(url)
    return data

def smscode_send(**kwargs):
    url = '%s/moneyplus/v1/smscode?' % MP_API
    #param = {
    #        mobile = kwargs.get(mobile),
    #        }
    
    param = urllib.urlencode(kwargs)

    return post(url,param)

def smscode_get(mobile):
    import db 
    #mobile = kwargs.get('mobile')
    inst_test = db.test()
    return inst_test.get_smscode(mobile)
    
def money_plus_login(**kwargs):
    url = '%s/moneyplus/v1/login' % MP_API
    param = urllib.urlencode(kwargs)
    data,ck = post_cookie(url,param)
    return data,ck

def money_plus_get_vcode(**kwargs):
    url = '%s/auth/v1/vcode'%QT_API
    param = {}
    param.update(kwargs)
    send_data = urllib.urlencode(param)
    return post(url,send_data)

