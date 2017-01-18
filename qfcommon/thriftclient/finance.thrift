namespace py finance

struct NewDebitRecord
{
    1: string userid,           //商户ID
    2: string name,             //商户姓名
    3: i64 payamt,              //打款金额
    4: string paydate           //打款日期
    5: string busicd            //业务类型
    6: string business_ref_num  //业务参考号
    7: string status            //打款状态
    8: string bankname          //开户行
    9: string bankaccount       //开户银行
    10: i64 tradeamt,           //交易金额
    11: i64 fee,                //手续费
}

struct NewDebitQuery
{
    1: list <string> userids,       //用户ID list     
    2: string startdate,        //开始时间
    3: string enddate,          //结束时间
    4: list <string> busicds,    //业务类型

}

struct DebitRet
{
    1: i64 payamt,
    2: string status;
    3: string expectdate;
    4: string paytime;
    5: string biznum;
}

struct DebitRecord
{
    1: i64 payamt,         //打款金额
    2: string status;      //打款状态
    3: string expectdate;  //预计打款日期
    4: string paytime;     //实际打款时间
    5: string biznum;      //打款业务参考号
    6: string merchantid;  //商户号
}

struct QposDebitRecord
{
    1:  string name                 //开户人姓名 
    2:  string bankname             //开户银行
    3:  string bankaccount          //开户账户
    4:  i64 payamt,                 //打款金额
    5:  string status;              //打款状态, 返回中文提示
    6:  string expectdate;          //预计打款日期
    7:  string paydate;             //实际打款日期, 为空返回'----'
    8:  string paytime;             //实际打款时间
    9:  string tradedate_start;     //实际打款时间
    10: string tradedate_end;       //实际打款时间
    11: string biznum;              //打款业务参考号
}

struct DebitQuery
{
    1: required i64 userid,		//用户id 
    2: required string appsrc,      	//app来源, 范围:qf,mmwd,qt 
    3: optional i64 merchantid,     	//商户号
    4: required i64 page,           	//页数,从0开始 
    5: required i64 maxnum          	//每页最大数
    6: optional string paytime_start	//打款时间范围 格式为%Y-%m-%d %H:%M:%S
    7: optional string paytime_end	//打款时间范围 格式为%Y-%m-%d %H:%M:%S
}

struct QposDebitQuery
{
    1: required i64 userid,		        //用户id 
    2: required i64 page,           	//页数,从0开始 
    3: required i64 maxnum          	//每页最大数
    4: optional string paytime_start	//打款时间范围 格式为%Y-%m-%d %H:%M:%S
    5: optional string paytime_end	//打款时间范围 格式为%Y-%m-%d %H:%M:%S
}

struct DebitRecordsRet
{
    1: i64 count;              //总笔数
    2: list<DebitRecord> debit_record_list
}

