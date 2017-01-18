namespace py qf_wxmp


// 发生错误时的返回码及其对应的描述信息
exception MPError
{
    1: string code, // 返回码
    2: string msg,  // 描述信息
}

// 发送的客服消息类型
enum KFMsgType
{
    TEXT      = 1,  // 文本消息
    IMAGE     = 2,  // 图片消息
    VOICE     = 3,  // 语音消息
    VIDEO     = 4,  // 视频消息
    MUSIC     = 5,  // 音乐消息
    NEWS_LINK = 6,  // 图文消息, 跳转到外链
    NEWS_ID   = 7,  // 图文消息, 指定图文id, 跳转到图文消息页面
    WXCARD    = 8,  // 微信卡券
}

// 推送类型
enum PushType
{
    IDS   = 1,  // 按openid列表推送
    GROUP = 2,  // 按组推送
    ALL   = 3,  // 全平台推送
}

// 根据media_id推送的素材类型 
enum PushMediaType
{
    MPNEWS   = 1,  // 推送图文
    VOICE    = 2,  // 推送语音
    IMAGE    = 3,  // 推送图片
    MPVIDEO  = 4,  // 推送视频
}

// 支持的菜单事件
enum MenuEvent
{
    CLICK = 1,  // 点击菜单推消息
    VIEW  = 2,  // 点击菜单，跳转url
}

// 支持的回复类型
enum ReplyType
{
    TEXT = 1,  // 回复文本消息
    NEWS = 2,  // 回复图文消息
}



// 分布查询时的输入参数
struct PageQuery
{
    1: required i32 num  = 1,   // 查询第几页
    2: required i32 size = 20,  // 每页的数量
}

// 分布查询时的返回值
struct PageQueryResp
{
    1: i32 num,     // 第几页
    2: i32 size,    // 每页的数量
    3: i32 total,   // 总页数
    4: i32 count,   // 总数据量
}

// 消费者信息
struct WXCustomer
{
    1:  i64     id,             // 消费者id
    2:  i16     subscribe,      // 消费者是否关注 1. 关注  0. 没关注
    3:  string  openid,         // 消费者的微信openid
    4:  string  nickname,       // 消费者的微信昵称
    5:  i16     sex,            // 消费者的性别
    6:  string  city,           // 消费者所在城市
    7:  string  country,        // 消费者所在国家
    8:  string  province,       // 消费者所在省
    9:  string  language,       // 消费者的语言
    10: string  headimgurl,     // 消费者的微信图像url
    11: i32     subscribe_time, // 消费者的关注时间
    12: string  unionid,        // 消费者的微信unionid
    13: string  remark,         // 公众号运营者对消费者的备注
    14: i64     groupid,        // 消费者所在的分组id
    15: string  tagid_list,     // 消费者被打上的标签id
}

// 微信access_token的结果
struct WXToken
{
    1: string   access_token,   // 微信的access_token
    2: i32      ttl,            // access_token的有效期
}

// 微信客服消息
struct KFMsg
{
    1: string    appid,         // 发送客服消息的公众号id
    2: string    openid,        // 接收客户消息的消费者openid
    3: KFMsgType msg_type,      // 消息类型
    4: string    msg_content,   // 消息内容，符合微信消息的消息内容
}

// 微信推送的信息
struct MPush
{
    1: required string appid,            // 微信公众号的appid
    2: required i64    pushid,           // 本次推送的id
    3: required i64    itemid,           // 切分的推送项的id
    4: required string media_id,         // 推送的素材id
    5: required PushMediaType media_type = PushMediaType.MPNEWS,   // 根据media_id推送的素材类型
    6: required PushType      push_type  = PushType.IDS,         // 1:按openid列表推送  2: 按组推送  3: 全员推送
    7: optional i32    group_id,         // 按组推送有效，推送的分组
    8: optional list<string>  openids,   // 按openid列表推送有效，推送的openid, 多个openid以逗号分隔
}

// 微信推送的信息
struct MPushBase
{
    1: required string appid,            // 微信公众号的appid
    2: required i64    pushid,           // 本次推送的id
    3: required i64    itemid,           // 切分的推送项的id
    4: required PushType     push_type  = PushType.IDS,         // 1:按openid列表推送  2: 按组推送  3: 全员推送
    5: optional i32    group_id,         // 按组推送有效，推送的分组
    6: optional list<string> openids,    // 按openid列表推送有效，推送的openid, 多个openid以逗号分隔
}

