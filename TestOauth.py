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
import requests as re 
from qfcommon.base import logger
logger.install('stdout')
from qfcommon.base.http_client import Urllib2Client
'''
OAuth2.0较1.0相比，整个授权验证流程更简单更安全，也是未来最主要的用户身份验证和授权方式。
关于OAuth2.0协议的授权流程可以参考下面的流程图，其中Client指第三方应用，Resource Owner指用户， Authorization Server是我们的授权服务器，Resource Server是API服务器。
step 1: 使用test_user_auth 将参数链接
step 2: 在浏览器中打开此url，确认并获取到跳转的code(授权)
step 3: 将code 放入test_access_token参数中请求获取access_token
step 4: 获取的access_token放入请求的其他接口中请求数据
'''
class TestOauth:
    def setUp(self):
        if DEBUG_MODE == 'offline':
            self.login_api = 'http://172.100.101.107:6310'
            self.open_api = 'https://openapi.qa.qfpay.net'
        else:
            self.login_api = 'https://o.qfpay.com'
            self.open_api = QT_API
        url = '%s/mchnt/user/login' % self.login_api
        param = {
                'username'  : '14700000291',
                'password'  : '000291',
                'udid'      : '14700000291000291',
                }
        req = urllib.urlencode(param)
        data = post(url,req)
        self.sessionid = data['data'].get('sessionid')
        #使用qfcommon
        #self.client = Urllib2Client()
        #data = self.client.post(url,param)
        #return  json.loads(data).get('access_token')
    
    def _access_token(self,code):
        '''
        私有函数，获取用户access_token
        '''
        url = '%s/oauth/v2/access_token'% self.open_api
        param = {
                'client_id'     : TEST_APP['app_code'],
                'client_secret' : TEST_APP['key'],
                'grant_type'    : 'authorization_code',
                'code'          : code,
                } 
        data = post(url,urllib.urlencode(param))
        #print data
        return  data.get('access_token')

    def _user_auth(self):
        ''' 获取code '''
        #生成请求url
        url = '%s/oauth/v2/authorize?' % self.open_api
        param = {
                'client_id'    : TEST_APP['app_code'],
                'redirect_uri' : 'http://www.baidu.com',
                'scope'        : 'user_baseinfo,user_tradelist,user_sendsms',
                'response_type': 'code',
                } 
        requrl = url + urllib.urlencode(param)
        print requrl
        #获取access_token
        re_param = {
                'scope-user_baseinfo'   : 'true',
                'scope-user_sendsms'    : 'true',
                'scope-user_tradelist'  : 'true',
                    }
        req = urllib2.Request(requrl,urllib.urlencode(re_param))
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie","sessionid=%s"%self.sessionid))
        res = opener.open(req)
        #print res.url.split("code=")[1] 
        return res.url.split("code=")[1] #split 分割为list ,取list[1]

    def test_user_auth(self):
        '''
        请求用户授权code
        '''
        code = self._user_auth()
        nose.tools.ok_(code,'获取用户授权失败')

    def test_access_token(self):
        '''
        获取access_token
        '''
        code = self._user_auth()
        access_token = self._access_token(code)
        nose.tools.ok_(access_token,'获取用户access_token失败')
       
    def test_get_baseinfo(self):
        '''
        获取user的baseinfo
        '''
        #预处理
        code = self._user_auth()
        access_token = self._access_token(code)
        
        url = '%s/user/v1/baseinfo?'%QT_API
        param = {'access_token': access_token}
        re = get(url+urllib.urlencode(param))

        nose.tools.ok_(re.get('respcd') == '0000','请求baseinfo失败')
        nose.tools.ok_(re['data'].get('userid'),'获取userid失败')

    def test_get_tradelist(self):
        '''
        获取user的tradelist
        '''
        #预处理
        code = self._user_auth()
        access_token = self._access_token(code)
        
        url = '%s/user/v1/tradelist?'%QT_API
        param = {
                'access_token': access_token,
                'start_time'  : datetime.datetime.now().strftime("%Y-%m-01 %H:%M:%S"),
                'end_time'    : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'page'        : 1,
                'page_size'   : 10,
                } 
        re = get(url+urllib.urlencode(param))
        
        nose.tools.ok_(re.get('respcd') == '0000','获取trade_list失败')
        nose.tools.ok_(isinstance(re['data'].get('tradelist'),list),'非list类型')
        struct = {u'pay_type': u'800207', u'sysdtm': u'2016-08-08 18:05:46', u'txcurrcd': u'CNY', u'txdtm': u'2016-08-08 18:05:46', u'txamt': u'1', u'syssn': u'20160808124500020000000357', u'customer_id': u''}
        if re['data'].get('tradelist'):
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(struct,re['data'].get('tradelist')[0]),msg='返回结构不一致')
    
    def test_send_message(self):
        '''
        测试发送短信
        '''
        #预处理
        code = self._user_auth()
        access_token = self._access_token(code)
        #print access_token
        url = '%s/user/v1/sendsms?'%QT_API
        param = {
                'access_token': access_token,
                'msg':'test 消息发送',
                } 
        re = get(url+urllib.urlencode(param))
        nose.tools.ok_(re.get('respcd') in ('0000','2003'),'发送短信失败')
