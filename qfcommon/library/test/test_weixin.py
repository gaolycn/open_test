# coding=utf-8
__author__ = 'cf'

import urllib
import urllib2
import json
import unittest
from xml.etree import ElementTree
import traceback

from qfcommon.library.weixin import *
import xmltodict


TEST_WEIXIN_MCHNTID = '10028073'
TEST_WEIXIN_APP_ID = 'wx370e5f2f9001f90b'
TEST_WEIXIN_SUB_MCHNTID = '1265195801'
# TEST_WEIXIN_GATEWAY = 'http://127.0.0.1:9999/weixin/'
TEST_WEIXIN_GATEWAY = 'https://api.mch.weixin.qq.com/pay/'
TEST_WEIXIN_SECAPI = 'https://api.mch.weixin.qq.com/secapi/pay/'
TEST_WEIXIN_KEY = 'dcf0ec7a3ca34ad1913939f21d18f558'
TEST_WEIXIN_AUTH_CODE = '130084284137285604'
TEST_WEIXIN_OUT_TRADE_NO = '20151202353615'

WEIXIN_METHOD_PRECREATE = TEST_WEIXIN_GATEWAY + 'unifiedorder'
WEIXIN_METHOD_PRECREATE_H5 = TEST_WEIXIN_GATEWAY + 'unifiedorder'
WEIXIN_METHOD_QUERY = TEST_WEIXIN_GATEWAY + 'orderquery'
WEIXIN_METHOD_REFUND = TEST_WEIXIN_SECAPI + 'refund'
WEIXIN_METHOD_REFUND_QUERY = TEST_WEIXIN_GATEWAY + 'refundquery'
WEIXIN_METHOD_DOWNLOADBILL = TEST_WEIXIN_GATEWAY + 'downloadbill'
WEIXIN_METHOD_CLOSE_ORDER = TEST_WEIXIN_GATEWAY + 'closeorder'
WEIXIN_METHOD_REVERSAL = TEST_WEIXIN_SECAPI + 'reverse'
WEIXIN_METHOD_SWIPE = TEST_WEIXIN_GATEWAY + 'micropay'


class _WeixinTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(_WeixinTestBase, self).__init__( *args, **kwargs)
        self.weixin = Weixin(TEST_WEIXIN_APP_ID, TEST_WEIXIN_KEY, TEST_WEIXIN_MCHNTID)

    def setUp(self):
        if self.__class__ != _WeixinTestBase:
            print('\n+++++++++++' + str(self.__class__) + '+++++++++++')

    def test_def(self):
        if self.__class__ == _WeixinTestBase:
            self.skipTest('Base Class.')

        req_json = self._make_param()
        req_xml = self._dict_to_xml(req_json)
        resp = self._do_request(req_xml)
        ret = self._do_parse(resp)

        self.assertEqual(ret, True)

    def _do_request(self, params):
        try:
            print 'request param is: ', params
            response = urllib2.urlopen(self._get_gateway(), params).read()
            print '\n', response, '\n'
            # print '\nresponse is : ', json.dumps(json.loads(response), indent=4)

            return response
        except Exception as e:
            traceback.print_exc()
            print 'Exception :', e
            raise e

    def _do_parse(self, resp):
        resp_dict = xmltodict.parse(resp, 'utf-8')
        resp_dict = resp_dict['xml']
        print '\nresponse is :', json.dumps(resp_dict, indent=4, ensure_ascii=False), '\n'
        if 'sign' in resp_dict and not Weixin.check_sign(resp_dict, TEST_WEIXIN_KEY):
            log.info("func=check_sign|result=fail")
            return False

        return self._judge_success(resp_dict)

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' and resp_dict['result_code'] == 'SUCCESS'

    def _make_param(self):
        raise NotImplemented('Please implemented this method!')

    def _get_gateway(self):
        raise NotImplemented('Please implemented this method!')

    def _dict_to_xml(self, indata):
        root = ElementTree.Element("xml")
        for k, v in indata.items():
            field = ElementTree.SubElement(root, str(k))
            field.text = str(v) if type(v) not in types.StringTypes else v
        xmlstr = ElementTree.tostring(root, encoding='utf8', method='xml')

        return xmlstr




