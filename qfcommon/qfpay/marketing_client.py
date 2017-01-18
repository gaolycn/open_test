# coding: utf-8
'''
帐务余额客户端
包装请求，统一返回值
'''

import logging
import traceback

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from qfcommon.base.tools import thrift_callex
from qfcommon.thriftclient.qf_marketing import QFMarketing
from qfcommon.thriftclient.qf_marketing.ttypes import *

from qfresponse import QFRET, error_map

log = logging.getLogger()


def call_func():
    def _(func):
        def __(*args, **kwargs):
            # 统一返回值
            resp = {
                'respcd' : QFRET.OK,       # 余额服务是大部分情况下，返回1成功
                'respmsg': error_map[QFRET.OK],
                'data'   : '',      # 实际返回的数据, 大部分情况下只要respcd就够了，有些需要
            }
            try:
                ret = func(*args, **kwargs)
            except ServerError, se:
                log.warn('request failed: errcode:%s errmsg:%s', se.code, se.msg)
                resp['respcd'] = se.code
                resp['respmsg'] = se.msg
            except Exception, e:
                log.error('not define exception: [[%s]]', traceback.format_exc())
                resp['respcd'] = QFRET.UNKOWNERR
                resp['respmsg'] = error_map[QFRET.UNKOWNERR]
            else:
                log.info('reuest success: %s', ret)
                resp['data'] = ret
            return resp
        return __
    return _

class MarketingClient(object):
    '''余额客户端'''
    def __init__(self, server):
        self.server = server

    @call_func()
    def coupon_rule_create(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'coupon_rule_create', *args, **kwargs)

    @call_func()
    def coupon_rule_change(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'coupon_rule_change', *args, **kwargs)

    @call_func()
    def coupon_rule_query(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'coupon_rule_query', *args, **kwargs)

    @call_func()
    def activity_create(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'activity_create', *args, **kwargs)

    @call_func()
    def activity_change(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'activity_change', *args, **kwargs)

    @call_func()
    def activity_query(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'activity_query', *args, **kwargs)

    @call_func()
    def activity_share(self, *args, **kwargs):
        for key in ['src', 'txamt', 'customer_id']:
            if not kwargs.has_key(key) or not kwargs[key]:
                raise ServerError("4200", "%s missing" % key)
        arg = ActivityShareArgs(src=kwargs['src'], customer_id=kwargs['customer_id'],
                trade_amt=int(kwargs['txamt']),  mchnt_id=str(kwargs.get('mchnt_id', '')), type=kwargs.get('type', 1))
        return thrift_callex(self.server, QFMarketing, 'activity_share', arg)

    @call_func()
    def activity_stat(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'activity_stat', *args, **kwargs)

    @call_func()
    def coupon_use(self, *args, **kwargs):
        for key in ['src', 'coupon_code', 'out_sn']:
            if not kwargs.has_key(key) or not kwargs[key]:
                raise ServerError("4200", "%s missing" % key)
                
        arg = CouponOperateArgs(kwargs['src'], coupon_code=kwargs['coupon_code'],
                out_sn=kwargs['out_sn'], type=3, mchnt_id=kwargs.get('mchnt_id', ''),
                customer_id=kwargs.get('customer_id', ''), trade_amt=int(kwargs.get('txamt', '0')), 
                content=kwargs.get('content', ''))

        return thrift_callex(self.server, QFMarketing, 'coupon_use', arg)

    @call_func()
    def coupon_rollback(self, *args, **kwargs):
        for key in ['src', 'coupon_code', 'out_sn', 'orig_out_sn']:
            if not kwargs.has_key(key) or not kwargs[key]:
                raise ServerError("4200", "%s missing" % key)

        arg = CouponOperateArgs(src=kwargs['src'], coupon_code=kwargs['coupon_code'],
                out_sn=kwargs['out_sn'], type=int(kwargs.get('type', '5')), mchnt_id=kwargs.get('mchnt_id', ''),
                orig_out_sn = kwargs.get('orig_out_sn', ''), customer_id=kwargs.get('customer_id', ''), 
                trade_amt=int(kwargs.get('txamt', '0')))

        return thrift_callex(self.server, QFMarketing, 'coupon_rollback', arg)

    @call_func()
    def coupon_use_record_query(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'coupon_use_record_query', *args, **kwargs)

    @call_func()
    def coupon_use_record_count(self, *args, **kwargs):
        return thrift_callex(self.server, QFMarketing, 'coupon_use_record_count', *args, **kwargs)


