# coding: utf-8
import hashlib, copy, urllib
import traceback

if __name__ == '__main__':
    def smart_utf8(strdata):
        ''' strdata转换为utf-8编码字符串'''
        return strdata.encode('utf-8') if isinstance(strdata, unicode) else str(strdata)
else:
    from qfcommon.base.tools import smart_utf8

# 签名算法
SIGN_METHOD_MD5 = 1
SIGN_METHOD_SHA_1 = 2

# 字符编码
CHARSET_GBK = 1

# 币种
CURRENCY_RMB = 1

# 支付方式
PAYTYPE_YURE = 1    # 余额支付（必须登录百度钱包）
PAYTYPE_WANGYIN = 2 # 网银支付（在百度钱包页面上选择银行，可以不登录百度钱包）
PAYTYPE_WANGGUAN = 3 #银行网关支付（直接跳到银行的支付页面，无需登录百度钱包）

# 返回编码列表 ret
ret_list = {}

class BaiFuBaoException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'BaiFuBao: [error] %s' % self.msg
        
def transcoding(orig_str, charset):
    if charset == CHARSET_GBK:
        charset_name = 'gbk'
    else:
        err_msg = 'sign undefine charset:"%d"' % charset
        raise BaiFuBaoException(err_msg)
    return smart_utf8(orig_str).decode('utf8').encode(charset_name)

def urldecode(data):
    d = {}
    a = data.split('&')
    for s in a:
        if s.find('='):
            k, v = map(urllib.unquote, s.split('='))
            try:
                d[k] = v
            except KeyError:
                d[k] = [v] 
    return d

