namespace py qf_account

// 发生错误时的返回码及其对应的描述信息
exception ServerError
{
    1: string code, // 返回码
    2: string msg,  // 描述信息
}

// 响应结果
// 请求时以list方式请求，则响应时
struct Response
{
    1: i64    id,       // id
    2: string biz_sn,   // 操作的流水号
    3: string code,     // 返回码
    4: string msg,      // 描述信息
}


// 分页查询时，应的分页信息
struct PageReq
{
}

// 分页查询时，响应的分页信息
struct PageResp
{
}

// 帐户信息
struct Account
{
    1: i64    id,           // 帐户id
    2: i64    userid,       // 商户id
    3: i64    biz_id,       // 业务类型
    4: i64    amt,          // 帐户中的金额
    5: string txcurrcd,     // 金额的币种
    6: i64    acct_type_id, // 帐户的类型
}

// 查询用户帐户
// userid与userids  biz_id与biz_ids  acct_type_id与acct_types
// 这三组每组只能存在一个，建议使用批量的，单个的只是为了兼容
// 如果每组都存在，则优先使用单个
struct AccountQueryArgs
{
    1:  i64    userid,              // 以商户id为条件查询
    2:  i64    biz_id,              // 以业务类型为条件查询
    3:  i64    amt,                 // 以帐户金额为条件查询, 帐户金额大于amt的
    4:  i32    pos   = 0,           // 查询的起始位置
    5:  i32    count = 20,          // 查询的个数
    6:  string txcurrcd = '',       // 查询的币种, 为空，则不限制币种
    7:  i64    acct_type_id,        // 查询的帐户类型, 主要是现金帐户，分为现金实名与现金帐户
    8:  list<i64> userids    = [],  // 以商户id为条件查询(批量
    9:  list<i64> biz_ids    = [],  // 以业务类型为条件查询(批量)
    10: list<i64> acct_types = [],  // 查询的帐户类型, 主要是现金帐户，分为现金实名与现金帐户(批量)
}

// 查询商户帐户记录流水
// 暂时只支持一次查询一天
struct AccountRecordArgs
{
    1:  i64    userid,       // 以商户id为条件查询
    2:  i64    biz_id,       // 以业务id为条件查询
    3:  string title,        // 以描述为条件查询
    4:  i32    start_time,   // 查询交易的起始时间，如果为空，则为昨天的00:00:00
    5:  i32    end_time,     // 查询交易的结束时间，如果为空，则为昨天的23:59:59
    6:  i32    pos   = 0,    // 查询的起始位置
    7:  i32    count = 20,   // 查询的个数
    8:  string chnl_code,    // 查询的通道id
    9:  string biz_sn,       // 查询的交易流水号
    10: i64    acct_id,      // 以帐户类型为条件查询
}

// 查询商户帐户记录流水结果
struct AccountRecord
{
    1:  i64    id,          // 帐户记录id
    2:  i64    userid,      // 以商户id为条件查询
    3:  i64    acct_id,     // 以帐户类型为条件查询
    4:  i64    biz_id,      // 业务id
    5:  string title,       // 以描述为条件查询
    6:  string detail,      // 帐户操作详情
    7:  string biz_sn,      // 交易流水号
    8:  i64    amt,         // 交易的金额，以分为单位
    9:  i32    fee,         // 手续费
    10: double fee_ratio,   // 本次交易的费率
    11: i32    max_fee,     // 费率封顶
    12: i32    sysdtm,      // 交易时间
    13: i64    chnl_id,     // 交易通道id
}

// 帐户统计
struct AccountStat
{
    1: i64    userid,       // 商户id
    2: i64    total_amt,    // 商户的总余额
    3: i64    withdraw_amt, // 商户的可提现余额
    4: string txcurrcd,     // 币种
}

