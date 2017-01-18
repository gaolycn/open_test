# coding: utf-8
import os, sys

# 正常
QF_OK                               = "0000"
# 系统维护
QF_ERR_MAINTEN                      = "1100"
# 需要主动冲正
QF_ERR_REVERSAL                     = "1101"
# 重复请求
QF_ERR_REPEAT                       = "1102"
# 报文格式错误
QF_ERR_JSON                         = "1103"
# 报文参数错误
QF_ERR_JSON_PARAM                   = "1104"
# 终端未激活
QF_ERR_TERM_NOTACTIVE               = "1105"
# 终端不匹配
QF_ERR_TERM_NOTMATCH                = "1106"
# 终端被封禁
QF_ERR_TERM_DENY                    = "1107"
# MAC校验失败
QF_ERR_MAC                          = "1108"
# 加解密错误
QF_ERR_CRYPT                        = "1109"
# 客户端重置，流水号错
QF_ERR_CLIENT_RESET                 = "1110"
# 外部服务不可用
QF_ERR_SERVICE_OUT                  = "1111"
# 内部服务不可用
QF_ERR_SERVICE_IN                   = "1112"
# 用户不存在
QF_ERR_USER_NOTEXIST                = "1113"
# 用户被封禁
QF_ERR_USER_DENY                    = "1114"
# 用户受限
QF_ERR_USER_LIMIT                   = "1115"
# 用户密码错误
QF_ERR_USER_PASS                    = "1116"
# 用户不在线
QF_ERR_USER_OFFLINE                 = "1117"
# 风控禁止交易
QF_ERR_RISK                         = "1118"
# 交易类型受限
QF_ERR_TRADE_TYPE                   = "1119"
# 交易时间受限
QF_ERR_TRADE_TIME                   = "1120"
# 交易卡类型受限
QF_ERR_TRADE_CARD                   = "1121"
# 交易币种受限
QF_ERR_TRADE_CURRENCY               = "1122"
# 交易额度受限
QF_ERR_TRADE_AMOUNT                 = "1123"
# 无效交易
QF_ERR_TRADE                        = "1124"
# 已退货
QF_ERR_REFUNDED                     = "1125"
# 原交易信息不匹配
QF_ERR_ORIG_TRADE                   = "1126"
# 数据库错误
QF_ERR_DB                           = "1127"
# 文件系统错误
QF_ERR_FS                           = "1128"
# 已上传凭证
QF_ERR_UPLOADED                     = "1129"
# 交易不在允许日期
QF_ERR_OUT_OF_DATE                  = "1130"
# 渠道错误
QF_ERR_CHANNEL_TIMEOUT              = "1131"
# 客户端版本信息错误
QF_ERR_CLIENT_VERSION               = "1132"
# 用户渠道信息错误
QF_ERR_CHANNEL_INFO                 = "1133"
# 撤销交易刷卡与消费时不是同一张卡
QF_ERR_DIFF_CARD                    = "1134"
# 用户配置错误
QF_ERR_USER_SETTING                 = "1135"
# 交易不存在
QF_ERR_TRADE_NOT_EXIST              = "1136"
# 联系方式不存在
QF_ERR_TRADE_NO                     = "1137"
# 用户更新密钥错
QF_ERR_UPDATE_KEYS                  = "1138"
# 卡号或者卡磁错误
QF_ERR_CARD                         = "1139"
# 账户未审核通过
QF_ERR_USER_NOT_VARIFIED            = "1140"
# 计算通道MAC错误
QF_ERR_CHANNEL_MAC                  = "1141"

# 订单已关闭
QF_ERR_ORDER_CLOSE                  = "1142"
# 交易不存在
QF_ERR_ORDER_NOT_EXIST              = "1143"
# 请求处理失败(协议)
QF_ERR_ORDER_FAIL                   = "1144"
# 订单状态等待支付
QF_ERR_ORDER_WAIT_PAY               = "1145"
## 订单业务处理结果未知
#QF_ERR_ORDER_UNKOWN                 = "1146"
# 订单处理业务错误
QF_ERR_ORDER_TRADE_FAIL             = "1146"
# 通道加密磁道错误
QF_ERR_CHANNEL_TRACK                = "1141"
# 微信刷卡失败
QF_ERR_WEIXIN_PAY_ERROR             = "1147"

# 钱方账户系统错误
QF_ERR_QFACCOUNT                    = "1148"

#机构不存在
QF_ERR_ORG_NOTEXIST                 = "2001"
#商户绑定失败
QF_ERR_ORG_MCHNT_BIND_ERROR         = "2002"
#签到失败
QF_ERR_ORG_SIGNIN_ERROR             = "2003"

