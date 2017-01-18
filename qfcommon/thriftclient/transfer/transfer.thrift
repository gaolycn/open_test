namespace py TransFer

// 通用异常
exception TransFerError {
    1: optional string respcd,
    2: optional string respmsg,
}

struct NeedTransferRet{
    1: required i64 amt,
    2: required i64 count,
}

struct BankrefundRet{
    1: required string settle_sn, // 钱方出款流水号
    2: required i64 amt,          //退票金额
    3: optional string memo,
    4: optional i16 type,
}

struct TransFerChnl{
    1: string chnl_id,             //出款通道Id
    2: i64 amt,                 //出款通道留存金额
}

struct UsersChnlInfo{
    1: required string userid,
    2: optional string trans_subchnlid,
    3: required string bat_id,
}

struct Capitalchangeret{
    1: optional i64 settle_amt,   //结算金额
    2: optional i64 fee,          //手续费收益  
    3: optional i64 month_fee,    //月服务费
    4: optional i64 fixed_amt,    //固定金额扣款
    5: optional i64 chnl_amt,     //渠道分润金额
    7: optional i64 transfer_date //到账日期
    8: required i32 chnlid,        //到账通道
    9: optional string memo,       //备注
    10: required string bat_id="0",    //批次号
}

service TransFerService {
    //ping
	string ping(),

    //生成指定的出款记录(异步生成,调用后会立刻返回结果)
    oneway void hand_settle_records(1:required string rule,2:required string txcurrcd),

    //异步获取可以出款的总数，以及总金额(调用后会立刻返回成功或者失败,然后异步去算多少出款信息)
    oneway void get_can_transfer(1:required string txcurrcd),

    //获取可提现的 出款信息
    oneway void get_withdraw_info(),
    //生成可提现的出款记录
    oneway void gen_withdraw_record(1:required string rule),

    //审核通过进行出款
    oneway void transferinfo(1:string bat_id),
    //生成相对应的出款表
    oneway void generate_record_excel(1:string bat_id),

    //退票接口,更新出款接口中对应的退票批次id()
    string bankrefund(1:list<BankrefundRet> params),
    //退票拒绝
    i64 refusereturn(1:required string bat_id,2:required string type),
    //审核通过后真正的退票
    i64 allowreturn(1:required string bat_id)

    //获取各个出款通道的用户留存金额
    list<TransFerChnl> get_transfer_chnl(),
    //更改指定用户的出款通道
    i32 set_users_chnl(1:list<UsersChnlInfo> params),
    //拒绝接口(type active代表是主动拒绝 的    passive代表审核 拒绝的)
    i32 verify_chnl(1:required string bat_id,2:required string type),
    
    //生成变更留存金额记录
    i32 set_capitalchange_record(1:Capitalchangeret params),
    //提供给审核的留存金额变更
    i32 verify_capitalchange(1:required string bat_id,2:required string type),

    //补款添加纪录
    i32 add_supplement_record(1:required i64 userid, 2:required i64 amt, 3:required string reason),
    //补款提审
    i32 supplement_apply(1:required i64 bat_id),
    //补款提审通过
    i32 supplement_audit(1:required i64 bat_id),
    //补款提审失败
    i32 supplement_audit_refuse(1:required i64 bat_id),

    // 调用代付出款
    oneway void paytransfer(1:required i64 bat_id),
    // 生成代付文件
    oneway void generate_payanother_excel(1:string bat_id),
}
