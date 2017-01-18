# coding=utf-8
from qfcommon.qfpay import defines

# LOGGER_NAME = 'huiyi_proto'
LOGGER_NAME = None

# 余额查询
BALANCE = {
    'qf2hy': {
        'type': '0200',
        'must': [2, 3, 7, 11, 12, 13, 18, 22, 25, 32, 33, 37, 41, 42, 43],
        'option': [14, 23, 26, 35, 36, 48, 49, 52, 53, 60, 61, 122, 128]
    },
    'hy2qf': {
        'type': '0210',
        'must': [2, 3, 7, 11, 12, 13, 14, 15, 18, 25, 32, 33, 37, 39, 41, 42, 100],
        # 19(C0), 49(C0), 54(C3), 57(C16), 61(C16), 121(C0), 122(C0), 128(C9)
        'option': [19, 49, 54, 57, 61, 121, 122, 123, 128],
    },
    'mac': ['MTI', 2, 3, 4, 7, 11, 18, 25, 28, 32, 33, 38, 39, 41, 42, 90],
}

# 消费
PAYMENT = {
    'qf2hy': {
        'type': '0200',
        'must': [2, 3, 4, 7, 11, 12, 13, 18, 22, 25, 32, 33, 37, 41, 42, 43, 49],
        # 26(C8), 35(C1), 36(C2), 48(C22), 52(C7), 53(C8), 57(C), 60(C), 61(C6), 128(C9)
        'option': [14, 23, 26, 35, 36, 48, 52, 53, 55, 57, 60, 61, 122, 128],
    },
    'hy2qf': {
        'type': '0210',
        'must': [2, 3, 4, 7, 11, 12, 13, 14, 15, 18, 25, 32, 33, 37, 39, 41, 42, 49, 100, ],
        # 5(C14), 6(C15), 9(C14), 10(C15), 16(C14), 19(C0), 50(C14), 51(C15), 54(C25), 57(C16), 61(C16), 121(C0), 122(C0) 128(C9)
        'option': [5, 6, 9, 10, 16, 19, 23, 38, 44, 50, 51, 54, 55, 57, 61, 121, 122, 123, 128],
    },
    'mac': ['MTI', 2, 3, 4, 7, 11, 18, 25, 28, 32, 33, 38, 39, 41, 42, 90],
}

# 消费撤销
CANCEL = {
    'qf2hy': {
        'type': '0200',
        'must': [2, 3, 4, 7, 11, 12, 13, 18, 22, 25, 32, 33, 37, 41, 42, 43, 49, 90, ],
        # 26(C8), 35(C1), 36(C2), 38(C4), 48(C22), 52(C7), 53(C8), 61(C6), 128(C9)
        'option': [23, 26, 35, 36, 38, 48, 52, 53, 55, 60, 61, 122, 128],
    },
    'hy2qf': {
        'type': '0210',
        'must': [2, 3, 4, 7, 11, 12, 13, 15, 18, 25, 32, 33, 37, 39, 41, 42, 100, ],
        #
        'option': [19, 23, 38, 44, 55, 57, 60, 61, 121, 122, 123, 128],
    },
    'mac': ['MTI', 2, 3, 4, 7, 11, 18, 25, 28, 32, 33, 38, 39, 41, 42, 90],
}

# 消费冲正
REVERSAL = {
    'qf2hy': {
        'type': '0420',
        'must': [2, 3, 4, 7, 11, 12, 13, 18, 22, 25, 32, 33, 37, 41, 42, 43, 49, 90, ],
        #
        'option': [23, 38, 48, 55, 60, 122, 128],
    },
    'hy2qf': {
        'type': '0430',
        'must': [2, 3, 4, 7, 11, 12, 13, 15, 18, 25, 32, 33, 37, 39, 41, 42, 49, ],
        #
        'option': [5, 9, 16, 23, 50, 55, 121, 122, 128],
    },
    'mac': ['MTI', 2, 3, 4, 7, 11, 18, 25, 28, 32, 33, 38, 39, 41, 42, 90],
}

# 消费撤销冲正
CANCEL_REVERSAL = REVERSAL

# 钱方发起的密钥更新申请
QF_SECRET = {
    'qf2hy': {
        'type': '0820',
        'must': [7, 11, 33, 53, 70],
        #
        'option': [],
    },
    'hy2qf': {
        'type': '0830',
        'must': [7, 11, 33, 39, 53, 70],
        #
        'option': [],
    },
    'mac': ['MTI', 7, 11, 39, 53, 70, 100],
}

# 汇宜发起的密钥更新
HY_SECRET = {
    'qf2hy': {
        'type': '0810',
        'must': [7, 11, 39, 53, 70, 100, ],
        #
        'option': [128],
    },
    'hy2qf': {
        'type': '0800',
        'must': [7, 11, 53, 70, 100, ],
        #
        'option': [48, 128, 96, ],
    },

    'mac': ['MTI', 7, 11, 39, 53, 70, 100],
}

# IC卡脚本通知
ICNOTICE = {
    'qf2hy': {
        'type': '0620',
        'must': [2, 3, 7, 11, 12, 13, 18, 22, 25, 32, 33, 37, 39, 41, 42, 43, 70, 90],
        #
        'option': [4, 23, 49, 55, 60, ],
    },
    'hy2qf': {
        'type': '0630',
        'must': [2, 3, 11, 12, 13, 15, 25, 32, 33, 39, 41, 42, 70, 100],
        #
        'option': [23, 55, 60],
    },
}

# 各个busicd对应的域信息
busicd2field_info = {
    defines.QF_BUSICD_BALANCE: BALANCE,  # 余额查询
    defines.QF_BUSICD_PAYMENT: PAYMENT,  # 消费
    defines.QF_BUSICD_CANCEL: CANCEL,  # 消费撤销
    defines.QF_BUSICD_REVERSAL: REVERSAL,  # 消费 冲正
    defines.QF_BUSICD_CANCEL_REVERSAL: CANCEL_REVERSAL,  # 消费撤销 冲正
    defines.QF_BUSICD_ICNOTICE: ICNOTICE,  # IC卡脚本处理通知
    # 以下是管理类
    defines.QF_BUSICD_SECRET: QF_SECRET,  # 钱方到汇宜的密钥更新请求
    defines.QF_BUSICD_MANAGE: HY_SECRET,  # 汇宜到钱方的密钥更新
}

# 钱方的busicd转交易处理码(第3域)
qfpay_busicd2huiyi_busicd = {
    defines.QF_BUSICD_BALANCE: '300000',
    defines.QF_BUSICD_PAYMENT: '000000',
    defines.QF_BUSICD_CANCEL: '200000',
    defines.QF_BUSICD_REVERSAL: '000000',
    defines.QF_BUSICD_CANCEL_REVERSAL: '200000',
    defines.QF_BUSICD_SECRET: '',  # 密钥更新无交易处理码
}