### 海外版支付系统增加 ####
# 消费者余额不足
QF_ERR_CUSTOMER_NOT_ENOUGH          = "2004"
# 消费者二维码过期
QF_ERR_CUSTOMER_QR_EXPIRE           = "2005"
# 消费者二维码非法
QF_ERR_CUSTOMER_QR_INVALID          = "2006"
# 消费者关闭了这次交易
QF_ERR_CUSTOMER_CANCEL              = "2007"
# 传递给通道的参数错误
QF_ERR_TO_CHNL_PARAM                = "2008"
# 连接通道失败
QF_ERR_TO_CHNL_CONNECT              = "2009"
# 和通道交互的未知错误
QF_ERR_TO_CHNL_UNKOWN               = "2010"
# 交易流水号重复
QF_ERR_SYSSN_USED                   = "2011"
# 用户的通道证书配置错误
QF_ERR_USER_CERT                    = "2012"

# 原预授权信息不匹配
QF_ERR_ORIG_PAUTH                   = "1151"
# 预授权完成不在允许日期
QF_ERR_PAUTHCP_OUT_OF_DATE          = "1152"
# 预授权完成金额错误
QF_ERR_PAUTHCP_AMOUNT               = "1153"
# 内部错误
QF_ERR_INTERNAL                     = "1154"
# 不允许撤销的交易
QF_ERR_REFUND_DENY                  = "1155"
# 交易结果未知，须查询
QF_ERR_CHANNEL_QUERY                = "1161"
# channeld不能提供服务
QF_ERR_CHANNELD_SHUTDOWN            = "1170"
# 路由重置，需重新路由
QF_ERR_ROUTE_AGAIN                  = "1180"

# 订单过期
QF_ERR_ORDER_EXPIRED                = "1181"


#####  无卡部分错误码
# 余额不足
QF_ERR_NOT_ENOUGH                   = "1201"
# 付款码错误
QF_ERR_AUTH_CODE                    = "1202"
# 账户错误
QF_ERR_ACCOUNT                      = "1203"
# 银行错误
QF_ERR_BANK                         = "1204"

