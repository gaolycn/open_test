namespace py qf_customer


// 发生错误时的返回码及其对应的描述信息
exception CustomerError
{
    1: string code, // 返回码
    2: string msg,  // 描述信息
}

struct Profile {
    1:  optional i32    user_id,
    2:  optional string nickname,   # 消费者的昵称
    3:  optional string avatar,
    4:  optional string signature,
    5:  optional string bgimageurl,
    6:  optional byte   gender,
    7:  optional string birthday,
    8:  optional string country,
    9:  optional string province,
    10: optional string city,
    11: optional string mobile,
    12: optional string unionid,
    13: optional byte   mark,
    14: optional string create_time,
    15: optional string update_time,
    16: optional string openid,
    17: required string follow_time,
    18: required string follow_source,
    19: optional string cname,      # 消费者的名字
}

struct LoginRecord {  # 登陆历史记录信息
    1: optional string ip,
    2: optional string user_agent,
    3: optional double longitude,
    4: optional double latitude,
}

struct LoginResult {  # 前两个字段有且只有一个为 None, 后两个字段要么都为 None 要么都不为 None
    1: optional byte error_code,  # 失败原因 1.短信验证码错误 2.密码错误 3.用户不存在
    2: optional Profile profile,
    3: optional bool app_local_newly_registered,
    4: optional bool global_newly_registered,
}

# app操作
struct App
{
    1: string appid,    # 外部的appid
    2: string name,     # app的名字
    3: i16    status,   # 状态 0:未启用  1: 启用
    4: i64    id,       # 内部的唯一的id
}

# app查询
struct AppQuery
{
    1: i32    id,       # 内部的唯一的id
    2: string appid,    # 外部的appid
}

# 微信的消费者信息
struct WXCustomer
{
    1: i32    appid,    # appid, 内部
    2: string wx_appid, # 微信公众号的appid，这两个必须至少存在一个, 如果wx_appid存在，则如果app未注册，则失败
    3: string openid,   # 微信公众号的openid
}


// 执行请求时，如果发生任何错误都已异常返回
service QFCustomer
{
    string ping() throws(1:CustomerError e);

    # ================================相同参数兼容open_user老接口================================
    # 微信登陆, 没有身份验证部分，直接用 unionid 之类进行查询, 新用户则注册
    # 这个接口在兼容老接口的基础上添加限制，即appid只能是好近的appid
    LoginResult wx_login(1:i32 appid, 2:Profile profile, 3:LoginRecord login_info) throws (1:CustomerError e);

    # 查询用户信息
    /*
     * spec 为 json 格式的字典,
     * spec: e.g  '{"id": 10001, "mobile": "18688888888"}'
     *
     * 复杂查询符号: $or(或)  $not(取反)  $and(并)
     * 值的查询符号: $lt(小于) $gt(大于) $le(小于等于)  $ge(大于等于)  $ne(不等于)  $like(字符串的模糊搜索(%是匹配规则) e.g nickname含有琦  {"nickname": {"$like": '%琦%'}} ) 
     * 关键字:  limit  offset  order_by desc
     * spec: e.g  '{"$or": {"id": {"$gt": 10001}, "mobile": "18688888888"}, "limit": 2}'
     */
    list<Profile> get_profiles(1:i32 appid, 2:string spec) throws (1:CustomerError e);

    # 微信取消关注
    i32 wx_logout(1:i32 appid, 2:string openid) throws (1:CustomerError e);

    # 通过openid 获取 用户ID 未查询到返回 -1
    i32 get_user_id_by_openid(1:i32 appid, 2:string openid) throws (1:CustomerError e);

    # 通过 user_ids 查询 openids，不保证返回值的数量和顺序。
    list<string> get_openids_by_user_ids(1:i32 appid, 2:list<i32> user_ids) throws (1:CustomerError e);

    # ================================app相关接口================================
    # 保存app
    # 成功返回appid
    i32 app_save(1:App req_args) throws (1:CustomerError e);

    # 查询app
    # 成功返回appid
    App app_query(1:AppQuery req_args) throws (1:CustomerError e);

    # ================================消费者相关接口================================
    # 新版的微信注册接口, 可以提供多个微信公众号以绑定微信
    # 如果提供的消费者的微信信息只有一个
    #   appid是好近公众号的appid, 则注册(没有的话)，查询返回
    #   appid是非好近，直接查，不注册, 如果user_id为-1
    # 如果提供的消费者信息有多个，则必须一个的是好近的appid
    Profile wx_bind(1:list<WXCustomer> wx_customers, 2:Profile profile) throws (1:CustomerError e);

    # 更新消费者的属性信息
    # profile中不能存在user_id，如果存在，则忽略
    # userid, openid, create_time, update_time, follow_time, follow_source不能通过这个接口更新
    # 该接口不会更新关注状态
    Profile profile_update(1:i32 cid, 2:Profile profile) throws (1:CustomerError e);

}

