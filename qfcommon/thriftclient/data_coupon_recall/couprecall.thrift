namespace java com.qfpay.service
namespace py couprecall

/*
* 红包召回推广接口
*/

service couprecall {

    //获取红包召回数据汇总：参数 userid:商户id，返回红包召回汇总列表包括商户id、老消费者数、召回数、交易笔数、金额
    string couprec(1:string userid)

    //获取推广数据汇总：参数 userid:商户id，返回商户id、消费者数、交易笔数
    string coupspr(1:string userid)
}


/*
*
* 红包召回返回列表说明
*[{"tx_cnt": 248, "tx_amt": 1835740, "user_id": "338758", "actv_id": "6136174405511547920","c30_cnt": 248, "recall_cnt": 248},{"tx_cnt": 11, "tx_amt": 65101, "user_id": "96418788", "actv_id": "6153798049985206880","c30_cnt": 11, "recall_cnt": 11}]
* 推广活动效果返回列表说明
*[{"tx_cnt": 6, "cstm_cnt": 4, "actv_id": "6142196577761759864","user_id": "1283794", "tx_amt": 560},{"tx_cnt": 243, "cstm_cnt": 139, "actv_id": "6133518890977462743","user_id": "1491630", "tx_amt": 352400},{"tx_cnt": 44, "cstm_cnt": 18, "actv_id": "6135366272769854249","user_id": "1541782", "tx_amt": 2725725}]
*/
