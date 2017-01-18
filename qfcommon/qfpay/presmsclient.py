# coding=utf-8

import logging
import traceback
import re
import types

from qfcommon.thriftclient.presms import PreSmsThriftServer
from qfcommon.server.client import ThriftClient

presmsClient_log = logging.getLogger("presmslog")

class PreSms():
    
    _MOBILESS_RE = '^(1\d{10},)*(1\d{10},?)$'
   
    
    
    def __init__(self, server, batch_mode=True):
        '''
        batch_mode是否是批量模式。True为批量模式，放在服务器端进行批量发送
        '''
        self.server = server
        self.batch_mode = batch_mode

    def _ping(self):
        '''
        检查服务接口
        '''
        try:
            self.thriftClient.call('ping')
        except:
            presmsClient_log.error(traceback.format_exc())
    
    def _checkphones(self, phones):
        '''
        检查手机号码是否正确
        '''
        phonestr = ""
        # 类型检查
        if type(phones) in (types.ListType, types.TupleType) :
            phonestr = ','.join(phones)
        elif type(phones) in (types.StringType, types.IntType):
            phonestr = str(phones)
        elif type(phones) == types.UnicodeType:
            phonestr = phones.encode("utf-8")
        else:
            return False, None
        
        # 格式检查
        if re.match(self._MOBILESS_RE, phonestr):
            return True, phonestr
        
        return False, None
    
    def sendSms(self, mobile, content, tag, source, target):
        '''
        发送短信
        mobile，短信的发送对象，可以是元组或者数组，也可以是单一的字符串，如果是字符串，必须符合手机格式
        content：短信内容，
        tag：标签，分类，
        source: 哪里调用
        target:作用是什么
        '''
        if not mobile or not content:
            return False, "参数为空" 
        
        
        checkresult, phone = self._checkphones(mobile)
        if not checkresult:
            return False, "手机号码格式不合法"
        # 转编码，统一使用utf-8
        if isinstance(content, types.UnicodeType):
            content = content.encode('utf-8')
        if isinstance(tag, types.UnicodeType):
            tag = tag.encode('utf-8')
        if isinstance(source, types.UnicodeType):
            source = source.encode('utf-8')
        if isinstance(target, types.UnicodeType):
            target = target.encode('utf-8')
        
        try:
            flag = 0
            if self.batch_mode:
                flag = ThriftClient(self.server, PreSmsThriftServer).call('sendsms', phone, content, tag, source, target)
            else:
                phonelist = phone.split(",")
                for p in phonelist:
                    ThriftClient(self.server, PreSmsThriftServer).call('sendsms', p, content, tag, source, target)
                flag = 1
            if flag >= 0:
                return True, "成功"
        except:
            presmsClient_log.error(traceback.format_exc())
            
        return False, "发送失败"
    
    
    def reportSms(self, mobile, jsoncontent, source="payserver", target="receipt"):
        '''
        发送短信
        mobile，短信的发送对象，可以是元组或者数组，也可以是单一的字符串，如果是字符串，必须符合手机格式
        json：短信内容，json结构
        source: 哪里调用,默认是payserver
        target:作用是什么，默认是receipt
        '''
        if not mobile or not jsoncontent:
            return False, "参数为空" 
        
        
        checkresult, phone = self._checkphones(mobile)
        if not checkresult:
            return False, "手机号码格式不合法"
        
        try:
            flag = 0
            if self.batch_mode:
                flag = ThriftClient(self.server, PreSmsThriftServer).call('sendcustomersms', phone, jsoncontent, source, target)
            else:
                phonelist = phone.split(",")
                for p in phonelist:
                    ThriftClient(self.server, PreSmsThriftServer).call('sendcustomersms', p, jsoncontent, source, target)
                flag = 1
            if flag >= 0:
                return True, "成功"
        except:
            presmsClient_log.error(traceback.format_exc())
            
        return False, "发送失败"
