# coding: utf-8

import logging

from qfcommon.qfpay.defines import QF_BUSICD_PAYMENT, QF_CARD_CREDIT, QF_CARD_DEBIT
from qfcommon.thriftclient.fund import FundService
from qfcommon.thriftclient.fund.ttypes import FundConfigArgs, MerchantPara, MerchantType

from qfcommon.base.tools import thrift_callex

log = logging.getLogger()


DEFAULT_TRADE_BUSICD = {
    # 刷卡
    '000000': {'trade_type': '100', 'card_type': 1, 'settletn': 1}, # 这里的卡类型没什么意义，到时会根据传过来的卡类型替换
    # 微信
    '800201': {'trade_type': '201', 'card_type': 5, 'settletn': 1}, 
    '800207': {'trade_type': '202', 'card_type': 5, 'settletn': 1}, 
    '800208': {'trade_type': '200', 'card_type': 5, 'settletn': 1}, 
    # 支付宝
    '800101': {'trade_type': '301', 'card_type': 5, 'settletn': 1}, 
    '800107': {'trade_type': '302', 'card_type': 5, 'settletn': 1}, 
    '800108': {'trade_type': '300', 'card_type': 5, 'settletn': 1}, 
    # 京东
    '800507': {'trade_type': '602', 'card_type': 5, 'settletn': 1}, 
    # QQ钱包
    '800601': {'trade_type': '701', 'card_type': 5, 'settletn': 1}, 
    '800607': {'trade_type': '702', 'card_type': 5, 'settletn': 1}, 
    '800608': {'trade_type': '700', 'card_type': 5, 'settletn': 1}, 
}

ACCT_TYPE_TRADE_QF       = 200
ACCT_TYPE_TRADE_CHNL     = 201
ACCT_TYPE_TRADE_NOSETTLE = None

# 帐户类型
TRADE_TYPE_SWIPE       = '100'  # 刷卡交易
TRADE_TYPE_SWIPE_HY_T0 = '110'  # 汇宜h0

def trade2acct_type(fund_server, userid, busicd, 
        chnl_code, chnl_termid, chnl_mchntid, cardtp=None, trade_busicd=None):
    '''
        获取交易的帐户类型与交易信息(交易类型，卡类型，结算类型)
        返回值: 帐户类型, 交易信息(交易类型，卡类型，结算类型)
        如果调用失败，则返回异常信息, 此交易不入帐户
        如果帐户类型为None，则交易不入帐户
        刷卡交易，cardtp必须提供
    '''
    trade_busicd = trade_busicd or DEFAULT_TRADE_BUSICD
    if not is_trade_settle(fund_server, userid, busicd, chnl_termid, chnl_mchntid):
        acct_type_id = ACCT_TYPE_TRADE_NOSETTLE
        trade_info   = None
    else:
        acct_type_id, trade_info = chnl2acct_type(fund_server, 
                chnl_code, chnl_mchntid, trade_busicd, busicd, cardtp)
    return acct_type_id, trade_info

def is_trade_settle(fund_server, userid, busicd, chnl_termid, chnl_mchntid):
    '''
        交易是否需要结算
        这个接口如果调用很频繁，建议自己缓存验证，因为大部分情况下它需要调用三次，才能拿到结果
    '''
    # 构造请求数据
    req_data = FundConfigArgs()    
    req_data.state = 1 
    req_data.iscompare = 2 
    req_data.page = 1 
    req_data.maxnum = 2
    req_data.busicds = [busicd, ]
    # 根据userid验证交易是否需要结算
    req_data.val_type = 3
    req_data.vals = [str(userid), ]
    log.debug('find fund req_data:%s', req_data)
    resp_data = thrift_callex(fund_server, FundService, 'findfund', req_data)
    log.info('find fund resp_data:%s', resp_data)
    if not resp_data:
        raise Exception, 'call findfund failed'
    if resp_data.records and len(resp_data.records) > 0:
        log.info('trade not need deal because of userid')
        return False
    # 根据通道商户号(chnl_termid)验证交易是否需要结算
    req_data.val_type = 2
    req_data.vals = [str(chnl_termid), ]
    log.debug('find fund req_data:%s', req_data)
    resp_data = thrift_callex(fund_server, FundService, 'findfund', req_data)
    log.info('find fund resp_data:%s', resp_data)
    if not resp_data:
        raise Exception, 'call findfund failed'
    if resp_data.records and len(resp_data.records) > 0:
        log.info('trade not need deal because of chnl termid')
        return False
    # 根据通道商户id(chnl_mchntid)验证交易是否需要结算
    req_data.val_type = 1
    req_data.vals = [str(chnl_mchntid), ]
    log.debug('find fund req_data:%s', req_data)
    resp_data = thrift_callex(fund_server, FundService, 'findfund', req_data)
    log.info('find fund resp_data:%s', resp_data)
    if not resp_data:
        raise Exception, 'call findfund failed'
    if resp_data.records and len(resp_data.records) > 0:
        log.info('trade not need deal because of chnl mchntid')
        return False
    # 需要结算
    return True

