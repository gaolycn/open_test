#coding: utf-8
import logging
log = logging.getLogger()
import traceback
import base64
import struct
import binascii
import datetime
import json
import hashlib
import M2Crypto
#from Crypto.Cipher import DES
from qfcommon.base.tools import smart_utf8
from qfcommon.base.http_client import PycurlClient
from qfcommon.base.dbpool import get_connection
from qiantai_base import util
from qiantai_base import constants

class JDPay:
    VERSION = "2.0"
    CURRENCY = "CNY"
    PAY_ENC_FIELDS = ["merchantRemark", "tradeNum", "tradeName", "tradeDescription", "tradeTime", 
                    "tradeAmount", "currency", "successCallbackUrl", "failCallbackUrl", "notifyUrl", "data"]
    TIME_FOTMAT = "%Y-%m-%d %H:%M:%S"
    PRIVATE_KEY = None
    DES_KEY = None
    PUBLIC_KEY = None
    MD5_KEY = None
    INIT = False

    @classmethod
    def has_initd(cls):
        return cls.INIT
    
    @classmethod 
    def init(cls, md5, des, pub, priv, passphase=None):
        if not getattr(cls, 'MD5_KEY', None):
            cls.MD5_KEy = md5        
        if not getattr(cls, 'DES_KEY', None):
            cls.DES_KEY = des
        if not getattr(cls, 'PRIVATE_KEY', None):
            cls.PRIVATE_KEY = M2Crypto.RSA.load_key_string(priv.encode('utf-8'))
        if not getattr(cls, 'PUBLIC_KEY', None):
            bi = M2Crypto.BIO.MemoryBuffer(pub.encode('utf-8'))
            cls.PUBLIC_KEY = M2Crypto.RSA.load_pub_key_bio(bi)
        cls.INIT = True

    @classmethod 
    def get_pay_params(cls, indata, goods_format='%s'):
        request_data = {"version":JDPay.VERSION, "currency":JDPay.CURRENCY}
        keys_must = ['order_id', 'chnl_id', 'notifyUrl', 'create_time', 'successCallbackUrl',
                    'failCallbackUrl', 'notifyUrl']
        for k in keys_must:
            if not indata.get(k, ''):
                log.debug("JD pay_params missing:%s", k)
                return {}
        request_data['tradeNum'] = indata.get('order_id', '')
        request_data['token'] = indata.get('token', '')
        request_data['merchantNum'] = indata['chnl_id']
        request_data['merchantRemark'] = indata.get('ext', '')
        request_data['tradeName'] = goods_format % indata['order_id']
        request_data['tradeDescription'] = 'test'
        request_data['tradeNum'] = '%s' % indata['order_id']
        request_data['tradeTime'] = datetime.datetime.fromtimestamp(int(indata['create_time'])).strftime(JDPay.TIME_FOTMAT)
        request_data['tradeAmount'] = int(indata['total_amt'])
        request_data['successCallbackUrl'] = indata['successCallbackUrl']
        request_data['failCallbackUrl'] = indata['failCallbackUrl']
        request_data['notifyUrl'] = indata['notifyUrl'] 
        JDPay.sign(request_data)
        return request_data
    
    @classmethod
    def sign(cls, params, field_not_sign = ['merchantSign', 'version', 'token']):
        ''' 签名方法 '''
        keys = params.keys()
        keys = filter(lambda k : k not in field_not_sign, keys)
        keys.sort()
        sign_str = ["%s=%s" % (smart_utf8(k), smart_utf8(params.get(k, ''))) for k in keys]   
        sign_str = smart_utf8('&'.join(sign_str))
        log.debug('sign_str:%s', sign_str)
        h = hashlib.sha256(sign_str)
        log.debug("hash:%s", h.hexdigest())
        sign_bytes = cls.PRIVATE_KEY.private_encrypt(h.hexdigest().lower(), M2Crypto.RSA.pkcs1_padding)
        sign = base64.b64encode(sign_bytes)
        log.debug('merchantSign:%s', sign)
        params['merchantSign'] = sign
        # 参数des加密
        for key in params.keys():
            if key in cls.PAY_ENC_FIELDS and params.get(key):
                des = base64.b64decode(cls.DES_KEY)
                des_cipher = M2Crypto.EVP.Cipher(alg='des_ecb', op=1, iv='123456', padding=1, key=des)
                v = des_cipher.update(str(params[key]))
                v += des_cipher.final()
                params[key] = base64.b64encode(v)
        return params

    @classmethod
    def verify(cls, response):
        data = binascii.unhexlify(response['data'])
        h = SHA256.new(data)
        verifier = PKCS1_v1_5.new(cls.PUBLIC_KEY)
        return verifier.verify(h, response['merchantSign'])
            

