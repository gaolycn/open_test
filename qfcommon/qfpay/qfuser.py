# coding: utf-8
import hashlib
import json
import logging
from qfcommon.base.tools import thrift_call
from qfcommon.base import dbpool
from qfcommon.thriftclient.session import Session
from qfcommon.conf import SESSION_CONF, USER_DB, FRAMEWORK

log = logging.getLogger()


class QFSession:
    def __init__(self, sessionid=None, expire=86400*3):
        self._sesid = sessionid
        self.expire = expire
        log.debug('sesid:%s', sessionid)
        self.data = {}
        self._config = {
            'name': 'sessionid',
            'domain': None,
            'path': '/',
            'httponly': False,
            'secure': False
        }

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

        if FRAMEWORK == 'web':
            self._setcookie()

    def _setcookie(self, expires=''):
        log.debug('setcookie:%s', self._sesid)
        import web
        web.setcookie(self._config['name'],
                      self._sesid,
                      expires=expires,
                      domain=self._config['domain'],
                      httponly=self._config['httponly'],
                      secure=self._config['secure'],
                      path=self._config['path'])

    def clean(self):
        self.data = {}

    def logout(self):
        ret = thrift_call(Session, "session_delete", SESSION_CONF, self._sesid)
        if ret != 0:
            log.warn('session delete error, sesid:%s ret:%d', self._sesid, ret)


class QFUser:
    def __init__(self, userid = 0, sessionid='', expire=86400*3):
        self.userid  = int(userid)
        self.ses = QFSession(sessionid, expire)
        self.data = {}

        if self.userid == 0:
            self.userid = int(self.ses.get('userid', 0))
            self.data['userid'] = self.userid
            self.data['opuid']  = int(self.ses.get('opuid', 0))
        elif self.userid > 0:
            self.load()

    @dbpool.with_database(USER_DB)
    def load(self):
        if self.userid <= 0:
            log.debug('no userid')
            return

        sql = "select merchant_code,state from auth_user where id=%d" % self.userid
        log.debug(sql)
        ret = self.db.get(sql)
        if not ret:
            log.debug('not found user %d in auth_user', self.userid)
            return
        self.data['usercd'] = ret['state']
        self.data['mchntcd'] = ret['merchant_code']

        sql = "select nickname,name,province,city,bankaccount,bankuser,mobile,brchbank_code,groupid,mcc from profile where userid=%d" % self.userid
        log.debug(sql)
        ret = self.db.get(sql)
        if not ret:
            log.debug('not found user %d in profile', self.userid)
            return

        self.data['mchntnm'] = ret['nickname'] or ret['name']
        self.data['account'] = {'brchbank_code':ret['brchbank_code'],
                                'cardcd':ret['bankaccount'],
                                'name': ret['bankuser']}
        self.data['userid']  = self.userid
        self.data['province'] = ret['province']
        self.data['city'] = ret['city']
        self.data['mobile'] = ret['mobile']
        self.data['groupid'] = ret['groupid']
        self.data['mcc'] = ret['mcc']
        self.data['terminalids'] = []

        sql = "select terminalid from termbind where userid=%d" % self.userid
        ret = self.db.query(sql, isdict=False)
        log.debug(sql)
        if not ret:
            log.debug('user %d not have terminal', self.userid)
        else:
            self.data['terminalids'] = [ x[0] for x in ret ]


    def is_login(self):
        if not self.ses:
            return False
        return self.ses.get('userid', 0) > 0

    def login(self, userid=None):
        if self.ses.get('userid', 0) > 0:
            return
        if userid:
            self.userid = userid
        self.ses['userid'] = self.userid

    def logout(self):
        if self.ses:
            self.ses.logout()

    def load_session(self, sessionid):

        #self.ses.load(sessionid)

        self.userid = int(self.ses.get('userid', 0))
        self.data['userid'] = self.userid
        self.data['opuid']  = self.ses.get('opuid', '0')

    @dbpool.with_database(USER_DB)
    def has_perm(self, per_code_name):
        if self.userid <= 0:
            return False

        sql = "select id from auth_user where (id in (select user_id from auth_user_user_permissions t where t.permission_id in (select id from auth_permission where codename='%s')) or id in (select user_id from auth_user_groups t1 where t1.group_id in (select group_id from auth_group_permissions where permission_id in (select id from auth_permission where codename='%s'))) or is_superuser=1 ) and id=%d " %(per_code_name,per_code_name,self.userid)

        ret = self.db.get(sql)
        if ret:
            return True
        return False

    def __str__(self):
        return '<QFUser userid:%d ses:%s data:%s>' % (self.userid, self.ses.data, self.data)