class BaiFuBao(object):
    def __init__(self, sp_no, key, sign_method=SIGN_METHOD_MD5, charset=CHARSET_GBK):
        self.sp_no = sp_no              # 百付宝商户号  10位数字组成的字符串
        self.key = key                  # 百付宝的合作密钥
        self.sign_method = sign_method  # 生成签名的方法
        self.charset = charset          # 中文编码

    @staticmethod
    def sign(params, baifubao_key, sign_method=SIGN_METHOD_MD5, charset=CHARSET_GBK):
        keys = params.keys()
        keys.sort()
        sign_data = ''
        for k in keys:
            sign_data += smart_utf8(k) + '=' + smart_utf8(params[k]) + '&'
        sign_data += 'key' + '=' + smart_utf8(baifubao_key)
        sign = ''
        sign_data = transcoding(sign_data, charset)
        print "sign_data: %r" % sign_data
        if sign_method == SIGN_METHOD_MD5:
            md5 = hashlib.md5()
            md5.update(sign_data)
            sign = md5.hexdigest().upper()
        elif sign_method == SIGN_METHOD_SHA_1:
            sha1 = hashlib.sha1()
            sha1.update(sign_data)
            sign = sha1.hexdigest().upper()
        else:
            err_msg = 'sign undefine sign_method:"%d"' % sign_method
            raise BaiFuBaoException(err_msg)
        print 'sign result: %s' % sign
        return sign

    # 检查百付宝回馈数据的签名
    @staticmethod
    def check_sign(params, baifubao_key):
        if not isinstance(params, dict):
            params = urldecode(params)
        print 'params: %s' % params
        try:
            sign = params['sign'].upper()
            sign_method = int(params['sign_method'])
            charset = int(params['input_charset'])
            if not sign:
                return False
            del params['sign']
            if sign != BaiFuBao.sign(params, baifubao_key, sign_method, charset):
                return False
        except Exception, e:
            #print e
            return False
        else:
            return True
    
    def __prepare_params(self, inputs, fields_must, fields_option):
        params = {}
        # 将必填字段(且签名的需要的字段)添加到params
        for key in fields_must:
            if fields_must[key]['in_sign'] == False:
                continue
            value = inputs.get(key)
            if not value: 
                if not fields_must[key]['default']:
                    err_msg = 'prepare params need key:"%s"' % key
                    raise BaiFuBaoException(err_msg)
                else:
                    params[key] = fields_must[key]['default']
            else:
                params[key] = value
        # 将选填字段(且签名的需要的字段)添加到params
        for key in fields_option:
            if fields_option[key]['in_sign'] == False:
                continue
            value = inputs.get(key)
            if not value: 
                if fields_option[key]['default']:
                    params[key] = fields_option[key]['default']
            else:
                params[key] = value
        # 计算签名
        sign_method = params.get('sign_method', SIGN_METHOD_MD5)
        charset = params.get('input_charset', CHARSET_GBK)
        params['sign'] = BaiFuBao.sign(params, self.key, sign_method, charset)
        # 将必填字段(且签名的不需要的字段)添加到params
        for key in fields_must:
            if fields_must[key]['in_sign'] == True:
                continue
            value = inputs.get(key)
            if not value: 
                if not fields_must[key]['default']:
                    err_msg = 'prepare params need key:"%s"' % key
                    raise BaiFuBaoException(err_msg)
                else:
                    params[key] = fields_must[key]['default']
            else:
                params[key] = value
        # 将选填字段(且签名的不需要的字段)添加到params
        for key in fields_option:
            if fields_option[key]['in_sign'] == True:
                continue
            value = inputs.get(key)
            if not value: 
                if fields_option[key]['default']:
                    params[key] = fields_option[key]['default']
            else:
                params[key] = value
        # 编码转换
        for key in params:
            params[key] = transcoding(params[key], charset)
        return params


    """
    扫码支付
        商户生成二维码，用户通过手机去扫描该二维码，并下单
    """
    def precreate(self, inputs):
        fields_must = {
            'service_code': {'default':1,       'in_sign':True},    # 服务编号  目前必须为1
            'sp_no':        {'default':self.sp_no, 'in_sign':True}, # 百付宝商户号   10位数字组成的字符串
            'order_create_time':{'default':None,'in_sign':True},    # 创建订单的时间    YYYYMMDDHHMMSS
            'order_no':     {'default':None,    'in_sign':True},    # 订单号，商户须保证订单号在商户系统内部唯一。  不超过20个字符
            'goods_name':   {'default':'支付',   'in_sign':True},    # 商品的名称    允许包含中文；不超过128个字符或64个汉字
            'total_amount': {'default':None,    'in_sign':True},    # 总金额，以分为单位    非负整数
            'currency':     {'default':CURRENCY_RMB, 'in_sign':True},# 币种，默认人民币
            'return_url':   {'default':None,    'in_sign':True},    # 百付宝主动通知商户支付结果的URLopener(仅支持http(s)的URL
            'pay_type':     {'default':PAYTYPE_YURE, 'in_sign':True},# 默认支付方式
            'version':      {'default':2,       'in_sign':True},    # 接口的版本号 必须为2 
            'sign_method':  {'default':SIGN_METHOD_MD5, 'in_sign':True},# 签名方法
            'input_charset':{'default':CHARSET_GBK, 'in_sign':True},# 请求参数的字符编码
        }
        fields_option = {
            # 不参与签名
            'code_type':    {'default':0,    'in_sign':False},  # 码类型(不参与签名)    整数，目前必须为0
            'code_size':    {'default':2,    'in_sign':False},  # 码大小(不参与签名)    取值范围：1-10；默认值：2
            'output_type':  {'default':1,    'in_sign':False},  # 输出格式(不参与签名)   0：image；1：json；默认值：0 
            'nologo':       {'default':1,    'in_sign':False},  # 不带百度钱包 LOGO(不参与签名) 0: 带 LOGO 1: 不带 LOGO 默认值:1
            'mno':          {'default':None, 'in_sign':False},  # 实体商户门店号 2-15位数字组成的字符串(不参与签名) 
            'mname':        {'default':None, 'in_sign':False},  # 实体商户门店名称 允许包含中文；不超过32个字符或汉字；不允许包含特殊字符。(不参与签名) 
            'tno':          {'default':None, 'in_sign':False},  # 实体商户终端号 8 -9位数字组成的字符串(不参与签名) 
            # 参与签名
            'goods_desc':   {'default':None, 'in_sign':True},   # 商品的描述信息    允许包含中文；不超过255个字符或127个汉字
            'goods_url':    {'default':None, 'in_sign':True},   # 商品在商户网站上的URL。   URL
            'unit_amount':  {'default':None, 'in_sign':True},   # 商品单价，以分为单位  非负整数
            'unit_count':   {'default':None, 'in_sign':True},   # 商品数量  非负整数
            'transport_amount':{'default':None, 'in_sign':True},# 运费  非负整数
            'buyer_sp_username':{'default':None, 'in_sign':True}, # 买家在商户网站的用户名  允许包含中文；不超过64字符或32个汉字
            'page_url':     {'default':None, 'in_sign':True},   # 用户点击该URL可以返回到商户网站；该URL也可以起到通知支付结果的作用    仅支持http(s)的URL
            'bank_no':      {'default':None, 'in_sign':True},   # 网银支付或银行网关支付时，默认银行的编码  取值范围参见附录  如果pay_type是银行网关支付，则必须有值
            'expire_time':  {'default':None, 'in_sign':True},   # 交易的超时时间    YYYYMMDDHHMMSS，不得早于交易创建的时间
            'sp_uno':       {'default':None, 'in_sign':True},   # 用户在商户端的用户id或者用户名(必须在商户端唯一，用来形成快捷支付合约)    不超过64个字符
            'extra':        {'default':None, 'in_sign':True},   # 商户自定义数据    不超过255个字符
            'profit_type':  {'default':1,    'in_sign':True},   # 分润类型  1：实时分账；2：异步分账 3：记账（只记账不分润)
            'profit_solution':{'default':None, 'in_sign':True}, # 分润方案  //分账明细：格式为(id类型\^id\^金额类型\^金额\^备注\|){0,4}(id类型\^id\^金额类型\^金额\^备注)
            # 原文{"offline_pay":1} 使用的是urlencode编码  但python的url.urlencode的结果与百度结果稍有不同 所以写成固定的形式
            'sp_pass_through':{'default':'%7B%22offline_pay%22%3A1%7D', 'in_sign':True},  # 商户定制服务字段商户定制服务字段,参与签名, 具体格否式参见附录 offline_pay 1 交易进行返现
             
        }
        return self.__prepare_params(inputs, fields_must, fields_option)

    """
    按订单号查询支付结果
    """
    def query(self, inputs):
        fields_must = {
            'sp_no':        {'default':self.sp_no, 'in_sign':True}, # 百付宝商户号   10位数字组成的字符串
            'order_no':     {'default':None,    'in_sign':True},    # 订单号，商户须保证订单号在商户系统内部唯一。  不超过20个字符
            'version':      {'default':2,       'in_sign':True},    # 接口的版本号 必须为2 
            'sign_method':  {'default':SIGN_METHOD_MD5, 'in_sign':True},# 签名方法
            'input_charset':{'default':CHARSET_GBK, 'in_sign':True},# 请求参数的字符编码
        }
        fields_option = {
        }
        return self.__prepare_params(inputs, fields_must, fields_option)

    """
    取消订单(支付接口的订单取消, 只要没有完成支付的就可以 包括支付失败)
        取消订单是指商户在百度钱包创建订单后，可以调用此接口来进行订单的取消
    """
    def cancel(self, inputs):
        fields_must = {
            'sp_no':        {'default':self.sp_no,    'in_sign':True},    # 商户号, 格式为：3400000001
            'order_no':     {'default':None,    'in_sign':True},    # 订单号 格式为：340000000110045430
            'output_type':  {'default':1,       'in_sign':True},    # 1: xml，2: json
            'output_charset': {'default':CHARSET_GBK,    'in_sign':True}, # 1: gbk
            'sign_method':  {'default':SIGN_METHOD_MD5,    'in_sign':True},    # 签名方式，1：Md5
        }
        fields_option = {
        }
        return self.__prepare_params(inputs, fields_must, fields_option)

    """
    退款
        商户网站提交退款请求后，由百度钱包进行验签，验签通过后执行退款操作。退款成功后，百度钱包会通知商户退款结果，商户通过退款结果通知数据及时修改订单的退款状态
    """
    def refund(self, inputs):
        fields_must = {
            'service_code': {'default':2,       'in_sign':True},    # 服务编号  目前必须为2
            'sp_no':        {'default':self.sp_no, 'in_sign':True}, # 百付宝商户号   10位数字组成的字符串
            'order_no':     {'default':None,    'in_sign':True},    # 订单号，商户须保证订单号在商户系统内部唯一。  不超过20个字符
            'currency':     {'default':CURRENCY_RMB, 'in_sign':True},# 币种，默认人民币
            'return_url':   {'default':None,    'in_sign':True},    # 百付宝主动通知商户支付结果的URLopener(仅支持http(s)的URL
            'version':      {'default':2,       'in_sign':True},    # 接口的版本号 必须为2 
            'sign_method':  {'default':SIGN_METHOD_MD5, 'in_sign':True},# 签名方法
            'input_charset':{'default':CHARSET_GBK, 'in_sign':True},# 请求参数的字符编码
            'output_type':  {'default':1, 'in_sign':True},          # 响应数据的格式，默认XML
            'output_charset':{'default':CHARSET_GBK, 'in_sign':True},# 请求参数的字符编码
            'cashback_amount':{'default':None, 'in_sign':True},     # 退款金额    退款金额，以分为单位。
            'cashback_time':{'default':None, 'in_sign':True},       # 退款请求时间    格式 YYYYMMDDHHMMSS
            'sp_refund_no': {'default':None, 'in_sign':True},       # 商户退款流水号 商户生成退款流水号，要求同一商户退款流水号不可重复，需要在数据库中根据退款id及商户退款流水号建立索引。(不超过21个字符)
        }
        fields_option = {
            'return_method':{'default':1, 'in_sign':True},          # 后台通知请求方式 1为GET，2为POST，默认为POST方式
            'refund_type':  {'default':2, 'in_sign':True},          # 退款类型  1为退至钱包余额，2为原路退回。默认为2原路退回。注：若指定退至钱包余额，但交易为纯网关交易，则自动更改为原路退回。实际退款类型在同步返回结果及退款通知中体现。
            'refund_profit_solution':{'default':None, 'in_sign':True},# 分润退款参数
        }
        return self.__prepare_params(inputs, fields_must, fields_option)

    """
    退款查询
    """
    def refund_query(self, inputs):
        fields_must = {
            'service_code': {'default':12,      'in_sign':True},   # 服务编号  目前必须为12
            'sp_no':        {'default':self.sp_no, 'in_sign':True}, # 百付宝商户号   10位数字组成的字符串
            'order_no':     {'default':None,    'in_sign':True},    # 订单号，商户须保证订单号在商户系统内部唯一。  不超过20个字符
            'version':      {'default':2,       'in_sign':True},    # 接口的版本号 必须为2 
            'sign_method':  {'default':SIGN_METHOD_MD5, 'in_sign':True},# 签名方法
            'output_type':  {'default':1,       'in_sign':True},          # 响应数据的格式，默认XML
            'output_charset':{'default':CHARSET_GBK, 'in_sign':True},# 请求参数的字符编码
        }
        fields_option = {
            'sp_refund_no': {'default':None,    'in_sign':True},    # 退款流水号 外部商户退款流水号(不超过21个字符)
        }
        return self.__prepare_params(inputs, fields_must, fields_option)