class JDQuery:
    @staticmethod
    def get_query_data(chnl_info, order_id):
        request_data = {'version':'1.0', 'merchantNum':chnl_info['chnl_id']}
        sign_data = json.dumps({"tradeNum":str(order_id)})
        length = len(sign_data)
        log.debug("length:%d, %s", length, struct.pack('!i', length))
        sign_data = struct.pack('!i', length) + sign_data
        padding = (8 - len(sign_data) % 8) * chr(0x00)
        log.debug("sign_data:%s", sign_data)
        sign_data = sign_data + padding
        log.debug("sign_data:%s", sign_data)
        des = base64.b64decode(chnl_info['chnl_key2'])
        des_cipher = M2Crypto.EVP.Cipher(alg='des_ede3_ecb', op=1, iv='123456', padding=1, key=des)
        v = des_cipher.update(sign_data)
        v += des_cipher.final()
        final_data = binascii.hexlify(v)
        request_data['data'] = final_data
        # sha256
        h = hashlib.sha256(final_data)
        message = h.hexdigest().lower()
        private_key = M2Crypto.RSA.load_key_string(chnl_info['priv_key'].encode('utf-8'))
        sign_bytes = private_key.private_encrypt(message, M2Crypto.RSA.pkcs1_padding)
        sign = base64.b64encode(sign_bytes)
        request_data['merchantSign'] = sign
        return request_data

    @staticmethod
    def do_query(request_data, order_id, query_url):
        log.debug("request_data:%s", request_data)
        result = None
        try:
            content = PycurlClient().post_json(query_url, request_data)
            result = json.loads(content)
        except: 
            log.warn(traceback.format_exc())
            return None 
        log.debug("query return:%s", result) 
        if not result:
            return False, 'no result'
        if result.get('resultCode', '') != 0:
            return False, result.get('resultMsg', '')
        result_data = result['resultData']
        where = {'id':order_id}
        order_info = {}
        with get_connection('qiantai') as conn:
            order_info = conn.select_one(table='order', where=where)
        if not order_info:
            return False, 'not found order info'
        channel = util.Channel(app_id=order_info['app_id'], mchnt_id=order_info['mchnt_id'], 
                pay_sub_type=constants.PAY_SUB_TYPE_JD_H5)
        account = channel.get_raw_account()
        bi = M2Crypto.BIO.MemoryBuffer(account['pub_key'].encode('utf-8'))
        public_key = M2Crypto.RSA.load_pub_key_bio(bi)
        log.debug("result sign:%s", result_data['sign'])
        log.debug("result data:%s", result_data['data'])
        # 公钥解密sign值
        raw_sign = str(result_data['sign'])
        raw_sign = base64.decodestring(raw_sign)
        decode_sign = public_key.public_decrypt(raw_sign, M2Crypto.RSA.pkcs1_padding)
        log.debug('decode hash;%s', decode_sign)
        #计算原来的hash
        h = hashlib.sha256(str(result_data['data']))
        log.debug("cal hash:%s", h.hexdigest().lower())
        if h.hexdigest().lower() != decode_sign:
            return False, "verify sign fail"
        des_key = base64.b64decode(account['chnl_key2'])
        des_cipher = M2Crypto.EVP.Cipher(alg='des_ede3_ecb', op=0, iv='123456', padding=0, key=des_key)
        v = des_cipher.update(binascii.unhexlify(result_data['data']))
        v += des_cipher.final()
        log.debug("decode:%s", v)
        length = struct.unpack("!i", v[:4])
        log.debug("length:%s", length)
        trade_data = json.loads(v[4:4+length[0]])
        return True, trade_data[0]['tradeStatus']
        
