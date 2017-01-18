namespace py qf_marketing


// 发生错误时的返回码及其对应的描述信息
exception ServerError
{
    1: string code, // 返回码
    2: string msg,  // 描述信息
}

// 分享信息
struct Share
{
    1: string share_url = '',   // 分享的url
    2: string title     = '',   // 分享的标题
    3: string icon_url  = '',   // 分享的图标url
    4: string desc      = '',   // 分享的描述
}

// 红包领取页面配置信息
// app_logo与bgimg是保留字段,暂时留空
struct ObtainPage
{
    1: string title      = '',  // 领取页面的标题
    2: string content    = '',  // 领取页面的内容
    3: string return_url = '',  // 领取页面的回调url
    4: string app_logo   = '',  // 领取页面的app的logo的url
    5: string bgimg      = '',  // 领取页面的背景图片url
    6: string usage      = '',  // 使用说明
    7: string ext        = '',  // 其他信息, json格式字符串
}

// 活动的扩展字段保存信息
struct ActivityExt
{
    1: Share      share,    // 活动分享的信息
    2: ObtainPage page,     // 红包领取页面配置信息
}

// 活动信息 定义红包的发放规则
struct Activity
{
    1:  i64         id,
    2:  string      src,                 // 来源
    3:  string      mchnt_id,            // 商户id
    4:  i16         type,                // 活动类型 1:满减 2:消费返券/分享券 3: 分发活动 4: 兑换活动 11:积分
    5:  string      title,               // 活动标题
    6:  i64         total_amt,           // 活动总金额(预算)
    7:  i16         xx_type,             // 活动的分享类型 1:红包  2:积分
    8:  i32         obtain_num,          // 活动分享的xx_type的数量
    9:  i64         obtain_xx_id,        // 活动领取的xx_type的id
    10: i32         sponsor_award_num,   // 活动奖励分享人的xx_type的数量
    11: i64         sponsor_xx_id,       // 活动奖励分享人的xx_type的id
    12: string      rule,                // 活动规则 {'obtain_rule': [['amt', '>=', 10], ['begin_time', '>=', 0], ['end_time', '<=', 86400], ['num_type', '=', 1], ['obtain_num', '<', '10']], 'share': [['amt', '>=', 10], ['num_type', '=', 1], ['share_num', '<', 10], ['begin_time', '>=', 0], ['end_time', '<=', 86400]]}
    13: string      return_url,          // 活动回调的url
    14: ActivityExt ext,                 // 活动扩展信息
    15: string      content,             // 活动描述信息
    16: i32         used_num,            // 活动已领取的数量
    17: i32         used_amt,            // 活动已领取的金额
    18: i16         status,              // 活动状态
    19: i32         start_time,          // 有效期的开始时间
    20: i32         expire_time,         // 有效期的结束时间

}

// 商户信息
struct Merchant
{
    1:  i64    id        = 0;       //用户唯一id
    2:  string name      = '';      //用户名称
    3:  string shopname  = '';      //店铺名称
    4:  string email     = '';      //用户的email
    5:  string mobile    = '';      //手机号码
    6:  string telephone = '';      //座机电话
    7:  i32    state;               //状态
    8:  string province;            //所在省份
    9:  string city;                //所在城市
    10: string mcc;                 //商户mcc
    11: string address;             //商户地址
    12: double longitude = 0.0;     //商户gps经度
    13: double latitude  = 0.0;     //商户gps维度
    14: string jointime;            //用户创建时间，为"YYYY-MM-DD HH:SS:mm"
}

// 红包信息
struct Coupon
{
    1:  i64      id,            // 红包id
    2:  string   src,           // 来源
    3:  string   mchnt_id,      // 商户id
    4:  string   title,         // 标题
    5:  i16      type,          // 红包类型
    6:  i32      amt,           // 红包金额
    7:  string   code,          // 红包码
    8:  i16      status,        // 状态
    9:  string   use_rule,      // 使用规则
    10: string   content,       // 内容
    11: i32      start_time,    // 红包有效期的开始时间
    12: i32      expire_time,   // 红包有效期的结束时间
    13: Merchant mchnt,         // 如果mchnt_id存在(单店红包)，则获取mchnt信息
}