err_state = {
    QF_OK                      : u'正常',
    QF_ERR_MAINTEN             : u'系统维护',
    QF_ERR_REVERSAL            : u'需要主动冲正',
    QF_ERR_REPEAT              : u'重复请求',
    QF_ERR_JSON                : u'报文格式错误',
    QF_ERR_JSON_PARAM          : u'报文参数错误',
    QF_ERR_TERM_NOTACTIVE      : u'终端未激活',
    QF_ERR_TERM_NOTMATCH       : u'终端不匹配',
    QF_ERR_TERM_DENY           : u'终端被封禁',
    QF_ERR_MAC                 : u'MAC校验失败',
    QF_ERR_CRYPT               : u'加解密错误',
    QF_ERR_CLIENT_RESET        : u'客户端重置，流水号错',
    QF_ERR_SERVICE_OUT         : u'外部服务不可用',
    QF_ERR_SERVICE_IN          : u'内部服务不可用',
    QF_ERR_USER_NOTEXIST       : u'用户不存在',
    QF_ERR_USER_DENY           : u'用户被封禁',
    QF_ERR_USER_LIMIT          : u'用户受限',
    QF_ERR_USER_PASS           : u'用户密码错误',
    QF_ERR_USER_OFFLINE        : u'用户不在线',
    QF_ERR_RISK                : u'风控禁止交易',
    QF_ERR_TRADE_TYPE          : u'交易类型受限',
    QF_ERR_TRADE_TIME          : u'交易时间受限',
    QF_ERR_TRADE_CARD          : u'交易卡类型受限',
    QF_ERR_TRADE_CURRENCY      : u'交易币种受限',
    QF_ERR_TRADE_AMOUNT        : u'交易额度受限',
    QF_ERR_TRADE               : u'无效交易',
    QF_ERR_REFUNDED            : u'已退货',
    QF_ERR_ORIG_TRADE          : u'原交易信息不匹配',
    QF_ERR_DB                  : u'数据库错误',
    QF_ERR_FS                  : u'文件系统错误',
    QF_ERR_UPLOADED            : u'已上传凭证',
    QF_ERR_OUT_OF_DATE         : u'交易不在允许日期',
    QF_ERR_CHANNEL_TIMEOUT     : u'渠道错误',
    QF_ERR_CLIENT_VERSION      : u'客户端版本信息错误',
    QF_ERR_CHANNEL_INFO        : u'用户渠道信息错误',
    QF_ERR_DIFF_CARD           : u'撤销交易刷卡与消费时不是同一张卡',
    QF_ERR_USER_SETTING        : u'用户配置错误',
    QF_ERR_TRADE_NOT_EXIST     : u'交易不存在',
    QF_ERR_TRADE_NO            : u'联系方式不存在',
    QF_ERR_UPDATE_KEYS         : u'用户更新密钥错',
    QF_ERR_CARD                : u'卡号或者卡磁错误',
    QF_ERR_USER_NOT_VARIFIED   : u'账户未审核通过',
    QF_ERR_CHANNEL_MAC         : u'计算通道MAC错误'  ,
    QF_ERR_ORDER_CLOSE         : u'订单已关闭',
    QF_ERR_ORDER_NOT_EXIST     : u'订单不存在',
    QF_ERR_ORDER_FAIL          : u'协议处理失败',
    QF_ERR_ORDER_WAIT_PAY      : u'订单已创建等待支付完成',
    QF_ERR_ORDER_TRADE_FAIL    : u'订单业务处理失败',
    QF_ERR_ORIG_PAUTH          : u'原预授权信息不匹配',
    QF_ERR_PAUTHCP_OUT_OF_DATE : u'预授权完成不在允许日期',
    QF_ERR_PAUTHCP_AMOUNT      : u'预授权完成金额错误',
    QF_ERR_INTERNAL            : u'内部错误',
    QF_ERR_REFUND_DENY         : u'交易不能撤销',
    QF_ERR_CHANNEL_QUERY       : u'交易结果未知，须查询',
    QF_ERR_CHANNELD_SHUTDOWN   : u'channeld不能提供服务',
    QF_ERR_ROUTE_AGAIN         : u'路由重置，需重新路由',
    QF_ERR_ORDER_EXPIRED       : u'订单过期',
    QF_ERR_WEIXIN_PAY_ERROR    : u"微信刷卡失败，需要重新刷卡",
    QF_ERR_ORG_NOTEXIST        : u"机构不存在",
    QF_ERR_ORG_MCHNT_BIND_ERROR: u"商户绑定失败",
    QF_ERR_ORG_SIGNIN_ERROR    : u"签到失败",
    QF_ERR_NOT_ENOUGH          : u'余额不足',
    QF_ERR_AUTH_CODE           : u'付款码错误',
    QF_ERR_ACCOUNT             : u'账户错误',
    QF_ERR_BANK                : u'银行错误',
}

# ---- 内部错误代码 ----
QF_PAY_OK                           = 0
QF_PAY_ERR                          = -1
QF_PAY_ERR_JSON                     = -2
QF_PAY_ERR_CONNECT                  = -11
QF_PAY_ERR_READ                     = -12
QF_PAY_ERR_WRITE                    = -13
QF_PAY_ERR_TIMEOUT                  = -14
QF_PAY_ERR_NETWORK                  = -15
QF_PAY_ERR_RISK                     = -16
QF_PAY_ERR_THRIFT                   = -17
QF_PAY_ERR_NOSERVER                 = -18
QF_PAY_ERR_TRADENOOUT               = -19
QF_PAY_ERR_PARA                     = -20
QF_PAY_ERR_MEMORY                   = -21


# ----  用户状态 ----
# 新建
QF_USTATE_NEW                       = 1
# 通过审核, 未设备激活
QF_USTATE_VARIFIED                  = 2
# 已设备激活，未业务激活
QF_USTATE_ACTIVE                    = 3
# 已业务激活，正常
QF_USTATE_OK                        = 4
# 呆户
QF_USTATE_DULL                      = 5
# 禁止
QF_USTATE_FORBID                    = 6
# 销户
QF_USTATE_DESTROY                   = 7

# ---- 订单状态 ----
# 订单创建
QF_ORDER_CREATED                    = 1
# 订单支付中
QF_ORDER_PAYING                     = 2
# 订单支付成功
QF_ORDER_PAY_SUCCESS                = 3
# 订单支付失败
QF_ORDER_PAY_FAIL                   = 4
# 订单关闭
QF_ORDER_CLOSE                      = 5
# 订单过期
QF_ORDER_EXPIRED                    = 6
# 定单撤销
QF_ORDER_CANCEL                     = 7

