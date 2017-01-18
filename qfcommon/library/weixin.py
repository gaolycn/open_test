# coding: utf-8

import hashlib
import datetime
import uuid
import logging
import time
import types

from qfcommon.base.tools import smart_utf8
from qfcommon.globale.currency import Currency
log = logging.getLogger()

WEIXIN_URL_UNIFIED_ORDER = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
WEIXIN_URL_ORDER_QUERY = 'https://api.mch.weixin.qq.com/pay/orderquery'
WEIXIN_URL_CLOSE_ORDER = 'https://api.mch.weixin.qq.com/pay/closeorder'
WEIXIN_URL_REFUND = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
WEIXIN_URL_REFUND_QUERY = 'https://api.mch.weixin.qq.com/pay/refundquery'
WEIXIN_URL_DOWNLOAD_BILL = 'https://api.mch.weixin.qq.com/pay/downloadbill'
WEIXIN_URL_SETTLEMENT_QUERY = 'https://api.mch.weixin.qq.com/pay/settlementquery'


class Weixin(object):
    '''
    微信支付协议实现
    '''
    # 微信支持的日期格式
    time_format = "%Y%m%d%H%M%S"

    def __init__(self, appid, key, mch_id):
        self.appid = appid
        self.key = smart_utf8(key)
        self.mch_id = mch_id
        self.charset = 'utf-8'
        #self.sign_type = 'MD5'

    @staticmethod
    def check_sign(params, key):
        '''检查签名'''
        if 'sign' in params:
            keys = params.keys()
            keys.sort()
            query = []
            for k in keys:
                if k not in ('sign') and params[k]:
                    query.append('%s=%s' % (smart_utf8(k), smart_utf8(params[k])))

            data = '&'.join(query)
            data += "&%s=%s" % ("key", smart_utf8(key))

            md5 = hashlib.md5()
            md5.update(data)
            return params['sign'] == md5.hexdigest().upper()

        return False

    def _build_header(self, result):
        '''填充通用的头部
             appid, mch_id, nonce_str
        '''
        result['appid'] = str(self.appid)
        result['mch_id'] = str(self.mch_id)
        result['nonce_str'] = uuid.uuid4().hex

    def _sign_(self, indata, not_include = ["sign"]):
        '''
        发送请求数据签名
        '''
        keys = indata.keys()
        keys.sort()
        tmp = []
        for key in keys:
            if key not in not_include and indata[key]:
                tmp.append("%s=%s" %  (smart_utf8(key), smart_utf8(indata[key])))

        tmp.append("%s=%s" % ("key", smart_utf8(self.key)))

        tmpStr = '&'.join(tmp)
        md5 = hashlib.md5()
        md5.update(tmpStr.decode('utf-8').encode(self.charset))
        indata['sign'] = md5.hexdigest().upper()
        return md5.hexdigest().upper()

    def swipe(self, auth_code, out_trade_no, body, spbill_create_ip, total_fee, **kwargs):
        result = {}
        self._build_header(result)
        result['auth_code'] = auth_code
        result['out_trade_no'] = out_trade_no
        result['body'] = body
        if type(body) == types.StringType:
            result['body'] = body.decode('utf-8')
        else:
            result['body'] = body
        result['spbill_create_ip'] = spbill_create_ip
        result['total_fee'] = total_fee

        extent_fields = ['attach', 'time_start', 'time_expire', 'goods_tag', 'device_info', 'detail', 'sub_mch_id', 'limit_pay', 'sub_appid']
        for key in extent_fields:
            if key in ['time_start', 'time_expire'] and kwargs.has_key(key):
                try:
                    _date = datetime.datetime.strptime(kwargs[key], Weixin.time_format)
                except:
                    continue
            if kwargs.has_key(key) and kwargs[key]:
                result[key] = kwargs[key]
        if 'fee_type' in kwargs:
            result['fee_type'] = kwargs['fee_type']

        self._sign_(result)
        return result

    # 统一预下单
    def unifiedorder(self, out_trade_no, product_id, body, spbill_create_ip, total_fee, trade_type='NATIVE',
            notify_url='', **kwargs):
        result = {}
        self._build_header(result)
        result['out_trade_no'] = out_trade_no
        result['product_id'] = product_id
        if type(body) == types.StringType:
            result['body'] = body.decode('utf-8')
        else:
            result['body'] = body
        result['spbill_create_ip'] = spbill_create_ip
        result['total_fee'] = total_fee
        result['trade_type'] = trade_type
        result['notify_url'] = notify_url

        extent_fields = ['attach', 'time_start', 'time_expire', 'goods_tag', 'openid', 'sub_mch_id', 'limit_pay', 'sub_appid']
        for key in extent_fields:
            if key in ['time_start', 'time_expire'] and kwargs.has_key(key):
                try:
                    _date = datetime.datetime.strptime(kwargs[key], Weixin.time_format)
                except:
                    continue
            if kwargs.has_key(key) and kwargs[key]:
                result[key] = kwargs[key]
        if kwargs.get('sub_openid', ''):
            result['sub_openid'] = kwargs['sub_openid']
        if kwargs.get('openid', ''):
            result['openid'] = kwargs['openid']
        if 'fee_type' in kwargs:
            result['fee_type'] = kwargs['fee_type']

        self._sign_(result)
        return result
    # 订单查询
    def orderquery(self, out_trade_no, transaction_id, sub_mch_id='', sub_appid=''):
        result = {}
        self._build_header(result)
        result['out_trade_no'] = out_trade_no
        if transaction_id:
            result['transaction_id'] = transaction_id
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        if sub_appid:
            result['sub_appid'] = sub_appid
        self._sign_(result)
        return result

    # 退款
    def refund(self, transaction_id, out_trade_no, out_refund_no, total_fee, refund_fee,
            sub_mch_id='', sub_appid='', device_info='', op_user_id=''):
        result = {}
        self._build_header(result)
        result['transaction_id'] = transaction_id
        result['out_trade_no'] = out_trade_no
        result['out_refund_no'] = out_refund_no
        result['total_fee'] = total_fee
        result['refund_fee'] = refund_fee
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        if sub_appid:
            result['sub_appid'] = sub_appid
        if device_info:
            result['device_info'] = device_info
        if not op_user_id:
            result['op_user_id'] = str(self.mch_id)
        else:
            result['op_user_id'] = str(op_user_id)

        self._sign_(result)
        return result

    # 退款查询
    def refundquery(self, transaction_id, out_trade_no, out_refund_no, refund_id,
                    sub_mch_id='', sub_appid='', device_info=''):
        result = {}
        self._build_header(result)
        result['transaction_id'] = transaction_id
        result['out_trade_no'] = out_trade_no
        result['out_refund_no'] = out_refund_no
        result['refund_id'] = refund_id
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        if sub_appid:
            result['sub_appid'] = sub_appid
        if device_info:
            result['device_info'] = device_info

        self._sign_(result)
        return result

    # 对账单
    def downloadbill(self, bill_date, bill_type, sub_mch_id='',
                     sub_appid='', device_info=''):
        result = {}
        self._build_header(result)
        try:
            bill = datetime.datetime.strptime(bill_date, '%Y%m%d')
        except:
            return None
        result['bill_date'] = bill_date
        result['bill_type'] = bill_type
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        if sub_appid:
            result['sub_appid'] = sub_appid
        if device_info:
            result['device_info'] = device_info

        self._sign_(result)
        return result

    #关闭订单
    def close_order(self, out_trade_no, sub_mch_id='', sub_appid=''):
        result = {}
        self._build_header(result)
        result['out_trade_no'] = out_trade_no
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        if sub_appid:
            result['sub_appid'] = sub_appid
        self._sign_(result)
        return result

    def settlementquery(self, date_start, date_end, usetag=1, limit=10, offset=1, sub_mch_id=''):
        result = {}
        self._build_header(result)
        result['date_start'] = date_start
        result['date_end'] = date_end
        result['usetag'] = usetag
        result['limit'] = limit
        result['offset'] = offset
        if sub_mch_id:
            result['sub_mch_id'] = sub_mch_id
        self._sign_(result)
        return result


