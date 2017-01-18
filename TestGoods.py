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
from qiantai_db import test as db
'''
用户提交证件，注册商户，查询
'''

class TestGoods:
    def setUp(self):
        self.mchnt = ''
    
    def tearDown(self):
        db1 = db()
        db1.del_goods_info()
        db1.del_cate_info()

    def _add_cate(self):
        url = '%s/goods/v1/add_cate' %QT_API
        name =  '商品分类' + str(int(time.time()))
        param = {'name':name}
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        return data['data'].get('cate_id')
    
    def _add_goods(self):
        url = '%s/goods/v1/add_goods' %QT_API
        cate_id = self._add_cate()
        goodsname =  '商品名称' + str(int(time.time()))
        param = {
                'cate_id' : cate_id,
                'name'    : goodsname,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        return cate_id,data['data'].get('unionid'),data['data'].get('goods_id')
        
    def test_add_cate(self):
        '''
        验证添加商品分类,  必传参数(/goods/v1/add_cate)
        '''
        url = '%s/goods/v1/add_cate' %QT_API
        name =  '商品分类' + str(int(time.time()))
        param = {
                'name'   :  name,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '增加菜品分类失败')
        nose.tools.ok_(19 == len(data['data'].get('cate_id')), msg = '返回的cate_id信息有误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(NEWADD_CATE,data),msg='返回结构不一致')

    def test_add_cate_all(self):
        '''
        验证添加商品分类,  添加所有参数(/goods/v1/add_cate)
        '''
        url = '%s/goods/v1/add_cate' %QT_API
        name =  '商品分类' + str(int(time.time()))
        param = {
                'name'   :  name,
                'descr'  :  name,
                'weight' :  random.randint(1,99),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '增加菜品分类失败')
        nose.tools.ok_(19 == len(data['data'].get('cate_id')), msg = '返回的cate_id信息有误')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(NEWADD_CATE,data),msg='返回结构不一致')
    
    def test_add_cate_error(self):
        '''
        验证添加商品分类，无必传参数，添加失败
        '''
        url = '%s/goods/v1/add_cate' %QT_API
        param = {
                'name'   : '',
                'descr'  : '商品分类',
                'weight' : random.randint(1,99),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '增加菜品分类失败')
    
    def test_add_cate_error2(self):
        '''
        验证添加商品分类，无必传参数name，添加失败
        '''
        url = '%s/goods/v1/add_cate' %QT_API
        param = {
                'descr'  : '商品分类',
                'weight' : random.randint(1,99),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' != data.get('respcd'), msg = '增加菜品分类失败')

    def test_modify_cate(self):
        '''
        验证修改商品分类，必传参数，修改成功(/goods/v1/modify_cate)
        '''
        url = '%s/goods/v1/modify_cate' %QT_API
        cate_id = self._add_cate()
        param = {
                'cate_id'  : cate_id,
                'available': '0',
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '增加菜品分类失败')

    def test_modify_cate_all(self):
        '''
        验证修改商品分类，修改成功，验证数据库数据成功(/goods/v1/modify_cate)
        '''
        url = '%s/goods/v1/modify_cate' %QT_API
        descr =  '商品分类' + str(int(time.time()))
        cate_id = self._add_cate()
        print cate_id, descr
        status = str(random.randint(0,1))
        param = {
                'cate_id'  : cate_id,
                'available': status,
                'descr'    : descr,
                'name'     : descr, 
                'weight'   : 50,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '修改菜品分类失败')
        if DEBUG_MODE == 'offline': 
            db1 = db()
            qd = db1.get_cate_info(cate_id)
            nose.tools.ok_(descr == qd.get('descr'))
            nose.tools.ok_(status == str(qd.get('available')))
            #print qd

    def test_modify_cate_error(self):
        '''
        验证修改商品分类，不存在的ID, 不返回失败(/goods/v1/modify_cate)
        '''
        url = '%s/goods/v1/modify_cate' %QT_API
        cate_id = '1111111111111111111'
        descr =  '商品分类' + str(int(time.time()))
        status = str(random.randint(0,1))
        param = {
                'cate_id'  : cate_id,
                'available': status,
                'descr'    : descr,
                'name'     : descr, 
                'weight'   : 50,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '修改菜品分类失败')
    
    def test_query_cate(self):
        '''
        验证查询商品分类, 分别使用ID, OFFSET, LIMIT,  查询成功(/goods/v1/query_cate)
        '''
        url = '%s/goods/v1/query_cate' %QT_API
        cate_id = self._add_cate()
        descr =  '商品分类' + str(int(time.time()))
        status = random.randint(0,1)
        for x in range(2):
            param = {}
            if x == 0:
                param['cate_id'] = cate_id
            if x == 1:
                #limit 和offset 必须同时存在
                param['limit'] = 1
                param['offset'] = 2
            sign = create_sign(param,TEST_APP['key'])
            req = urllib.urlencode(param)
            data = post(url,req,sign,mchnt=self.mchnt)
            #print data
            nose.tools.ok_('0000' == data.get('respcd'), msg = '查询菜品分类失败')
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(CATE_INFO,data),msg='返回结构不一致')

    def test_add_goods(self):
        '''
        验证增加商品名称，必传参数 (/goods/v1/add_goods)
        '''
        url = '%s/goods/v1/add_goods' %QT_API
        cate_id = self._add_cate()
        goodsname =  '商品名称' + str(int(time.time()))
        param = {
                'cate_id' : cate_id,
                'name'    : goodsname,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '添加菜品失败')
        nose.tools.ok_(data['data'].get('goods_id'), msg = 'goods_id没有返回')
        nose.tools.ok_(data['data'].get('unionid'), msg = 'unionid没有返回')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(GOODS_INFO,data),msg='返回结构不一致')

    def test_add_goods_all(self):
        '''
        验证增加商品名称，除关联ID 的其他参数 (/goods/v1/add_goods)
        '''
        url = '%s/goods/v1/add_goods' %QT_API
        cate_id = self._add_cate()
        goodsname =  '商品名称' + str(int(time.time()))
        txamt = random.randint(1,100)
        param = {
                'cate_id' : cate_id,
                'name'    : goodsname,
                'descr'   : '商品描述' + str(int(time.time())),
                'info'    : '商品描述' + str(int(time.time())),
                'spec'    : 'big',  
                'txamt'   : txamt,
                'origamt' : txamt,
                'weight'  : random.randint(1,100),
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '添加菜品失败')
        nose.tools.ok_(data['data'].get('goods_id'), msg = 'goods_id没有返回')
        nose.tools.ok_(data['data'].get('unionid'), msg = 'unionid没有返回')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(GOODS_INFO,data),msg='返回结构不一致')

    def test_add_goods_unionid(self):
        '''
        验证增加商品名称, 关联unionid (/goods/v1/add_goods)
        '''
        url = '%s/goods/v1/add_goods' %QT_API
        cate_id,unionid,goods_id = self._add_goods()
        #print cate_id,unionid
        goodsname =  '商品名称' + str(int(time.time()))
        txamt = random.randint(1,100)
        param = {
                'cate_id' : cate_id,
                'name'    : goodsname,
                'descr'   : '商品描述' + str(int(time.time())),
                'info'    : '商品描述' + str(int(time.time())),
                'spec'    : 'big',  
                'txamt'   : txamt,
                'origamt' : txamt,
                'weight'  : random.randint(1,100),
                'unionid' : unionid,
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '添加菜品失败')
        nose.tools.ok_(data['data'].get('goods_id'), msg = 'goods_id没有返回')
        nose.tools.ok_(unionid == data['data'].get('unionid'), msg = 'unionid没有返回')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(GOODS_INFO,data),msg='返回结构不一致')

    def test_add_goods_img(self):
        '''
        验证增加商品名称, 添加商品主图片 (/goods/v1/add_goods)
        '''
        url = '%s/goods/v1/add_goods' %QT_API
        cate_id,unionid,goods_id = self._add_goods()
        goodsname =  '商品名称' + str(int(time.time()))
        txamt = random.randint(1,100)
        param = {
                'cate_id' : cate_id,
                'name'   : '商品描述' + str(int(time.time())),
                'info'    : '商品描述' + str(int(time.time())),
                'spec'    : 'big',  
                'txamt'   : txamt,
                'origamt' : txamt,
                'weight'  : random.randint(1,100),
                'img'     : "http://qmm.la/nzpDHn",
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '添加商品失败')
        nose.tools.ok_(data['data'].get('goods_id'), msg = 'goods_id没有返回')
        nose.tools.ok_(data['data'].get('unionid'), msg = 'unionid没有返回')
        nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(GOODS_INFO,data),msg='返回结构不一致')
    
    def test_modify_goods(self):
        '''
        验证修改商品信息  (/goods/v1/modify_goods)
        '''
        url = '%s/goods/v1/modify_goods' %QT_API
        cate_id,unionid,goods_id = self._add_goods()
        goodsname =  '商品名称' + str(int(time.time()))
        txamt = random.randint(1,100)
        param = {
                'goods_id': goods_id,
                'cate_id' : cate_id,
                'name'    : goodsname,
                'descr'   : '商品描述' + str(int(time.time())),
                'info'    : '商品描述' + str(int(time.time())),
                'spec'    : 'big',  
                'txamt'   : txamt,
                'origamt' : txamt,
                'weight'  : random.randint(1,100),
                'img'     : "http://qmm.la/nzpDHn",
                }
        sign = create_sign(param,TEST_APP['key'])
        req = urllib.urlencode(param)
        data = post(url,req,sign,mchnt=self.mchnt)
        #print data
        nose.tools.ok_('0000' == data.get('respcd'), msg = '修改商品失败')
        if DEBUG_MODE == 'offline': 
            db1 = db()
            qd = db1.get_goods_info(goods_id)
            nose.tools.ok_(goodsname == qd.get('name'),msg ='修改商品失败')

    def test_query_goods(self):
        '''
        验证查询商品, 分别使用cate_id,goods_id, offset, limit, unionid  查询成功(/goods/v1/query_cate)
        '''
        url = '%s/goods/v1/query_goods' %QT_API
        cate_id,unionid,goods_id = self._add_goods()
        descr =  '商品分类' + str(int(time.time()))
        for x in range(4):
            param = {}
            if x == 0:
                param['cate_id'] = cate_id
            if x == 1:
                #limit 和offset 必须同时存在
                param['limit'] = 1
                param['offset'] = 2
            if x == 2:
                param['goods_id'] = goods_id
            if x == 3:
                param['unionid'] = unionid

            sign = create_sign(param,TEST_APP['key'])
            req = urllib.urlencode(param)
            data = post(url,req,sign,mchnt=self.mchnt)
            #print data
            nose.tools.ok_('0000' == data.get('respcd'), msg = '查询商品失败')
            nose.tools.assert_true(cmp_struct.CmpStructure().cmp_object(GOODS_QUERY_INFO,data),msg='返回结构不一致')

