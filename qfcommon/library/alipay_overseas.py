# coding: utf-8
import hashlib
import types
import datetime
import json
import logging
from Crypto.Signature import PKCS1_v1_5 as PK
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import rsa
import base64
import re

import xmltodict
from qfcommon.base.tools import smart_utf8

# 支付宝可能返回的错误码
ALIPAY_ERR_SYSTEM_ERROR = 'SYSTEM_ERROR'
ALIPAY_ERR_EXIST_FORBIDDEN_WORD = 'EXIST_FORBIDDEN_WORD'
ALIPAY_ERR_ILLEGAL_SIGN = 'ILLEGAL_SIGN'
ALIPAY_ERR_INVALID_PARAMETER = 'INVALID_PARAMETER'
ALIPAY_ERR_ILLEGAL_ARGUMENT = 'ILLEGAL_ARGUMENT'
ALIPAY_ERR_ILLEGAL_PARTNER = 'ILLEGAL_PARTNER'
ALIPAY_ERR_ILLEGAL_EXTERFACE = 'ILLEGAL_EXTERFACE'
ALIPAY_ERR_ILLEGAL_PARTNER_EXTERFACE = 'ILLEGAL_PARTNER_EXTERFACE'
ALIPAY_ERR_ILLEGAL_SIGN_TYPE = 'ILLEGAL_SIGN_TYPE'
ALIPAY_ERR_HAS_NO_PRIVILEGE = 'HAS_NO_PRIVILEGE'
ALIPAY_ERR_REASON_TRADE_BEEN_FREEZEN = 'REASON_TRADE_BEEN_FREEZEN'
ALIPAY_ERR_TRADE_BUYER_NOT_MATCH = 'TRADE_BUYER_NOT_MATCH'
ALIPAY_ERR_TRADE_HAS_CLOSE = 'TRADE_HAS_CLOSE'
ALIPAY_ERR_TRADE_NOT_EXIST = 'TRADE_NOT_EXIST'
ALIPAY_ERR_TRADE_STATUS_ERROR = 'TRADE_STATUS_ERROR'
ALIPAY_ERR_SELLER_NOT_EXIST = 'SELLER_NOT_EXIST'
ALIPAY_ERR_BUYER_NOT_EXIST = 'BUYER_NOT_EXIST'
ALIPAY_ERR_BUYER_ENABLE_STATUS_FORBID = 'BUYER_ENABLE_STATUS_FORBID'
ALIPAY_ERR_BUYER_SELLER_EQUAL = 'BUYER_SELLER_EQUAL'
ALIPAY_ERR_CLIENT_VERSION_NOT_MATCH = 'CLIENT_VERSION_NOT_MATCH'
ALIPAY_ERR_SOUNDWAVE_PARSER_FAIL = 'SOUNDWAVE_PARSER_FAIL'
ALIPAY_ERR_REFUND_AMT_RESTRICTION = 'REFUND_AMT_RESTRICTION'
ALIPAY_ERR_REQUEST_AMOUNT_EXCEED = 'REQUEST_AMOUNT_EXCEED'
ALIPAY_ERR_RETURN_AMOUNT_EXCEED = 'RETURN_AMOUNT_EXCEED'
# and more...

# 支付宝的service字符串
# _ALIPAY_SERVICE_CREATEANDPAY = 'alipay.trade.pay'
# _ALIPAY_SERVICE_PRECREATE = 'alipay.acquire.createandpay'
_ALIPAY_SERVICE_SWIPE = 'alipay.acquire.overseas.spot.pay'
_ALIPAY_SERVICE_QUERY = 'alipay.acquire.overseas.query'
_ALIPAY_SERVICE_REVERSE = 'alipay.acquire.overseas.spot.reverse'
_ALIPAY_SERVICE_CANCEL = 'alipay.acquire.overseas.spot.cancel'
_ALIPAY_SERVICE_REFUND = 'alipay.acquire.overseas.spot.refund'
_ALIPAY_SEPORATOR = '&'  # 字符串拼接时候使用的分隔符

