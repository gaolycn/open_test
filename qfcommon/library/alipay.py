# coding: utf-8
import hashlib

from qfcommon.base.tools import smart_utf8
ALIPAY_GATEWAY = 'https://mapi.alipay.com/gateway.do'
ALIPAY_SERVICE_PRECREATE = 'alipay.acquire.precreate'
ALIPAY_SERVICE_CREATEANDPAY = 'alipay.acquire.createandpay'
ALIPAY_SERVICE_REFUND = 'alipay.acquire.refund'
ALIPAY_SERVICE_CANCEL = 'alipay.acquire.cancel'
ALIPAY_SERVICE_QUERY = 'alipay.acquire.query'
ALIPAY_SERVICE_CREATE_DIRECT_PAY_BY_USER = 'alipay.wap.create.direct.pay.by.user'

class Alipay(object):
    def __init__(self, pid, key, account, charset='utf-8'):
        self.pid = pid
        self.key = key
        self.account = account
        self.charset = charset
        self.sign_type = 'MD5'

    @staticmethod
    def check_sign(params, alikey, charset='utf-8'):
        if 'sign' in params:
            keys = params.keys()
            keys.sort()
            query = []
            for key in keys:
                if key not in ('sign', 'sign_type'):
                    query.append('%s=%s' % (smart_utf8(key), smart_utf8(params[key])))

            data = '&'.join(query) + smart_utf8(alikey)

            md5 = hashlib.md5()
            md5.update(data)
            return params['sign'].upper() == md5.hexdigest().upper()

        return False

    # 统一预下单
    def precreate(self, out_trade_no, subject, total_fee, seller_id=None, seller_email=None, notify_url='http://0.openapi2.qfpay.com/trade/alipay/v1/notify', **args):
        return self.common_create(service=ALIPAY_SERVICE_PRECREATE, out_trade_no=out_trade_no, subject=subject, total_fee=total_fee,
                                  seller_id=seller_id, seller_email=seller_email, product_code='QR_CODE_OFFLINE', notify_url=notify_url, **args)

    # 统一下单并支付
    def createandpay(self, out_trade_no, subject, total_fee, dynamic_id_type, dynamic_id, seller_id=None, seller_email=None,
                     product_code='SOUNDWAVE_PAY_OFFLINE', notify_url='http://0.openapi2.qfpay.com/trade/alipay/v1/notify', **args):
        return self.common_create(service=ALIPAY_SERVICE_CREATEANDPAY, out_trade_no=out_trade_no, subject=subject,
                                  total_fee=total_fee, seller_id=seller_id, seller_email=seller_email, product_code=product_code,
                                  notify_url=notify_url, dynamic_id_type=dynamic_id_type, dynamic_id=dynamic_id, **args)

    # 收单退款
    def refund(self, out_trade_no, refund_amount, trade_no=None, out_request_no=None, refund_reason=None, **args):
        return self.common_create(service=ALIPAY_SERVICE_REFUND, out_trade_no=out_trade_no, refund_amount=refund_amount,
                                  trade_no=trade_no, out_request_no=out_request_no, refund_reason=refund_reason, **args)

    # 收单撤销
    def cancel(self, out_trade_no, trade_no, **args):
        return self.common_create(service=ALIPAY_SERVICE_CANCEL, out_trade_no=out_trade_no, trade_no=trade_no, **args)

    # 收单查询
    def query(self, out_trade_no, trade_no=None, **args):
        return self.common_create(service=ALIPAY_SERVICE_QUERY, out_trade_no=out_trade_no, trade_no=trade_no, **args)

    def h5(self, out_trade_no, subject, total_fee, seller_id=None, seller_email=None, notify_url='http://0.openapi2.qfpay.com/trade/alipay/v1/notify',return_url=None, **args):
        return self.common_create(service=ALIPAY_SERVICE_CREATE_DIRECT_PAY_BY_USER, out_trade_no=out_trade_no, subject=subject or out_trade_no, total_fee=total_fee,
                                  seller_id=seller_id or self.pid, seller_email=seller_email or self.account, notify_url=notify_url, return_url=return_url, payment_type='1', **args)

    # 通用接口
    def common_create(self, service, out_trade_no, subject=None, total_fee=None, product_code=None, notify_url=None, return_url=None, price=None,
                      quantity=None, body=None, show_url=None, seller_id=None, seller_email=None, buyer_id=None, buyer_email=None,
                      operator_type=None, operator_id=None, goods_detail=None, extend_params=None, it_b_pay='1c', royalty_type=None,
                      royalty_parameters=None, channel_parameters=None, currency=None, alipay_ca_request=None, dynamic_id_type=None,
                      dynamic_id=None, ref_ids=None, refund_amount=None, trade_no=None, out_request_no=None, refund_reason=None,
                      payment_type=None):
        params = {}
        params['service'] = service
        params['partner'] = self.pid
        params['out_trade_no'] = out_trade_no

        if subject:
            params['subject'] = subject
        if total_fee:
            params['total_fee'] = '%.2f' % total_fee
        if product_code:
            params['product_code'] = product_code

        if notify_url:
            params['notify_url'] = notify_url
        if return_url:
            params['return_url'] = return_url
        if show_url:
            params['show_url'] = show_url

        if total_fee and price and quantity and price * quantity == total_fee:
            params['price'] = '%.2f' % price
            params['quantity'] = quantity

        if body:
            params['body'] = body

        if seller_id:
            params['seller_id'] = seller_id
        elif seller_email:
            params['seller_email'] = seller_email
        elif service == ALIPAY_SERVICE_PRECREATE or service == ALIPAY_SERVICE_CREATEANDPAY:
            params['seller_id'] = self.pid

        if buyer_id:
            params['buyer_id'] = buyer_id
        if buyer_email:
            params['buyer_email'] = buyer_email

        if operator_type:
            params['operator_type'] = operator_type
        if operator_id:
            params['operator_id'] = operator_id

        if goods_detail:
            params['goods_detail'] = goods_detail
        if extend_params:
            params['extend_params'] = extend_params
        if it_b_pay:
            params['it_b_pay'] = it_b_pay
        if royalty_type:
            params['royalty_type'] = royalty_type
        if royalty_parameters:
            params['royalty_parameters'] = royalty_parameters
        if channel_parameters:
            params['channel_parameters'] = channel_parameters
        if currency:
            params['currency'] = currency
        if alipay_ca_request:
            params['alipay_ca_request'] = alipay_ca_request

        if dynamic_id_type:
            params['dynamic_id_type'] = dynamic_id_type
        if dynamic_id:
            params['dynamic_id'] = dynamic_id
        if ref_ids:
            params['ref_ids'] = ref_ids

        if refund_amount:
            params['refund_amount'] = '%.2f' % refund_amount
        if trade_no:
            params['trade_no'] = trade_no
        if out_request_no:
            params['out_request_no'] = out_request_no
        if refund_reason:
            params['refund_reason'] = refund_reason
        if payment_type:
            params['payment_type'] = payment_type


        params['_input_charset'] = self.charset
        params['charset'] = self.charset

        param_keys = params.keys()
        param_keys.sort()
        unsigned_data = ''
        for key in param_keys:
            unsigned_data += smart_utf8(key) + '=' + smart_utf8(params[key])
            if key != param_keys[-1]:
                unsigned_data += '&'

        unsigned_data += smart_utf8(self.key)
        if self.sign_type == 'MD5':
            md5 = hashlib.md5()
            md5.update(unsigned_data)
            sign = md5.hexdigest()
        else:  # 其它签名方式未实现
            sign = ''

        params['sign'] = sign
        params['sign_type'] = self.sign_type
        #for key in params:
        #    params[key] = str(params[key]).decode('utf-8').encode(self.charset)

        return params


