# coding: utf-8
import hashlib
import types
import datetime
import json
from collections import OrderedDict
import logging

from Crypto.Signature import PKCS1_v1_5 as PK
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import rsa
import base64

from qfcommon.base.tools import smart_utf8
_ALIPAY_SERVICE_CREATEANDPAY = 'alipay.trade.pay'
_ALIPAY_SERVICE_PRECREATE = 'alipay.trade.precreate'
_ALIPAY_SERVICE_SWIPE = 'alipay.trade.pay'
_ALIPAY_SERVICE_QUERY = 'alipay.trade.query'
_ALIPAY_SERVICE_CANCEL = 'alipay.trade.cancel'
_ALIPAY_SERVICE_REFUND = 'alipay.trade.refund'

ALIPAY_RESPONSE_CREATEANDPAY = 'alipay_trade_pay_response'
ALIPAY_RESPONSE_PRECREATE = 'alipay_trade_precreate_response'
ALIPAY_RESPONSE_SWIPE = 'alipay_trade_pay_response'
ALIPAY_RESPONSE_QUERY = 'alipay_trade_query_response'
ALIPAY_RESPONSE_CANCEL = 'alipay_trade_cancel_response'
ALIPAY_RESPONSE_REFUND = 'alipay_trade_refund_response'

_ALIPAY_SEPORATOR = '&'  # 字符串拼接时候使用的分隔符
_ALIPAY_SIGN_TYPE = 'RSA'

# 测试使用,线上不要使用
_log_alipay_codec_v2 = logging.getLogger('alipay_codec_v2')
_log_alipay_codec_v2.addHandler(logging.NullHandler()) # do noting

class AlipayRetError(Exception):
    """
    支付宝返回的参数有问题，一般是我们请求出错，还有可能是有人伪造。
    """
    pass


class AlipayParamError(Exception):
    """
    传给支付宝的参数有错
    """
    pass


class AlipayVerifyError(Exception):
    """
    alipay返回的数据，签名校验失败
    """
    pass