order_state = {
    QF_ORDER_CREATED: u'订单创建',
    QF_ORDER_PAYING: u'支付中',
    QF_ORDER_PAY_SUCCESS: u'支付成功',
    QF_ORDER_PAY_FAIL: u'支付失败',
    QF_ORDER_CLOSE: u'订单关闭',
    QF_ORDER_EXPIRED: u'订单过期',
}

# ------订单支付方式----
#刷卡支付
QF_ORDER_PAY_METHOD_CARD            = 1
#支付宝
QF_ORDER_PAY_METHOD_ALIPAY          = 2
#微信
QF_ORDER_PAY_METHOD_WEIXIN          = 3
#百付宝
QF_ORDER_PAY_METHOD_BAIFUBAO        = 4

# ---- 设备绑定状态 ----
# 未激活
QF_DSTATE_NOACTIVE                  = 1
# 正常
QF_DSTATE_OK                        = 2
# 激活失败
QF_DSTATE_ACT_ERR                   = 3
# 失效
QF_DSTATE_NOTVALID                  = 4

term_state = {
    QF_DSTATE_NOACTIVE: u'未激活',
    QF_DSTATE_OK: u'已激活',
    QF_DSTATE_ACT_ERR: u'激活失败',
    QF_DSTATE_NOTVALID: u'已失效',
}

# ---- 交易类型 ----
# POSP消费收款(消费，撤销，退货，余额查询)
QF_TRADE_TYPE_POSP                  = 0x01
# 支付宝
QF_TRADE_TYPE_ALIPAY                = 0x02
# 支付宝(海外 需要钱方转汇率)
QF_TRADE_TYPE_ALIPAY_OVERSEAS       = 0x03
# 支付宝(海外 通道支持使用外币交易)
QF_TRADE_TYPE_ALIPAY_OVERSEAS_ATUO_EXCHANGE     = 0x05
# 便民(转帐, 还款，缴费，充值)
QF_TRADE_TYPE_TRANSFER              = 0x04
# 微信
QF_TRADE_TYPE_WEIXIN                = 0x08
# 微信(海外 需要钱方转汇率)
QF_TRADE_TYPE_WEIXIN_OVERSEAS       = 0x09
# 微信(海外 通道支持使用外币交易)
QF_TRADE_TYPE_WEIXIN_OVERSEAS_ATUO_EXCHANGE     = 0x0A
# 百付宝
QF_TRADE_TYPE_BAIFUBAO              = 0x10
# 百付宝(海外 需要钱方转汇率)
QF_TRADE_TYPE_BAIFUBAO_OVERSEAS     = 0x11
# 百付宝(海外 通道支持使用外币交易)
QF_TRADE_TYPE_BAIFUBAO_OVERSEAS_ATUO_EXCHANGE   = 0x12
# 京东钱包 只能硬着头皮塞了
QF_TRADE_TYPE_JDPAY                 = 0x0B
# 微信APP
QF_TRADE_TYPE_WEIXIN_APP            = 0x0C
# QQ钱包
QF_TRADE_TYPE_QQPAY                 = 0x0D
# 会员储值
QF_TRADE_TYPE_PREPAID               = 0x1F
# 预授权
QF_TRADE_TYPE_PAUTH                 = 0x20
# 现金
QF_TRADE_TYPE_CASH                  = 0x40
# 管理
QF_TRADE_TYPE_MANAGE                = 0x80

trade_type = {
    QF_TRADE_TYPE_POSP: u'POSP消费',
    QF_TRADE_TYPE_ALIPAY: u'支付宝',
    QF_TRADE_TYPE_TRANSFER: u'便民',
    QF_TRADE_TYPE_WEIXIN: u'微信',
    QF_TRADE_TYPE_WEIXIN_APP: u'微信APP',
    QF_TRADE_TYPE_JDPAY: u'京东钱包',
    QF_TRADE_TYPE_QQPAY: u'QQ钱包',
    QF_TRADE_TYPE_PAUTH: u'预授权',
    QF_TRADE_TYPE_CASH: u'现金',
    QF_TRADE_TYPE_MANAGE: u'管理',
    QF_TRADE_TYPE_BAIFUBAO: u'百付宝',
    QF_TRADE_TYPE_WEIXIN_OVERSEAS: u'微信海外支付c方案',
    QF_TRADE_TYPE_WEIXIN_OVERSEAS_ATUO_EXCHANGE: u'微信海外支付ab方案',
    QF_TRADE_TYPE_PREPAID: '会员储值',
}