// 活动分享返回信息
struct ActivityShare
{
    1: Share        share;      // 分享的信息
    2: list<Coupon> coupons;    // 分享时奖励的红包信息
    3: ObtainPage   page;       // 红包领取页面配置信息
    4: i32          integral;   // 奖励的积分数
    5: i64          id = 0;     // 本次分享的id, 如果id为0，则share也必不存在
}

// 活动或分享统计
struct ActivityStat
{
    1: i32 obtain_num,  // 领取数量(活动或分享)
    2: i32 obtain_amt,  // 领取金额(活动或分享)
    3: i32 award_num,   // 奖励数量(活动或分享)
    4: i32 award_amt,   // 奖励金额(活动或分享)
    5: i32 use_num,     // 核销数量(活动或分享)
    6: i32 use_amt,     // 核销金额(活动或分享)
    7: i32 total_amt,   // 活动总预算
    8: list<i64> share_ids, // 活动分享的列表 
    9: i64 trade_amt,   // 交易总金额
}

// 红包使用规则的扩展属性
struct CouponRuleProfile
{
    1: i16 mchnt_limit   = 1,   // 红包使用商户限制类型  1: 随活动限制   2: 领取的商户与使用的商户一致
    2: i16 effect_type   = 1,   // 有效期的限制类型  
                                //   1: 固定有效期,与使用规则有效期一致 忽略effect_offset 与 effect_len
                                //   2: 动态的有效期 [curr_date + effect_offset,  curr_date + effect_offset + effect_len]
                                //      动态的有效期忽略使用规则的开始时间与结束时间
    3: i32 effect_offset = 1,   // 有效期的偏移(单位: 天) value >= 0   0: 立刻生效
    4: i32 effect_len    = 7,   // 持续时间(单位:天) value > 0
}

// 红包使用规则
struct CouponRule
{
    1:  i64     id,                 // 红包规则id
    2:  string  src,                // 来源
    3:  string  mchnt_id,           // 商户id
    4:  string  title,              // 红包规则标题
    5:  i64     amt_max,            // 生成红包的最大金额
    6:  i64     amt_min,            // 生成红包的最小金额
    7:  string  use_rule,           // 红包使用规则
    8:  string  content,            // 红包使用规则的描述
    9:  i16     status,             // 红包使用规则的状态
    10: i32     start_time,         // 有效期的开始时间
    11: i32     expire_time,        // 有效期的结束时间
    12: CouponRuleProfile profile,  // 红包使用规则的扩展属性
}

// 红包记录信息
struct CouponRecord
{
    1:  i64     id,             // 记录id
    2:  string  src,            // 来源
    3:  string  mchnt_id,       // 商户id
    4:  string  customer_id,    // 消费者id
    5:  string  out_sn,         // 外部唯一标识
    6:  string  orig_out_sn,    // 原交易的唯一标识
    7:  string  coupon_code,    // 红包唯一码
    8:  i32     coupon_amt,     // 红包金额
    9:  i16     type,           // 记录类型
    10: string  content,        // 备注
    11: i32     create_time,    // 记录创建时间
}

// 查询活动的参数
struct ActivityQueryArgs
{
    1: required string src,         // 来源，必填
    2: optional string mchnt_id,    // 商户id,  选填，如果为空，则查询来源创建的活动，否则查询指定商户创建的活动
    3: optional i64    activity_id, // 活动id,  选填，如果不为空，则查询指定的活动
    4: optional i32    pos   = 0,   // 查询的位置, <0, 则0
    5: optional i32    count = 20,  // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
    6: optional i16    type  = -1,  // 活动类型 1. 满减 2. 消费返券/消费分享券 3. 分发活动 4. 兑换活动 11. 消费返积分,  选填，>0，则查询指定的活动
    7: optional list<i16> status_list,          // 活动状态 1. 未生效 2. 正在进行的 3. 已结束,  选填，为空，则查询所有
    8: optional string apply_mchnt_id = '',     // 商户可以参加的活动
}

