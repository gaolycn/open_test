# coding: utf-8
import json
import logging
from qfcommon.base.tools import thrift_call
from qfcommon.thriftclient.session import Session
from qfcommon.conf import SESSION_CONF 

log = logging.getLogger()


class ApolloSession:
    def __init__(self, sessionid=None, expire=86400*3):
        self._sesid = sessionid
        self.expire = expire
        log.debug('sesid:%s', sessionid)
        self.data = {}

        self.load()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, val):
        self.data[key] = val

    def __contains__(self, key):
        return key in self.data

    def get(self, key, defval=None):
        return self.data.get(key, defval)

    def load(self, sesid=None):
        if not self._sesid and not sesid:
            return
        if sesid:
            self._sesid = sesid
        #log.debug('load session from %s with id:%s', self._addr, self._sesid)
        sesval = thrift_call(Session, 'session_get', SESSION_CONF, self._sesid)
        if sesval and sesval.ret == 0 and sesval.value:
            #log.debug('session value:%s, type:%s', sesval.value, type(sesval.value))
            self.data = json.loads(sesval.value)
            #log.debug('data:%s', self.data)

    def save(self):
        if self._sesid:
            ret = thrift_call(Session, "session_set", SESSION_CONF, self._sesid, json.dumps(self.data, separators=(',', ':')))
            if ret != 0:
                log.warn('session set error, key=%s ret=%s', self._sesid, str(ret))
        else:
            #sesval = thrift_call(Session, "session_create", SESSION_CONF, json.dumps(self.data, separators=(',', ':')))
            sesval = thrift_call(Session, "session_create_expire", SESSION_CONF, json.dumps(self.data, separators=(',', ':')), expire=self.expire)
            if sesval and sesval.ret == 0:
                self._sesid = sesval.skey

    def clean(self):
        self.data = {}

    def logout(self):
        ret = thrift_call(Session, "session_delete", SESSION_CONF, self._sesid)
        if ret != 0:
            log.warn('session delete error, sesid:%s ret:%d', self._sesid, ret)

class ApolloUser:
    def __init__(self, userid='', sessionid='', expire=86400*3):
        self.userid  = str(userid)
        self.ses = ApolloSession(sessionid, expire)
        self.data = {}

        if not self.userid:
            self.userid = str(self.ses.get('userid', ''))
            self.data['userid'] = self.userid

    def is_login(self):
        if not self.ses:
            return False
        return bool(self.ses.get('userid', ''))

    def login(self, userid=''):
        if self.ses.get('userid', ''):
            return
        if userid:
            self.userid = str(userid)
        self.ses['userid'] = self.userid

    def logout(self):
        if self.ses:
            self.ses.logout()

    def load_session(self, sessionid):
        self.userid = str(self.ses.get('userid', ''))
        self.data['userid'] = self.userid

    def __str__(self):
        return '<ApolloUser userid:%s ses:%s data:%s>' % (self.userid, self.ses.data, self.data)
    
def user_from_session(sessionid, load_now=True):
    user = ApolloUser(sessionid=sessionid)
    #user.load_session(sessionid)
    if load_now:
        user.load()
    return user

