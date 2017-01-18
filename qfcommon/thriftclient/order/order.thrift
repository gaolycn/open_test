namespace py order
//异常定义
exception ServerException{
    1: string respcd,
    2: string respmsg,

}
//通用返回
struct ReturnMsg{
    1: string respcd,
    2: string respmsg,

}
//商品库相关
struct GoodsArgs{
    1: optional string mchnt_id,    //商户id
    2: optional string goodsid,     //商品id
    3: optional string menuid,         //菜单id
    4: optional string menutype,       //菜单类型  0一级菜单
    5: optional i32 page=1,
    6: optional i32 maxnum=20,
}
struct GoodsInfo{
    1: optional string goodsid,      //商品id
    2: optional string goodsname,    //商品名称
    3: optional i64 goodsprice,      //商品价格
    4: optional i64 goodscnt,        //商品个数
    5: optional string menuid,          //菜单id
    6: optional string menuname,     //菜单名称
    7: optional string menutype,        //菜单类型
    8: optional string picaddr,      //商品图片地址
    9: optional string unionid,     //关联id
    10: optional string goodsinfo,  //商品详情
    11: optional string descr, //商品描述
    12: optional string goodsspec, // 商品规格
    13: optional string mchnt_id,
    14: optional i16 weight,      //权重
    15: optional i64 goodsorgprice, //商品原价格
}
struct MenuInfo{
    1: optional string menuid,       //菜单id
    2: optional string descr,        //菜单描述
    3: optional string menuname,            //菜单名称
    4: optional string mchnt_id,
    5: optional i16 weight,       //权重
}

struct GoodsRet{
    1: list<GoodsInfo> goods_list, 
    2: i64 cnt,
}
//订单相关
struct OrderPayInfo{
    1: required i64 order_id,     //订单号
    2: optional i64 pay_sn,       //支付流水号 
    3: required i64 pay_amt,         //支付金额
    4: required i32 pay_type,        //支付类型
    5: required string pay_chnl,     //支付通道
    6: optional i16 pay_state,       //支付状态
    7: optional string chnl_sn,      //通道流水号
    8: optional i64 pay_time,        //支付时间
    9: optional string txcurrcd,    //币种
    10: optional string pay_ret,     //支付结果
    11: optional string chnl_retcd,  //通道返回码
    12: optional i64 amt,         //订单金额(针对于支付拆分)
}
struct OrderAddress{
    1: optional string detail_address,
    2: optional string phone,
}
struct OrderDetail{
    1: optional i64 order_id,
    2: optional OrderAddress addr,
    3: optional list<GoodsInfo> goodsinfo,

}
struct OrderInfo{
    1: required string mchnt_id,             //商户id
    2: required string customer_id,          //消费者id
    3: required string source,               //来源
    4: optional list<GoodsInfo> goodsinfo,    //商品信息 
    5: optional OrderAddress addr,          //订单配送地址
    6: required i64 amt,                     //应该支付金额
    7: required string busicd,               //交易类型
    8: required i16 order_type,               //订单类型
    9: optional i16 state,                   //订单状态 
    10: optional string note,                 //备注 
    11: optional string open_id,             //第三方商户号
    12: optional string order_name,          //订单名称
    13: optional i16 print_state,         //打印状态
    14: optional i64 order_id,               //订单id
    15: optional string order_sn,             //流水号
    16: optional i64 ctime,                   //创建时间
    17: optional string appid,
    18: optional i32 shipping_fee,          // 运费
    19: optional i64 addr_id               // 外卖关联的地址id
}

struct OrderArgs{
    1: optional string mchnt_id,          //商户id
    2: optional i64 order_id,          //订单id
    3: optional string customer_id,       //消费者id
    4: optional string source,            //订单来源
    5: optional i16 state,                //订单状态
    6: optional i16 order_type,           //订单状态
    7: optional i64 start_time,           //开始时间
    9: optional i64 end_time,             //结束时间
    10: optional i32 page =1,        
    11: optional i64 maxnum = 15,
}
struct OrderRet{
    1: list<OrderInfo> orderinfo,
    2: i64 cnt,
}
service Order{
    //ping
    string ping();
    //查询商品库信息
    list<GoodsInfo> findGoodsInfo(1:GoodsArgs goodquery) throws(1:ServerException e),
    //查询商品菜单信息
    list<MenuInfo> findMenuInfo(1:GoodsArgs goodquery) throws(1:ServerException e),
    //订单创建
    ReturnMsg addOrder(1:OrderInfo orderinfo) throws(1:ServerException e),
    //订单支付信息创建
    ReturnMsg addOrderPay(1:list<OrderPayInfo> orderpay) throws(1:ServerException e),
    //订单查询
    OrderRet findOrder(1:OrderArgs orderargs) throws(1:ServerException e),
    //订单支付信息查询
    list<OrderPayInfo> findOrderPay(1:required list<i64> order_ids) throws(1:ServerException e),
    //订单详细信息查询
    list<OrderDetail> findOrderDetail(1:required list<i64> order_ids) throws(1:ServerException e),
    //订单支付回调
    ReturnMsg payOrderBack(1:required list<OrderPayInfo> orderpay) throws(1:ServerException e),
    //订单退款
    ReturnMsg payOrderRefund(1:OrderPayInfo orderpay) throws(1:ServerException e),
    //订单关闭
    ReturnMsg payOrderClose(1:required i64 order_id) throws(1:ServerException e),
    //更新订单打印状态
    ReturnMsg printOrder(1:required i64 order_id,2:required i16 state) throws(1:ServerException e),
}