# 签名类型
SIGN_TYPE_MD5 = 'MD5'
SIGN_TYPE_RSA = 'RSA'
SIGN_TYPE_DSA = 'DSA'

# 支付宝的签名方式 @ATTENTION 请使用RSA！
_ALIPAY_SIGN_TYPE = SIGN_TYPE_RSA
_ALIPAY_CHARSET = 'UTF-8'

# 构建的准备传给支付宝的必须参数
BASIC_MUST_KEY = ['service', 'sign_type', 'partner']  # 'sign' 参数是我们这边计算得到的，不需要传入
SERVICE2MUST_KEY = {
    _ALIPAY_SERVICE_SWIPE: BASIC_MUST_KEY + ['alipay_seller_id', 'trans_name', 'partner_trans_id', 'currency',
                                             'trans_amount', 'buyer_identity_code', 'identity_code_type',
                                             'trans_create_time', 'biz_product'],
    _ALIPAY_SERVICE_QUERY: BASIC_MUST_KEY + ['partner_trans_id'],
    _ALIPAY_SERVICE_REVERSE: BASIC_MUST_KEY + ['partner_trans_id'],
    _ALIPAY_SERVICE_CANCEL: BASIC_MUST_KEY + ['partner_trans_id'],
    _ALIPAY_SERVICE_REFUND: BASIC_MUST_KEY + ['partner_trans_id', 'partner_refund_id', 'refund_amount', 'currency'],
}

# 用来从xml字符串中匹配字符编码集
ENCODING_SEARCH_PATTERN = re.compile(
    r"""
    encoding    #
    \s*         # 可能存在空格
    =           #
    \s*         # 可能存在空格
    "           #
    (.*?)       # 我们需要的字符编码 @IMPORTANT 使用非贪婪
    "           #
    """,
    re.VERBOSE
)

# 测试使用,线上不要使用
_log_alipay_codec_v2 = logging.getLogger('alipay_codec_v2')
_log_alipay_codec_v2.addHandler(logging.NullHandler())  # do noting


class AlipayError(Exception):
    pass


class AlipayRetError(AlipayError):
    """
    支付宝返回的参数有问题，一般是我们请求出错，还有可能是有人伪造。
    """
    pass


class AlipayParamError(AlipayError):
    """
    传给支付宝的参数有错
    """
    pass


class AlipayVerifyError(AlipayError):
    """
    alipay返回的数据，签名校验失败
    """
    pass


class AlipayNotSupportSignTypeError(AlipayError):
    """
    使用了不支持的的签名方案
    """

    pass