# ---- 交易分类 ----
# 交易类
QF_TRADE_CLASS_PAYMENT              = 0x01
# 冲正类
QF_TRADE_CLASS_REVERSAL             = 0x02
# 撤销类
QF_TRADE_CLASS_CANCEL               = 0x04
# 查询类
QF_TRADE_CLASS_BALANCE              = 0x08
# 其他
QF_TRADE_CLASS_OTHER                = 0x10

# ---- 交易时间 ----
# 8 - 20点
QF_TRADE_TIME_8TO20                 = 0x01
# 20 - 0点
QF_TRADE_TIME_20TO0                 = 0x02
# 0 - 8点
QF_TRADE_TIME_0TO80                 = 0x04

# ---- 业务代码 ----
# 转账
QF_BUSICD_TOCARD                        =   "420000"
# 还款
QF_BUSICD_TOCREDIT                      =   "401000"
# 充值
QF_BUSICD_RECHARGE                      =   "500000"
# 消费
QF_BUSICD_PAYMENT                       =   "000000"
# 消费冲正
QF_BUSICD_REVERSAL                      =   "040000"
# 退货
QF_BUSICD_REFUND                        =   "200000"
# 余额查询
QF_BUSICD_BALANCE                       =   "300000"
# 上传凭证
QF_BUSICD_UPLOAD                        =   "180100"
# 交易列表
QF_BUSICD_TRADELIST                     =   "180200"
# 交易详情
QF_BUSICD_TRADEINFO                     =   "180300"
# 发送收据
QF_BUSICD_RECEIPT                       =   "180400"
# 交易查询
QF_BUSICD_TRADEQUERY                    =   "180600"
# 初始化
QF_BUSICD_INIT                          =   "170100"
# 激活
QF_BUSICD_ACTIVE                        =   "170200"
# 登录
QF_BUSICD_LOGIN                         =   "170300"
# 统计
QF_BUSICD_STAT                          =   "170500"
# 反馈
QF_BUSICD_FEED                          =   "170600"
# 修改密码
QF_BUICD_CHPASS                         =   "170700"
# 更新密钥
QF_BUICD_UPDATEKEYS                     =   "170800"
# 消费撤销
QF_BUSICD_CANCEL                        =   "201000"
# 消费撤销冲正
QF_BUSICD_CANCEL_REVERSAL               =   "041000"
# 现金记账
QF_BUSICD_CASH                          =   "180500"
# 订单支付
QF_BUSICD_ORDER_PAY                     =   "181000"
QF_BUSICD_ORDER_CREATE                  =   "181001"
QF_BUSICD_ORDER_QUERY                   =   "181002"
QF_BUSICD_ORDER_CLOSE                   =   "181003"
QF_BUSICD_ORDER_CANCEL                  =   "181004"
# IC卡脚本通知
QF_BUSICD_ICNOTICE                      =   "210000"
# 预授权
QF_BUSICD_PAUTH                         =   "032000"
# 预授权冲正
QF_BUSICD_PAUTH_REVERSAL                =   "042000"
# 预授权撤销
QF_BUSICD_PAUTH_CANCEL                  =   "202000"
# 预授权撤销冲正
QF_BUSICD_PAUTH_CANCEL_REVERSAL         =   "044000"
# 预授权完成
QF_BUSICD_PAUTHCP                       =   "033000"
# 预授权完成冲正
QF_BUSICD_PAUTHCP_REVERSAL              =   "043000"
# 预授权完成撤销
QF_BUSICD_PAUTHCP_CANCEL                =   "203000"
# 预授权完成撤销冲正
QF_BUSICD_PAUTHCP_CANCEL_REVERSAL       =   "045000"
# 管理类报文
QF_BUSICD_MANAGE                        =   "800000"
# 密码更新报文
QF_BUSICD_SECRET                        =   "820000"
# 烟草订购
QF_BUSICD_BACOO_ORDER                   =   "182000"
# 烟草消费
#QF_BUSICD_BACCO_PAYMENT                 =   "000000"

# 7开头内部系统业务
# 储值消费
QF_BUSICD_PREPAID_CONSUME               = "700000"
# 储值查询
QF_BUSICD_PREPAID_QUERY                 = "700001"
# 储值退款
QF_BUSICD_PREPAID_REFUND                = "700002"

