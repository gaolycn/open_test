# coding=utf-8

from py8583.spec import Py8583Spec
from py8583.field import Py8583SimpleField,Py8583ComposedField
from py8583.constant import LengthType, DataType


class Huiyi8583SimpleField(Py8583SimpleField):
    def _gen_data_type(self, content_type):
        if content_type == 'b':
            return DataType.BIN
        else:
            return DataType.ASCII

    def _trans_track_data(self, value):
        return value

    def _untrans_track_data(self, value):
        return value


class HuiyiSpec(Py8583Spec):
    def __init__(self):
        super(HuiyiSpec, self).__init__()

        huiyi_spec = {
            'MTI': Huiyi8583SimpleField('MTI', 'message type indentify', 'a', 4, LengthType.FIXED),
            1: Huiyi8583SimpleField(1, 'extended bitmap', 'b', 8, LengthType.FIXED),
            2: Huiyi8583SimpleField(2, 'primary_acct_num', 'n', 19, LengthType.LLVAR),
            3: Huiyi8583SimpleField(3, 'processing_code', 'n', 6, LengthType.FIXED),
            4: Huiyi8583SimpleField(4, 'amout transaction', 'n', 12, LengthType.FIXED),
            5: Huiyi8583SimpleField(5, 'amount settlement', 'n', 12, LengthType.FIXED),
            6: Huiyi8583SimpleField(6, 'amount, cardholder billing', 'n', 12, LengthType.FIXED),
            7: Huiyi8583SimpleField(7, 'transmsn_date_time', 'n', 10, LengthType.FIXED, remark='MMDDhhmmss'),
            11: Huiyi8583SimpleField(11, 'sys_trace_audit_num', 'n', 6, LengthType.FIXED),
            12: Huiyi8583SimpleField(12, 'time_local_trans', 'n', 6, LengthType.FIXED, remark='hhmmss'),

            13: Huiyi8583SimpleField(13, 'date_local_trans', 'n', 4, LengthType.FIXED, remark='MMDD'),
            14: Huiyi8583SimpleField(14, 'date_expr', 'n', 4, LengthType.FIXED, remark='YYMM'),
            15: Huiyi8583SimpleField(15, 'date_settlmt', 'n', 4, LengthType.FIXED, remark='MMDD'),
            18: Huiyi8583SimpleField(18, 'mchnt_type', 'n', 4, LengthType.FIXED),
            19: Huiyi8583SimpleField(19, 'acq_inst_cntry_code', 'n', 3, LengthType.FIXED),

            22: Huiyi8583SimpleField(22, 'pos_entry_mode_code', 'n', 3, LengthType.FIXED),
            23: Huiyi8583SimpleField(23, 'card_sequence_num', 'n', 3, LengthType.FIXED),
            25: Huiyi8583SimpleField(25, 'pos_cond_code', 'n', 2, LengthType.FIXED),
            26: Huiyi8583SimpleField(26, 'pos_pin_captr_code', 'n', 2, LengthType.FIXED),
            32: Huiyi8583SimpleField(32, 'acq_inst_id_code', 'n', 11, LengthType.LLVAR),
            33: Huiyi8583SimpleField(33, 'fwd_inst_id_code', 'n', 11, LengthType.LLVAR),

            35: Huiyi8583SimpleField(35, 'track_2_data', 'z', 37, LengthType.LLVAR),
            36: Huiyi8583SimpleField(36, 'track_3_data', 'z', 104, LengthType.LLLVAR),
            37: Huiyi8583SimpleField(37, 'retrivl_ref_num', 'an', 12, LengthType.FIXED),
            38: Huiyi8583SimpleField(38, 'authorization Identification Response', 'an', 6, LengthType.FIXED),
            39: Huiyi8583SimpleField(39, 'resp_code', 'an', 2, LengthType.FIXED),
            41: Huiyi8583SimpleField(41, 'card_accptr_termnl_id', 'ans', 8, LengthType.FIXED),

            42: Huiyi8583SimpleField(42, 'card_accptr_id', 'ans', 15, LengthType.FIXED),
            43: Huiyi8583SimpleField(43, 'card_accptr_name_loc', 'ans', 40, LengthType.FIXED, encoding='gbk'),
            44: Huiyi8583SimpleField(44, 'Addtnl_resp_code', 'ans', 25, LengthType.LLVAR),
            45: Huiyi8583SimpleField(45, 'track_1_data', 'z', 79, LengthType.LLVAR),
            48: Huiyi8583SimpleField(48, 'addtnl_data_private', 'ans', 512, LengthType.LLLVAR),
            49: Huiyi8583SimpleField(49, 'currcy_code_trans', 'an', 3, LengthType.FIXED),

            52: Huiyi8583SimpleField(52, 'pin_data', 'b', 8, LengthType.FIXED),
            53: Huiyi8583SimpleField(53, 'sec_relatd_ctrl_info', 'n', 16, LengthType.FIXED),
            54: Huiyi8583SimpleField(54, 'addtnl_amt', 'an', 40, LengthType.LLLVAR),
            55: Huiyi8583SimpleField(55, 'icc_data', 'ansb', 255, LengthType.LLLVAR),
            57: Huiyi8583SimpleField(57, 'issr_addtnl_data', 'ans', 100, LengthType.LLLVAR),
            60: Huiyi8583SimpleField(60, 'reserved', 'ans', 100, LengthType.LLLVAR),

            61: Huiyi8583SimpleField(61, 'ch_auth_info', 'ans', 200, LengthType.LLLVAR),
            70: Huiyi8583SimpleField(70, 'network management info code', 'n', 3, LengthType.FIXED),
            90: Huiyi8583SimpleField(90, 'original data elements', 'n', 42, LengthType.FIXED),
            96: Huiyi8583SimpleField(96, 'message security-code', 'b', 8, LengthType.FIXED),
            100: Huiyi8583SimpleField(100, 'rcvg_inst_id_code', 'n', 11, LengthType.LLVAR),
            121: Huiyi8583SimpleField(121, 'national_sw_resved', 'ans', 100, LengthType.LLLVAR),
            122: Huiyi8583SimpleField(122, 'acq_inst_resvd', 'ans', 100, LengthType.LLLVAR),
            123: Huiyi8583SimpleField(123, 'issr_inst_resvd', 'ans', 100, LengthType.LLLVAR),
            128: Huiyi8583SimpleField(128, 'msg_authn_code', 'b', 8, LengthType.FIXED),
        }

        self._spec = huiyi_spec
        # self._spec.update()

        # self._spec[1].data_type = DataType.BIN
