namespace java com.qfpay.service
namespace py activiquer

/*
* 活动数据接口
*/

service activiquer {

    //获取活动数据：参数 index: 活动索引，query: 查找排序
    string activiq(1:string index, 2:string query)

}


/*
*
* 中秋活动榜单参数说明，中秋节活动索引 index=actzqj；按人气值从大到小排序榜单query=pop；按潜力值从大到小排序榜单query=pot
* activiq(actzqj,pop) 返回按人气值从大到小排序榜单 ； activiq(actzqj,pot) 返回按潜力值从大到小排序榜单
* 返回列表说明
* [{"b4_cnt": 0, "tm_cnt": 0, "mobile": "13711547136", "aft_cnt": 256, "pop_value": 740, "userid": "1495199", "hb_cnt": 74, "b4_days": 0, "datain_date": "2016-09-08", "nickname": "喜洋洋便利店2198分店", "aft_days": 7, "potential_value": 0},{"b4_cnt": 0, "tm_cnt": 0, "mobile": "18255312537", "aft_cnt": 86, "pop_value": 240, "userid": "1552051", "hb_cnt": 24, "b4_days": 0, "datain_date": "2016-09-08", "nickname": "风客网咖云顶店", "aft_days": 7, "potential_value": 0}]
*
*/
