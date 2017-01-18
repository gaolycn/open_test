# coding=utf-8
__author__ = 'cf'

import urllib
import urllib2
import json
import unittest
import logging
import sys

from qfcommon.library.alipay_overseas import *
from qfcommon.library.alipay_overseas import _log_alipay_codec_v2

_log_alipay_codec_v2.addHandler(logging.StreamHandler(sys.stdout))
_log_alipay_codec_v2.setLevel('INFO')

ALIPAY_GATEWAY = 'https://intlmapi.alipay.com/gateway.do'

TEST_ALIPAY_MD5_KEY = 'bxpi3j3w17hkdmrd4nvwxj32yphetb5z'
TEST_ALIPAY_PARTNER_ID = '2088021966645500'
TEST_ALIPAY_SELLER_ID = '2088021966645500'

TEST_OUT_TRADE_NO = '20150812988888889' #qfpay syssn
TEST_TRADE_NO = '2015122121001004610039776870' # alipay trans_id
TEST_AUTH_CODE = '289938236670579430'
TEST_ALIPAY_CURRENCY = 'HKD'
TEST_ALIPAY_TXAMT = '1'


class _AlipayTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(_AlipayTestBase, self).__init__(*args, **kwargs)
        self.alipay = Alipay(TEST_ALIPAY_PARTNER_ID, TEST_ALIPAY_SELLER_ID)

    def test_def(self):
        '''
        defautl test.
        :return:
        '''
        if self.__class__ == _AlipayTestBase:
            self.skipTest('Base Class.')

        param = self._make_param()
        print '\n++++++++++++', param['service'], '+++++++++++++'
        param = self._sign_data(param)
        resp = self._do_request(param)
        ret = self._do_parse(resp)

        self.assertEqual(ret, True)

    def _sign_data(self, data):
        print 'unsign data is: ', str(data)
        Alipay.sign(data, TEST_ALIPAY_MD5_KEY)

        return urllib.urlencode(data)

    def _do_request(self, param):
        try:
            print 'request param is: ', param
            response = urllib2.urlopen(ALIPAY_GATEWAY, param, timeout=2).read()
            print '\n', response, '\n'
            # print '\nresponse is : ', json.dumps(json.loads(response), indent=4)

            return response
        except Exception as e:
            print 'Exception :', e
            raise e

    def _do_parse(self, resp):
        print resp
        trade_data = self.alipay.parse(resp, TEST_ALIPAY_MD5_KEY)
        print '\n####trade_data: ', trade_data

        return self._judge_success(trade_data)

    def _judge_success(self, trade_data):
        return trade_data['result_code'] == 'SUCCESS'

    def _make_param(self):
        raise NotImplemented('Please implemented this method!')


# @unittest.skip('')
class TestSwipe(_AlipayTestBase):
    def _make_param(self):
        return self.alipay.swipe(TEST_OUT_TRADE_NO, TEST_AUTH_CODE, TEST_ALIPAY_TXAMT, '测试', TEST_ALIPAY_CURRENCY)

    def _judge_success(self, trade_data):
        return trade_data['result_code'] == 'FAILED'
#
# class TestPrecreate(_AlipayTestBase):
#     def _get_data_filed_name(self):
#         return ALIPAY_RESPONSE_PRECREATE
#
#     def _make_param(self):
#         return self.alipay.precreate('20151208354058', '测试商品', 119)

# @unittest.skip
class TestQuery(_AlipayTestBase):

    def _make_param(self):
        return self.alipay.query(TEST_OUT_TRADE_NO, TEST_TRADE_NO)


# @unittest.skip('')
class TestCancel(_AlipayTestBase):

    def _make_param(self):
        return self.alipay.cancel(TEST_OUT_TRADE_NO)


# @unittest.skip('')
class TestRefund(_AlipayTestBase):

    def _make_param(self):
        return self.alipay.refund(TEST_OUT_TRADE_NO, '11111', TEST_ALIPAY_TXAMT, TEST_ALIPAY_CURRENCY)

    def _judge_success(self, trade_data):
        return trade_data['result_code'] == 'FAILED'\
               and trade_data['error'] == 'TRADE_HAS_CLOSE'


# @unittest.skip('')
class TestReverse(_AlipayTestBase):

    def _make_param(self):
        return self.alipay.reverse(TEST_OUT_TRADE_NO)

    # def _judge_success(self, trade_data):
    #     pass




if __name__ == '__main__':
    unittest.main()