class Alipay(object):
    def __init__(self, partner_id, seller_id):
        """

        :param str partner_id: The Id of the partner on the Alipay system
        :param str seller_id: The Id of the partner on the Alipay system
        :return:
        """
        self.partner_id = partner_id
        self.seller_id = seller_id

    def _get_timestamp(self):
        """获得当前的datetime字符串，不包含毫秒"""
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    @staticmethod
    def _make_pre_signed_str(data):
        data_list = []
        # '_input_charset' 必须位于第一个位置。 这里做特殊处理，防止有数字开头的key时，排序不能位于第一个。
        input_charset = data.get('_input_charset', _ALIPAY_CHARSET)
        if '_input_charset' in data:
            input_charset_str = '_input_charset=' + input_charset
            data_list.append(input_charset_str)

        sorted_keys = data.keys()
        sorted_keys.sort()
        other_data_list = [smart_utf8(key)+'='+smart_utf8(data[key])
                           for key in sorted_keys
                           if key not in ['sign', 'sign_type', '_input_charset'] and data[key]]
        data_list.extend(other_data_list)

        return _ALIPAY_SEPORATOR.join(data_list)

    @staticmethod
    def sign(data, sign_key, sign_type=''):
        """
        计算data的签名，并写入data中。 data['sign'] = sign
        :param dict data: 需要签名的dict数据
        :param str sign_key: 签名使用的私玥
        :param str sign_type: 签名使用的方法，若data中也存在，优先使用参数sign_type
        :return dict: 增加了签名的data
        """
        data['sign'] = Alipay.make_sign(data, sign_key, sign_type)

    @staticmethod
    def parse(resp, key_dict):
        """
        解析从alipay返回的数据
        :param str resp: 字符串形式的数据
        :param dict key_dict: 用来校验的key的字典，形如： {'md5': 'md5_key', 'rsa': 'rsa_key'}
        :return dict/None: 成功返回字典，失败返回None
        :raise AlipayRetError,AlipayVerifyError,AlipayNotSupportSignTypeError:
        """

        obj = _parse_xml_str(resp)
        if not obj:
            _log_alipay_codec_v2.warn("Can't parse The alipay's return xml_str: %s" % resp)
            raise AlipayRetError("Can't parse The alipay's return xml_str")

        obj = obj['alipay']
        is_success = obj['is_success']
        if is_success != 'T':
            _log_alipay_codec_v2.warn('is_success is NOT T, request may error, error is: %s', obj['error'])
            raise AlipayRetError("is_success is %s but expect 'T'. "
                                 "alipay return error is %s" % (is_success, obj['error']))

        result = obj['response']['alipay']

        # TODO ???? 不知道是做什么的
        for k in result.keys():
            if type(result[k]) not in types.StringTypes:
                key_start = resp.find(k)
                key_end = resp.find("/" + k, key_start + len(k))
                result[k] = resp[(key_start - 1):(key_end + len("/" + k) + 1)]

        sign_type = obj['sign_type']
        ret_sign = obj['sign']
        if sign_type in (SIGN_TYPE_MD5, SIGN_TYPE_RSA):
            verify_key = key_dict[sign_type]
        else:
            raise AlipayNotSupportSignTypeError('{sign_type} is not implement.'.format(sign_type=sign_type))

        if not Alipay.verify(result, ret_sign, verify_key, sign_type):
            _log_alipay_codec_v2.warn('alipay check sign error')
            raise AlipayVerifyError('Check verify failed.')

        return result

    @staticmethod
    def verify(indata, ret_sign, verify_key, sign_type):
        """
        对indata使用sign_type和verify_key以及ret_sign进行签名验证。

        :attention 当indata中也有sign_type时，优先使用param的sign_type。
        :param dict indata: 要验证签名的dict数据
        :param str ret_sign: indata的签名
        :param str verify_key: 用来校验的key
        :param str sign_type: 签名方式
        :return:
        """

        _log_alipay_codec_v2.debug("indata: %s, ret_sign: %s, sign_type: %s", indata, ret_sign, sign_type)

        if sign_type == SIGN_TYPE_MD5:
            return ret_sign == Alipay.make_sign(indata, verify_key, sign_type)
        elif sign_type == SIGN_TYPE_RSA:
            pub_key = RSA.importKey(
                rsa.pem.save_pem(
                    contents=base64.decodestring(verify_key),
                    pem_marker='RSA PUBLIC KEY'
                )
            )
            unverify_str = Alipay._make_pre_signed_str(indata)
            return rsa.verify(unverify_str, base64.b64decode(ret_sign), pub_key)
        else:
            raise AlipayNotSupportSignTypeError('{sign_type} is not implement.'.format(sign_type=sign_type))

    @staticmethod
    def make_sign(data, sign_key, sign_type=''):
        """
        根据传入的字典数据data，根据sign_type或data中的sign_type生成并返回sign(优先使用 参数sign_type)，不修改data。

        :param dict data: 需要计算签名的字典数据，可以包含sign_type
        :param str sign_key: 签名使用的key
        :param str sign_type: 签名方法, 优先使用传入的sign_type，其次才是data中的sign_type
        :return str: 根据sign_type或data['sign_type']计算产生的签名
        """

        unsigned_data = Alipay._make_pre_signed_str(data)
        _log_alipay_codec_v2.debug('presigned data_str is: %s', unsigned_data)

        if not sign_type:
            sign_type = data.get('sign_type', '')
        if sign_type == SIGN_TYPE_MD5:
            unsigned_data += smart_utf8(sign_key)
            md5 = hashlib.md5()
            md5.update(unsigned_data.decode('utf-8').encode(_ALIPAY_CHARSET))
            sign = md5.hexdigest()
        elif sign_type == SIGN_TYPE_RSA:
            pri_key = RSA.importKey(
                rsa.pem.save_pem(
                    contents=(base64.decodestring(sign_key)),
                    pem_marker='RSA PRIVATE KEY'
                )
            )
            sign = rsa.sign(unsigned_data, pri_key, 'SHA-1')
            sign = base64.b64encode(sign)
        else:
            raise AlipayNotSupportSignTypeError('{sign_type} is not implement.'.format(sign_type=sign_type))

        _log_alipay_codec_v2.debug("sign: %s", sign)

        return sign

    def _make_req_data(self, service, ext_data=None):
        """
        根据service和ext_data创建向alipay发起请求的data。
        会将ext_data中的数据update到data中。

        :param str service: 接口名称
        :param dict ext_data: 需要扩展到发送给alipay的data中的数据，
        :return dict: 生成的要发送给alipay的data的数据。
        :raise AlipayParamError: 传入参数不完整或有误
        """

        # basic parameter
        data = {
            'service': service,
            'sign': '',  # 占位
            'sign_type': _ALIPAY_SIGN_TYPE,
            'partner': self.partner_id,
            '_input_charset': _ALIPAY_CHARSET,
        }
        # operation parameter
        if ext_data is not None:
            data.update(ext_data)

        self._valid_param(data)  # 校验参数是否完整

        return data

    # 收单退款
    def refund(self, out_trade_no, refund_no, refund_amount, currency, refund_reason='', notify_url=''):
        """
        退款，可以退北京时间的自然日当日以及次日的交易。 撤销可能会失败，需要再次撤销。
        :param str out_trade_no: 钱方的订单序列号
        :param str refund_no: 退款订单号，不能和out_trade_no一样。 partner_id和refund_no一起标志一次退款交易
        :param str refund_amount: 退款金额
        :param str currency: 退款货币，应与交易货币一致
        :param str refund_reason: 退款原因
        :param str notify_url: 异步通知地址
        :return:
        """
        ext_data = {
            'partner_trans_id': out_trade_no,
            'partner_refund_id': refund_no,
            'refund_amount': self._trans_txamt(refund_amount),
            'currency': currency,
            'refund_reason': refund_reason,
            'notify_url': notify_url,
        }

        return self._make_req_data(_ALIPAY_SERVICE_REFUND, ext_data)

    # 收单撤销
    def cancel(self, out_trade_no):
        """
        撤销订单，只能是北京时间的自然日当日的交易的全部金额。 撤销可能会失败，需要再次撤销。
        :param str out_trade_no:  钱方的订单序列号
        :return dict: 构造的请求参数dict
        """
        ext_data = {
            'partner_trans_id': out_trade_no,
        }

        return self._make_req_data(_ALIPAY_SERVICE_CANCEL, ext_data)

    # 收单查询
    def query(self, out_trade_no, trade_no=''):
        """

        :param str out_trade_no:  钱方的订单序列号
        :param str trade_no: 支付宝的订单序列号
        :attention: 同时存在时，优先使用trade_no
        """

        ext_data = {
            'partner_trans_id': out_trade_no,
            'alipay_trans_id': trade_no
        }

        return self._make_req_data(_ALIPAY_SERVICE_QUERY, ext_data)

    # 刷卡支付，即反扫
    def swipe(self, out_trade_no, auth_code, txamt, subject, currency, memo='', extend_params=None):
        ext_data = {
            'alipay_seller_id': self.seller_id,
            'trans_name': subject,
            'partner_trans_id': out_trade_no,
            'currency': currency,
            'trans_amount': self._trans_txamt(txamt),
            'buyer_identity_code': auth_code,
            'identity_code_type': 'barcode',  # @IMPORTANT 目前只支持barcode
            'trans_create_time': self._get_timestamp(),
            'memo': memo,
            'biz_product': 'OVERSEAS_MBARCODE_PAY',  # @IMPORTANT 目前是一个常量
        }

        if extend_params:
            if not isinstance(extend_params, basestring):
                extend_params = json.dumps(extend_params)
            ext_data['extend_info'] = extend_params

        return self._make_req_data(_ALIPAY_SERVICE_SWIPE, ext_data)

    # 冲正
    def reverse(self, out_trade_no):
        """
        冲正，只能是北京时间的自然日当日的交易的全部金额。 冲正可能会失败，需要再次冲正。
        :param str out_trade_no:  钱方的订单序列号
        :return dict: 构造的请求参数dict
        """
        ext_data = {
            'partner_trans_id': out_trade_no,
        }

        return self._make_req_data(_ALIPAY_SERVICE_REVERSE, ext_data)

    def _trans_txamt(self, txamt):
        """
        将单位为分的整型txamt，转换为单位为元的保留两位小数的字符串
        :param int,str txamt: 单位为分的整型数txamt的字符串或整型数
        :return str: 单位为元的保留两位小数的txamt的字符串
        """

        return '%.2f' % (int(txamt)/100.0)

    def _valid_param(self, param):
        """
        校验param是否合法
        :param dict param: 已经准备好的，要传递给支付宝的参数
        :return:
        :raise AlipayParamError: 传递给支付宝的参数有问题
        """

        service = param['service']
        must_keys = SERVICE2MUST_KEY[service]
        try:
            for key in must_keys:
                if not param[key]:
                    raise AlipayParamError('value of "%s" is null' % key)
        except Exception as e:
            lost_keys = set(must_keys)-set(param.keys())
            err_str = 'Parameters ({0}) Lost for alipay[{1}] Or {2}.'
            err_str = err_str.format(lost_keys, service, str(e))
            _log_alipay_codec_v2.warn(err_str)

            raise AlipayParamError(err_str)


