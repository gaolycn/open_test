# coding=utf-8
import json
import logging
import struct
import datetime
import re
import binascii

from qfcommon.qfpay import defines

from py8583.py8583 import Py8583
from py8583 import err as py8583_err
from huiyi_spec import HuiyiSpec
import huiyi_field55
from huiyi_constant import busicd2field_info, qfpay_busicd2huiyi_busicd, LOGGER_NAME
import huiyi_err


log = logging.getLogger(LOGGER_NAME)


# 报文类型
class HY_MSG_TYPE:
    MANAGE = 'manage'  # 管理类
    TRADE = 'trade'  # 交易类


_NO_DATA = object()  # 该域无数据
_DONT_NEED = object()  # 该域没有使用(不需要)


class HuiyiProto(object):
    """
    汇宜协议封/解包
    """

    _HEADER_LEN = 46  # 头部长度固定为46字节
    _HEADER_FLAG_VERSION = 0b00000010  # 生产环境最高位是0，测试环境最高为是1
    _ORGANIZATION_NUMBER = '66810000'  # 生成环境钱方在汇宜下的机构号
    _CUPS_NUMBER = '00010000'  # CUPS的机构号
    _KEEP_CHAR_PATTERN = re.compile(r'[^A-Z0-9,. ]')  # 用于移除非保留字符
    _SPACE_TRANS_PATTERN = re.compile(r'( ){2,}')  # 用于替换连续多个空格为一个空格

    def __init__(self, debug=False):
        if debug:
            self._HEADER_FLAG_VERSION = 0b10000010  # 测试环境的头标志和版本号
            self._ORGANIZATION_NUMBER = '66800000'  # 测试环境钱方在汇宜下的机构号

        self.spec = HuiyiSpec()

    def qf2huiyi(self, indata, mac_generator=None):
        """

        :param indata:
        :param mac_generator:
        :type indata: dict
        :type mac_generator: callable | None
        :return:
        :rtype: str
        """

        if not callable(mac_generator) and \
                        mac_generator is not None:
            raise TypeError('mac_generator must be callable!')

        busicd = indata['busicd']
        field_info = busicd2field_info[busicd]

        req_data = {}
        # 填充必填域
        for index in field_info['qf2hy']['must']:
            value = self._get_value_from_qfpay(index, indata)
            if value == _NO_DATA:
                log.warn('Gen must field(%s) failed!', index)
                raise huiyi_err.HuiyiLackMustFieldError('Lack must field(%s)' % index)

            req_data[index] = value

        # 填充可选域
        for index in field_info['qf2hy']['option']:
            value = self._get_value_from_qfpay(index, indata)
            if value == _NO_DATA:
                log.debug('Gen option field(%s) got NO_DATA', index)
                continue

            req_data[index] = value

        return self.build(req_data, field_info, mac_generator)

    def huiyi2qf(self, req_data, resp_str, mac_checker=None):
        """

        :param req_data:
        :param resp_str:
        :param mac_checker:
        :type req_data: dict
        :type resp_str: str
        :type mac_checker: callable | None
        :return:
        :rtype: str
        """

        if not callable(mac_checker) and \
                        mac_checker is not None:
            raise TypeError('mac_checker must be callable!')

        busicd = req_data['busicd']
        field_info = busicd2field_info[busicd]
        result_data = {}

        resp8583 = self.parse(resp_str, field_info['mac'], mac_checker)

        def _update_result_data(key, value):
            if value is _DONT_NEED:
                return

            result_data[key] = value

        # 解析必填域
        for index in field_info['hy2qf']['must']:
            try:
                key, value = self._get_value_from_huiyi_imp(index, resp8583)
            except py8583_err.Py8583BitNotExistError as e:
                log.warn('Not found must field(%s) in resp_8583. err: %s' % (index, e))
                raise huiyi_err.HuiyiLackMustFieldError('Lack must field(%s)', index)

            _update_result_data(key, value)

        # 解析可选域
        for index in field_info['hy2qf']['option']:
            try:
                key, value = self._get_value_from_huiyi(index, resp8583)
            except py8583_err.Py8583BitNotExistError as e:
                log.debug('Not found optional field(%s) in resp_8583. err: %s' % (index, e))
                continue

            _update_result_data(key, value)

        # 拼接一些参数
        if 'date_local_trans' in result_data and\
                'time_local_trans' in result_data:
            result_data['localdt'] = result_data['date_local_trans'] + result_data['time_local_trans']

        if 'date_local_trans' in result_data and\
                'clisn' in result_data:
            result_data['syssn'] = result_data['date_local_trans'] + result_data['clisn']

        if 'settlement_date' in result_data:
            result_data['stldt'] = str(datetime.datetime.now().year) + result_data['settlement_date']

        return result_data

    def build(self, req_data, field_info, mac_generator):
        """
        从req_data中打包8583数据包，并返回已经打包完成的数据包字符串. 一般情况下不要直接调用。
        :param req_data:
        :param field_info:
        :param mac_generator:
        :type req_data: dict
        :type field_info: dict
        :type mac_generator: callable | None
        :return:
        :rtype: str
        """

        req8583 = Py8583(self.spec)

        # 填充域
        req8583.MTI = field_info['qf2hy']['type']
        for index, value in req_data.items():
            req8583.set_bit(index, value)

        #  当传入了mac_generator时，生成mac
        if mac_generator is not None:
            mac = mac_generator(self._gen_mab(req8583, field_info['mac']))
            req8583.set_bit(128, mac)

        # 生成请求体
        body = req8583.build()

        return self._pack_header(len(body)) + body

    def parse(self, resp_str, mac_fields, mac_checker):
        """
        将收到的8583数据包字符串解析为py8583对象. 一般情况下不要直接调用。
        :param resp_str:
        :param mac_fields:
        :param mac_checker:
        :type resp_str: str
        :type mac_fields: list | None
        :type mac_checker: callable | None
        :return:
        :rtype: Py8583
        :raise: huiyi_err.HuiyiParseHeaderError | huiyi_err.HuiyiCheckMacError
        """

        resp8583 = Py8583(self.spec)

        header, body = self._unpack_header(resp_str)
        if body == '':
            raise huiyi_err.HuiyiParseHeaderError('Get null body!')

        resp8583.parse(body)

        #  当传入了mac_checker时，校验mac
        if mac_checker is not None:
            ret_mac = resp8583.get_bit(128)
            ret = mac_checker(self._gen_mab(resp8583, mac_fields), ret_mac)
            if ret != defines.QF_PAY_OK:
                raise huiyi_err.HuiyiCheckMacError('Check mac faield!')

        return resp8583

    def _gen_mab(self, py8583, mac_fields):
        """

        :param py8583:
        :param mac_fields:
        :type py8583: Py8583
        :type mac_fields: list
        :return:
        :rtype: str
        """

        all_field_data = []
        for index in mac_fields:
            if index == 'MTI':
                field_value = py8583.MTI
            else:
                # 忽略不存在的域
                try:
                    field_value = py8583.get_bit(index)
                except py8583_err.Py8583BitNotExistError:
                    log.debug('func=_gen_mab|msg=field(%s) not exsist, ignore it.' % index)
                    continue

            field_spec = py8583.get_field_spec(index)
            data = field_spec.pack(field_value)
            data = str(data)
            if index == 90:  # 90域只取前20位
                data = data[:20]

            # 为生成mab做一些转换
            data = data.upper()  # 所有小写字母转大写
            data = self._KEEP_CHAR_PATTERN.sub('', data)  # 移除所有非字母(A-Z)，数字(0-9),空格，逗号，点号意外的字符
            data = data.strip()  # 移除首尾空格
            data = self._SPACE_TRANS_PATTERN.sub(' ', data)  # 多个连续空格，用一个替换

            all_field_data.append(data)

        mab = ' '.join(all_field_data)  # message authentication block
        log.debug('gen mab: %s', mab)

        return mab

    def _pack_header(self, message_len):
        """
        打包汇宜8583数据包的头部
        :param message_len: 消息体的长度
        :return:
        :rtype: str
        """
        if message_len < 46 or message_len > 1846:
            raise huiyi_err.HuiyiBuildError('message is too long or small(%s)' % message_len)

        header = b''

        header_len = struct.pack('!B', self._HEADER_LEN)
        header_flag_version = struct.pack('!B', self._HEADER_FLAG_VERSION)
        message_len = '{0:0>4}'.format(message_len)
        dst_id = '{0: <11}'.format(self._CUPS_NUMBER)  # 入网机构发出的报文中，该域必须为CUPS的ID，00010000
        src_id = '{0: <11}'.format(self._ORGANIZATION_NUMBER)
        reserved = '000'  # 24bit的0
        batch_number = '0'
        transaction_info = '00000000'  # 入网机构必须填8byte的0
        user_info = '0'  # 8bit的用户信息，不需要必须填0
        reject_code = '00000'  # 入网机构必须填5byte的0

        header = header.join(
            [header_len, header_flag_version, message_len,
             dst_id, src_id, reserved, batch_number,
             transaction_info, user_info, reject_code]
        )
        log.debug('func=_pack_header|msg=gen_header is: %s', header)
        if len(header) != self._HEADER_LEN:
            log.warn('Expected header_len is %s, got is %s', self._HEADER_LEN, len(header))
            raise huiyi_err.HuiyiBuildHeaderError('Pack header got invalid header_len(%s)', len(header))

        return header

    def _unpack_header(self, message):
        """
        解包汇宜8583数据包的头部
        :param message:
        :return: 头部字典和报文体字符串
        :rtype: (dict,str)
        """

        header = message[:self._HEADER_LEN]
        log.debug('func=_unpack_header|msg=origin header: %s', header)

        pos = 0
        header_len = struct.unpack('!B', message[pos])[0];  pos += 1
        if header_len != self._HEADER_LEN:
            log.warn('unpack Got invalid header_len(%s), expected(%s)', header_len, self._HEADER_LEN)
            raise huiyi_err.HuiyiParseHeaderError('Invalid header_len(%s), expected(%s).'
                                                  % (header_len, self._HEADER_LEN))
        header_flag_version = struct.unpack('!B', header[pos])[0];  pos += 1
        if header_flag_version != self._HEADER_FLAG_VERSION:
            log.warn('Expected header_flag_version (%s), got (%s)', self._HEADER_FLAG_VERSION, header_flag_version)
            raise huiyi_err.HuiyiParseHeaderError('Invalid header_lag_version(%s)' % header_flag_version)
        message_len = header[pos:pos + 4]; pos += 4
        dst_id = header[pos:pos + 11];  pos += 11
        if dst_id.strip() != self._ORGANIZATION_NUMBER:
            log.warn('Expected dst_id(%s), got(%s)', self._ORGANIZATION_NUMBER, dst_id)
            raise huiyi_err.HuiyiParseHeaderError('Invalid dst_id(%s)' % dst_id)
        src_id = header[pos:pos + 11];  pos += 11
        reserved = header[pos:pos + 3];  pos += 3
        batch_number = header[pos];  pos += 1
        transaction_info = header[pos:pos + 8];  pos += 8
        user_info = header[pos];  pos += 1
        reject_code = header[pos:pos + 5];  pos += 5

        header_data = {
            'header_len': header_len,
            'header_flag_version': header_flag_version,
            'message_len': message_len,
            'dst_id': dst_id,
            'src_id': src_id,
            'reserved': reserved,
            'batch_number': batch_number,
            'transaction_info': transaction_info,
            'user_info': user_info,
            'reject_code': reject_code,
        }

        log.debug(
            'unpack_header: %s',
            json.dumps(
                header_data,
                indent=4,
            )
        )

        return header_data, message[header_len:]

    def _get_value_from_qfpay(self, index, indata):
        """

        :param index:
        :param indata:
        :type index: int
        :type indata: dict
        :return:
        :rtype: object
        """

        try:
            value = self._get_value_from_qfpay_imp(index, indata)
        except KeyError as e:
            log.debug('_get_value_from_qfpay err: %s', e)
            return _NO_DATA

        return value

    def _get_value_from_huiyi(self, index, resp8583):
        """

        :param index:
        :param resp8583:
        :type index: int
        :type resp8583: Py8583
        :return:
        :rtype: (str, object)
        """

        try:
            key, value = self._get_value_from_huiyi_imp(index, resp8583)
        except py8583_err.Py8583BitNotExistError as e:
            log.debug('_get_value_from_huiyi err: %s', e)
            raise

        return key, value

    def _get_value_from_qfpay_imp(self, index, indata):
        """

        :param index:
        :param indata:
        :type index: int
        :type indata: dict
        :return:
        """

        busicd = indata['busicd']
        # 取交易记录生成的sysdtm，以避免产生时间差，导致关联交易失败
        sysdtm_obj = datetime.datetime.strptime(indata['sysdtm'], '%Y-%m-%d %H:%M:%S')

        # primary account number  交易主账号
        if index == 2:
            return indata['cardcd']

        # processing_code  交易处理码
        if index == 3:
            return qfpay_busicd2huiyi_busicd[busicd]

        # amt_trans  交易金额
        if index == 4:
            return indata['txamt']

        # trasmsn_date_time   交易日期时间
        if index == 7:
            value = sysdtm_obj.strftime('%m%d%H%M%S')  # MMDDhhmmss

            return indata.get('transmsn_date_time', value)

        # sys_trace_audit_num  系统跟踪号
        if index == 11:
            return indata['clisn']

        # time_local_trans  受卡方所在地时间
        if index == 12:
            # 关联交易(冲正、转入确认、存款确认) 为原交易的时间
            if busicd in (defines.QF_BUSICD_REVERSAL, defines.QF_BUSICD_CANCEL_REVERSAL):
                origdt = indata['origdt']

                return origdt[-6:]  # origdt 形如： 0513144601
            else:
                return sysdtm_obj.strftime('%H%M%S')  # hhmmss

        # date_local_trans  受卡方所在地日期
        if index == 13:
            # 关联交易(冲正、转入确认、存款确认)  为原交易的日期
            if busicd in (defines.QF_BUSICD_REVERSAL, defines.QF_BUSICD_CANCEL_REVERSAL):
                origdt = indata['origdt']

                return origdt[:4]  # origdt 形如： 0513144601
            else:
                return sysdtm_obj.strftime('%m%d')  # MMDD

        # date_expr  卡有效期
        if index == 14:
            return indata['cardexpire']

        # mchnt_type 商户类型
        if index == 18:
            return indata['mcc']

        # pos_entry_mode_code  服务点输入方式
        if index == 22:
            return indata['posentrymode']

        # card seq id
        if index == 23:
            cardseqnum = indata['cardseqnum']

            # @ATTENTION IC卡特有字段 卡序列号为空代表为磁条卡，则返回无数据
            return cardseqnum if cardseqnum else _NO_DATA

        # pos_cond_code  服务店条件码
        if index == 25:
            if busicd in [defines.QF_BUSICD_PAYMENT, defines.QF_BUSICD_REVERSAL,
                          defines.QF_BUSICD_CANCEL, defines.QF_BUSICD_CANCEL_REVERSAL,
                          defines.QF_BUSICD_BALANCE, ]:
                return '00'
            elif busicd in [defines.QF_BUSICD_PAUTH, defines.QF_BUSICD_PAUTH_REVERSAL,
                            defines.QF_BUSICD_PAUTH_CANCEL, defines.QF_BUSICD_PAUTH_CANCEL_REVERSAL,
                            defines.QF_BUSICD_PAUTHCP, defines.QF_BUSICD_PAUTHCP_REVERSAL,
                            defines.QF_BUSICD_PAUTHCP_CANCEL, defines.QF_BUSICD_PAUTHCP_CANCEL_REVERSAL,
                            ]:
                return '06'

            else:
                return '91'

        # pos_pin_captr_code  服务点PIN获取码
        if index == 26:
            # 仅当有密交易,才送26域
            if 'cardpin' in indata:
                return indata.get('capture_code', '12')
            else:
                return _NO_DATA

        # acq_inst_id_code  受理机构标志码
        if index == 32:
            return indata['chcd']

        # fwd_inst_id_code  发送机构标识码
        if index == 33:
            return self._ORGANIZATION_NUMBER

        # track_2_data  第二磁道信息
        if index == 35:
            return indata['trackdata2']

        # track_3_data  第三磁道信息
        if index == 36:
            return indata['trackdata3']

        # retrivl_ref_num  检索参考号,系统流水号
        if index == 37:
            return indata['syssn']

        # authr_id_resp  授权标志应答码
        if index == 38:
            return indata['authid'] if indata['authid'] else _NO_DATA

        # resp_code 应答码
        if index == 39:
            return indata['resp_code']

        # card_accptr_termnl_id  受卡机标识码
        if index == 41:
            return indata['terminalid']

        # card_accptr_id  受卡方标识码
        if index == 42:
            return indata['mchntid']

        # card_accptr_name_loc  受卡方名称地址
        if index == 43:
            return 'qfpay'

        # addtnl_data_private  附加数据-私有
        if index == 48:
            return _NO_DATA

        # curcy_code_trans  交易货币代码
        if index == 49:
            return indata['txcurrcd']

        # pin_data  个人标识码数据
        if index == 52:
            cardpin = indata['cardpin']

            # payoffline 传入的是hexlify之后的16进制字符串,而汇宜需要二进制数据。 故转换之
            return binascii.unhexlify(cardpin)

        # sec_relatd_ctrl_info  安全控制信息
        if index == 53:
            if 'sec_relatd_ctrl_info' in indata:
                return indata['sec_relatd_ctrl_info']
            else:
                if indata.get('is_update_key'):  # 密钥管理类
                    field = [
                        indata['key_type'],  # 密钥类型  1 PIK,  2 MAK
                        indata['encryptor_flag'],  # 加密算法标志  0 单倍长密钥算法， 6 双倍长密钥算法
                        '0' * 14,  # 保留使用
                    ]
                else:
                    field = [
                        indata['pin_format'],  # 密钥格式。 1 ANSI x9.8(不带主账号信息),  2 ANSI X9.8（带主账号信息）
                        indata['encryptor_flag'],  # 加密算法标志。 0 单倍长密钥算法， 6 双倍长密钥算法
                        '0' * 14,  # 保留使用
                    ]

                return ''.join(field)

        # icc data
        if index == 55:
            iccdata = indata['iccdata']

            # @ATTENTION IC卡特有字段
            if iccdata:
                # 余额查询、消费撤销、预授权撤销、存款撤销、预授权完成（请求）、预授权完成（请求）撤销交易 不送55域
                if busicd in {defines.QF_BUSICD_BALANCE, defines.QF_BUSICD_CANCEL,
                              defines.QF_BUSICD_PAUTH_CANCEL, defines.QF_BUSICD_PAUTHCP_CANCEL}:
                    return _NO_DATA
                # 冲正需要剔除一些TLV
                elif busicd in {defines.QF_BUSICD_REVERSAL, defines.QF_BUSICD_CANCEL_REVERSAL}:
                    iccdata_bin = binascii.unhexlify(iccdata)
                    iccdata_data = huiyi_field55.parse(iccdata_bin)

                    new_iccdata_tags = ['95', '9f1e', '9f10', '9f36', 'df31'] # 使用小写的tag
                    # 从原iccdata数据中取需要的TLV，并忽略原iccdata不存在的TLV
                    new_iccdata_data = {
                        tag:iccdata_data[tag]
                        for tag in new_iccdata_tags
                        if tag in iccdata_data
                    }
                    new_iccdata = huiyi_field55.build(new_iccdata_data)

                    return binascii.unhexlify(new_iccdata)
                else:
                    return binascii.unhexlify(iccdata)
            # 为空代表为磁条卡，返回无数据
            else:
                return _NO_DATA

        # issr_addtnl_data  附加交易信息
        if index == 57:
            return _NO_DATA
            # 我们目前不传入57域，以商户号来区分是T0还是T1.
            #tag = 'BD'
            #value = qfpay_busicd2huiyi_busicd[busicd]
            #value_len = len(value)

            #return '{tag}{value_len:0>3}{value}'.format(tag=tag, value_len=value_len, value=value)

        # reserved  自定义域
        if index == 60:
            # 60.1 报文原因码
            if busicd == defines.QF_BUSICD_REVERSAL:
                message_reason_code = '0000'  # TODO 冲正不一样
            else:
                message_reason_code = '0000'
            sub_field1 = message_reason_code

            # 60.2 服务点附加信息
            sub_field2 = [
                '9',  # 60.2.1  账户所有人类型
                '0',  # 60.2.2  终端读取能力
                '0',  # 60.2.3  IC卡条件码
                '0',  # 60.2.4  保留使用
                '00',  # 60.2.5  终端类型
                '0',  # 60.2.6 境外受理免密网络标志以及跨境汇款到账比重要求
                '1',  # 60.2.7  IC卡验证可靠性标志
                '00',  # 60.2.8  电子商户标志
                '00',  # 60.2.9  交互方式标志
            ]
            sub_field2 = ''.join(sub_field2)

            # 60.3 交易发生附加信息
            sub_field3 = [
                '00',  # 60.3.1  特殊计费类型
                '0',   # 60.3.2  特殊计费档次
                '000',  # 60.3.3  保留使用
                '0',   # 60.3.4  支持部分承兑和返回余额标志
                '0',   # 60.3.5  交易发起方式
                '0',   # 60.3.6  交易介质
                '0',   # 60.3.7  IC卡应用类型
                '00',   # 60.3.8  账户结算类型
                '0',   # 60.3.9  卡账户等级
                '00',  # 60.3.10  卡产品
            ]
            sub_field3 = ''.join(sub_field3)

            return sub_field1 + sub_field2 + sub_field3

        # ch_auth_info  持卡人身份认证信息
        if index == 61:
            # 61.1 证件编号

            # 所有交易类型中都为C6, 即根据需要填充
            return _NO_DATA

        # network management information code 网络管理信息码
        if index == 70:
            # 汇宜约定的为'101'
            return indata.get('netwk_mgmt_info_code', '101')

        # orig_data_elemts  原始数据元
        if index == 90:
            # 90.1 原始报文类型  4byte
            _orig_busicd = indata['origbusicd']  # 原始交易的busicd
            orig_mti = busicd2field_info[_orig_busicd]['qf2hy']['type']
            # 90.2 原始系统跟踪号  6byte
            orig_clisn = indata['origclisn']
            # 90.3 原始系统日期时间  10byte
            orig_dtm = indata['origdt']
            # 90.4 原始受理机构标识码  11byte
            orig_acq_org_num = '{:0>11}'.format(self._ORGANIZATION_NUMBER)
            # 90.5 原始发送机构标识码  11byte
            orig_fwd_org_num = '{:0>11}'.format(self._ORGANIZATION_NUMBER)

            return orig_mti + orig_clisn + orig_dtm + orig_acq_org_num + orig_fwd_org_num

        # rcvg_inst_id_code 接受机构标识码
        if index == 100:
            return indata.get('rcvg_inst_id_code', self._ORGANIZATION_NUMBER)

        # acq_inst_resvd  受理方保留
        if index == 122:
            # 122.1 商户扣率
            # 122.2 手里放信息

            # 所有交易类型中都是可选字段，所以可以不填充
            return _NO_DATA

        # msg_authn_code  报文鉴别码
        if index == 128:
            return _NO_DATA  # 需要手动计算

    def _get_value_from_huiyi_imp(self, index, resp8583):
        """
        [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 23, 25, 32, 33, 37, 38, 39, 41, 42, 44, 48, 49, 50, 51, 53, 54, 55, 57, 60, 61, 70, 96, 100, 121, 122, 123, 128]
        :type resp8583: Py8583
        """

        value = resp8583.get_bit(index)

        # primary account number   主账户
        if index == 2:
            return 'cardcd', value

        # processing code, 交易处理吗
        if index == 3:
            pass

        # amt trans, 交易金额
        if index == 4:
            return 'txamt', value

        # settle_amt， 清算金额
        if index == 5:
            pass

        # cardholder billing, 持卡人扣款金额
        if index == 6:
            pass

        # transmission date and time, 交易传输时间
        if index == 7:
            return 'transmsn_date_time', value

        # settle_rate, 清算汇率
        if index == 9:
            pass

        # cardholder billing rate, 持卡人扣款汇率
        if index == 10:
            pass

        # sys trace audit num,  系统跟踪号
        if index == 11:
            return 'clisn', value

        # time local trans, 受卡方所在地时间
        if index == 12:
            return 'time_local_trans', value

        # date local trans, 受卡方所在地日期
        if index == 13:
            return 'date_local_trans', value

        # card expired date, 卡有效期
        if index == 14:
            return 'expiredate', value

        #  date_settlmt  清算时间
        if index == 15:
            return 'settlement_date', value

        # date_conv, 兑换日期
        if index == 16:
            pass

        # mchnt_type, 商户类型 mcc
        if index == 18:
            pass

        # acq_inst_cntry_code, 受理机构国家代码
        if index == 19:
            pass

        # pos entry mode code, 服务店输入方式码
        if index == 22:
            return 'posentrymode', value

        # card seq id， 卡序列号
        if index == 23:
            return 'card_seq_id', value

        # acq inst id code, 代理机构标识码
        if index == 32:
            return 'inscd', value

        # forwarding institution identification code, 发送机构标识码
        if index == 33:
            return 'fwd_inst_id_code', value

        # track 2 data
        if index == 35:
            return 'trackdata2', value

        # track 3 data
        if index == 36:
            return 'trackdata3', value

        # retrivl ref num, 检索参考号
        if index == 37:
            return 'retrievalnum', value

        # auth id response, 授权标识应答码
        if index == 38:
            return 'authid', value

        # resp code, 应答码
        if index == 39:
            return 'respcd', value

        # card accptr termnl id, 受卡机终端标识码
        if index == 41:
            return 'terminalid', value

        # card accptr id, 受卡方标识码
        if index == 42:
            return 'mchntid', value

        # addtnl_resp_code, 附加响应数据
        if index == 44:
            return '_addtnl_resp_code', value

        # addtnl_data_private,  附加数据私有
        if index == 48:
            return 'addtnl_data_private', value

        # currcy code trans， 交易货币代码
        if index == 49:
            return 'txcurrcd', value

        # currcy_code_settlmt,  清算货币代码
        if index == 50:
            pass

        # currcy_code_cdhldr_bil, 持卡人账户货币代码
        if index == 51:
            pass

        # pin data, 个人标识码
        if index == 52:
            return 'cardpin', value

        # security related control information, 安全控制信息
        if index == 53:
            return 'sec_relatd_ctrl_info', value

        # addtnl_amt, 实际余额
        if index == 54:
            pos = 0
            # 账面余额
            ledger_balance_account_type = value[pos:pos+2];  pos += 2  # 账户类型
            ledger_balance_type = value[pos:pos+2];  pos += 2  # 余额类型
            ledger_balance_currency = value[pos:pos+3];  pos += 3  # 货币代码
            ledger_balance_symbol = value[pos:pos+1];  pos += 1  # 余额符号
            ledger_balance_amount = value[pos:pos+12];  pos += 12  # 余额

            # 可用余额
            available_balance_account_type = value[pos:pos+2];  pos += 2  # 账户类型
            available_balance_type = value[pos:pos+2];  pos += 2  # 余额类型
            available_balance_currency = value[pos:pos+3];  pos += 3  # 货币代码
            available_balance_symbol = value[pos:pos+1];  pos += 1  # 余额符号
            available_balance_amount = value[pos:pos+12];  pos += 12  # 余额


            return 'balance_txamt', ledger_balance_amount

        # IC卡数据域
        if index == 55:
            return 'iccdata', binascii.hexlify(value)

        # addtnl_data,  附加交易信息
        if index == 57:
            pass

        # 明细查询域
        if index == 59:
            return 'detail_inqrng', value

        # reserved, 自定义域
        if index == 60:
            pass

        # ch_auth_info, 持卡人身份认证信息
        if index == 61:
            pass

        # 平台签到时，更新密钥
        if index == 62:
            return 'swiching_data', value

        # 网络管理信息码
        if index == 70:
            return 'netwk_mgmt_info_code', value

        # msg_security_code  报文安全码
        if index == 96:
            return 'msg_security_code', value

        # rcvg_inst_id_code  接受机构标识码
        if index == 100:
            return 'rcvg_inst_id_code', value

        # national_sw_resvd,  银联处理中心保留
        if index == 121:
            pass

        # acq_inst_resvd,  受理方保留
        if index == 122:
            pass

        # issr_inst_resvd,  发卡方保留
        if index == 123:
            pass

        # 报文鉴别码,mac, message authentication code
        if index == 128:
            return 'mac', value

        return 'NOT_KEY', _DONT_NEED