# 支付宝预下单
QF_BUSICD_ALIPAY_PRECREATE              =   "800101"
# 支付宝下单并支付
QF_BUSICD_ALIPAY_CREATEANDPAY           =   "800102"
# 支付宝退款
QF_BUSICD_ALIPAY_REFUND                 =   "800103"
# 支付宝查询
QF_BUSICD_ALIPAY_QUERY                  =   "800104"
# 支付宝撤销
QF_BUSICD_ALIPAY_CANCEL                 =   "800105"
# 支付宝H5
QF_BUSICD_ALIPAY_H5                     =   "800107"
# 支付宝刷卡
QF_BUSICD_ALIPAY_SWIPE                  =   "800108"
# 支付宝冲正 @ATTENTION 目前只有海外版使用
QF_BUSICD_ALIPAY_REVERSE                =   "800109"

# 微信统一预下单
QF_BUSICD_WEIXIN_PRECREATE              =   "800201"
# 微信退款查询
QF_BUSICD_WEIXIN_REFUND_QUERY           =   "800202"
# 微信退货
QF_BUSICD_WEIXIN_REFUND                 =   "800203"
# 微信订单查询
QF_BUSICD_WEIXIN_QUERY                  =   "800204"
# 微信关闭订单
QF_BUSICD_WEIXIN_CLOSE_ORDER            =   "800205"
# 微信账单查询
QF_BUSICD_WEIXIN_DOWNLOADBILL           =   "800206"
# 微信H5统一预下单
QF_BUSICD_WEIXIN_PRECREATE_H5           =   "800207"
# 微信小额支付
QF_BUSICD_WEIXIN_SWIPE                  =   "800208"
# 微信小额支付冲正
QF_BUSICD_WEIXIN_REVERSAL               =   "800209"
# 微信APP
QF_BUSICD_WEIXIN_APP                    =   "800210"

#银联代收交易
QF_BUSICD_UNIONPAY_WITHHOLDING_TRADE    =   "800301"
QF_BUSICD_UNIONPAY_WITHHOLDING_VERIFY   =   "800302"
QF_BUSICD_UNIONPAY_WITHHOLDING_QUERY    =   "800303"
QF_BUSICD_UNIONPAY_WITHHOLDING_REFUND   =   "800304"
QF_BUSICD_UNIONPAY_WITHHOLDING_BIND     =   "800305"
QF_BUSICD_UNIONPAY_WITHHOLDING_UNBIND   =   "800306"

# 百度的百付宝预下单
QF_BUSICD_BAIFUBAO_PRECREATE            =   "800401"
# 百度的百付宝退款查询
QF_BUSICD_BAIFUBAO_REFUND_QUERY         =   "800402"
# 百度的百付宝退货
QF_BUSICD_BAIFUBAO_REFUND               =   "800403"
# 百度的百付宝订单查询
QF_BUSICD_BAIFUBAO_QUERY                =   "800404"
# 百度的百付宝关闭订单
QF_BUSICD_BAIFUBAO_CLOSE_ORDER          =   "800405"
# 百度的百付宝条码支付
QF_BUSICD_BAIFUBAO_PAY                  =   "800408"
# 百度的百付宝支付冲正
QF_BUSICD_BAIFUBAO_REVERSAL             =   "800409"

# 京东钱包扫码下单
QF_BUSICD_JDPAY_PRECREATE               =   "800501"
# 京东钱包退款
QF_BUSICD_JDPAY_REFUND                  =   "800503"
# 京东钱包查询
QF_BUSICD_JDPAY_QUERY                   =   "800504"
# 京东钱包预下单
QF_BUSICD_JDPAY_H5                      =   "800507"
# 京东钱包付款码
QF_BUSICD_JDPAY_SWIPE                   =   "800508"

# QQ钱包扫码下单
QF_BUSICD_QQPAY_QRCODE                  =   "800601"
# QQ钱包退款
QF_BUSICD_QQPAY_REFUND                  =   "800603"
# QQ钱包查询
QF_BUSICD_QQPAY_QUERY                   =   "800604"
# QQ钱包H5预下单
QF_BUSICD_QQPAY_H5                      =   "800607"
# QQ钱包付款码
QF_BUSICD_QQPAY_SWIPE                   =   "800608"

#机构签到 buscid
QF_BUSICD_ORG_SIGNIN                    =   "600001"
#机构绑定商户 buscid
QF_BUSICD_ORG_MCHNT_BIND                =   "600002"

