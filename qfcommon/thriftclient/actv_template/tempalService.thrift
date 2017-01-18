namespace java com.qfpay.service
namespace py tempalService

/*
* 商户红包模板信息查询接口
*/

service tempalService {

    //获取商户红包模板列表：参数 userid:商户id  返回商户红包模板
    string tempal(1:string userid)
}

/*
*
* 商户红包模板返回列表说明
*[{"p50_tx_amt": 1000, "user_id": "1333989", "use_amt": 900, "vperiod": 13, "var_p": 50, "recharge_rate": 53, "max_tx_amt": 11200, "p75_tx_amt": 1400, "min_tx_amt": 300, "datain_date": "2016-06-02", "day_get_cnt": 5, "coupon_amt": 100, "get_amt": 800, "p25_tx_amt": 800}]
*
*/
