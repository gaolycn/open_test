namespace py Kuma
/*
 * Kuma 是一套应用接口，而非数据管理接口。
 * 所以 service 查询的数据默认只限“有效数据”（status=1）
 */

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

// 位置 - 点
struct Point {
    // 本服务使用国标 GCJ-02 坐标系
    1: required double lng,
    2: required double lat,
}

// 位置 - 多边形
struct Polygon {
    // 多边形的第一个和最后一个 Point 元素总是相同的
    1: required list<Point> coordinates,
}

// 行政区
struct Area {
    1: optional i32 id,
    2: optional string name  # 行政区名字
    3: optional i32 parent_id  # 上级行政区 id, 为 0 代表最高级
    4: optional string stat_code  # 统计局行政区划代码
    6: optional i32 weight
    7: optional i32 status
}

// 店铺类别
struct ShopCategory {
    1: optional i32 id,
    2: optional string name  # 分类名字
    3: optional i32 parent_id  # 上级分类 id, 为 0 代表最高级
    6: optional i32 weight
    7: optional i32 status
}

// 商圈对象
struct Region {
    1: optional string id,
    3: optional string name,
    4: optional i32 area_id,
    7: optional Polygon field,
    8: optional i32 weight,
    9: optional i32 status,
    10: optional string created,
11: optional string modified,
12: optional Point loc,
13: optional i32 radius,
14: optional i32 max_shop_count,

15: optional string business_type,
16: optional string open_type,
}

// 店铺对象
struct Shop {
    1: optional string id,
    2: optional i32 qf_uid,
    3: optional string title,
    4: optional string descr,
    5: optional i32 category_id,
    6: optional i32 avg_price,
    7: optional string tel,
    8: optional string head_img,
    9: optional list<string> region_ids,
    10: optional string building_id,
    11: optional string addr,
    12: optional Point loc,
    13: optional i32 status,
    14: optional string created,
    15: optional string modified,
    16: optional list<string> imgs,
    17: optional i32 is_test,
    18: optional i32 is_pay,
    19: optional i32 weight,
20: optional list<string> hours,  # 营业时间 ['08:00', '22:00']
21: optional string logo_url,

}

// 写字楼对象
struct Building {
    1: optional string id,
    2: optional string name,
    3: optional string region_id,
    4: optional Point loc,
    5: optional i32 weight,
    6: optional i32 status,
    7: optional string created,
    8: optional string modified,
}


struct SearchResultRegion {
1: optional i32 total_count,
2: optional list<Region> region_list,
}
struct SearchResultShop {
1: optional i32 total_count,
2: optional list<Shop> shop_list,
}

service Kuma {
    string ping(),

    // 获取某个行政区划的下级列表，0 代表取最高级
    list<Area> query_areas(1:i32 parent_id, 2:string spec)
        throws (1:Error error)

    // 获取某个行政区划的上级列表，含参数自身
    list<Area> parent_areas(1:i32 area_id, 2:string spec)
        throws (1:Error error)

    // 获取店铺类别
    list<ShopCategory> query_shop_categorys(1:i32 parent_id, 2: string spec)

    // 定位商圈（严格“处于”商圈之内）
    list<Region> locate_region(1:Point loc)
        throws (1:Error error)

    // 宽松定位商圈（包含非标准商圈，即没有多边形的商圈，此为 B 端用临时接口）
    list<Region> one_punch(1:Point loc)
        throws (1:Error error)

    // 通过行政区划 id /stat_code 获取商圈列表
    list<Region> query_regions(1:Area area, 2:string spec)
        throws (1:Error error)

    // 获取商圈内写字楼(可以提供坐标辅助排序)
    list<Building> query_buildings(1:string region_id, 2:Point loc, 3:string spec)
        throws (1:Error error)

    // 获取店铺列表  林浩管理后台专用，不设置默认 status=1
    list<Shop> query_shops(1:string spec)
        throws (1:Error error)

    // 统计店铺数量  林浩管理后台专用，不设置默认 status=1
    i32 count_shops(1:string spec)
        throws (1:Error error)

    // 查询店铺当前折扣 店铺不存在或无折扣信息 将返回'10'，无折扣
    string query_shop_current_discount(1:i32 qf_uid)
        throws (1:Error error)

    // 创建店铺
    Shop create_shop(1:Shop shop)
        throws (1:Error error)

    // 更新店铺信息
    Shop update_shop(1:Shop shop)
        throws (1:Error error)

// query region shop count
map<string, i32> query_multi_region_shop_count(1:optional list<string> region_id_list)
        throws (1:Error error)

// area list
map<i32, Area> get_area_by_ids(1:optional list<i32> area_id_list)
        throws (1:Error error)

// mis query region
SearchResultRegion mis_search_region(1:optional string name, 2:optional i32 status, 3: optional i32 area_id, 4:optional i32 offset 5:optional i32 limit, 6:optional list<string>id_list)
throws (1:Error error)

// mis query shop
SearchResultShop mis_search_shop(1:optional string name, 2:optional string region_id, 3: optional string tel, 4:optional i32 offset, 5:optional i32 limit, 6:optional i32 status, 7:optional list<i32> qf_uid_list, 8:optional list<string> area_region_id_list)
throws (1:Error error)

// create region
Region create_region(1:required Region region)
throws (1:Error error)

// query region type
map<string, string> query_region_type_map()

// query region open_type
map<string, string> query_region_open_type_map()

// query shop
Shop get_shop_by_id(1:required string shop_id)
throws (1:Error error)

// query shop category path
list<ShopCategory> query_shop_category_path(1:required i32 shop_category_id)
throws (1:Error error)

// edit shop region
i32 mis_edit_shop_region(1:required list<i32> qf_uid_list, 2:required string region_id)
throws (1:Error error)

Shop get_shop_by_qf_uid(1: required i32 qf_uid)
throws (1:Error error)

Region get_region_by_id(1: required string region_id)
throws (1:Error error)

list<Shop> search_shop_by_distance(1:required Point loc, 2:required list<i32> qf_uid_list, 3: required i32 distance, 4: required i32 limit)
throws (1:Error error)

}

/* spec 参数：
 * spec 是个经过 json.dumps 处理的字典。查询服务的一些通用需求（分页，排序等）可以通过这个字段指定。
 * 
 * 字段示例：
 * offset: i32,  偏移量，默认 0
 * limit: i32,  分页量，默认不分页（全取）
 * order_by: string,  排序字段，默认 id
 * desc: bool,  是否倒序，默认 false
 *
 * 另外如 query_shops 这样的接口，spec 还可以含有额外的具体查询条件，如：
 * id: '55b9c9d4c69575999049b2b4',
 * status: [1, 2]  # list 代表 `in`
 * weight: {'$gt': 1}  # 带 `$` 的特殊查询条件，遵从 mongodb 的语法规则。（'$and' 和 '$or' 暂时可能有问题）
 */