struct QposDebitRecordsRet
{
    1: i64 count;              //总笔数
    2: list<QposDebitRecord> debit_record_list
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

struct AccountTradeRecord
{
    1: i64 tradeamt,            //交易本金
    2: i64 settleamt,           //结算金额
    3: i64 fee,                 //手续费
    4: string status;           //结算状态
    5: string tradetime;        //交易时间
    6: string tradetype;        //交易类型
    7: string merchantid;       //商户号 
    8: string syssn;            //钱方交易查询号
    9: string external_sn;      //外部交易查询号
}

struct TradeRecordsRet
{
    1: i64 count;              //总笔数
    2: list<AccountTradeRecord> trade_record_list
}

struct BalanceRet
{
    1: i64 total_amt,
    2: i64 available_amt,
    3: i64 unavailable_amt,
}

struct UserAccountRet 
{
    1: i32 total_balance,                       #全部余额
    2: i32 available_balance,                   #可用余额
    3: i32 unavailable_balance,                 #不可用余额
    4: i32 proxy_balance,                       #代清算账户余额
}

struct AccountBill
{
    1: i64 change_amt,
    2: string desc,
    3: i32 type,
    4: string status,
    5: string optoken,
    6: string biznum;
    7: string optime;
}

struct BillArgs
{
    1: required i32 userid,
    2: required string appsrc,
    3: optional string startdate,
    4: optional string enddate,
    5: optional i32 page,
    6: optional i64 maxnum,
}

struct RemittanceRecordPara
{
    1: required string serialno,
    2: required string head_bank_name,
    3: required string bank_name,
    4: required string branch_bank_code,
    5: required string bank_user,
    6: required string bank_account,
    7: required string bank_province,
    8: required string bank_city,
    9: required i32 payamt,
    10: optional string note,
}

struct RemittanceApprovalPara
{
    1: required string out_userid,
    2: required string batch_number,
    3: required i32 total_money,
    4: required i32 total_items,
    5: required string applicant_id,
    6: required list<RemittanceRecordPara> remittance_records,
    7: required string src,
    8: optional string note,
}

struct RemittanceApprovalQuery
{
    1: required string out_userid,
    2: required i32 page,
    3: required i32 maxnum,
    4: required string src,
    5: optional i16 biz_type,
    6: optional string batch_number,
    7: optional i64 approval_id,
    8: optional i32 batch_status,
    9: optional string start_date,
    10: optional string end_date,
}

struct RemittanceApproval
{
    1: i64 id,
    2: string out_userid,
    3: string batch_number,
    4: string memo,
    5: i32 total_money,
    6: i32 total_items,
    7: i32 batch_status,
    8: string applicant_id,
    9: string approver_id,
    10: string application_time,
    11: string processing_time,
    12: string remittance_time,
    13: string errortip,
}

struct RemittanceApprovalRet
{
    1: i32 count,
    2: i32 page,
    3: i32 maxnum,
    4: list<RemittanceApproval> remittance_approvals,
}

struct RemittanceSummaryRet
{
    1: string batch_number,
    2: string out_userid,
    3: string memo,
    4: i32 batch_status,
    5: string applicant_id,
    6: string approver_id,
    7: string application_time,
    8: string processing_time,
    9: string remittance_time,
    10: string errortip,
    11: i32 total_money,
    12: i32 total_items,
    13: i32 success_money,
    14: i32 success_items,
    15: i32 fail_money,
    16: i32 fail_items,
    17: string update_time,
}

struct RemittanceRecord
{
    1: string serialno,
    2: string remittance_serialno,
    3: i32 pay_money,
    4: i16 status,
    5: string memo,
    6: string update_time,
    7: string errortip,
    8: string bank_account,
    9: string bank_user,
    10: string bank_name,
}

struct RemittanceRecordRet
{
    1: i32 count,
    2: i32 maxnum,
    3: i32 page,
    4: string out_userid,
    5: list<RemittanceRecord> remittance_records,
}

enum RemittanceRecordStatus
{
    UNCONFIRMED = 1,
    CONFIRMED = 2,
    CANCELED = 3,
    SUCCESS = 4,
    FAIL = 5,
}

struct RemittanceRecordQuery
{
    1: required i64 approval_id,
    2: required i32 page,
    3: required i32 maxnum,
    4: required string src,
    5: optional RemittanceRecordStatus status,
}

struct BillRet
{
    1: i64 total_count,
    2: i64 count,
    3: list<AccountBill> bill_list,
}

struct RemittanceRet
{
    1: i64 payamt,
    2: string status;
    3: string expectdate;
    4: string paydate;
}

struct RemitsettlefeeRet
{
    1: string out_userid,
    2: string src,
    3: i32 remit_settlefee,
}

struct AccountFeeRet
{
    1: i64 userid,
    2: double feeratio,
    3: double creditratio,
    4: i64 maxfee,
    5: i64 creditmaxfee,
}

struct AccountFee
{
    1: i64 userid,
    2: double feeratio,
    3: double creditratio,
    4: i64 maxfee,
    5: i64 creditmaxfee,
}

struct FeeRatioRecord
{
    1: required string out_userid,
    2: required string src,
    3: optional double feeratio,
    4: optional double creditratio,
    5: optional double preauthratio,
    6: optional double tenpay_ratio,
    7: optional double yeepay_ratio,
    8: optional double unionpay_ratio,
    9: optional double alipay_ratio,
    10: optional i32 maxfee,
    11: optional i32 creditmaxfee,
    12: optional i32 preauthmaxfee,
    13: optional i32 tenpay_maxfee,
    14: optional i32 alipay_maxfee,
    15: optional i32 yeepay_maxfee,
    16: optional i32 unionpay_maxfee,
    17: optional double alipay_qr_ratio=0.006,
    18: optional double tenpay_qr_ratio=0.006,
    19: optional i64 qfuid=0,
}

struct TradeFeeStruct
{
    1: required i64 userid,     //用户ID
    2: required string src,     //来源,钱台务必设置为"qt", 喵喵微店务必设置为"mmwd", 钱方为空即可
    3: i16 groupid,             //渠道ID,喵喵微店务必设置为21001, 其他可为空
    4: double debit_ratio,      //借记卡费率, 浮点型
    5: double credit_ratio,     //信用卡费率, 浮点型
    6: i16 debit_maxfee,        //借记卡手续费封顶,-1表示没有封顶手续费
    7: i16 credit_maxfee,       //信用卡手续费封顶,-1表示没有封顶手续费
    8: double tenpay_ratio,     //微信支付手续费, 浮点型
    9: double alipay_ratio,     //支付宝手续费, 浮点型
    10: i16 tenpay_maxfee,      //微信手续费封顶费用,-1表示没有封顶手续费
    11: i16 alipay_maxfee,      //支付宝手续费封顶,-1表示没有封顶手续费
    12: double jdpay_ratio,     // 京东手续费
    13: double qqpay_ratio,        //QQ钱包手续费
}

struct AccountPeriodRet
{
    1: string start_date,
    2: string end_date,
    3: string settle_date,
    4: string search_date,
}

struct RiskDelayRet
{
    1: i32 no,
    2: i32 count,
    3: i16 status,
    4: i32 delayid,
    5: i64 userid,
    6: i16 delay_level,
    7: i16 category,
    8: string risk_flag,
    9: string trade_date,
    10: string clear_date,
    11: string appsrc,
    12: string memo,
}

struct RiskDelayQuery
{
    1: required i32 page=0,
    2: required i32 maxnum=100,
    3: required i16 delay_level,
    4: optional string appsrc,
    5: optional i32 delayid,
    6: optional i64 userid,
    7: optional i16 category,
    8: optional string risk_flag,
    9: optional string trade_date_start,
    10: optional string trade_date_end,
    11: optional string clear_date_start,
    12: optional string clear_date_end,
}

struct WithDrawalAmtRet
{
    1: i64 ongoing_amt,
    2: i64 available_amt,
    3: i64 withdrawled_amt,
    4: i64 return_amt,
    5: i64 risk_amt,
}

struct WithDrawalInfoRet
{
    1: i64 payamt,
    2: i64 fee,
    3: i32 status;
    4: string paytime;
}

struct WithholdRule {
    1: i32 id;          //规则ID
    2: string title;    //规则名称
    3: string desc;     //规则说明
    4: string memo;
}

struct WithholdHistory {
    1: i32 id;
    2: i64 userid;
    3: i32 user_withhold_id;
    4: i32 amount;
    5: string op_token;
    6: string evidence_date;
    7: string withhold_time;
    8: i32 operatorid;
    9: string memo;
    10: string appsrc;
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

struct ApplyRecharge{
    1: i64 id;                    #唯一id
    2: string out_userid;         #用户id
    3: i32 apply_status;          #申请状态
    4: i64 recharge_money;        #充值金额
    5: string gogal_account;      #目标用户
    6: string create_time;        #申请时间
    7: string apply_memo;         #申请备注
    8: string admin_id;           #审批人id
    9: string admin_memo;         #审批备注
    10: string admin_time;        #审批时间
}

struct ApplyRechargeQuery{
    1: required string out_userid;        #用户id
    2: required i32 page;                 #页数
    3: required i32 maxnum;               #每页的数目
    4: optional string start_time;        #开始时间
    5: optional string end_time;          #结束时间
    6: optional i32 apply_status;         #申请状态
}

struct ApplyRechargeRet{
    1: i32 page;
    2: i32 maxnum;
    3: i32 count;
    4: list<ApplyRecharge> apply_recharge_list;
}

struct UserWithhold {
    1: i32 id;
    2: string title;
    3: i64 userid;
    4: i32 amount;
    5: i16 withhold_type;
    6: bool enable;
    7: i16 opentype;
    8: string start_date;
    9: string end_date;
    10: string memo;
    11: string appsrc;
}

struct UserWithholdRet {
    1: i32 count;
    2: list<UserWithhold> user_withhold_list;
}

struct UserWithholdQuery {
    1: i32 page=0;
    2: i32 maxnum=100;
    3: string title;
    4: i64 userid;
    5: i32 amount;
    6: i16 withhold_type;
    7: bool enable;
    8: i16 opentype;
    9: list<string> start_date;
    10: list<string> end_date;
    11: string appsrc;
}

enum BankType {
    BUSINESS = 1,   // 对公
    PERSONAL = 2    // 对私
}

struct QtBankInfo {
    1: required i64 userid;
    2: required i64 merchant_id;
    3: required string head_bank_name;
    4: required string bank_user;
    5: required string bank_account;
    6: optional BankType bank_type;
    7: optional string bank_name;
    8: optional string branch_bank_code;
    9: optional string bank_province;
    10: optional string bank_city;
    11: optional i16 is_reremit;
}

struct QtBankInfoRet {
    1: i32 count;
    2: i32 page=1;
    3: i32 maxnum=100;
    4: list<QtBankInfo> bank_info_list;
}

enum AccountType
{
    UNAVAILABLE = 0,             #不可用
    AVAILABLE = 1,               #可用
    PROXY = 2,                   #代理
}

struct BillQuery
{
    1: required string out_userid,              #用户id
    2: optional string src,                     #来源
    3: optional AccountType account_type,       #账户类型, 为空则是全部类型
    4: optional string start_time,              #起始时间 格式:%Y-%m-%d %H:%M:%S
    5: optional string end_time,                #截止时间 格式:%Y-%m-%d %H:%M:%S
    6: optional i16 op_type,                    #操作类型(交易类型)
    7: optional i16 status,                     #状态
    8: optional i32 page,                       #页数
    9: optional i64 maxnum,                     #每页最大数
}


struct BillArgsV2
{
    1: required string userid,                  #用户id, 钱台userid为"%(appid)_%(mchnt_id)"
    2: optional string src,                     #来源, 钱台为"qt"
    3: list <AccountType> account_type,         #账户类型, 为空则是全部类型,list列表形式
    4: optional string start_time,              #起始时间 格式:%Y-%m-%d %H:%M:%S
    5: optional string end_time,                #截止时间 格式:%Y-%m-%d %H:%M:%S
    6: list <i16> op_type,                      #操作类型(交易类型),list列表形式
    7: list <i16> status,                       #状态,list列表形式
    8: optional i32 page,                       #页数
    9: optional i64 maxnum,                     #每页最大数
}


struct UserBillItem
{
    1: i32 change_amt,                          #变更余额
    2: i16 op_type,                             #操作类型(交易类型)
    3: AccountType account_type,                #账户类型
    4: i32 open_balance,                        #操作前余额
    5: i32 close_balance,                       #操作后余额
    6: string op_token,                         #唯一标示(例如：交易的syssn)
    7: string out_token,                        #外部唯一标示(例如：交易的syssn)
    8: string relate_op_token,                  #相关操作唯一标示(例如：交易撤销的原始syssn)
    9: i16 status,                              #状态
    10: string other_side,                      #交易对方(无卡就是支付宝账号，有卡是加密卡号)
    11: string product_name,                    #商品名称
    12: string biz_summary,                     #业务摘要（简单描述业务的过程要点，可为空）
    13: string note,                            #备注
    14: string create_time,                     #创建时间, 格式为%Y-%m-%d %H:%M:%S
}

struct UserBillRet
{
    1: i64 total_count,                         #总数
    2: list<UserBillItem> bill_list,                #账单列表
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



exception ServerException
{
    1: i32 error_code,
    2: string error_msg
}

service Finance {
    i16 alipay_batch_trans_notify(1:string serialno, 2:bool success, 3:string note),
    i16 alipay_batch_trans_notify_2(1:string batch_no, 2:string success_details, 3:string fail_details),

    list<DebitRet> get_debitinfo(1:i32 userid, 2:string appsrc, 3:i32 page, 4:i64 maxnum) throws(1:ServerException e),

    list<RemittanceRet> get_remittanceinfo(1:i32 userid, 2:string appsrc, 3:i32 page, 4:i64 maxnum) throws(1:ServerException e),

    BalanceRet get_balanceinfo(1:i32 userid, 2:string appsrc) throws(1:ServerException e),
    BillRet get_userbill_by_page(1:i32 userid, 2:string appsrc, 3:i32 page, 4:i64 maxnum) throws(1:ServerException e),
    BillRet get_userbill_by_date(1:i32 userid, 2:string appsrc, 3:string startdate, 4:string enddate) throws(1:ServerException e),
    BillRet get_userbill(1:BillArgs billargs) throws(1:ServerException e),
    list<TradeRet> get_tradeinfo_by_biznum(1:string biznum) throws(1:ServerException e)

    list<AccountPeriodRet> get_account_period(1:list<string> search_date_list) throws(1:ServerException e)

    # 旧费率接口，QPOS、喵喵使用,只有刷卡费率
    list<AccountFeeRet> get_account_fee(1:list<i32> userid_list) throws(1:ServerException e)
    i16 set_account_fee(1:i32 userid, 2:i32 src_channel_id, 3:string appsrc) throws(1:ServerException e)
    i16 set_qpos_account_fee(1:AccountFee accout_fee) throws(1:ServerException e)

    # 新费率接口

    # 插入成功返回0, 更新成功返回1, 其他错误返回2
    i16 set_feeratio(1: FeeRatioRecord feeratio) throws(1:ServerException e)

    # 返回存在的list
    list<FeeRatioRecord> get_feeratio(1:list<string> out_userid_list, 2: string src) throws(1:ServerException e)

    #添加余额申请记录
    i64 add_apply_recharge_record(1:string out_userid,2:i32 recharge_money, 3:string gogal_account, 4:string apply_memo) throws(1:ServerException e)
    #查询余额申请记录返回一个list
    ApplyRechargeRet get_apply_recharge_list(1:ApplyRechargeQuery query) throws(1:ServerException e)
    #查询指定id的申请记录
    ApplyRecharge get_apply_recharge(1:i32 id) throws(1:ServerException e)

    RiskDelayRet add_long_risk_delay(1:i32 userid, 2:string risk_flag, 3: string appsrc) throws(1:ServerException e)
    RiskDelayRet add_short_risk_delay(1:i32 userid, 2:string trade_date, 3:string clear_date, 4:string risk_flag,
                                      5:string appsrc) throws(1:ServerException e)

    RiskDelayRet add_tl_short_risk_delay(1:i32 userid, 2:string trade_date, 3:string clear_date, 4:string risk_flag,
                                      5:string appsrc) throws(1:ServerException e)

    list<RiskDelayRet> get_risk_delay_info(1:RiskDelayQuery query) throws(1:ServerException e)
    RiskDelayRet disable_risk_delay(1:i32 delayid) throws(1:ServerException e)
    RiskDelayRet cancel_delay_trade(1:i32 delayid) throws(1:ServerException e)

    RiskDelayRet set_risk_delay(1:i32 delayid, 2:i32 userid, 3:string trade_date, 4:string clear_date,
                                      5:string risk_flag, 6:string appsrc) throws(1:ServerException e)
    RiskDelayRet set_clear_date(1:i32 delayid, 2:string clear_date) throws(1:ServerException e)

    WithDrawalAmtRet get_withdralwal_amt(1:i32 userid) throws(1:ServerException e)
    i16 make_withdralwal(1:i32 userid) throws(1:ServerException e)
    list<WithDrawalInfoRet> get_withdralwal_info(1:i32 userid, 2:i32 page, 3:i64 maxnum) throws(1:ServerException e)

    list<WithholdHistory> get_withhold_history(1: i32 userid, 2: string appsrc) throws(1: ServerException e);
    list<WithholdHistorySummary> get_withhold_history_by_biznum(1:string biznum) throws(1: ServerException e);

    bool add_user_withhold(1: string title, 2: i32 userid, 3: i32 amount, 4: i16 withhold_type, 5: string start_date,
                           6: string end_date, 7: string memo, 8: string appsrc) throws(1: ServerException e)
    UserWithholdRet get_user_withhold(1: UserWithholdQuery query) throws(1: ServerException e);
    bool update_user_withhold(1: UserWithhold user_withhold) throws(1: ServerException e);

    i64 get_all_income(1:i32 userid, 2:string appsrc) throws(1:ServerException e)

    DebitRecordsRet get_debit_records(1:DebitQuery query) throws(1:ServerException e) //获取清算记录
    QposDebitRecordsRet get_qpos_debit_records(1:QposDebitQuery query) throws(1:ServerException e) //qpos获取清算记录定制版
    TradeRecordsRet get_trade_records_by_biznum(1:i64 userid, 2:string biznum) throws(1:ServerException e) //根据业务参考号获取结算明细记录

    QtBankInfo get_qt_bank_info(1:i64 userid, 2:i64 merchant_id) throws(1:ServerException e);
    QtBankInfo set_qt_bank_info(1:QtBankInfo qtbank_info) throws(1:ServerException e);

    QtBankInfoRet fetch_qt_bank_info_list(1:list<i64> userid_list, 2:i32 page=1, 3:i32 maxnum=100);


    //检查商户的批次号是否可用
    //如果均可用则返回真，否则返回假
    bool check_batch_number_available(1: string out_userid, 2: string batch_number, 3: string src) throws(1:ServerException e);

    //检查商户上传的划款流水号是否可用
    //返回重复的列表
    list<string> check_remittance_serialno_available(1: string out_userid, 2: list<string> serialno_list, 3: string src) throws(1:ServerException e);

    //添加划款审批记录
    //添加成功返回大于0的approval_id，返回0表示添加失败。
    //失败原因可能有: 参数中的金额数目核对不上、RemittanceRecordPara参数不全等
    i64 add_remittance_approval(1: RemittanceApprovalPara remittance_para) throws(1:ServerException e);

    //查询划款审批记录
    RemittanceApprovalRet get_remittance_approval_list(1: RemittanceApprovalQuery query) throws(1:ServerException e);

    //确认划款
    //成功返回1，余额不足返回2，其他错误返回3
    i32 confirm_remittance(1: i64 approval_id, 2: string approver_id, 3: string src) throws(1:ServerException e);

    //拒绝划款
    //操作成功返回真，否则返回假
    bool reject_remittance(1: i64 approval_id, 2: string approver_id, 3: string src) throws(1:ServerException e);

    //划款结果总览
    RemittanceSummaryRet get_remittance_summary(1: i64 approval_id, 2: string src) throws(1:ServerException e);

    //划款明细
    RemittanceRecordRet get_remittance_records(1: RemittanceRecordQuery query) throws(1:ServerException e);

    //获取余额信息
    UserAccountRet get_balance_account_info(1:string out_userid, 2:string src) throws(1:ServerException e);

    //获取用户帐单
    UserBillRet get_user_bill(1:BillQuery bill_args) throws(1:ServerException e);

    //获取用户账单新版, 部分请求条件可使用list
    UserBillRet get_user_bill_v2(1:BillArgsV2 bill_args) throws(1:ServerException e);

    //获取手续费,注:如果不存在记录,会生成默认的费率返回,其中groupid=-1

    TradeFeeStruct get_trade_fee(1:i64 userid, 2:string src) throws(1:ServerException e)
    //设置手续费, 返回1设置成功,失败返回异常
    i16 set_trade_fee(1:TradeFeeStruct trade_fee_args) throws(1:ServerException e)

    //设置或者修改代清算手续费, 返回1表示修改成功，返回2添加成功，其他错误返回3
    i16 set_remit_settlefee(1:string out_userid, 2:string src, 3:i32 remit_settlefee) throws(1:ServerException e)
    //查看代清算费率
    RemitsettlefeeRet get_remit_settlefee(1:string out_userid, 2:string src) throws(1:ServerException e)

    //查询大商户账期
    list<NewDebitRecord> get_newdebit_list(1:NewDebitQuery newquery) throws(1:ServerException e)

    //下载对账表相关数据
    list<AccountRecord> get_accounttrades(1:AccounttradeArgs act_args) throws(1:ServerException e)
}
