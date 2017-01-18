namespace py FundSuspend

//通用返回
struct FundSuspendReturn{
    1: required string respcd,
    2: required string respmsg,
}

service FundSuspendService {
    //ping
	FundSuspendReturn ping(),
    
    //生成延迟纪录  ----->参数 txcurrcd 币种  hand_type 操作类型(1 延迟 2释放延迟) src(1 账务  2风控)
    oneway void gen_suspend_records(1:required string txcurrcd,2:required i16 hand_type, 3:required i16 src),

    //生成延迟纪录  ----->参数 txcurrcd 币种  hand_type 操作类型(1 延迟 2释放延迟) userids(用户id串)
    oneway void add_suspend_records(1:required string txcurrcd,2:required i16 hand_type, 3:required string userids),

    //审核操作延迟纪录
    FundSuspendReturn audit_suspend_records(1:required i64 batid,2:required i16 hand_state),

}