busicd = {
    QF_BUSICD_TOCARD: u'转账',
    QF_BUSICD_TOCREDIT: u'还款',
    QF_BUSICD_RECHARGE: u'充值',
    QF_BUSICD_PAYMENT: u'刷卡消费',
    QF_BUSICD_REVERSAL: u'消费冲正',
    QF_BUSICD_REFUND: u'退货',
    QF_BUSICD_BALANCE: u'余额查询',
    QF_BUSICD_UPLOAD: u'上传凭证',
    QF_BUSICD_TRADEQUERY:u'交易查询',
    QF_BUSICD_TRADELIST: u'交易查询',
    QF_BUSICD_TRADEINFO: u'交易详情',
    QF_BUSICD_RECEIPT: u'发送收据',
    QF_BUSICD_INIT: u'初始化',
    QF_BUSICD_ACTIVE: u'激活',
    QF_BUSICD_LOGIN: u'登录',
    QF_BUSICD_STAT: u'统计',
    QF_BUSICD_FEED: u'反馈',
    QF_BUICD_CHPASS: u'修改密码',
    QF_BUICD_UPDATEKEYS: u'更新秘钥',
    QF_BUSICD_CANCEL: u'消费撤销',
    QF_BUSICD_CANCEL_REVERSAL: u'消费撤销冲正',
    QF_BUSICD_CASH: u'现金记账',
    QF_BUSICD_ORDER_PAY: u'订单支付',
    QF_BUSICD_ORDER_CREATE: u'创建订单',
    QF_BUSICD_ORDER_QUERY: u'订单查询',
    QF_BUSICD_ORDER_CANCEL: u'定单撤销',
    QF_BUSICD_ICNOTICE: u'脚本通知',
    QF_BUSICD_PAUTH: u'预授权',
    QF_BUSICD_PAUTH_REVERSAL: u'预授权冲正',
    QF_BUSICD_PAUTH_CANCEL: u'预授权撤销',
    QF_BUSICD_PAUTH_CANCEL_REVERSAL: u'预授权撤销冲正',
    QF_BUSICD_PAUTHCP: u'预授权完成',
    QF_BUSICD_PAUTHCP_REVERSAL: u'预授权完成冲正',
    QF_BUSICD_PAUTHCP_CANCEL: u'预授权完成撤销',
    QF_BUSICD_PAUTHCP_CANCEL_REVERSAL: u'预授权完成撤销冲正',
    QF_BUSICD_MANAGE: u'管理报文',
    QF_BUSICD_SECRET: u'秘钥更新',
    QF_BUSICD_BACOO_ORDER: u'烟草订购',
    #QF_BUSICD_BACCO_PAYMENT: u'烟草消费',
    QF_BUSICD_ALIPAY_PRECREATE: u'支付宝扫码',
    QF_BUSICD_ALIPAY_CREATEANDPAY: u'支付宝下单并支付',
    QF_BUSICD_ALIPAY_REFUND: u'支付宝退款',
    QF_BUSICD_ALIPAY_QUERY: u'支付宝查询',
    QF_BUSICD_ALIPAY_CANCEL: u'支付宝撤销(冲正)',
    QF_BUSICD_ALIPAY_H5: u'支付宝H5',
    QF_BUSICD_WEIXIN_PRECREATE: u'微信扫码',
    QF_BUSICD_WEIXIN_PRECREATE_H5: u'微信H5',
    QF_BUSICD_WEIXIN_QUERY: u'微信订单查询',
    QF_BUSICD_WEIXIN_CLOSE_ORDER: u'微信关闭订单',
    QF_BUSICD_WEIXIN_REFUND: u'微信退款',
    QF_BUSICD_WEIXIN_SWIPE: u'微信刷卡支付',
    QF_BUSICD_WEIXIN_APP: u'微信APP',
    QF_BUSICD_ALIPAY_SWIPE: u'支付宝刷卡',
    QF_BUSICD_WEIXIN_REVERSAL:u"微信刷卡撤销(冲正)",
    QF_BUSICD_BAIFUBAO_PRECREATE: u'百度的百付宝预下单',
    QF_BUSICD_BAIFUBAO_REFUND_QUERY: u'百度的百付宝退款查询',
    QF_BUSICD_BAIFUBAO_REFUND: u'百度的百付宝退货',
    QF_BUSICD_BAIFUBAO_QUERY: u'百度的百付宝订单查询',
    QF_BUSICD_BAIFUBAO_CLOSE_ORDER: u'百度的百付宝关闭订单',
    QF_BUSICD_BAIFUBAO_PAY: u'百度的百付宝条码支付',
    QF_BUSICD_BAIFUBAO_REVERSAL: u'百度的百付宝支付冲正',
    QF_BUSICD_JDPAY_PRECREATE: u'京东扫码',
    QF_BUSICD_JDPAY_REFUND: u'京东退款',
    QF_BUSICD_JDPAY_QUERY: u'京东查询',
    QF_BUSICD_JDPAY_H5: u'京东H5',
    QF_BUSICD_JDPAY_SWIPE: u'京东付款码',
    QF_BUSICD_QQPAY_QRCODE:u'QQ钱包扫码',
    QF_BUSICD_QQPAY_REFUND:u'QQ钱包退款',
    QF_BUSICD_QQPAY_QUERY:u'QQ钱包查询',
    QF_BUSICD_QQPAY_H5:u'QQ钱包H5',
    QF_BUSICD_QQPAY_SWIPE:u'QQ钱包退款',
    QF_BUSICD_PREPAID_CONSUME: u'储值消费',
    QF_BUSICD_PREPAID_QUERY: u'储值查询',
    QF_BUSICD_PREPAID_REFUND: u'储值退款',
}


