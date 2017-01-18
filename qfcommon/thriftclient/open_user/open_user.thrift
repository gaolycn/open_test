namespace py open_user

# app 表现有 id:
# 10001 - Honey; 10002 - Near; 10003 - HoneyWeb; 10004 - NearMP


struct Profile {
    1: optional i32 user_id,
    2: optional string nickname,
    3: optional string avatar,
    4: optional string signature,
    5: optional string bgimageurl,
    6: optional byte gender,
    7: optional string birthday,
    8: optional string country,
    9: optional string province,
    10: optional string city,
    11: optional string mobile,
    12: optional string unionid,
    13: optional byte mark,
    14: optional string create_time,
    15: optional string update_time,
16: optional string openid,
17: required string follow_time,
18: required string follow_source,
}


struct AuthInfo {  # 手机登陆用凭证信息
    5: optional string mobile,
    6: optional string email,
    7: optional string password,
    8: optional string sms_code,
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


struct App {
    1: optional i32 id,
    2: optional string name,
    3: optional byte status,
}


// 通用异常
exception Error {
    /* errcode:
     * 1. 参数错误
     * 2. 数据库错误
     * 9. 其他错误
     */
    1: optional i32 errcode,
    2: optional string errmsg,
}


// 编码异常
exception CodecError {
    1: optional string message
}


// 参数异常
exception ArgumentError {
    1: optional string message
}


// 数据库约束异常
exception IntegrityError {
    1: optional string message
}


// 数据库异常
exception DatabaseError {
    1: optional string message
}


// 超时异常
exception TimeoutError {
    1: optional string message
}


// 未知异常
exception UnknownError {
    1: optional string message
}

exception InexistentWechatUser {
1: optional string message
}

service OpenUser {
    string ping(),

    # 手机 + 短信验证码/密码登陆, 新用户则注册, 注册必须提供短信验证码
    LoginResult mobile_login(1:required i32 app_id, 2:required AuthInfo auth_info, 3:optional LoginRecord login_info)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 微信登陆, 没有身份验证部分，直接用 unionid 之类进行查询, 新用户则注册
    LoginResult wx_login(1:required i32 app_id, 2:required Profile profile, 3:optional LoginRecord login_info)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 通过 user_id 更新 profile 表, set_value 为 json 字典，代表要更新的字段和更新的值, 返回是否成功
    bool update_profile(1:required i32 app_id, 2:required i32 user_id, 3:required string set_value)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 通过 user_id 修改认证信息，如密码, set_value 为 json 格式的字典，只许含有 User 表的字段，现在只有 password 可以修改，明文
    bool update_auth(1:required i32 app_id, 2:required i32 user_id, 3:required string set_value)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 保存验证码
    bool record_sms_code(1:required i32 app_id, 2:required string mobile, 3:required string auth_code)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

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
    list<Profile> get_profiles(1:required i32 app_id, 2:required string spec)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 通过openid 获取 用户ID 未查询到返回 -1
    i32 get_user_id_by_openid(1:required i32 app_id, 2:required string openid)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 通过 user_ids 查询 openids，不保证返回值的数量和顺序。
    list<string> get_openids_by_user_ids(1:i32 app_id, 2:list<i32> user_ids)
        throws (1:Error error)

    # 跨 app 获取 profiles
    # app_subset 为 app_id 的列表，查询范围为登陆过 app_subset 中 app 的用户
    # app_subset 为空时，本接口与 get_profiles 相同，即不过滤 app_id
    list<Profile> get_profiles_subset(1:required i32 app_id, 2:required list<i32> app_subset, 3:required string spec)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 计数用户信息
    i32 count_profiles(1:required i32 app_id, 2:required string spec)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 跨 app 计数用户信息
    i32 count_profiles_subset(1:required i32 app_id, 2:required list<i32> app_subset, 3:required string spec)
        throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

    # 查询 app 信息
    list<App> get_apps(1:required i32 app_id, 2:optional string spec)
throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)

# 微信取消关注
i32 wx_logout(1: required i32 app_id, 2: required string openid)
throws (1:CodecError ce, 2:ArgumentError ae, 3:IntegrityError ie, 4:DatabaseError de, 5: TimeoutError te, 6:UnknownError ue)
}
