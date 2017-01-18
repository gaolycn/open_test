# coding=utf-8
__author__ = 'cf'

import urllib
import urllib2
import json
import unittest
from qfcommon.library.alipay_v2 import *

ALIPAY_GATEWAY = 'https://openapi.alipay.com/gateway.do?charset=utf-8'
ALIPAY_APP_ID = '2015080700203117'
private_key_filename = './test/key/qf_rsa_private_key.pem'
public_key_filename = './test/key/alipay_rsa_public_key.pem'
with open(private_key_filename, 'r') as file:
        private_key = file.read()
with open(public_key_filename, 'r') as file:
        public_key = file.read()
TEST_OUT_TRADE_NO = '20150812988888889' #qfpay syssn
TEST_AUTH_CODE = '289938236670579430'

class _AlipayTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.alipay = Alipay(ALIPAY_APP_ID, '')
        super(_AlipayTestBase, self).__init__(*args, **kwargs)

    def test_def(self):
        '''
        defautl test.
        :return:
        '''
        if self.__class__ == _AlipayTestBase:
            self.skipTest('Base Class.')

        param = self._make_param()
        param = self._sign_data(param)
        resp = self._do_request(param)
        ret = self._do_parse(resp)

        self.assertEqual(ret, True)

    def _sign_data(self, data):
        print 'unsign data is: ', str(data)
        Alipay.sign(data, private_key)

        return urllib.urlencode(data)

    def _do_request(self, params):
        try:
            print 'request param is: ', params
            response = urllib2.urlopen(ALIPAY_GATEWAY, params).read()
            print '\n', response, '\n'
            # print '\nresponse is : ', json.dumps(json.loads(response), indent=4)

            return response
        except Exception as e:
            print 'Exception :', e
            raise e

    def _do_parse(self, resp):
        filed_name = self._get_data_filed_name()
        trade_data = self.alipay.parse(resp, public_key, filed_name)

        return self._judge_success(trade_data)

    def _judge_success(self, trade_data):
        return trade_data['msg'] == 'Success' or trade_data['code'] == '10000'

    def _get_data_filed_name(self):
        raise NotImplemented('Please implemented this method!')

    def _make_param(self):
        raise NotImplemented('Please implemented this method!')


class TestCreateAndPay(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_CREATEANDPAY

    def _make_param(self):
        return self.alipay.createandpay(TEST_OUT_TRADE_NO, TEST_AUTH_CODE, '1', '测试')

    def _judge_success(self, trade_data):
        return trade_data['code'] == '40004' \
               and trade_data['sub_code'] == 'ACQ.TRADE_HAS_CLOSE'

class TestSwipe(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_SWIPE

    def _make_param(self):
        return self.alipay.swipe(TEST_OUT_TRADE_NO, TEST_AUTH_CODE, '1', '测试')

    def _judge_success(self, trade_data):
        return trade_data['code'] == '40004' \
               and trade_data['sub_code'] == 'ACQ.TRADE_HAS_CLOSE'

class TestPrecreate(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_PRECREATE

    def _make_param(self):
        return self.alipay.precreate('20151208354058', '测试商品', 119)

class TestQuery(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_QUERY

    def _make_param(self):
        return self.alipay.query(TEST_OUT_TRADE_NO)

class TestCancel(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_CANCEL

    def _make_param(self):
        return self.alipay.cancel(TEST_OUT_TRADE_NO)

class TestRefund(_AlipayTestBase):
    def _get_data_filed_name(self):
        return ALIPAY_RESPONSE_REFUND

    def _make_param(self):
        return self.alipay.refund(TEST_OUT_TRADE_NO, '1')

    def _judge_success(self, trade_data):
        return trade_data['code'] == '40004'\
               and trade_data['sub_code'] == 'ACQ.TRADE_HAS_CLOSE'




if __name__ == '__main__':
    unittest.main()