# 交易动作
QF_ACTION_QUERY                         = 1
QF_ACTION_REVERSAL                      = 2

# ---- 交易状态 ----
# 交易中
QF_TRADE_NOW                        = 0
# 交易成功
QF_TRADE_SUCC                       = 1
# 交易失败
QF_TRADE_FAILED                     = 2
# 交易超时
QF_TRADE_TIMEOUT                    = 3

trade_state = {
    QF_TRADE_NOW: u'交易中',
    QF_TRADE_SUCC: u'交易成功',
    QF_TRADE_FAILED: u'交易失败',
    QF_TRADE_TIMEOUT: u'交易超时',
}

QF_TRADE_NOW_STR                    = "0"
QF_TRADE_SUCC_STR                   = "1"
QF_TRADE_FAILED_STR                 = "2"
QF_TRADE_TIMEOUT_STR                = "3"

# ---- 取消状态 ----
QF_CANCEL_NO                        = 0
# 已冲正
QF_CANCEL_REVERSAL                  = 1
# 已撤销
QF_CANCEL_CANCELED                  = 2
# 已退货
QF_CANCEL_REFUND                    = 3
# 已完成预授权
QF_CANCEL_PAUTHCP                   = 4

cancel_state = {
    QF_CANCEL_NO: u'无',
    QF_CANCEL_REVERSAL: u'已冲正',
    QF_CANCEL_CANCELED: u'已撤销',
    QF_CANCEL_REFUND: u'已退货',
    QF_CANCEL_PAUTHCP: u'已预授权完成',
}

# ---- 卡类型 ----
# 未识别卡
QF_CARD_UNKNOWN                     = 0
# 借记卡
QF_CARD_DEBIT                       = 1
# 信用卡(贷记卡)
QF_CARD_CREDIT                      = 2
# 准贷记卡
QF_CARD_SEMICREDIT                  = 3
# 储值卡
QF_CARD_VALUE                       = 4
# zhanghao
QF_CARD_ACCOUNT                     = 5

# ---- 卡种 ----
# 磁条卡
QF_CARD_CLASS_MAGNETIC              = 1
# IC卡
QF_CARD_CLASS_IC                    = 2
# 无卡交易
QF_CARD_CLASS_NOCARD                = 3
# 复合卡
QF_CARD_CLASS_IC_MAGNETIC           = 4

card_type = {
    QF_CARD_UNKNOWN: u'未识别卡',
    QF_CARD_DEBIT: u'借记卡',
    QF_CARD_CREDIT: u'信用卡',
    QF_CARD_SEMICREDIT: u'准贷记卡',
    QF_CARD_VALUE: u'储值卡',
    QF_CARD_ACCOUNT: u'第三方账号',
}


# ---- 卡类型限制 ----
# 国内借记卡
QF_CARDALLOW_DEBIT_CN               = 1
# 国外借记卡
QF_CARDALLOW_DEBIT_FOREIGN          = 2
# 国内信用卡
QF_CARDALLOW_CREDIT_CN              = 4
# 国外信用卡
QF_CARDALLOW_CREDIT_FOREIGN         = 8

# ---- 渠道接入模式 ----
# 我们的渠道路由方(讯联)
QF_CHNLMODE_CHNL                    = 0
# 终端接入
QF_CHNLMODE_TERM                    = 1
# 机构接入
QF_CHNLMODE_ORG                     = 2

# 已上传凭证
QF_SIGN_NO                          = 0
# 未上传凭证
QF_SIGN_OK                          = 1

# --- 撤销控制查询类型 ---
# userid
QF_SETTLE_CONFIG_TYPE_USERID        = 0
# groupid
QF_SETTLE_CONFIG_TYPE_GROUPID       = 1
# 通道商户号
QF_SETTLE_CONFIG_TYPE_CHNLUSERID    = 2