def _get_xml_encoding(desc_str):
    """
    从xml文档描述字符串中读取编码方式(比如：encoding="UTF-8")
    :param str desc_str: xml字符串的文档描述字符串
    :return str: 该xml文档描述字符串中包含的编码
    :raise AttributeError: 当没有找到encoding="xxx"时抛出
    """

    return ENCODING_SEARCH_PATTERN.search(desc_str).groups()[0]


def _split_xml_str(xml_str):
    """
    将xml字符串分割为xml文档描述字符串 和 xml内容字符串，以"?>"来标记文档描述字符串的结束。
    :param str xml_str:
    :return str: xml中找到的文档描述字符串，形如：'<?xml version="1.0" encoding="UTF-8"?>'
    :raise ValueError: 当没有找到文档描述字符串的时候
    """

    desc_end_flag = '?>'
    desc_end_index = xml_str.index(desc_end_flag) + len(desc_end_flag)  # may raise Exception
    desc_str = xml_str[:desc_end_index]
    content_str = xml_str[desc_end_index:]

    return desc_str, content_str


def _parse_xml_str(xml_str):
    """

    :param str xml_str:
    :return:
    """

    try:
        desc_str, content_str = _split_xml_str(xml_str)
        encoding = _get_xml_encoding(desc_str)
        _log_alipay_codec_v2.debug("XML encoding is ### %s ###", encoding)
        ret_str = content_str.decode(encoding).encode(_ALIPAY_CHARSET)
        obj = xmltodict.parse(ret_str)
    except Exception as e:
        _log_alipay_codec_v2.warn(e)
        return None

    return obj