// 活动分享的参数
struct ActivityShareArgs
{
    1: required string src,         // 来源，必填
    2: required string customer_id, // 分享人
    3: required i32    trade_amt,   // 交易金额
    4: optional string mchnt_id,    // 商户id,  选填，如果为空，则分享来源创建的活动
                                    // 否则查询指定商户创建的活动或来源创建的，该商户可用的活动
    5: optional i16    type,        // 分享的红包类型 1. 满减  2. 消费返券/消费分享券
    6: optional i16    award_status;// 活动奖励的状态, 1: 领取(相当于未激活) 2: 绑定(相当于已激活)
    7: optional string out_sn = ''; // 交易生成分享时，交易流水号
}

// 活动统计的参数
struct ActivityStatArgs
{
    1: required string src,         // 来源，必填
    2: optional i64    activity_id, // 统计的活动id
    3: optional i64    share_id,    // 统计的分享id，活动id与分享id至少存在一个
    4: optional i32    start_time,  // 统计的活动的起始时间，默认为0
    5: optional i32    end_time,    // 统计活动的结束时间，默认为当前时间
    6: optional list<i64> activity_ids, // 批量统计活动的活动id列表, 与activity_id互斥
}

// 查询活动的参数
struct CouponRuleQueryArgs
{
    1: required string src,         // 来源，必填
    2: optional string mchnt_id,    // 商户id,  选填，如果为空，则查询来源创建的活动，否则查询指定商户创建的活动
    3: optional i64    rule_id,     // 规则id,  选填，如果不为空，则查询指定的红包使用规则
    4: optional i32    pos   = 0,   // 查询的位置, <0, 则为0
    5: optional i32    count = 20,  // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
}

// 使用或回滚红包参数
struct CouponOperateArgs
{
    1:  required string src,            // 来源
    2:  required string coupon_code,    // 红包的唯一标识
    3:  required i16    type,           // 红包操作类型 1: 领取  2: 绑定  3: 使用  4: 还原  5: 作废
    4:  optional string out_sn,         // 交易唯一标识
    5:  optional string orig_out_sn,    // 原始交易唯一标识
    6:  optional string mchnt_id,       // 商户id, 使用红包的商户的id
    7:  optional string customer_id,    // 消费者id
    8:  optional i32    trade_amt,      // 交易金额
    9:  optional string content,        // 操作说明
    10: optional i32    coupon_amt = -1,// 红包金额，如果提供，则验证金额是否正确, 如果小于0，则不验证
}

// 消费者领取红包的参数
struct CouponObtainArgs
{
    1: required string  src,            // 来源
    2: required string  customer_id,    // 消费者id
    3: required string  code,           // 红包领取码
    4: optional i16     status,         // 领取红包时，红包的状态 1: 领取  2: 绑定, 默认是领取
}

// 分发红包的参数
// 分发时，红包状态一定是绑定
struct CouponDispatchArgs
{
    1: required string       src,           // 来源
    2: required list<string> customer_list, // 消费者id
    3: required i64          activity_id,   // 活动id
    4: optional i16          num = 1,       // 发放数量，默认为1
    5: optional string       mchnt_id = '', // 商户id
                                            //     如果存在，则为商户自己给消费者发放红包
                                            //               那活动必须是商户自己创建的单店红包活动
                                            //     如果不存在，则为平台创建的活动，那活动必须发放平台活动
}

// 红包分发结果
struct DispatchResp
{
    1: string customer_id,  // 红包分发失败的消费者id
    2: i16    num,          // 消费者已发放的数量 
                            // 如果需要给消费者发10张，但只发了2张，剩下8张失败了，则这里显示出已发放的数量
                            // 所以这里大部分情况都为0
}