// 交易信息
struct Trade
{
    1:  required i64    userid,             // 交易的商户id
    2:  required i64    amt,                // 交易的金额，以分为单位
    3:  required string txcurrcd = '156',   // 交易的币种
                                            // 如果商户的帐户不存在，则以此币种创建帐户
                                            // 如果商户的帐户存在，则需要验证此币种
                                            // 它必传的原因是: 如果币种为人民币但交易时使用美元，那就悲剧了
                                            // 但帐户类型不支持按币种来创建(以后有需要再说)，所以这里需要验证
    4:  required string biz_sn,             // 交易流水号
    5:  required i32    sysdtm,             // 交易时间
    6:  optional i64    biz_id,             // 交易的业务类型
    7:  optional string trade_type,         // 交易类型 交易时根据交易类型与卡类型计算手续费, 
                                            //          100.银行卡 110.汇宜T+0(settletn只能为0) 
                                            //          200.微信刷卡 201.微信扫码 202.微信H5 203. 微信app 
                                            //          300.支付宝反扫  301.支付宝扫码 302.支付宝H5 303.支付宝app 
                                            //          400.银联支付 500.代清算
    8:  optional i16    card_type,          // 卡类型   1.借记卡 2.信用卡 3.准贷记卡 4.储值卡 5.无卡
    9:  optional i16    settletn,           // 清算类型, 默认为t1.  0: t0 1: t1 ...
    10: optional string title,              // 交易的描述
    11: optional string detail,             // 帐户操作详情
    12: optional string orig_biz_sn,        // 原交易的流水号
    13: optional string chnl_code,          // 交易通道码
    14: optional i64    qfpay_acct_id = -1, // 交易时对钱方留存现金帐户的影响
    15: optional i64    acct_type_id  = -1, // 交易时影响那个帐户类型的id, 如果不传，则根据biz_id转
    16: optional i32    fee_amt       = 0,  // 本次交易的手续费，暂时只有提现用的上
}

// 转帐信息
// 两个帐户之间的资金转移
struct Transfer
{
    1:  required i64    amt,                // 转帐的金额，以分为单位
    2:  required string txcurrcd = '156',   // 转帐的币种
                                            // 如果商户的帐户不存在，则以此币种创建帐户
                                            // 如果商户的帐户存在，则需要验证此币种
                                            // 它必传的原因是: 如果币种为人民币但交易时使用美元，那就悲剧了
                                            // 但帐户类型不支持按币种来创建(以后有需要再说)，所以这里需要验证
    3:  required string biz_sn,             // 交易流水号
    4:  required i64    from_userid,        // 转帐的商户id
    5:  optional i64    from_biz_id,        // 转帐的业务id
    6:  optional i64    from_acct_type_id,  // 转帐的帐户类型，如果不存在，则根据业务id转
    7:  optional i64    to_userid,          // 到帐的商户id
    8:  optional i64    to_biz_id,          // 到帐的业务id
    9:  optional i64    to_acct_type_id,    // 到帐的帐户类型，如果不存在，则根据业务id转
    10: optional i32    sysdtm,             // 交易时间
    11: optional string title,              // 结算的描述
    12: optional string detail,             // 帐户操作详情
    13: optional string orig_biz_sn = '',   // 原交易的流水号。目前转帐无撤销操作，不涉及原交易，所以暂时留空，只做为保留
    14: optional i64    qfpay_acct_id = -1, // 交易时对钱方留存现金帐户的影响
    15: optional list<string> biz_sns,      // 结算使用，结算影响到的流水号
}

// 充值信息
// 普通用户充值，则充值到充值帐户, 只能使用userid标识用户
// 钱方现金留存帐户充值，充值到留存帐户
struct Recharge
{
    1:  required string biz_sn,              // 充值的流水号
    2:  required string txcurrcd = '156',    // 交易的币种
                                             // 如果商户的帐户不存在，则以此币种创建帐户
                                             // 如果商户的帐户存在，则需要验证此币种
                                             // 它必传的原因是: 如果币种为人民币但交易时使用美元，那就悲剧了
                                             // 但帐户类型不支持按币种来创建(以后有需要再说)，所以这里需要验证
    3:  required i32    sysdtm,              // 交易时间
    4:  required i64    amt,                 // 充值金额
    5:  optional string title  = '',         // 交易的描述
    6:  optional string detail = '',         // 帐户操作详情
    7:  optional string orig_biz_sn = '',    // 撤销充值时的原充值流水号
    8:  optional i64    acct_id = -1,        // 向钱方留存帐户充值, 帐户id
                                             //        1. 钱方现金帐户     2. 钱方汇宜现金帐户 
                                             //        3. 钱方讯联现金帐户 4. 钱方通联现金帐户
    9:  optional i64    userid = -1,         // 商户id
    10: optional i64    acct_type_id  = -1,  // 交易时影响那个帐户类型的id, 如果不传，则根据biz_id转
}