def test_precreate():
    import urllib
    import urllib2
    import xmltodict
    alipay = Alipay('2088201565141845', 'ai1ce2jkwkmd3bddy97z0xnz3lxqk731', 'alipay-test20@alipay.com')
    params = alipay.precreate('TESTTRADENO10', '测试商品', 1.0, notify_url=None)
    try:
        response = urllib2.urlopen(ALIPAY_GATEWAY, urllib.urlencode(params)).read()
        print xmltodict.parse(response.decode('gbk').encode('utf-8').replace('encoding="GBK"', 'encoding="UTF-8"'))
    except:
        print response


def test_createandpay():
    import urllib
    import urllib2
    import xmltodict
    alipay = Alipay('2088201565141845', 'ai1ce2jkwkmd3bddy97z0xnz3lxqk731', 'alipay-test20@alipay.com')
    params = alipay.createandpay('TESTTRADENO10', '测试商品', 1.0, 'wave_code', 'pmyxn9bljuzkzd4123', notify_url=None)
    try:
        response = urllib2.urlopen(ALIPAY_GATEWAY, urllib.urlencode(params)).read()
        print xmltodict.parse(response.decode('gbk').encode('utf-8').replace('encoding="GBK"', 'encoding="UTF-8"'))
    except:
        print response

def test_h5():
    import urllib
    alipay = Alipay('2088711407753777', 'kfy8iitaqvki7wlsvu9p4tb9bp54goke', 'mmhz@qfpay.com')
    params = alipay.h5('test_trade_no_4', '开发测试', 0.01,   notify_url='https://o2.qfpay.com/trade/test')
    print ALIPAY_GATEWAY+'?'+urllib.urlencode(params)

def test_check_sign():
    data = {'trade_no': '2016010421001004690053721036', 'seller_email': 'mmhz@qfpay.com', 'seller_id': '2088711407753777', 'trade_status': 'TRADE_SUCCESS', 'is_total_fee_adjust': 'N', 'notify_id': 'ce91aeb5c0ea7f0816b2005d5b7ffa8lbo', 'price': '0.01', 'buyer_email': '454756061@qq.com', 'sign': 'b591e4d192f2c7828591774762bad127', 'use_coupon': 'N', 'gmt_create': '2016-01-04 13:21:59', 'out_trade_no': 'test_trade_no_4', 'payment_type': '1', 'total_fee': '0.01', 'sign_type': 'MD5', 'notify_time': '2016-01-04 13:22:00', 'quantity': '1', 'gmt_payment': '2016-01-04 13:21:59', 'notify_type': 'trade_status_sync', 'buyer_id': '2088202997229693', 'subject': '\xe5\xbc\x80\xe5\x8f\x91\xe6\xb5\x8b\xe8\xaf\x95'}
    print Alipay.check_sign(data, 'kfy8iitaqvki7wlsvu9p4tb9bp54goke')



if __name__ == '__main__':
    # test_precreate()
    #test_createandpay()
    #test_h5()
    test_check_sign()

