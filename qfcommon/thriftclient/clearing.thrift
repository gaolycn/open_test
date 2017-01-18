namespace py clearing

struct ClearingParams
{
	1: optional i64 chnl_id,               #结算通道id,如果为空,则结算所有可结算通道
	2: optional string check_date,         #对账日期,默认结算此通道下所有可结算数据
	3: optional i64 check_bat_id,          #对账的批次, 默认最大的批次
}

struct ClearingRet
{
	1:i64 chnl_id,              #通道id
	2:string check_date,        #结算的对账日期
	3:string retcode,           #该结算是否能执行
	4:string errmsg,            #错误信息
}

service Clearing
{	
	#根据通道来结算
	list<ClearingRet> clearing_by_channel(1:list<ClearingParams> params)
}