// 银行卡信息
struct UserCard
{
    1:  i64     id,         // id
    2:  i64     userid,     // 商户id
    3:  string  name,       // 持卡人姓名
    4:  string  cardno,     // 卡号
    5:  i16     card_type,  // 卡类型 1: 借记卡 2: 信用卡
    6:  string  bank_name,  // 银行
    7:  string  bank_brch,  // 支行
    8:  string  bank_area,  // 开户省
    9:  string  bank_city,  // 开户市
    10: string  bank_code,  // 银联标准的联行号
    11: i16     bank_type,  // 银行类型 1: 对私 2: 对公
    12: string  mobile,     // 持卡人手机号
    13: i16     state,      // 状态 1: 未认证 2: 已认证
    14: i16     enable,     // 状态 1: 启用   2: 禁用
    15: i32     ctime,      // 创建时间
    16: i32     uptime,     // 更新时间
    17: string  swift_code, // 国际标准的联行号
    18: string  bank_addr,  // 银行的地址
    19: string  content,    // 备注
}

// 银行卡查询参数
struct CardQueryArgs
{
    1: list<i64> userid,    // 以商户id为查询条件
    2: i16       state,     // 以认证状态为查询条件
    3: i16       enable,    // 以启用状态为查询条件
    4: i32       pos   = 0, // 查询的起始位置
    5: i32       count = 20,// 查询的数量
}

// 银行卡变更记录查询参数
struct CardRecordArgs
{
    1: list<i64> userid,    // 以商户id为查询条件
    2: i32       pos   = 0, // 查询的起始位置
    3: i32       count = 20,// 查询的数量
}

// 费率信息
struct FeeRatio
{
    1:  i64    id,           // id
    2:  i64    userid,       // 商户id
    3:  string trade_type,   // 交易类型
    4:  i32    card_type,    // 卡类型
    5:  i16    settletn,     // 清算方式 0:t0 1:t1 ...
    6:  double ratio,        // 费率
    7:  i32    max_fee,      // 费率封顶
    8:  i16    enable,       // 启用状态 1: 启用 2: 禁用
    9:  i32    ctime,        // 创建时间
    10: i32    uptime,       // 更新时间
    11: i16    is_update = 0,// 费率是否可以修改, 默认是不能修改
}

// 费率查询参数
struct FeeQueryArgs
{
    1: i64    userid,      // 以商户id为条件查询
    2: string trade_type,  // 以交易类型为条件查询
    3: i16    card_type,   // 以卡类型为条件查询
    4: i16    settletn,    // 清算方式 0:t0 1:t1 ...
    5: i16    enable,      // 以启用状态为条件查询
    6: i32    pos   = 0,   // 查询的起始位置
    7: i32    count = 20,  // 查询的数量
}

// 计算手续费
struct CalculateFeeArgs
{
    1: required i64    userid,          // 以商户id为条件查询
    2: required string trade_type,      // 以交易类型为条件查询
    3: required i16    card_type,       // 以卡类型为条件查询
    4: required i16    settletn = 1,    // 清算方式 0:t0 1:t1 ...
    5: required i64    trade_amt,       // 交易金额
}

// 手续费计算结果
struct FeeResp
{
    1: i32    fee,      // 手续费
    2: double ratio,    // 费率
    3: i32    max_fee,  // 费率封顶
}

// 是否可以撤销的返回值
struct IsCancelResp
{
    1: i64 cancel_amt,      // 撤销金额
}


