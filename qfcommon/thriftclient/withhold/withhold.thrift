namespace py WithHold

// 通用异常
exception WithHoldError {
    1: optional string respcd,
    2: optional string respmsg,
}

// 上传规则参数
struct RuleParam {
    1: required i64 userid,         # 用户id
    2: optional string title,      # 描述
    3: required i64 should_amt,     # 应扣金额
    4: required i16 withhold_type,  # 扣款类型
    5: required i16 enable,         # 是否启用
    6: required string effective_time, # 生效时间
    7: required string expire_time,    # 过期时间
}

// 上传规则参数
struct UpdateRuleParam {
    1: required i64 id,             # id 
    2: required i64 userid,         # 用户id
    3: optional string title,      # 描述
    4: required i64 should_amt,     # 应扣金额
    5: required i16 withhold_type,  # 扣款类型
    6: required i16 enable,         # 是否启用
    7: required string effective_time, # 生效时间
    8: required string expire_time,    # 过期时间
}

service WithHold{
    # ping
    string ping(),

    //添加扣款规则 返回：0, 成功；否则抛出异常
    i32 add_withhold_rule(1:required list<RuleParam> params) throws(1:WithHoldError e),

    //修改扣款规则 返回：0, 成功；否则抛出异常
    i32 update_withhold_rule(1:required UpdateRuleParam update_rule) throws(1:WithHoldError e),

    //扣款 返回：扣款笔数, 成功；否则抛出异常
    oneway void withhold(),

    //取消扣款 返回：0, 成功；否则抛出异常
    i32 withhold_cancel(1:required i64 userid) throws(1:WithHoldError e),

    //提交审核 返回：0, 成功；否则抛出异常
    i32 withhold_apply(1:required i64 withhold_bat_id) throws(1:WithHoldError e),

    //扣款审核成功 返回：0, 成功；否则抛出异常
    i32 withhold_audit(1:required i64 withhold_bat_id) throws(1:WithHoldError e),

    //扣款审核失败 返回：0, 成功；否则抛出异常
    i32 withhold_audit_refuse(1:required i64 withhold_bat_id) throws(1:WithHoldError e),

    //下载规则
    oneway void download_rule_excel(1:required string userid, 2:required string title, 3:required string finish, 4:required string enable),

    //下载纪录
    oneway void download_history_excel(1:required string bat_id),

    //获取完成标记
    i16 get_finish_flag() throws(1:WithHoldError e),
}