class TestPrecreate(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.unifiedorder(out_trade_no=TEST_WEIXIN_OUT_TRADE_NO, product_id='1234',
                                        body='xxxxx', spbill_create_ip='127.0.0.1', total_fee=1,
                                        txcurrcd='156',notify_url='http://127.0.0.1',
                                        mch_id=TEST_WEIXIN_MCHNTID, sub_mch_id=TEST_WEIXIN_SUB_MCHNTID)

    def _get_gateway(self):
        return WEIXIN_METHOD_PRECREATE

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'FAIL' \
               and resp_dict['err_code'] == 'OUT_TRADE_NO_USED'

class TestPrecreateH5(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.unifiedorder(out_trade_no=TEST_WEIXIN_OUT_TRADE_NO, product_id='1234',
                                        body='xxxxx', spbill_create_ip='127.0.0.1', total_fee=1,
                                        txcurrcd='156',notify_url='http://127.0.0.1',
                                        mch_id=TEST_WEIXIN_MCHNTID, sub_mch_id=TEST_WEIXIN_SUB_MCHNTID)

    def _get_gateway(self):
        return WEIXIN_METHOD_PRECREATE_H5

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'FAIL' \
               and resp_dict['err_code'] == 'OUT_TRADE_NO_USED'

class TestQuery(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.orderquery(out_trade_no=TEST_WEIXIN_OUT_TRADE_NO, transaction_id='',
                                        sub_mch_id=TEST_WEIXIN_SUB_MCHNTID)

    def _get_gateway(self):
        return WEIXIN_METHOD_QUERY

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'SUCCESS'

# class TestRefund(_WeixinTestBase):
#     # TODO NEED cert
#     def _make_param(self):
#         return self.weixin.refund(out_trade_no=TEST_WEIXIN_OUT_TRADE_NO, transaction_id='',
#                                   out_refund_no='', total_fee=1, refund_fee=1,
#                                   sub_mch_id=TEST_WEIXIN_SUB_MCHNTID)
#
#     def _get_gateway(self):
#         return WEIXIN_METHOD_REFUND
#
#     def _judge_success(self, resp_dict):
#         return resp_dict['return_code'] == 'SUCCESS' \
#                and resp_dict['result_code'] == 'SUCCESS'


class TestRefundQuery(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.refundquery(out_trade_no=TEST_WEIXIN_OUT_TRADE_NO, out_refund_no='',
                                       transaction_id='', refund_id='',
                                        sub_mch_id=TEST_WEIXIN_SUB_MCHNTID, device_info='')

    def _get_gateway(self):
        return WEIXIN_METHOD_REFUND_QUERY

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'SUCCESS' \

class TestCloseOrder(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.close_order(TEST_WEIXIN_AUTH_CODE, TEST_WEIXIN_SUB_MCHNTID)

    def _get_gateway(self):
        return WEIXIN_METHOD_CLOSE_ORDER

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'SUCCESS'

# class TestReversal(_WeixinTestBase):
#     # TODO NEED cert
#     def _make_param(self):
#         return self.weixin.close_order(TEST_WEIXIN_AUTH_CODE, TEST_WEIXIN_SUB_MCHNTID)
#
#     def _get_gateway(self):
#         return WEIXIN_METHOD_REVERSAL
#
#     def _judge_success(self, resp_dict):
#         return resp_dict['return_code'] == 'SUCCESS' \
#                and resp_dict['result_code'] == 'FAIL' \
#                and resp_dict['err_code'] == 'AUTHCODEEXPIRE'

class TestSwipe(_WeixinTestBase):
    def _make_param(self):
        return self.weixin.swipe(TEST_WEIXIN_AUTH_CODE, TEST_WEIXIN_OUT_TRADE_NO,
                                 'xxxxx', '127.0.0.1', '1',
                                 sub_mch_id=TEST_WEIXIN_SUB_MCHNTID)

    def _get_gateway(self):
        return WEIXIN_METHOD_SWIPE

    def _judge_success(self, resp_dict):
        return resp_dict['return_code'] == 'SUCCESS' \
               and resp_dict['result_code'] == 'FAIL' \
               and resp_dict['err_code'] == 'AUTHCODEEXPIRE'

class TestDownloadBill(_WeixinTestBase):
    def _do_parse(self, resp):
        # print(resp)
        return True

    def _make_param(self):
        return self.weixin.downloadbill(bill_date='20151113', bill_type='ALL',
                                 sub_mch_id=TEST_WEIXIN_SUB_MCHNTID, device_info='')

    def _get_gateway(self):
        return WEIXIN_METHOD_DOWNLOADBILL

if __name__ == '__main__':
    unittest.main()