class Alipay(object):
    def __init__(self, app_id, account, charset='utf-8'):
        self.app_id = app_id
        self.account = account
        self.charset = charset

    def _get_timestamp(self):
        """获得当前的datetime字符串，不包含毫秒"""
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def sign(data, sign_key):
        """
        计算data的签名，并写入data中。 data['sign'] = sign
        :param dict data: 需要签名的dict数据
        :param str sign_key: 签名使用的私玥
        :return dict: 增加了签名的data
        """
        data['sign'] = Alipay.make_sign(data, sign_key)

    @staticmethod
    def parse(resp, verify_key, data_field_name):
        """
        解析从alipay返回的数据
        :param str resp: 字符串形式的数据
        :return dict/None: 成功返回字典，失败返回None
        """

        data = json.loads(resp, encoding='utf-8', object_pairs_hook=OrderedDict)  # 使用有序的序列化
        try:
            ############ FUCK the code, YOU mast DO in this way!
            verify_start = resp.find('{', resp.find(data_field_name))
            verify_end = resp.rfind('}', verify_start, resp.find('sign'))
            verify_str = resp[verify_start:verify_end + 1]
            ############

            ret_sign = data['sign']
            trade_data = data[data_field_name]
        except:
            raise AlipayRetError('Alipay return param is not valid.')

        if not Alipay.verify(verify_str, ret_sign, verify_key):
            raise AlipayVerifyError('Sign verify failed.')

        return dict(trade_data)

    @staticmethod
    def verify(indata, ret_sign, verify_key):
        """

        :param indata:
        :param ret_sign:
        :param verify_key:
        :return:
        """
        _log_alipay_codec_v2.debug("indata: %s", indata)
        _log_alipay_codec_v2.debug("ret_sign: %s", ret_sign)
        _log_alipay_codec_v2.debug('verify_key: %s', verify_key)
        pub_key = RSA.importKey(
            rsa.pem.save_pem(
                contents=base64.decodestring(verify_key),
                pem_marker='RSA PUBLIC KEY'
            )
        )
        # sign_str = SHA.new(indata)
        # return PK.new(pub_key).verify(sign_str, base64.b64decode(ret_sign))

        # pub_key = rsa.PublicKey.load_pkcs1(verify_key) # if verify_key is start_with '----BEGIN...'
        return rsa.verify(indata, base64.b64decode(ret_sign), pub_key)

    @staticmethod
    def make_sign(data, sign_key):
        """
        根据传入的字典数据data，根据data中的sign_type生成sign，并放置到data中。

        :param dict data: 需要计算签名的字典数据，需要包含sign_type
        :return str: 根据data['sign_type']计算产生的签名
        """

        sorted_keys = data.keys()
        sorted_keys.sort()

        data_list = [smart_utf8(key)+'='+smart_utf8(data[key])
                     for key in sorted_keys
                     if key not in ['sign'] and data[key]]  # ATTENTION: 包含sign_type，但不包含sign, 且不能包含空字段
        _log_alipay_codec_v2.debug('data_list is: %s', str(data_list))

        unsigned_data = _ALIPAY_SEPORATOR.join(data_list)

        pri_key = RSA.importKey(
            rsa.pem.save_pem(
                contents=(base64.decodestring(sign_key)),
                pem_marker='RSA PRIVATE KEY'
            )
        )
        # signer = PK.new(key_obj)
        # sign_str = SHA.new(unsigned_data)
        # sign_raw = signer.sign(sign_str)
        # sign = base64.b64encode(sign_raw)

        # pri_key = rsa.PrivateKey.load_pkcs1(sign_key) # if verify_key is start_with '----BEGIN...'
        sign = rsa.sign(unsigned_data, pri_key, 'SHA-1')
        sign = base64.b64encode(sign)

        _log_alipay_codec_v2.debug("sign: %s", sign)

        return sign

    def _make_req_data(self, method, ext_data=None):
        """
        根据service和ext_data创建向alipay发起请求的data。
        会将ext_data中的数据update到data中。

        :param str method: 接口名称
        :param dict ext_data: 需要扩展到发送给alipay的data中的数据，
        :return dict: 生成的要发送给alipay的data的数据。
        """

        data = dict(
            app_id=self.app_id,
            method=method,
            charset=self.charset,
            timestamp=self._get_timestamp(),
            version='1.0',
            sign_type=_ALIPAY_SIGN_TYPE,
            sign='',  # 占位
            notify_url='',  # 占位
            biz_content='',  #  占位
        )

        if ext_data is not None:
            data.update(ext_data)

        return data

    # +++统一预下单
    def precreate(self, out_trade_no, subject, txamt, extend_params=None, seller_id='',
                  seller_email='', notify_url='http://0.openapi2.qfpay.com/trade/alipay/v1/notify', **kwargs):
        biz_data = dict(
            out_trade_no=out_trade_no,
            seller_id=seller_id,
            total_amount=self._trans_txamt(txamt),
            subject=subject,
        )
        biz_data.update(kwargs)

        if extend_params:
            # extend_params's type must is dict
            if type(extend_params) is not dict:
                extend_params = json.loads(extend_params)
            biz_data['extend_params'] = extend_params

        ext_data = dict(
            biz_content=json.dumps(biz_data),
            notify_url=notify_url,
        )

        return self._make_req_data(_ALIPAY_SERVICE_PRECREATE, ext_data)

    def _trade_pay(self, scene, syssn, auth_code, txamt, subject, body, goods_detail,
                   extend_params, **kwargs):
        """
        zengsao
        :param scene:
        :param syssn:
        :param auth_code:
        :param txamt:
        :param subject:
        :param body:
        :param goods_detail:
        :param dict extend_params:
        :return:
        """
        expire = datetime.datetime.now() + datetime.timedelta(seconds=30*60) # 默认过期时间为30分钟内
        expire_str = expire.strftime('%Y-%m-%d %H:%M:%S')
        biz_data = dict(
            out_trade_no=syssn,
            auth_code=auth_code,
            seller_id=self.account,
            total_amount=self._trans_txamt(txamt),
            subject=subject,
            scene=scene,
            time_expire=expire_str,
        )
        biz_data.update(kwargs)

        if body:
            biz_data['body'] = body
        if goods_detail:
            biz_data['goods_detail'] = goods_detail
        if extend_params:
            # extend_params's type must is dict
            if type(extend_params) is not dict:
                extend_params = json.loads(extend_params)
            biz_data['extend_params'] = extend_params

        ext_data = dict(
            biz_content=json.dumps(biz_data),
        )

        return self._make_req_data(_ALIPAY_SERVICE_CREATEANDPAY, ext_data)

    # 统一下单并支付??? 声波支付
    def createandpay(self, syssn, auth_code, txamt, subject, body='', goods_detail='',
                     extend_params=None, **kwargs):
        return self._trade_pay('wave_code', syssn, auth_code, txamt, subject, body, goods_detail,
                               extend_params, **kwargs)

    # 收单退款
    def refund(self, out_trade_no, txamt, trade_no='', out_request_no='', refund_reason='', **kwargs):
        biz_data = dict(
            out_trade_no=out_trade_no,
            trade_no=trade_no,
            refund_amount=self._trans_txamt(txamt),
            out_request_no=out_request_no,
            refund_reason=refund_reason,
        )
        biz_data.update(kwargs)

        ext_data = dict(
            biz_content=json.dumps(biz_data),
        )

        return self._make_req_data(_ALIPAY_SERVICE_REFUND, ext_data)

    # 收单撤销
    def cancel(self, out_trade_no, **kwargs):
        biz_data = dict(
            out_trade_no=out_trade_no,
        )
        biz_data.update(kwargs)

        ext_data = dict(
            biz_content=json.dumps(biz_data),
        )

        return self._make_req_data(_ALIPAY_SERVICE_CANCEL, ext_data)

    # 收单查询
    def query(self, out_trade_no, trade_no='', **kwargs):
        """

        param str out_trade_no:  '20' + 钱方的订单序列号
        param str trade_no: 支付宝的订单序列号
        attention: 同时存在时，优先使用trade_no
        """
        biz_data = dict(
            out_trade_no=out_trade_no,
            trade_no=trade_no,
        )
        biz_data.update(kwargs)

        ext_data = dict(
            biz_content=json.dumps(biz_data),
        )

        return self._make_req_data(_ALIPAY_SERVICE_QUERY, ext_data)

    # 刷卡支付，即反扫
    def swipe(self, syssn, auth_code, txamt, subject, body='', goods_detail='', extend_params=None, **kwargs):
        """ 支付宝刷卡交易 """
        return self._trade_pay('bar_code', syssn, auth_code, txamt, subject, body, goods_detail,
                               extend_params, **kwargs)

    def _trans_txamt(self, txamt):
        """
        将单位为分的整型txamt，转换为单位为元的保留两位小数的字符串
        :param txamt: 单位为分的整型数txamt
        :return: 单位为元的保留两位小数的txamt
        """

        return '%.2f' % (int(txamt)/100.0)
