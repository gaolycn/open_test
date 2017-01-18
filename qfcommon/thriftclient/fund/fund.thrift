//新账务对外接口
namespace py fundserve

//通用返回
struct ReturnMsgInfo{
    1: optional string respcd,
    2: optional string respmsg,
}

//异常
exception ServerException
{
    1: string error_code,
    2: string error_msg
}

//账务配置查询参数
struct FundConfigArgs{
    1: list<string> vals,     //账务配置的值   数组类型
    2: i16 val_type,          //账务配置类型    1:商户ID 2:商户号 3:子商户  
    3: list<string> busicds,  //交易类型   
    4: i16 state,             //状态       0无效   1:有效
    5: i16 iscompare,         //是否对账   1:对账  2:不对帐
    6: string effectdate,     //查询日期
    8: i32 page,              //页数
    9: i32 maxnum,            //每页最大数
}

//账务配置查询返回详细
struct FundconfigRecord{
    1: required string val,          //账务配置的值
    2: required i16 val_type,        //配置值的类型
    3: required string busicd,       //交易类型
    4: optional i16 state,           //状态
    5: optional i16 iscompare,       //是否对账
    6: optional string effecttime,   //生效时间
    7: optional string expiretime,   //失效时间
    8: optional string utime,        //最后更新时间
}

//账务配置返回结果
struct FundConfigRet{
    1: i64 count,                         //总笔数
    2: list <FundconfigRecord> records,   //配置返回值集合
}

//获取交易标签的参数类型
enum TradeTagArgsType {
    //用户ID
    USERID = 1,
    //通道号
    HYUSERID = 2
}

// 用户类型
enum UserTag {
     NON_T1_CLEARING = 1, // T1不清算
}

enum MerchantType {
    BIG_MERCHANT = 1, //大商户
    REAL_MERCHANT = 2, //实名商户
    T0_MERCHANT = 3, //T0商户
}

struct MerchantPara {
    1: list<string> chnl_userids, //商户id
    2: string chnl_code, //通道码
}

// 错误代码
enum ERRCODE {
     DBERR = 2000, // 数据库错误
     PARAMERR = 2101, // 参数错误
     SERVERERR = 2600, // 服务器错误
     WITHDRAW_NOT_COMPLETE = 5000, // 提现操作未完成
     WITHDRAW_NO_PRIVILEGE = 50001, // 用户无提现权限
}

//划账表相关
struct DebitRet
{
    1: i64 payamt,
    2: string status;
    3: string expectdate;
    4: string paytime;
    5: string biznum;
}

struct TradeRet
{
    1: i64 tradeamt,
    2: i64 payamt,
    3: i64 fee,
    4: string status,
    5: string tradetime,
    6: string tradetype,
    7: i64 ori_coupon_amt, //红包本金
    8: i64 coupon_amt,     //红包除去手续费金额
    9: string chnlid,      //通道id
}

struct AccounttradeArgs
{
    1: optional string userid,                  #用户id,如果是钱台数据  则格式 应该是 appid_merchantid
    2: optional i16 settletype,                 #结算类型
    3: optional string starttime,               #交易开始时间
    4: optional string endtime,                 #交易结束时间
    5: optional i16 settleflag=3,               #结算状态 默认取已结算
    6: optional i16 equalflag=1,                #平账状态 默认取平账
    7: optional list<string> userids            #userids 先针对于qpos用户
}

struct AccountRecord
{
    1: string userid,                        #用户id,如果是钱台数据  则格式 应该是 appid_merchantid
    2: i16 settletype,                       #结算类型
    3: i16 settleflag,                       #结算状态
    4: i16 equalflag,                        #平账状态
    5: string syssn,                         #系统流水号
    6: string orderno,                       #订单号
    7: string busicd,                        #交易类型
    8: i64 tradenum,                         #交易金额
    9: i64 settleamt,                        #结算金额
    10: i64 qffee,                           #钱方手续费
    11: string tradedtm,                     #交易时间
    12: string qfstldate,                    #钱方结算日期
}

struct TradeStatis{
    1: i64 tradeamt,
    2: i64 fee,
    3: i32 cnt,
    4: string tradedt,
}


struct WithholdHistorySummary {
    1: i64 userid;
    2: string title;
    3: i32 amount;
    4: string withhold_time;
    5: string op_token;
    6: string evidence_date;
    7: string appsrc;
}

service FundService{
    //ping
    string ping(),

    FundConfigRet findfund(1: FundConfigArgs fund_args) throws(1:ServerException e),
    
    //获取交易的标签。
    map<string, string> findTradeTags(1: list<string> query_args, 2: TradeTagArgsType query_type) throws(1:ServerException e),

    //获取无卡交易的标签。
    map<string, MerchantType> getMerchantType(1: MerchantPara mcht_args) throws(1:ServerException e),

    //提现
    //必传参数，userid：用户id， amt: 提现金额， fee: 提现手续费，biz_sn: 提现流水号
    //返回值：提现纪录流水号
    string withdraw(1:i64 userid, 2:i64 amt, 3:i32 fee, 4:string biz_sn) throws(1:ServerException e),

    // 批量添加用户信息, 并设置为有效状态
    // 传入参数: userids: 用户id, user_type: 用户类型, 目前只支持T1不清算用户
    // 返回值为: {userid: 1, userid2: 0}, 1: 添加成功, 0: 添加失败
    // 注意: 如果已经存在userid-user_type则设置不会成功
    map<i64, i32> addUserConf(1:list<i64> userids, 2:UserTag user_tag) throws(1: ServerException e),

    // 批量修改用户状态信息
    // 传入参数: userids 用户id, user_type:用户类型,目前只支持T1不清算用户, user_state 用户状态
    // 返回值: {userid: 1, userid2: 0}, 1: 添加成功, 0: 添加失败 
    map<i64, i32> setUserState(1: list<i64> userids, 2: UserTag user_tag, 3: i32 user_state) throws(1: ServerException e),

    // 批量查找某类型用户的状态
    // 传入参数: userids: 用户id, user_type:用户类型,目前只支持T1不清算用户
    // 返回值, 只返回有用户信息的信息, {userid1: 1, userid2: 0}, 1: 状态有效, 0: 状态无效
    map<i64, i32> findUserConf(1: list<i64> userids, 2: UserTag user_tag) throws(1: ServerException e),

    //到账记录相关
    list<string> findDebitpageInfo(1:i64 userid, 2:i64 page 3:i64 pagesize) throws(1:ServerException e),
    list<DebitRet> findDebitInfo(1:i64 userid, 2:list<string> expectdates) throws(1:ServerException e),
    
    //对账表详细信息
	list<TradeRet> findActtradeInfo(1:i64 userid, 2:string expectdate,3:i64 page,4:i64 pagesize) throws(1:ServerException e),

    list<AccountRecord> get_accounttrades(1:AccounttradeArgs act_args) throws(1:ServerException e),
    
    //对账表统计
    list<TradeStatis> findActtradeStatis(1:i64 userid, 2:string expectdate) throws(1:ServerException e),

    //获取扣款历史
    list<WithholdHistorySummary> findWithholdHistory(1:i64 userid, 2:string expectdate) throws(1:ServerException e), 

}
