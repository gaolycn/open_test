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
区域信息查询，总行信息查询， 城市信息查询，支行信息查询
'''

class TestCommon:
    def setUp(self):
        self.login_url = "http://api.qa.qfpay.net"
        pass
        
    def test_area_info(self):
        '''
        测试区域信息查询(/tool/v1/area)
        返回预期：查询成功 
        请求类型：GET
        '''
        url = '%s/tool/v1/area'%QT_API
        res = get(url)
        nose.tools.ok_('0000' == res.get('respcd'), msg = '区域信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(AREA_INFO,res),msg='返回结构不一致')

    def test_city_info(self):
        '''
        测试城市信息查询，使用正确的area_id(/tool/v1/city)
        返回预期：查询成功
        请求类型：get
        '''
        url = '%s/tool/v1/city?'%QT_API
        param = {
                'area_id' : '11',
                } 
        #print req
        url = url + urllib.urlencode(param)
        sign = create_sign(param,TEST_APP['key'])
        res = get(url,sign)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '城市信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(CITY_INFO,res),msg='返回结构不一致')
    
    def test_city_info_err(self):
        '''
        测试城市信息查询，使用错误的area_id(/tool/v1/city)
        返回预期：查询为空
        请求类型：get
        '''
        url = '%s/tool/v1/city?'%QT_API
        param = {
                'area_id' : '1111',
                } 
        #print req
        url = url + urllib.urlencode(param)
        sign = create_sign(param,TEST_APP['key'])
        res = get(url,sign)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '城市信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(CITY_INFO,res),msg='返回结构不一致')

    def test_headbank_info(self):
        '''
        测试总行信息查询(/tool/v1/headbank)
        返回预期：查询成功
        请求类型：GET
        '''
        url = '%s/tool/v1/headbank'%QT_API
        res = get(url)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '总行信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(HEADBANK_INFO,res),msg='返回结构不一致')
    
    def test_branchbank_info(self):
        '''
        测试支行信息查询，使用正确的city_id，仅传必传参数(/tool/v1/branchbank)
        返回预期：查询成功
        请求类型：get
        '''
        url = '%s/tool/v1/branchbank?'%QT_API
        param = {
                'city_id' : '181',
                } 
        #print req
        url = url + urllib.urlencode(param)
        sign = create_sign(param,TEST_APP['key'])
        res = get(url,sign)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '城市信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(BRANCHBANK_INFO,res),msg='返回结构不一致')
    
    def test_branchbank_info_all(self):
        '''
        测试支行信息查询，使用正确的city_id, 传送所有参数(/tool/v1/branchbank)
        返回预期：查询成功
        请求类型：get
        '''
        url = '%s/tool/v1/branchbank?'%QT_API
        param = {
                'city_id'     : '181',
                'headbank_id' : '19',
                'keyword'     : '中关村',
                } 
        url = url + urllib.urlencode(param)
        sign = create_sign(param,TEST_APP['key'])
        res = get(url,sign)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '支行信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(BRANCHBANK_INFO,res),msg='返回结构不一致')
    
    def test_branchbank_info_err(self):
        '''
        测试支行信息查询，使用错误的city_id,验证异常情况(/tool/v1/branchbank)
        返回预期：查询失败
        请求类型：get
        '''
        url = '%s/tool/v1/branchbank?'%QT_API
        param = {
                'city_id' : '2000',
                } 
        #print req
        url = url + urllib.urlencode(param)
        sign = create_sign(param,TEST_APP['key'])
        res = get(url,sign)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = '支行信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(BRANCHBANK_INFO,res),msg='返回结构不一致')
    def test_mcc_info(self):
        '''
        测试mcc 信息查询 (/tool/v1/mcc)
        返回预期：查询成功
        请求类型：get
        '''
        url = '%s/tool/v1/mcc'%QT_API
        res = get(url)
        #print res
        nose.tools.ok_('0000' == res.get('respcd'), msg = 'MCC信息查询失败')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(MCC_INFO,res),msg='返回结构不一致')
