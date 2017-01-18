# coding: utf-8
"""定义推送服务中使用到的一些常量."""


class Platform(object):
    """推送平台"""
    IOS = 'ios'
    Android = 'android'
    PC = 'pc'

    @classmethod
    def contains(cls, platform):
        return platform in (Platform.IOS, Platform.Android, Platform.PC)


class MsgType(object):
    """消息类型"""
    Multi = 1  # 通过 userid 推送
    MultiDevice = 2  # 通过 deviceid 推送
    Group = 11  # 通过分组推送
    All = 21  # 全量推送

    @classmethod
    def contains(cls, msgtype):
        return msgtype in (MsgType.Multi, MsgType.MultiDevice, MsgType.Group, MsgType.All)


KEY_PREFIX = 'qfpush'


class MsgKeyFormat(object):
    """pushentry <--> pushswift 之间通信时使用的 key."""
    MESSAGE = KEY_PREFIX + ':msg:{msgid}'
    MESSAGE_STAT = KEY_PREFIX + ':msg_stat:{msgid}'
    QUEUE = {
        Platform.Android: KEY_PREFIX + ':queue:android',
        Platform.IOS: KEY_PREFIX + ':queue:ios',
        Platform.PC: KEY_PREFIX + ':queue:pc',
    }


class PushcoreKeyFormat(object):
    """pushswift <--> pushcore 之间通信时使用的 key."""
    MESSAGE = KEY_PREFIX + ':pushcore:message:{msgid}'
    QUEUE = KEY_PREFIX + ':pushcore:{deviceid}:{apptype}'
    RECORD = KEY_PREFIX + ':pushcore:record:{pushid}'