#-------------------------------  for test -----------------------------#
notiful_url = 'http://120.131.72.3:8080/trade/baifubao/v1/notify'
def test_sign():
    params = {
        'service_code':1,
        'sp_no':'1234567890',
        'order_create_time':'20080808080808',
        'goods_name':'商品的名称',
        'goods_desc':'这是一笔使用百度钱包支付的订单',
        'total_amount':1000,
        'currency':1,
        'return_url':'http://www.yoursite.com/return_url',
        'expire_time':'20080908080808',
        'input_charset':'1',
        'version':2,
        #'sign':'0EBBD22EF456D779B21A97482B9D3504',
        'sign_method':1,
    }
    baifubao_key = 'XXXXXXXXXXXXXXXX'
    BaiFuBao.sign(params, baifubao_key)

def test_check_sign():
    params = {
        'service_code':1,
        'sp_no':'1234567890',
        'order_create_time':'20080808080808',
        'goods_name':'商品的名称',
        'goods_desc':'这是一笔使用百度钱包支付的订单',
        'total_amount':1000,
        'currency':1,
        'return_url':'http://www.yoursite.com/return_url',
        'expire_time':'20080908080808',
        'input_charset':'1',
        'version':2,
        'sign':'0EBBD22EF456D779B21A97482B9D3504',
        'sign_method':1,
    }
    baifubao_key = 'XXXXXXXXXXXXXXXX'
    if BaiFuBao.check_sign(params, baifubao_key):
        print 'check ok'
    else:
        print 'check fail'