def chnl2acct_type(fund_server, chnl_code, chnl_mchntid, trade_busicd, busicd, cardtp=None):
    '''
        获取通道的帐户类型
        返回值: 帐户类型, 是否是汇宜t0
        如果调用失败，则返回异常信息, 此交易不入帐户
    '''
    req_args = MerchantPara()
    req_args.chnl_userids = [chnl_mchntid, ]
    req_args.chnl_code = chnl_code
    log.debug('get user chnl req_data:%s', req_args)
    resp_data = thrift_callex(fund_server, FundService, 'getMerchantType', req_args)
    log.info('get user chnl resp_data:%s', resp_data)
    if not resp_data:
        # 调用失败，入不可结算
        log.warn('call failed. not settle channle')
        raise Exception, 'getMerchantType failed. chnl_code:%s chnl_userid:%s' % (chnl_code, chnl_mchntid)
    acct_type_id = ACCT_TYPE_TRADE_NOSETTLE
    if chnl_mchntid not in resp_data:
        # 调用失败，入不可结算
        log.warn('call failed. not settle channle')
        raise Exception, 'getMerchantType failed. chnl_code:%s chnl_userid:%s' % (chnl_code, chnl_mchntid)
    elif resp_data[chnl_mchntid] == MerchantType.BIG_MERCHANT:
        log.info('qf settle. chnl_code:%s chnl_userid:%s', chnl_code, chnl_mchntid)
        acct_type_id = ACCT_TYPE_TRADE_QF
        is_hy_t0     = False
    elif resp_data[chnl_mchntid] == MerchantType.REAL_MERCHANT:
        log.info('channel settle. chnl_code:%s chnl_userid:%s', chnl_code, chnl_mchntid)
        acct_type_id = ACCT_TYPE_TRADE_CHNL
        is_hy_t0     = False
    elif resp_data[chnl_mchntid] == MerchantType.T0_MERCHANT:
        log.info('channel settle, HY_T0 . chnl_code:%s chnl_userid:%s', chnl_code, chnl_mchntid)
        acct_type_id = ACCT_TYPE_TRADE_CHNL
        is_hy_t0     = True
    else:
        # 非正常返回, 正常不会走到
        raise Exception, 'getMerchantType failed. chnl_code:%s chnl_userid:%s' % (chnl_code, chnl_mchntid)
    trade_info = busicd2trade(trade_busicd, busicd, is_hy_t0, cardtp)
    return acct_type_id, trade_info

def busicd2trade(trade_busicd, busicd, is_hy_t0, cardtp=None):
    '''busicd转trade_type'''
    if cardtp is None and busicd == QF_BUSICD_PAYMENT:
        raise Exception, 'swipe card trade, no cardtp. busicd:%s cardtp:%s' % (busicd, cardtp)
    trade = trade_busicd[busicd]
    if busicd == QF_BUSICD_PAYMENT:
        # 如果卡类型不为信用卡，则为借记卡
        trade['card_type']  = cardtp if cardtp == QF_CARD_CREDIT else QF_CARD_DEBIT
        trade['trade_type'] = TRADE_TYPE_SWIPE_HY_T0 if is_hy_t0 else TRADE_TYPE_SWIPE
    return trade


if __name__ == '__main__':
    from qfcommon.base import logger
    log = logger.install('stdout')

    fund_server = [{'addr': ('172.100.101.107', 2009), 'timeout': 2000}]
    # 根据userid验证交易不结算
    ret = is_trade_settle(fund_server, 11751, '800207', 123, 132)
    assert ret == False
    # 根据chnl_termid验证交易不结算
    ret = is_trade_settle(fund_server, 1234, '800207', 11751, 132)
    assert ret == False
    # 根据chnl_mchntid验证交易不结算
    ret = is_trade_settle(fund_server, 1234, '800207', 123, 11751)
    assert ret == False
    # 结算
    ret = is_trade_settle(fund_server, 1234, '800207', 123, 1234)
    assert ret == True



