namespace py cashdraw

// 代付服务异常
exception CashdrawError
{
    1: i32      respcd,     // 返回码
    2: string   resperr,    // 错误信息
    3: optional string   ext_json,   // 扩展字段(json字符串), 返回一些额外的扩展信息
}

enum ERRCODE
{
    // 系统异常类错误
    INNER_SERVICE_ERR = 5001,   // 内部调用失败
    OUT_SERVICE_ERR,            // 外部调用失败
    SYSTEM_MAINTAIN,            // 系统维护
    SYSTEM_ERROR,               // 系统错误

    // 逻辑类错误
    LOGIC_ERROR = 6001,        // 逻辑错误
    CHNL_FAILED = 6002,        // 通道返回业务请求失败
    PARAM_ERROR = 6003,        // 参数错误
}

// 交易状态码
enum TradeStatus
{
    SUCCESS=0,  //成功
    FAILED,     //失败
    PROCESSING, // 交易中
    TIMEOUT,    //交易超时
    REFUNDED,   //已退款
}

// 账户类型
enum AccountType
{
    CORPORATE=1,        // 对公
    PERSONAL=2,         // 个人
}

//卡类型
enum CardType
{
    DE=1,       // 借记卡
    CR=2,       // 信用卡
}

enum ChnlFlag
{
    HUIYI=1,        // 汇宜
    JD=2,           // 京东
    TFB=3,          // 天付宝
}

// 付款人信息
struct PriInfo
{
    1: string   account_no,     // 付款人账号
    2: string   account_name,   // 付款人名称
}

// 收款人信息
struct PyeInfo
{
    1: string   account_no,     // 收款人账号
    2: string   account_name,   // 收款人名称
    3: AccountType   account_type,   // 收款账号类型
    4: string   bank_no,        // 收款行开户行银联号
    5: string   bank_name,      // 收款行 银行名
    6: CardType card_type,      // 卡类型
    7: string   card_code,      // 银行编码, 例如农业银行== ABC
}

// 交易配置参数
struct TradeConf
{
    1: required ChnlFlag  chnl_flag,      // 通道标志
    2: optional string  ins_id_cd,      // 机构编号(通道分配的机构编号), 汇宜使用
    3: optional string  mchnt_cd,       // 商户代码,  汇宜: 汇宜分配的商户代码; 京东: 京东分配的商户号
    4: optional string  bus_cd,         // 业务代码, 汇宜使用
}


// 实时代付请求参数
struct Pay4AnotherArg
{
    1: required PriInfo  pri_info,      // 付款人信息
    2: required PyeInfo  pye_info,      // 收款人信息
    3: required TradeConf trade_conf,   // 交易配置
    4: required string   syssn,          // 流水号. 必须全局唯一，建议格式：机构号+商户号+提交时间+固定位数顺序流水号。
    5: required string   sysdtm,         // 服务器时间, 形如: 20160122100812
    6: required i64      txamt,          // 交易金额, 单位: 分
    7: required string   purpose='qfpay',    // 用途
    8: required string   pos_script='qfpay', // 附言
    9: optional string   qf_reversed,   // 发起方保留参数, 通道原样返回, 京东: 京东只有回调时才会返回此数据
}

// 实时代付查询请求 参数
struct Pay4AnotherQueryArg
{
    1: required string syssn,        // 交易流水号
    2: required string sysdtm,       // 服务器时间, 形如: 20160122100812
    3: required string origssn,      // 原交易流水号, 要查询的交易号,我们自己的syssn
    4: required string origdtm,      // 原交易时间, 形如: 20160122100812
    5: required TradeConf trade_conf,   // 交易配置
    6: optional string   qf_reversed,   // 发起方保留参数, 京东无此参数, 汇宜使用
}

// 交易返回信息
struct TradeInfo
{
    1: required string syssn,       // 交易流水号
    2: required TradeStatus status,      // 交易状态
    3: optional i64 txamt,          // 交易金额, 单位: 分
    4: optional string trade_no,    // 通道流水号
    5: optional string currency,    // 交易币种
}

//数据返回
struct Pay4AnotherResult
{
    1: required string respcd,      
    2: required string respmsg,
    3: required TradeInfo trade_info,   // 交易信息
    4: optional string extend,          // 扩展字段, json字符串
}

//  以下接口,如无特殊注明均放回json字符串,形如:
// {'respcd': '0000', 'respmsg': 'OK', 'huiyi_extend': {}}
service cashdraw
{
    ////////  实时代付相关 /////////
    // 实时代付
    Pay4AnotherResult pay4another(1:Pay4AnotherArg arg) throws(1:CashdrawError e);  // 返回json字符串
    // 实时代付查询
    Pay4AnotherResult pay4another_query(1:Pay4AnotherQueryArg arg) throws(1:CashdrawError e);
}