// 查询消费者红包的参数
struct CouponQueryArgs
{
    1:  required string    src,             // 来源
    2:  required string    customer_id,     // 消费者id
    3:  optional list<i16> type_list,       // 查询类型 1: 领取  2: 绑定  3: 使用  4: 作废, 如果查所有，则为空
    4:  optional i32       start_time,      // 查询红包的起始时间，默认为0
    5:  optional i32       end_time,        // 查询红包的结束时间，默认为当前时间
    6:  optional i32       pos   = 0,       // 查询的位置, <0, 则为0
    7:  optional i32       count = 20,      // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
    8:  optional i32       trade_amt,       // 交易金额，如果提供，则验证查询出来的红包的使用金额是否大于交易金额
    9:  optional i16       status = 0xFF,   // 查询红包的状态. 0x01: 生效  0x02: 过期  0x04: 未生效
    10: optional string    mchnt_id,        // 商户id 如果存在，则查询该店铺下和平台下的红包，否则返回所有的红包
}

// 查询红包核销记录的参数
struct CouponUseRecordArgs
{
    1: required string src,         // 来源，必填, 多个来源，以','分隔, 如果为空串，则查询所有的
    2: optional string mchnt_id,    // 商户id,  选填，如果为空，则查询来源创建的活动，否则查询指定商户创建的活动
    3: optional i64    rule_id,     // 规则id,  选填，如果不为空，则查询指定的红包使用规则
    4: optional i32    start_time,  // 查询红包核销的开始时间
    5: optional i32    end_time,    // 查询红包核销的结束时间
    6: required i32    pos   = 0,   // 查询的位置, <0, 则为0
    7: required i32    count = 20,  // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
}

// 活动申请参数
struct ActivityApply
{
    1: required string       src,           // 来源，必填
    2: required list<string> mchnt_list,    // 添加该活动的商户
    3: required i64          activity_id,   // 活动id, 报名添加的活动id
    4: required i16          op_type,       // 报名操作的类型，1: 添加  2: 删除
    5: optional string       content,       // 备注
}

// 积分规则
struct IntegralRule
{
    1:  i64     id,                 // 积分规则id
    2:  string  src,                // 来源
    3:  string  title,              // 规则标题
    4:  i64     trade_exchange,     // 交易金额多少钱兑换一积分
    5:  i64     integral_exchange,  // 多少积分兑换一分钱
    6:  string  content,            // 规则的描述
    7:  i16     status = 1,         // 规则的状态 1: 创建  2: 启用  3: 关闭
    8:  i32     start_time,         // 有效期的开始时间
    9:  i32     expire_time,        // 有效期的结束时间
}

// 积分规则查询参数 
struct IntegralRuleQueryArgs
{
    1: required string src,             // 来源，必填
    2: optional i64    rule_id  = 0,    // 规则id, 选填，如果不为空，则查询指定的红包使用规则
    3: optional i32    pos   = 0,       // 查询的位置, <0, 则为0
    4: optional i32    count = 20,      // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
}

// 交易积分兑换
struct IntegralExchange
{
    1:  required string src,            // 来源
    2:  required string customer_id,    // 消费者id
    3:  required string out_sn,         // 交易唯一标识
    4:  required i16    type,           // 操作类型  1: 交易兑换积分  2: 积分兑换交易金额
    5:  optional i32    trade_amt,      // 支付金额
    6:  optional i32    integral,       // 兑换积分
    7:  optional string mchnt_id,       // 商户id
    8:  optional string orig_out_sn,    // 原始交易唯一标识
    9:  optional string content,        // 操作说明
    10: optional i64    total_amt = 0,  // 交易总金额
}

// 积分兑换的基本信息
struct BIntegralExchange
{
    1:  required string src,            // 来源
    2:  required string customer_id,    // 消费者id
    3:  required i32    integral,       // 兑换的积分
    4:  required string out_sn   = '',  // 交易唯一标识
    5:  optional string mchnt_id = '',  // 商户id
    6:  optional string content  = '',  // 操作说明
}