class QFCustomer:
    def __init__(self, customer_id = 0, csessionid='', expire=60*60):
        self.customer_id  = int(customer_id)
        self.ses = QFSession(csessionid, expire)
        self.data = {}

        if self.customer_id == 0:
            self.customer_id= int(self.ses.get('customer_id', 0))

    def login(self, customer_id=None):
        if self.ses.get('customer_id', 0) > 0:
            return
        if customer_id:
            self.customer_id = int(customer_id)
        self.ses['customer_id'] = self.customer_id
        self.ses.save()

    def openid(self, appid, openid=None):
        if openid:
            if 'openids' not in self.ses.data:
                self.ses.data['openids'] = {}
            self.ses.data['openids'][appid] = openid

        return self.ses.data.get('openids',{}).get(appid, None)

    def logout(self):
        if self.ses:
            self.ses.logout()

    def is_login(self):
        if not self.ses:
            return False
        return self.ses.get('customer_id', 0) > 0

    def __str__(self):
        return '<QFCustomer cid:%d ses:%s data:%s>' % (self.customer_id, self.ses.data, self.data)

def user_from_session(sessionid, load_now=True):
    user = QFUser(sessionid=sessionid)
    #user.load_session(sessionid)
    if load_now:
        user.load()
    return user

def customer_from_session(csessionid):
    customer = QFCustomer(csessionid = csessionid)
    return customer

def get_hexdigest(algorithm, salt, raw_password):
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def constant_time_compare(val1, val2):
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


def check_password(raw_password, enc_password):
    algo, salt, hsh = enc_password.split('$')
    return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))


def auth(username, password, expire=86400*3, opuid=0):
    user = None
    db = dbpool.acquire(USER_DB)
    try:
        record = db.get("select id,password from auth_user where username='%s'" % db.escape(username))
        if opuid and record:
            op_record = db.select_one(table='opuser',
                                    where={'opuid': opuid,
                                           'userid': record['id'],
                                           'status': 1},
                                    fields='password')
            if op_record:
                record['password'] = op_record['password']
            else:
                record['password'] = 'sha1$1234$sssss'
    finally:
        dbpool.release(db)

    if record and check_password(password, record['password']):
        userid = record['id']
        user = QFUser(userid, expire=expire)
        user.login(userid)
        if opuid:
            user.ses['opuid'] = opuid
        user.ses.save()
        log.debug('user %s auth success', username)
    else:
        log.debug('user %s auth failed', username)

    return user

def with_customer(func):
    def _(self, *args, **kwargs):
        csid = self.get_cookie('csid')
        self.customer = customer_from_session(csid)
        ret = func(self, *args, **kwargs)
        if self.customer.ses.data:
            self.customer.ses.save()
            self.set_cookie('csid',
                            self.customer.ses._sesid)
            # XXX 这里应该指定cookie参数
            #self.set_cookie('csid',
            #                self.customer.ses._sesid,
            #                **config.COOKIE_CONFIG)
        return ret
    return _

def with_user(func):
    def _(self, *args, **kwargs):
        import web
        sessionid = web.cookies().get('sessionid')
        self.user = user_from_session(sessionid)
        ret = func(self, *args, **kwargs)
        if self.user.ses.data:
            self.user.ses.save()

        return ret
    return _

def with_user_tornado(func):
    def _(self, *args, **kwargs):
        sessionid = self.get_cookie('sessionid')
        self.user = user_from_session(sessionid, load_now = False)
        ret = func(self, *args, **kwargs)
        if self.user.ses.data:
            self.user.ses.save()
            if 'qfpay' in self.request.host:
                self.set_cookie('sessionid',
                             self.user.ses._sesid,
                             domain='.qfpay.com',
                             expires=None,
                             path='/',
                             expires_days=3,
                            )
            else:
                self.set_cookie('sessionid',
                             self.user.ses._sesid,
                             expires=None,
                             expires_days=3,
                            )
        return ret
    return _

def with_permission_tornado(per_code_name):
    import tornado.web
    def with_user_tornado(func):
        def _(self, *args, **kwargs):
            sessionid = self.get_cookie('sessionid')
            self.user = user_from_session(sessionid)
            #无权限返回403
            if not self.user.has_perm(per_code_name):
                raise tornado.web.HTTPError(403)
            ret = func(self, *args, **kwargs)
            if self.user.ses.data:
                self.user.ses.save()
                if 'qfpay' in self.request.host:
                    self.set_cookie('sessionid',
                                self.user.ses._sesid,
                                domain='.qfpay.com',
                                expires=None,
                                path='/',
                                expires_days=3,
                                )
                else:
                    self.set_cookie('sessionid',
                                self.user.ses._sesid,
                                expires=None,
                                expires_days=3,
                                )
            return ret
        return _
    return with_user_tornado


def test():
    import settings
    import web

    dbpool.install(settings.DATABASE)

    class Hello:
        @with_user
        def GET(self):
            print self.user
            print 'userid :', self.user.ses.get('userid', 0)

            if self.user.is_login():
                print 'user login'
            else:
                print 'user not login'

            if self.user.ses.data:
                print 'user:%d' % self.user.ses.get('userid', 0)
            else:
                print 'no user'
                self.user.userid = 10128
                self.user.login()

            return '<a href="/11">gogo</a>'

    urls = (
        '/.*', 'Hello'
    )

    app = web.application(urls, locals())
    app.run()



if __name__ == '__main__':
    test()

