
include "notify.thrift"

namespace py paycell_coupon_pay



service PayCellCouponPay
{
    i16 ping();

    // 同步调用分享
    // 参数是所有的交易数据
    // 处理正扫与扫二维码
    // 返回分享的链接
    string activity_share(1:string req_data) throws(1:notify.ServerException e);

    // 异步调用交易接口
    // 参数是所有的交易数据
    // 只处理反扫
    i32 subscribe(1:string req_data) throws(1:notify.ServerException e);
}