// 积分兑换红包
struct IntegralCoupon
{
    1: BIntegralExchange base,      // 积分兑换的基本信息
    2: required i64 activity_id,    // 兑换的红包的活动id
    3: required i16 status   = 2,   // 红包的状态, 1: 领取  2: 绑定
}

// 积分兑换交易结果
struct ExchangeResp
{
    1: string   src,                // 来源
    2: string   customer_id,        // 消费者id
    3: i16      type,               // 操作类型 1: 交易兑换积分  2: 积分兑换交易金额
    4: i32      integral,           // 兑换的积分
    5: i32      amt,                // 对于交易兑换积分，则为交易的金额 对于积分兑换交易金额，则为兑换的金额
    6: i64      trade_exchange,     // 使用的积分兑换规则, 交易金额多少钱兑换一积分
    7: i64      integral_exchange,  // 使用的积分兑换规则, 多少积分兑换一分钱
    8: i32      curr_integral,      // 兑换后, 消费者现在的积分
}

// 积分兑换返值的基本信息
struct BExchangeResp
{
    1: string   src,                // 来源
    2: string   customer_id,        // 消费者id
    3: i32      integral,           // 兑换的积分
    4: i32      curr_integral,      // 兑换后, 消费者现在的积分
}

// 积分兑换红包的信息
struct CouponExchangeResp
{
    1: BExchangeResp base,
    2: i64           activity_id,   // 兑换的规则
    3: Coupon        coupon,        // 兑换的红包信息
}

// 消费者营销信息查询参数
struct ProfileQueryArgs
{
    1: required string    src,              // 来源
    2: required string    customer_id,      // 消费者id
    3: optional list<i16> type_list,        // 查询类型  1: 红包  2: 积分  3: 余额, 默认查询所有的
    4: optional list<i16> status,           // 查询红包状态  
                                            // 1: 领取  2: 绑定  3: 使用  4: 作废, 如果查所有，则为空
}

// 消费者积分信息
struct Integral
{
    1: i64 integral,            // 消费者当前积分
    2: i64 integral_exchange,   // 积分兑换交易金额
    3: i64 trade_exchange,      // 交易兑换积分
}

// 消费者信息
struct Profile
{
    1: string       src,            // 来源
    2: string       customer_id,    // 消费者id
    3: Integral     integral,       // 消费者积分信息
    4: i64          balance = 0,    // 余额
    5: list<Coupon> coupon,         // 消费者红包信息
}

// 消费者营销记录查询参数
struct RecordQueryArgs
{
    1: required string    src,              // 来源
    2: required string    customer_id,      // 消费者id
    3: optional list<i16> type_list,        // 查询类型  1: 红包  2: 积分  3: 余额
    4: optional list<i16> status,           // 查询状态  0: 领取  1: 使用  2: 还原  3: 作废, 如果查所有，则为空
    5: optional i32       pos   = 0,        // 查询的位置, <0, 则为0
    6: optional i32       count = 20,       // 查询的个数, <=0, 则查从0开始的所有的数据, 忽略pos
}

// 消费者营销记录查询信息
// FIXME: 需要加商户信息
struct CustomerRecord
{
    1:  i64     id,             // 记录id
    2:  string  src,            // 来源
    3:  string  mchnt_id,       // 商户id
    4:  string  customer_id,    // 消费者id
    5:  string  out_sn,         // 外部唯一标识
    6:  string  orig_out_sn,    // 原交易的唯一标识
    7:  i16     xx_type,        // 类型，1: 优惠券 2: 积分
    8:  i32     amt,            // 优惠券金额/积分兑换金额
    9:  i32     num,            // 使用的数量，优惠券则使用为1，积分则使用的数量
    10: i32     curr_num,       // 积分与余额使用，当前的积分或余额
    11: i16     type,           // 记录类型 0: 领取  1:使用红包/积分  2:还原红包/积分  3:作废红包
    12: string  content,        // 备注
    13: i32     create_time,    // 记录创建时间
}