#-------test---------------

def test_sign():
    import urllib2
    w = Weixin()
    data = w.unifiedorder('132444','1234',u'测试商品','127.0.0.1',1L,trade_type='JSAPI',notify_url="http://baidu.com",openid="oLrs5uEhnrfGb4f7tUXgTN1zsnlg")
    print data

def test_settlementquery():
    from qfcommon.base import logger
    logger.install('stdout')
    from qfcommon.base.http_client import Urllib2Client
    w = Weixin('wxd3cd0fc1de73438d','2991947cf8dc4077a2258ee7dfc259c0','1301629101')
    data = w.settlementquery('20160214','20160315', 1)
    import urllib2
    print Urllib2Client().post_xml(WEIXIN_URL_SETTLEMENT_QUERY, {'xml': data}, handlers = [urllib2.HTTPSHandler(debuglevel=1)])

def test_down():
    from qfcommon.base import logger
    logger.install('stdout')
    from qfcommon.base.http_client import Urllib2Client,RequestsClient
    w = Weixin('wxd3cd0fc1de73438d','2991947cf8dc4077a2258ee7dfc259c0','1301629101')
    time = '20160222'
    data = w.downloadbill(time,'ALL')
    import urllib2
    ret = Urllib2Client().post_xml(WEIXIN_URL_DOWNLOAD_BILL, {'xml': data}, handlers = [urllib2.HTTPSHandler(debuglevel=2)])



if __name__ == '__main__':
    # test_sign()
    test_settlementquery()
    # test_down()