service UserAccount
{
    i16 ping();
    // 用户帐户操作
    // 初始化用户帐户
    i16 account_init(1:i64 userid, 2:string txcurrcd) throws(1:ServerError e);
    // 查询用户帐户
    list<Account> account_query(1:AccountQueryArgs query_args) throws(1:ServerError e);
    // 查询用户帐户的数量, 与account_query一起进行分页查询
    i32 account_count(1:AccountQueryArgs query_args) throws(1:ServerError e);
    // 查询帐户流水
    list<AccountRecord> account_record(1:AccountRecordArgs query_args) throws(1:ServerError e);
    // 查询帐户流水数量, 与account_record一起进行分页查询
    i32 record_count(1:AccountRecordArgs query_args) throws(1:ServerError e);
    // 帐户统计
    AccountStat account_stat(1:i64 userid) throws(1:ServerError e);

    // 交易，操作交易帐户
    // 先定义这三种，以后不够再加
    // 支付交易，交易金额入交易帐户
    // 必须参数:['userid', 'biz_id', 'chnl_code', 'amt', 'txcurrcd',
    //           'biz_sn', 'sysdtm', 'trade_type', 'card_type', ]
    i16 trade_payment(1:Trade pay_args) throws(1:ServerError e);
    // 撤销交易，交易金额从交易帐户中扣除
    // 必须参数:['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'orig_biz_sn', 'sysdtm', ]
    i16 trade_cancel(1:Trade cancel_args) throws(1:ServerError e);
    // 是否可以撤销交易
    // 必须参数:['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'orig_biz_sn', 'sysdtm', ]
    IsCancelResp trade_is_cancel(1:Trade cancel_args) throws(1:ServerError e);
    // 退货交易，交易金额从交易帐户中扣除
    // 必须参数:['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'orig_biz_sn', 'sysdtm', ]
    i16 trade_refund(1:Trade refund_args) throws(1:ServerError e);
    // 帐户调整，直接调整交易帐户的金额，谨慎使用
    // 这个接口不算手续费
    // 必须参数:['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'sysdtm', ]
    i16 trade_modify(1:Trade refund_args) throws(1:ServerError e);

    // 结算(从钱方出款的交易帐户结算)
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 settle(1:Trade param) throws(1:ServerError e);
    // 结算延迟(从钱方出款的交易帐户结算)
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 settle_delay(1:Trade param) throws(1:ServerError e);
    // 结算到现金实名(从钱方出款的交易帐户结算)
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 settle_realname(1:Trade param) throws(1:ServerError e);
    // 结算到现金中信(从钱方出款的交易帐户结算)
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 settle_zxswiftpass(1:Trade param) throws(1:ServerError e);
    // 通用的结算接口
    // 必传参数: ['from_userid', 'amt', 'txcurrcd', 'biz_sn', 'from_biz_id']
    i16 settlement(1:Transfer req_args) throws(1:ServerError e);
    // 实时结算接口
    // 必传参数: ['from_userid', 'amt', 'txcurrcd', 'biz_sn', 'from_biz_id']
    i16 settlement_realtime(1:Transfer req_args) throws(1:ServerError e);

    // 出款
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'sysdtm', ]
    i16 remit(1:Trade param) throws(1:ServerError e);
    // 出款退票
    // 必传参数: ['userid', 'biz_id', 'amt', 'txcurrcd', 'biz_sn', 'orig_biz_sn', 'sysdtm']
    i16 remit_return(1:Trade param) throws(1:ServerError e);

    // 资金冻结
    // 资金冻结时，可以将现金帐户的金额小于0
    // 必传参数: ['userid', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 fund_blocking(1:Trade param) throws(1:ServerError e);
    // 资金解冻
    // 必传参数: ['userid', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 fund_deblocking(1:Trade param) throws(1:ServerError e);
    // 资金解冻，资金到现金实名帐户
    // 必传参数: ['userid', 'amt', 'txcurrcd', 'biz_sn', ]
    i16 fund_deblocking_realname(1:Trade param) throws(1:ServerError e);

    // 通用的资金冻结
    // 必传参数: ['from_userid', 'amt', 'txcurrcd', 'biz_sn', 'to_biz_id']
    i16 fund_blocking_general(1:Transfer param) throws(1:ServerError e);
    // 通用的资金解冻
    // 必传参数: ['from_userid', 'amt', 'txcurrcd', 'biz_sn', 'to_biz_id']
    i16 fund_deblocking_general(1:Transfer param) throws(1:ServerError e);

    // 充值
    // 必传参数: ['amt', 'txcurrcd', 'biz_sn', 'sysdtm']
    i16 recharge(1:Recharge param) throws(1:ServerError e);
    // 充值撤销
    // 必传参数: ['amt', 'txcurrcd', 'biz_sn', 'sysdtm', 'orig_biz_sn']
    i16 recharge_cancel(1:Recharge param) throws(1:ServerError e);

    // 提现时验证很难做，因为有太多不确定性，包括：
    // 1. 不确定不同的交易帐户是否可以使用同一业务一起提现
    //    比如提现时是将qt+qpos的交易帐户的钱加起来提现？还是单独交易帐户提现
    // 2. 提现时不同的现金帐户的金额如何验证
    // 3. 提现时是否需要计算手续费
    // 等
    // 所以这里只考虑汇宜T0,即提现不做验证，由业务来保证提现的金额不会超过交易帐户的金额，且提现不计算手续费
    // 提现
    // 必传参数: ['userid', 'amt', 'txcurrcd', 'biz_sn', 'sysdtm', 'qfpay_acct_id', ]
    i16 withdraw(1:Trade req_args) throws(1:ServerError e);
    // 提现返回
    // 必传参数: ['userid', 'amt', 'txcurrcd', 'biz_sn', 'orig_biz_sn', 'sysdtm', 'qfpay_acct_id', ]
    i16 withdraw_return(1:Trade req_args) throws(1:ServerError e);
    // 是否可以开通提现功能
    // 返回值，可以开通提现功能的商户id
    list<i64> is_open_withdraw(1:list<i64> userids) throws(1:ServerError e);

    // 银行卡管理
    // 保存银行卡信息, 如果用户与卡存在，则修改，不存在，则添加
    i64 card_save(1:UserCard card_info) throws(1:ServerError e);
    // 保存银行卡信息, 只能存在一个有效的银行卡，如果用户的卡存在，则保存至卡记录表中，不存在，则添加
    i64 card_save_one(1:UserCard card_info) throws(1:ServerError e);
    // 查询银行卡信息
    list<UserCard> card_query(1:CardQueryArgs query_args) throws(1:ServerError e);
    // 查询银行卡信息数量, 与card_query一起进行分页查询
    i32 card_count(1:CardQueryArgs query_args) throws(1:ServerError e);
    // 查询银行卡变更记录
    list<UserCard> card_record(1:CardRecordArgs query_args) throws(1:ServerError e);

    // 费率管理
    // 保存费率信息 id存在，则修改，不存在，则添加
    i64 fee_ratio_save(1:FeeRatio fee_info) throws(1:ServerError e);
    // 查询费率信息
    list<FeeRatio> fee_ratio_query(1:FeeQueryArgs query_args) throws(1:ServerError e);
    // 查询费率数量, 与fee_ratio_query一起进行分页查询
    i32 fee_ratio_count(1:FeeQueryArgs query_args) throws(1:ServerError e);
    // 计算手续费
    FeeResp calculate_fee(1:CalculateFeeArgs param) throws(1:ServerError e);



    // 异步调用交易接口
    // req_data = {
    //     'func': 'trade_payment',    // 接口名
    //     'args': {                   // 参数，与Trade相同
    //         'userid': xxxx,
    //         'amt': xxxx,
    //         'txcurrcd': 'xxx',
    //         'biz_sn': 'xxxxx',
    //         'sysdtm': xxxxxx,
    //         'biz_id': xxxx,
    //         'chnl_code': 'xxxx',
    //         'trade_type': xxx,
    //         'card_type': xxx,
    //         'settletn': xxx,
    //         'title': 'xxxx',
    //         'detail': 'xxxx',
    //         'orig_biz_sn': 'xxxx',
    //     }
    // }
    i32 subscribe(1:string req_data) throws(1:ServerError e);
}