// 红包活动营销案例
struct CouponStory
{
    1:  i64     id,                     // id
    2:  string  src = 'QPOS',           // 来源
    3:  i64     activity_id,            // 活动id
    4:  string  mchnt_id,               // 商户id，单店活动不为空
    5:  i32     obtain_num = 0,         // 活动领取数量
    6:  i32     use_num = 0,            // 活动使用数量
    7:  i32     use_per = 0,            // 使用率, 单位:万分之n
    8:  i32     avg_spend = 0,          // 人均消费, 单位:分
    9:  i64     coupon_trade_amt = 0,   // 红包交易的总交易金额
    10: i32     coupon_amt_per = 0,     // 红包金额占交易金额的百分比，红包金额/人均消费, 单位:万分之n
    11: string  industry = ''           // 所属行业
    12: i16     type   = 1,             // 红包活动营销案例类型，1: 成功案例 2: 失败案例
    13: i16     status = 2,             // 状态: 1. 创建  2. 启用  3. 关闭
}

// 查询红包活动营销案例参数
struct StoryQueryArgs
{
    1: i32    coupon_amt_per,   // 红包金额占交易金额的百分比，红包金额/人均消费, 单位:万分之n
    2: string industry,         // 所属行业
    3: i16    type  = 1,        // 红包活动营销案例类型，1: 成功案例 2: 失败案例
    4: i16    mode  = 2,        // 查询的营销案例的查询方式，1: 顺序 2: 随机
    5: i32    pos   = 0,        // 查询的位置
    6: i32    count = 20,       // 查询的数量, 最大不超过200, 如果为-1，则为2000
}



