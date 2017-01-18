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
from data_struct import *
'''
用户提交证件，注册商户，查询
'''

class TestMch:
    def setUp(self):
        self.login_url = "http://api.qa.qfpay.net"
        pass
        
    def _order(self,mchnt=""):
        '''
        验证下单
        '''
        url = '%s/trade/v1/payment' %QT_API
        out_trade_sn = int(time.time()*10000)
        param = {
                'txamt'   : 1,
                'txcurrcd': 'CNY',
                'pay_type': 800207,
                'out_trade_no': out_trade_sn,
                'txdtm': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'openid':'oMGYCj7dkqBDjry172r83XgD-t3s',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=mchnt)
        #print data
        return data

    def _user_login(self,username):
        '''
        私有函数，获取用户session
        '''
        url = '%s/mchnt/user/login'%self.login_url
        param = {
                'username'  : kwargs.get('username'),
                'password'  : '000291',
                'udid'      : '14700000294000291',
                }
        req = urllib.urlencode(param)
        data = post(url,req)
        return data['data'].get('sessionid')

    def test_mch_signup_base(self):
        '''
        测试用户注册， 只传必要参数(/mch/v1/signup)
        返回预期：注册成功 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/signup'%QT_API
        username = '1472' + str(int(time.time()))[3:]
        param = {
                'username'     :  username ,
                'idnumber'     : '330184198501184115',
                'name'         : '某某A',
                'province'     : '北京',
                'city'         : '北京',
                'address'      : '朝阳',
                'shopname'     : '朝阳店铺',
                'headbankname' : '中国银行',
                'bankuser'     : '某某B',
                'bankaccount'  : '6217710700008888',
                'bankprovince' : '北京',
                'bankcity'     : '北京市',
                'bankname'     : '中国银行北京分行',
                'bankcode'     : '104100006669',
                'banktype'     : '1', #银行类型，1为对私， 2为对公
                'mcc_id'       : '21004',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['idcardfront'] = open(second_image,'rb') 
        param['idcardback'] = open(first_image,'rb')
        param['licensephoto'] = open(second_image,'rb')
        param['livingphoto'] = open(first_image,'rb')
        param['goodsphoto'] = open(first_image,'rb')
        param['shopphoto'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '注册用户失败')
        nose.tools.ok_(res['data'].get('mchid'), msg = '注册用户失败')
        #验证注册用户是否可以使用
        #info = self._order(res['data'].get('mchid'))
        #nose.tools.ok_('0000' == info.get('respcd'), msg = '新注册用户不能使用')
    
    def test_mch_signup_for_company_err(self):
        '''
        测试用户注册， banktype 为对公(/mch/v1/signup)
        返回预期：注册失败
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/signup'%QT_API
        username = '1472' + str(int(time.time()))[3:]
        param = {
                'username'     :  username ,
                'idnumber'     : '330184198501184115',
                'name'         : '某某A',
                'province'     : '北京',
                'city'         : '北京',
                'address'      : '朝阳',
                'shopname'     : '朝阳店铺',
                'headbankname' : '中国银行',
                'bankuser'     : '某某B',
                'bankaccount'  : '6217710700008888',
                'bankprovince' : '北京',
                'bankcity'     : '北京市',
                'bankname'     : '中国银行北京分行',
                'bankcode'     : '104100006669',
                'banktype'     : '2', #银行类型，1为对私， 2为对公
                'mcc_id'       : '21004',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['idcardfront'] = open(second_image,'rb') 
        param['idcardback'] = open(first_image,'rb')
        param['licensephoto'] = open(second_image,'rb')
        param['livingphoto'] = open(first_image,'rb')
        param['goodsphoto'] = open(first_image,'rb')
        param['shopphoto'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('2101' == res.get('respcd'), msg = '注册用户失败')

    def test_mch_signup_again(self):
        '''
        测试用户注册，重复用户注册 (/mch/v1/signup)
        返回预期：注册失败 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/signup'%QT_API
        username = '14700000294'
        param = {
                'username'     :  username ,
                'idnumber'     : '330184198501184115',
                'name'         : '某某A',
                'province'     : '北京',
                'city'         : '北京',
                'address'      : '朝阳',
                'shopname'     : '朝阳店铺',
                'headbankname' : '中国银行',
                'bankuser'     : '某某B',
                'bankaccount'  : '6217710700008888',
                'bankprovince' : '北京',
                'bankcity'     : '北京市',
                'bankname'     : '中国银行北京分行',
                'bankcode'     : '104100006669',
                'banktype'     : '1', #银行类型，1为对私， 2为对公
                'mcc_id'       : '21004',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['idcardfront'] = open(second_image,'rb') 
        param['idcardback'] = open(first_image,'rb')
        param['licensephoto'] = open(second_image,'rb')
        param['livingphoto'] = open(first_image,'rb')
        param['goodsphoto'] = open(first_image,'rb')
        param['shopphoto'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('2101' == res.get('respcd'), msg = '返回码错误')

    def test_mch_signup_all(self):
        '''
        测试用户注册， 发送所有参数(/mch/v1/signup)
        返回预期：注册成功 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/signup'%QT_API
        username = '1472' + str(int(time.time()))[3:]
        param = {
                'username'     :  username ,
                'idnumber'     : '330184198501184115',
                'name'         : '某某A',
                'province'     : '北京',
                'city'         : '北京',
                'address'      : '朝阳',
                'shopname'     : '朝阳店铺',
                'headbankname' : '中国银行',
                'bankuser'     : '某某B',
                'bankaccount'  : '6217710700008888',
                'bankprovince' : '北京',
                'bankcity'     : '北京市',
                'bankname'     : '中国银行北京分行',
                'bankcode'     : '104100006669',
                'banktype'     : '2', #银行类型，1为对私， 2为对公
                'legalperson'  : '张散',
                'latitude'     : '38.000',
                'latitude'     : '114.000',
                'post'         : '100086',
                'telephone'    : '010-132423232',
                'provision'    : 'shipin,shui',
                'areaid'       : '110',
                'city'         : '110',
                'bankareaid'   : '110',
                'bankcityid'   : '110',
                'headbankid'   : '1102',
                'mcc_id'       : '21004',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['idcardfront'] = open(second_image,'rb') 
        param['idcardback'] = open(first_image,'rb')
        param['licensephoto'] = open(second_image,'rb')
        param['livingphoto'] = open(first_image,'rb')
        param['goodsphoto'] = open(first_image,'rb')
        param['shopphoto'] = open(first_image,'rb')
        param['taxphoto'] = open(first_image,'rb')
        param['orgphoto'] = open(first_image,'rb')
        param['openlicense'] = open(first_image,'rb')
        param['authcertphoto'] = open(first_image,'rb')
        param['authidcardfront'] = open(first_image,'rb')
        param['authidcardback'] = open(first_image,'rb')
        param['authbankcardfront'] = open(first_image,'rb')
        param['authbankcardback'] = open(first_image,'rb')
        param['rentalagreement'] = open(first_image,'rb')
        param['insurancecert'] = open(first_image,'rb')
        param['licensephoto1'] = open(first_image,'rb')
        param['foodcirculationpermit'] = open(first_image,'rb')
        param['foodhygienelicense'] = open(first_image,'rb')
        param['foodservicelicense'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '注册用户失败')
        #验证注册用户是否可以使用
        info = self._order(res['data'].get('mchid'))
        nose.tools.ok_('0000' == info.get('respcd'), msg = '新注册用户不能使用')
    
    def test_mch_upload(self):
        '''
        测试用户补充证件， 只传必要参数(/mch/v1/uploadphoto)
        返回预期：注册成功 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/uploadcert'%QT_API
        param = {
                'mchid'     :  'MNbbIQp0ge',
                } 
        if DEBUG_MODE != 'offline':
            param['mchid'] = 'e9vVecQOmn'
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        third_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['foodservicelicense'] = open(third_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '注册用户失败')
    
    def test_mch_upload_err(self):
        '''
        测试用户补充证件， 参数错误返回失败(/mch/v1/uploadphoto)
        返回预期：更新失败 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/uploadcert'%QT_API
        param = {
                'mchid'     :  'MNbbIQp0ge',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        third_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['taxphotoerror'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('2101' == res.get('respcd'), msg = '注册用户失败')
    
    def test_mch_upload_all(self):
        '''
        测试用户补充证件， 传送所有参数(/mch/v1/uploadphoto)
        返回预期：注册成功 
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/uploadcert'%QT_API
        param = {
                'mchid'     :  'MNbbIQp0ge',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        third_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['taxphoto'] = open(first_image,'rb')
        param['orgphoto'] = open(first_image,'rb')
        param['openlicense'] = open(first_image,'rb')
        param['authcertphoto'] = open(first_image,'rb')
        param['authidcardfront'] = open(first_image,'rb')
        param['authidcardback'] = open(first_image,'rb')
        param['authbankcardfront'] = open(first_image,'rb')
        param['authbankcardback'] = open(first_image,'rb')
        param['rentalagreement'] = open(first_image,'rb')
        param['insurancecert'] = open(first_image,'rb')
        param['licensephoto1'] = open(first_image,'rb')
        param['foodcirculationpermit'] = open(first_image,'rb')
        param['foodhygienelicense'] = open(first_image,'rb')
        param['foodservicelicense'] = open(third_image,'rb')
        param['delegateagreement'] = open(third_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '注册用户失败')
    
    def test_mch_upload_user_err(self):
        '''
        测试用户补充证件， 用户不存在(/mch/v1/uploadphoto)
        返回预期：更新失败
        请求类型：POST
        '''
        import poster
        from poster.encode import multipart_encode
        from poster.streaminghttp import register_openers
        register_openers()
        url = '%s/mch/v1/uploadcert'%QT_API
        param = {
                'mchid'     :  '1111',
                } 
        #print req
        second_image = '/home/qfpay/joyce_quan/qiantai/22.jpg'
        first_image = '/home/qfpay/joyce_quan/qiantai/11.jpg'
        third_image = '/home/qfpay/joyce_quan/qiantai/33.jpg'
        sign = create_sign(param,TEST_APP['key'])
        param['taxphoto'] = open(first_image,'rb')
        data, headers = multipart_encode(param)
        res = post_img(url, data, sign, dict(headers))
        #print res
        nose.tools.ok_('1108' == res.get('respcd'), msg = '注册用户失败')
    def test_query_mch(self):
        '''
        测试商户信息查询，使用mchid(/mch/v1/query)
        返回预期：查询成功
        请求类型：GET
        '''
        url = '%s/mch/v1/query?'%QT_API
        param = {
                'mchid' : 'MNbbIQp0ge',
                } 
        #print req
        sign = create_sign(param,TEST_APP['key'])
        url = url + urllib.urlencode(param)
        res = get(url,sign)
        #for key,value in res['data'].items():
        #    print key, ':', value
        nose.tools.ok_('0000' == res.get('respcd'), msg = '用户查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(QUERY_MCH,res),msg='返回结构不一致')
    
    def test_query_mch_username(self):
        '''
        测试商户信息查询，使用username(/mch/v1/query)
        返回预期：查询成功
        请求类型：GET
        '''
        url = '%s/mch/v1/query?'%QT_API
        param = {
                'username' : '14700000294',
                } 
        #print req
        sign = create_sign(param,TEST_APP['key'])
        url = url + urllib.urlencode(param)
        res = get(url,sign)
        #for key,value in res['data'].items():
        #    print key, ':', value
        nose.tools.ok_('0000' == res.get('respcd'), msg = '用户查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(QUERY_MCH,res),msg='返回结构不一致')
    
    def test_query_mch_err(self):
        '''
        测试商户信息查询，使用错误的mchid(/mch/v1/query)
        返回预期：查询失败
        请求类型：GET
        '''
        url = '%s/mch/v1/query?'%QT_API
        param = {
                'mchid' : '1111',
                } 
        #print req
        sign = create_sign(param,TEST_APP['key'])
        url = url + urllib.urlencode(param)
        res = get(url,sign)
        nose.tools.ok_('1108' == res.get('respcd'), msg = '用户查询失败')