// 微信推送的信息
struct MPushTxt
{
    1: required MPushBase base,         // 推送的基本配置
    2: required string    content,      // 推送的内容
}

// 推送统计
struct PushStat
{
    1: i32 total_num,       // 推送的总数(推送完成的统计)
    2: i32 filter_num,      // 真正推送的数量(推送完成的统计)
    3: i32 sent_num,        // 推送成功的数量(推送完成的统计)
    4: i32 error_num,       // 推送失败的数量(推送完成的统计)
    5: list<i64> itemids,   // 未完成的推送id, XXX: 推送失败的话，sent_num应该就0(猜测，未出现过，也不知道怎么出现这个情况，先这样假定，以后有问题再改)
}

// 公众号的配置
struct MPConf
{
    1:  i64     id,         // id
    2:  i32     userid,     // 商户id
    3:  i32     hj_appid,   // 消费者体系的appid
    4:  string  thrid_appid,// 第三方平台的appid
    5:  string  appid,      // 微信公众号的appid
    6:  string  appsecret,  // 微信公众号的appsecret
    7:  string  wxmp_id,    // 微信公众号的原始id, gh_xxx
    8:  string  wxmp_num,   // 微信公众号的微信号
    9:  i16     is_auth,    // 对于商户号公众号，是否授权
    10: i16     status,     // 状态 0: 不启用  1: 启用
    11: i32     ctime,      // 创建时间
    12: i32     uptime,     // 更新时间
    13: string  nick_name,  // 微信公众号的昵称
    14: string  head_img,   // 微信公众号的头像
    15: string  service_type,   // 公众号类型: 0:订阅号, 1:由历史老帐号升级后的订阅号, 2:服务号
    16: string  verify_type,    // 认证类型: -1:未认证, 0:微信认证, 1:新浪微博认证, 2:腾讯微博认证, 3:已资质认证通过但还未通过名称认证, 4:代表已资质认证通过、还未通过名称认证，但通过了新浪微博认证，5:代表已资质认证通过、>还未通过名称认证，但通过了腾讯微博认证
    17: string  qrcode_url,     // 二维码图片的URL
    18: list<string> funcs,     // 公众号授权给开发者的权限集列表
}

// 子菜单配置
struct SubMenu
{
    1: string    name;  // 子菜单名
    2: MenuEvent event; // 子菜单事件
    3: string    value; // 子菜单执行动作
}

// 完整的菜单配置
struct Menu
{
    1: string    name;  // 菜单名
    2: MenuEvent event; // 菜单事件
    3: string    value; // 菜单执行动作
    4: list<SubMenu> sub_menu;  // 子菜单信息, 如果存在，则菜单事件为空, 子菜单最多可以有5个
}

// 自动回复规则
struct Reply
{
    1:  string appid,   // 微信公众号的appid
    2:  string mp_key,  // 按关键字回复时，指定的关键字
    3:  ReplyType push_type = ReplyType.TEXT,    // 回复类型
    4:  string push_txt     = '',  // 回复文本消息时，消息内容
    5:  string push_title   = '',  // 回复图文消息时，图文的标题
    6:  string push_content = '',  // 回复图文消息时, 图文的内容
    7:  string push_pic_url = '',  // 回复图文消息时，图文的图片url
    8:  string push_url     = '',  // 回复图文消息时，图文的跳转url
    9:  string content      = '',  // 备注
    10: i16    status=1,       // 状态 0: 不启用  1: 启用
    11: string create_time,    // 创建时间
    12: string update_time,    // 更新时间
    13: i16    weight=1,       // 权重
}

// 查询自动回复规则
struct ReplyQuery
{
    1: required string appid,   // 微信公众号的appid
    2: optional string mp_key,  // 按回复的关键字查询
    3: optional i16    status,  // 按状态查询
    4: required PageQuery page, // 分页查询的信息
    5: optional list<string> mp_keys, // 按回复的关键字批量查询
}

// 查询自动回复规则
struct ReplyQueryResp
{
    1: PageQueryResp page,  // 分页查询时返回的分页信息
    2: list<Reply>   data,  // 本页显示的数据
}