// 执行请求时，如果发生任何错误都已异常返回
service QFMarketing
{
    i64 ping() throws(1:ServerError e);
    // ================活动相关接口================

    // 创建活动
    // 返回值: activity_id
    i64 activity_create(1:Activity activity) throws(1:ServerError e);
     
    // 修改活动
    // 返回值: 0: 成功
    i32 activity_change(1:Activity activity) throws(1:ServerError e);
     
    // 查询活动
    list<Activity> activity_query(1:ActivityQueryArgs query) throws(1:ServerError e);
     
    // 分享活动(消费活动与满减活动)
    ActivityShare activity_share(1:ActivityShareArgs share) throws(1:ServerError e);
     
    // 活动统计
    // src:         来源,  必填
    // activity_id: 统计的活动id
    // share_id   : 统计的活动分享id，与activity_id只需存在一个，若都存在，则优先使用activity_id
    // start_time : 统计的活动的起始时间，默认为0
    // end_time   : 统计活动的结束时间，默认为当前时间
    ActivityStat activity_stat(1:ActivityStatArgs stat) throws(1:ServerError e);

    // 批量活动统计
    // src:         来源,  必填
    // activity_id: 统计的活动id
    // share_id   : 统计的活动分享id，与activity_id只需存在一个，若都存在，则优先使用activity_id
    // start_time : 统计的活动的起始时间，默认为0
    // end_time   : 统计活动的结束时间，默认为当前时间
    // 返回值为字典，每个活动对应一个统计结果
    map<i64, ActivityStat> activitys_stat(1:ActivityStatArgs stat) throws(1:ServerError e);

    // 申请活动
    // 返回值: 0: 成功
    i32 activity_apply(1:ActivityApply apply) throws(1:ServerError e);

    // 查询可分享的活动
    // 返回值: 可分享的活动
    Activity activity_shareable(1:ActivityShareArgs req_args) throws(1:ServerError e);


    // ================红包使用规则相关接口================
    
    // 创建红包使用规则
    // 返回值: coupon_rule_id
    i64 coupon_rule_create(1:CouponRule coupon_rule) throws(1:ServerError e);
     
    // 修改红包使用规则
    // 返回值: 0: 成功
    i32 coupon_rule_change(1:CouponRule coupon_rule) throws(1:ServerError e);
     
    // 查询红包使用规则
    list<CouponRule> coupon_rule_query(1:CouponRuleQueryArgs query) throws(1:ServerError e);


    // ================红包相关接口================
     
    // 绑定红包
    // 返回值: 0: 成功
    i32 coupon_bind(1:CouponOperateArgs bind_args) throws(1:ServerError e);

    // 使用红包
    // 返回值: 0: 成功
    i32 coupon_use(1:CouponOperateArgs use_args) throws(1:ServerError e);

    // 红包使用验证
    // 返回值: True: 成功 False: 失败
    bool coupon_verify(1:CouponOperateArgs verify_args) throws(1:ServerError e);

    // 红包使用回滚
    // 返回值: 0: 成功
    i32 coupon_rollback(1:CouponOperateArgs rollback_args) throws(1:ServerError e);

    // 领取红包
    Coupon coupon_obtain(1:CouponObtainArgs obtain_args) throws(1:ServerError e);

    // 查询消费者的红包
    list<Coupon> coupon_query(1:CouponQueryArgs query_args) throws(1:ServerError e);

    // 分发红包
    // 返回结果，分发失败的消费者id
    list<DispatchResp> coupon_dispatch(1:CouponDispatchArgs dispatch_args) throws(1:ServerError e);

    // 可以使用红包的商户
    list<Merchant> coupon_mchnt(1:string src, 2:string coupon_code) throws(1:ServerError e);

    // ================积分规则相关接口================

    // 创建红包使用规则
    // 返回值: integral_rule_id
    i64 integral_rule_create(1:IntegralRule param) throws(1:ServerError e);
     
    // 修改红包使用规则
    // 返回值: 0: 成功
    i32 integral_rule_change(1:IntegralRule param) throws(1:ServerError e);
     
    // 查询红包使用规则
    list<IntegralRule> integral_rule_query(1:IntegralRuleQueryArgs query) throws(1:ServerError e);

    // ================积分兑换相关接口================

    // 积分兑换
    // 返回值: 兑换结果，如果交易兑换积分，则返回兑换积分数
    //         如果积分抵金额，则返回抵的金额
    ExchangeResp integral_exchange(1:IntegralExchange exchange_args) throws(1:ServerError e);

    // 积分回滚
    // 返回值: 兑换结果，如果交易兑换积分，则返回兑换积分数
    //         如果积分抵金额，则返回抵的金额
    ExchangeResp integral_rollback(1:IntegralExchange exchange_args) throws(1:ServerError e);

    // 积分兑换红包
    CouponExchangeResp integral2coupon(1:IntegralCoupon req_args) throws(1:ServerError e);

    // ================消费者相关接口================

    // 消费者营销信息查询
    Profile customer_info(1:ProfileQueryArgs param) throws(1:ServerError e);

    // 消费者营销领取,使用...记录
    list<CustomerRecord> customer_record(1:RecordQueryArgs param) throws(1:ServerError e);

    // ================记录相关接口================
     
    // 红包核销记录查询
    // 数据库中的mchnt_id标识使用红包的店铺
    list<CouponRecord> coupon_use_record_query(1:CouponUseRecordArgs verify) throws(1:ServerError e);

    // 红包核销记录查询
    // 数据库中的mchnt_id标识平台红包或店铺红包
    list<CouponRecord> coupon_use_record_query_v2(1:CouponUseRecordArgs verify) throws(1:ServerError e);

    // 红包核销记录总数
    i32 coupon_use_record_count(1:CouponUseRecordArgs verify) throws(1:ServerError e);

    // 红包核销记录总数
    i32 coupon_use_record_count_v2(1:CouponUseRecordArgs verify) throws(1:ServerError e);


    // ================营销成功案例相关接口================
    
    // 创建成功案例
    list<i64> story_create(1:list<CouponStory> req_args) throws(1:ServerError e);
     
    // 修改成功案例
    // 返回值: 0: 成功
    i32 story_change(1:CouponStory req_args) throws(1:ServerError e);
     
    // 查询成功案例
    list<CouponStory> story_query(1:StoryQueryArgs req_args) throws(1:ServerError e);
}



