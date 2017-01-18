# coding=utf-8

class HuiyiError(Exception):
    """
    汇宜异常基类
    """
    pass


class HuiyiBuildError(HuiyiError):
    """
    构建到钱方到汇宜的报文错误
    """

class HuiyiBuildHeaderError(HuiyiBuildError):
    """
    构建头部出错
    """


class HuiyiLackMustFieldError(HuiyiError):
    """
    8583报文中发现，缺少必填参数
    """


class HuiyiParseError(HuiyiError):
    """
    解析汇宜到钱方的报文错误
    """


class HuiyiCheckMacError(HuiyiParseError):
    """
    校验mac出错
    """


class HuiyiParseHeaderError(HuiyiParseError):
    """
    解析头部出错
    """