// 模板消息发送的数据结构
struct TemplateSend
{
    1: required string appid,       // 微信公众号的appid
    2: required string openid,      // 模板消息接收者的openid
    3: required string template_id, // 模板消息id
    4: optional string url='',      // 模板消息跳转的url
    5: required string data,        // 模板消息内容
}

// 接收公众号事件的数据结构
struct MPEvent
{
    1: required string appid,       // 微信公众号的appid
    2: required string data,        // 事件通知的数据
}

// 授权公众号绑定商户
struct MPAuthBind
{
    1: required i32    userid,      // 授权公众号绑定的userid
    2: required string auth_code,   // 授权公众号的授权码
    3: required i32    expire,      // 授权码的过期时间
}


// 执行请求时，如果发生任何错误都已异常返回
service QFMP
{
    i64 ping() throws(1:MPError e);

    // ================微信公众号api相关接口================
    // 创建公众号配置
    //i64 mp_create(1: MPConf req_args) throws(1:MPError e);
    // 修改公众号配置
    // 返回值: 0: 成功
    //i16 mp_change(1: MPConf req_args) throws(1:MPError e);
    // 查询公众号配置
    list<MPConf> mp_query(1: i32 userid) throws(1:MPError e);
    // 获取微信的access_token
    WXToken access_token(1: string appid) throws(1:MPError e);
    // 生成永久的带参数二维码
    // 返回值: {'param': 'url'}, 如果某个参数生成失败，则结果为空串
    map<string, string> gen_forever_qr(1: string appid, 2: list<string> params) throws(1:MPError e);
    // 授权公众号绑定到商户
    // 返回值 0: 成功  <0与异常: 失败
    i16 mp_auth_bind(1: MPAuthBind req_args) throws(1:MPError e);

    // ========消费者相关接口========
    // 根据openid获取消费者信息, 如果消费者不存在，则创建
    WXCustomer openid2customer(1: string appid, 2: string openid) throws(1:MPError e);
    // 将消费者转为活跃消费者
    i32 customer_active(1: string appid, 2: string openid) throws(1:MPError e);

    // ========客服消息相关接口========
    // 客户消息
    // 同步发送，未做重试(access_token不合法除外)，未做异步队列
    i32 msg_send(1: KFMsg msg) throws(1:MPError e);
    // 获取卡券的扩展信息
    string card_ext(1: string appid, 2: string cardid, 3: string code) throws(1:MPError e);

    // ========公众号推送相关接口========
    // 公众号的media_id推送
    // 返回值: 0成功  异常或<0 失败
    i32 push_media(1: MPush req_args) throws(1:MPError e);
    // 公众号的push_txt推送
    // 返回值: 0成功  异常或<0 失败
    i32 push_txt(1: MPushTxt req_args) throws(1:MPError e);
    // 查看推送结果
    map<i64, PushStat> push_stat(1: string appid, 2: list<i64> pushids) throws(1:MPError e);

    // ========菜单相关接口========
    // 菜单的创建是全覆盖的，如果需要修改，则在原有的基础上修改
    // 一级菜单最多有3个，二级菜单最多5个
    // 返回值 0: 成功  异常失败
    i16 menu_create(1: string appid, 2: list<Menu> mp_menu) throws(1:MPError e);
    // 查询菜单
    list<Menu> menu_query(1: string appid) throws(1:MPError e);

    // ========自动回复相关接口========
    // 创建自动回复规则
    // 创建成功，返回规则id
    i64 reply_save(1: Reply req_args) throws(1:MPError e);
    // 查询自动回复规则
    // 分页查询
    ReplyQueryResp reply_query(1: ReplyQuery req_args) throws(1:MPError e);

    // ========模板消息相关接口========
    // 发送模板消息
    // 返回值 0: 发送成功 异常失败
    i16 template_send(1: TemplateSend req_args) throws(1:MPError e);

    // ========公众号通知事件相关接口========
    // 实名公众号接收消费者操作事件并响应相应的结果
    // 返回值 成功: 公众号的响应结果(xml字符串)
    string realname_event(1: MPEvent req_args) throws(1:MPError e);
    // 授权公众号接收消费者事件并响应相应的结果
    // 返回值 成功: 公众号的响应结果(xml字符串)
    string auth_event(1: MPEvent req_args) throws(1:MPError e);
    // 第三方平台授权公众号的授权事件处理
    // 返回值 成功: 公众号的响应结果(xml字符串)
    string mp_auth_event(1: string data) throws(1:MPError e);
}

