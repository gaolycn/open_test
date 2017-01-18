namespace py AccountCheck

// 通用异常
exception AccountCheckError {
    1: optional string respcd,
    2: optional string respmsg,
}

# 对账参数
struct AccountCheckParam {
	1: required i64 biz_id,        # 待对账的业务id
	2: required i64 chnl_id,       # 待对账的通道id 
	3: optional string trade_date, # 对账数据交易时间默认是昨天etc:2015-11-11
	4: optional i64 chnl_bat_id,   # 通道批次,默认数据库中最大的
	5: optional i64 acct_bat_id,   # 账户批次,默认数据库中最大的
	6: optional i64 biz_bat_id,    # 业务批次,默认数据库中最大的
}

# 对账返回参数
struct AccountCheckRet {
	1: required i64 chnl_id,        # 通道id
	2: required i64 biz_id,         # 业务id
	3: required string check_date,  # 对账日期
	4: required string respcd,      # 返回代码
	5: required string respmsg,     # 错误信息
}

service AccountCheck {
    # ping
	string ping(),

    #下载导入用户流水
    oneway void parse_download_accountrecord(1:required string date),
    #下载导入业务流水
    oneway void parse_download_bizrecord(1: required string date, 2: required string chnl_name),
    #下载导入通道流水
    oneway void parse_download_chnlrecord(1:required string chnl_name,2:required string date,3:required i16 isupload),

    # 根据通道对账
	oneway void check_by_biz(1:required list<AccountCheckParam> params),
    # 对账审核通过 返回: 0, 成功; 否则抛出异常
	i32 check_audit(1:required i64 check_bat_id) throws (1:AccountCheckError e),
    # 差错批次审核 返回: 0, 成功; 否则抛出异常
    # optype: success:审核成功, fail:审核失败
	i32 unequal_audit(1:required i64 unequal_bat_id, 2:required string optype) throws (1:AccountCheckError e),
}