def test_check_sign_1():
    baifubao_sp_no = '9000100005'
    baifubao_key = 'pSAw3bzfMKYAXML53dgQ3R4LsKp758Ss'
    params = 'bank_no=&bfb_order_create_time=20151127160910&bfb_order_no=2015112790001000051110843447475&buyer_sp_username=&currency=1&extra=&fee_amount=0&input_charset=1&order_no=20151127160759&pay_result=1&pay_time=20151127160909&pay_type=2&sign_method=1&sp_no=9000100005&total_amount=1&transport_amount=0&unit_amount=1&unit_count=1&version=2&sign=20b1e003ec8a3c0f28ef223450493af1'
    if BaiFuBao.check_sign(params, baifubao_key):
        print 'check ok'
    else:
        print 'check fail'

def test_precreate():
    baifubao_sp_no = '9000100005'
    baifubao_key = 'pSAw3bzfMKYAXML53dgQ3R4LsKp758Ss'
    baifubao = BaiFuBao(baifubao_sp_no, baifubao_key)
    inputs = {}
    inputs['order_create_time'] = time.strftime('%Y%m%d%H%M%S') # YYYYMMDDHHMMSS
    inputs['order_no'] = int(time.time())
    inputs['total_amount'] = 100    #1 RMB
    inputs['return_url'] = notiful_url
    try:
        params = baifubao.precreate(inputs)
    except Exception, e:
        print traceback.format_exc()
    else:
        print 'params: %s' % params

if __name__ == '__main__':
    import time
    #test_check_sign()
    #test_precreate()
    test_check_sign_1()


