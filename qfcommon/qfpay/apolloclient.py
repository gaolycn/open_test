# coding=utf-8
import json
import types
import logging
import traceback

from qfcommon.conf import SESSION_CONF
from qfcommon.thriftclient.session import Session
from qfcommon.base.tools import thrift_callex

from qfcommon.thriftclient.apollo.ttypes import User, UserProfile, UserService, ApolloException, UserQuery, UserCate
from qfcommon.thriftclient.apollo import ApolloServer
from qfcommon.server.client import ThriftClient
from qfcommon.qfpay.apollouser import ApolloUser

log = logging.getLogger()

class ApolloRet:
    APOLLO_ERR_USER       = "1001"
    APOLLO_ERR_PARAM      = "1002"
    APOLLO_ERR_UNKNOWN    = "1003"
    APOLLO_ERR_INTERNAL   = "1004"
    APOLLO_ERR_DBERR      = "1005"
    APOLLO_ERR_USER_EXIST = "1006"
    APOLLO_ERR_USER_NOT_EXIST = "1007"
    APOLLO_ERR_PASSWD         = "1008"

mapping = {
    ApolloRet.APOLLO_ERR_USER       : "用户信息不存在",
    ApolloRet.APOLLO_ERR_PARAM      : "参数错误",
    ApolloRet.APOLLO_ERR_DBERR      : "数据库错误",
    ApolloRet.APOLLO_ERR_UNKNOWN    : "未知错误",
    ApolloRet.APOLLO_ERR_USER_EXIST : "用户已经注册",
    ApolloRet.APOLLO_ERR_USER_NOT_EXIST : "用户未注册",
    ApolloRet.APOLLO_ERR_PASSWD     : "密码不正确",
}

class Apollo(object):

    def __init__(self, server):
        self.server = server

    def _user_service_dict(self, data):
        if isinstance(data, UserService):
            ret = data.__dict__
        else:
            raise ValueError('user is not UserService type')
        return ret

    def user_service(self, userid, status = 1):
        '''
        获取用户开通的服务的接口
        params:
            userid: int, userid
            status: int, 状态
        return:
            user_service: list
        '''
        user_service = None
        try:
            ret = thrift_callex(self.server, ApolloServer, 'getUserServices', int(userid), status)
            log.debug('ret : %s' % ret)
            user_service = [self._user_service_dict(i) for i in ret]
        except ApolloException, e:
            log.debug('get user services error: %s' % e)
            user_service = []
        except:
            log.error(traceback.format_exc())
            user_service = []

        return user_service

    def set_user_service(self, userid, user_services):
        '''
        设置用户开通的服务的接口
        params:
            userid: int, userid
            user_services: list<UserSerive>, 列表
        '''
        ret = {}
        try:
            ret = thrift_callex(self.server, ApolloServer, 'setUserServices', int(userid), user_services)
            ret = {k:v for k, v in ret.iteritems() if v}
            if ret:
                log.warn('set user service error : %s' % ret)
        except ApolloException, e:
            log.debug('set user services error: %s' % e)
        except:
            log.error(traceback.format_exc())

    def set_user_category(self, userid, user_categorys):
        '''
        设置用户角色的接口
        params:
            userid: int, userid
            user_categorys: list<userCategory>, 列表
        '''
        try:
            ret = thrift_callex(self.server, ApolloServer, 'setUserCategory', int(userid), user_categorys)
            log.debug('ret : %s' % ret)
            ret = {k:v for k, v in ret.iteritems() if v}
            if not ret:
                return True
            else:
                log.warn('set user category error : %s' % ret)
        except ApolloException, e:
            log.debug('set user category error: %s' % e)
        except:
            log.error(traceback.format_exc())
        return False

    def signup(self, userprofile, recommenduid=None, recommendtype=1, allow_exist=True):
        '''
        用户注册接口
        params:
            userprofile: UserProfile, 用户信息
        return:
            userid : str, 用户id; None, 注册失败
            respmsg : str, 如果注册失败, 返回的提示信息将放在里面放回
        '''
        userid = None
        try:
            try:
                if recommenduid:
                    userid = thrift_callex(self.server, ApolloServer, 'registerUserWithRecommend', userprofile, recommenduid, recommendtype)
                else:
                    userid = thrift_callex(self.server, ApolloServer, 'registerUser', userprofile)
            except ApolloException, e:
                log.debug('signup error: %s' % e)
                if e.respcd == ApolloRet.APOLLO_ERR_USER_EXIST:
                    if not allow_exist:
                        return None, '商户已经注册'

                    mobile, user_cates = userprofile.user.mobile, [_.__dict__ for _ in (userprofile.user.userCates or [])]
                    user = self.user_by_mobile(mobile)
                    userid = user['uid']

                    add_user_cates = set([i['code'] for i in user_cates]) - set([i['code'] for i in user['userCates']])
                    if add_user_cates:
                        log.warn('%s need add user_cates: %s' % (userid, add_user_cates))
                        user_cate_names = {i['code'] : i['name'] for i in user_cates}
                        add_user_cates  = [UserCate(code=i, name=user_cate_names[i]) for i in add_user_cates]
                        self.set_user_category(userid, add_user_cates)

                    return userid, mapping.get(e.respcd, '未知错误')

            else:
                log.debug('signup userid:%s' % userid)
                return userid, None

        except:
            log.error(traceback.format_exc())
        return None, '系统繁忙'

    def auth(self, username, password, user_cates=None, expire=86400*3, kickuser=False, set_session=True):
        '''
        检查用户密码接口
        params:
            username: str, 用户手机号码
            password: str, 密码
            user_cates: str or list, 允许登录的用户角色
            expire: int, 有效期(单位秒)
            kickuser: bool, 是否剔除商户
            set_session: 是否设置session
        return:
            userinfo: dict, 用户信息; None, 登录失败
        '''
        userinfo = None
        try:
            r = thrift_callex(self.server, ApolloServer, 'checkUser', username, password)
            # 检验用户登录
            if r == 0:
                userinfo = self.user_by_mobile(username)
                if not userinfo:
                    raise ValueError('get user by mobile error')
                userid = userinfo.get('uid', '')
            else:
                raise ValueError('check user fail')

            # 验证用户角色
            if user_cates:
                if isinstance(user_cates, (types.UnicodeType, types.StringType)):
                    allow_cates = set([user_cates])
                elif isinstance(user_cates, (types.ListType, types.TupleType)):
                    allow_cates = set(user_cates)
                else:
                    raise ValueError('user_cates type error')
                userCates = set([i['code'] for i in userinfo['userCates']])
                if not(allow_cates & userCates):
                    raise ValueError('user_cates error')
        except ApolloException, e:
            log.debug('login error: %s' % e)
            raise ValueError(mapping.get(e.respcd, '用户登录失败'))
        except ValueError, e:
            log.debug(str(e))
            userid = None
        except:
            log.debug(traceback.format_exc())
            userid = None

        if userid:
            # 剔除用户
            if kickuser:
                thrift_callex(SESSION_CONF, Session, 'user_offline', [userid])

            # 设置session
            if set_session:
                user = ApolloUser(userid, expire = expire)

                # 存储userCates
                user.ses['userCates'] = userinfo['userCates']
                user.login(userid)
                user.ses.save()

                userinfo['sessionid'] = user.ses._sesid

            log.debug('user %s auth success', username)
        else:
            log.debug('user %s auth failed', username)
            userinfo = None

        return userinfo

    def change_pwd(self, username,  old_password, new_password):
        '''
        修改用户密码
        params:
            username: str, 用户账号
            old_password: str, 用户旧密码
            new_password: str, 用户新密码
        return:
            ret: str  True, 成功;False, 失败
        '''
        try:
            user = self.auth(self, username, old_password, expire=86400*3)
            if not user:
                raise ValueError('old password is not true')
            ret = ThriftClient(self.server, ApolloServer).call('changePwd',  user.ses.get('userid'), new_password)
            if ret == 0:
                return True
            else:
                raise ValueError('change password fail')
        except ValueError, e:
            log.warn(str(e))
        except:
            log.error(traceback.format_exc())

        return False

    def _user_dict(self, user):
        if isinstance(user, User):
            ret = user.__dict__
            ret['userCates'] = ret['userCates'] or []
            ret['userCates'] = [_.__dict__ for _ in ret['userCates']]
            return ret
        else:
            raise ValueError('user is not User type')

    def _userprofile_dict(self, userprofile):
        if isinstance(userprofile, UserProfile):
            ret = userprofile.__dict__
            ret['user'] = self._user_dict(ret['user'])
            ret['bankInfo'] = ret['bankInfo'].__dict__
            ret['userTags'] = ret['userTags'] or []
            ret['userTags'] = [_.__dict__ for _ in ret['userTags']]
            ret['relations'] = ret['relations'] or []
            ret['relations'] = [self._user_dict(i) for i in ret['relations']]
            return ret
        else:
            raise ValueError('user is not User type')

    def user_by_mobile(self, mobile):
        '''
        获取用户基本信息
        params:
            mobile: str, 用户手机号码
        return:
            user: dict, 用户基本信息; None, 获取用户信息失败
        '''
        user = None
        try:
            ret  = ThriftClient(self.server, ApolloServer).call('findUserByMobile', mobile)
            user = self._user_dict(ret)
        except ValueError,e:
            log.debug(str(e))
            user = None
        except:
            log.debug(traceback.format_exc())
            user = None

        return user

    def user_by_id(self, userid):
        '''
        获取用户基本信息
        params:
            userid: str, 用户id
        return:
            user: dict, 用户基本信息; None, 获取用户信息失败
        '''
        user = None
        try:
            ret  = ThriftClient(self.server, ApolloServer).call('findUserByid', int(userid))
            user = self._user_dict(ret)
        except ValueError,e:
            log.debug(str(e))
            user = None
        except:
            log.debug(traceback.format_exc())
            user = None

        return user

    def userprofile_by_id(self, userid):
        '''
        获取用户详细信息
        params:
            userid: str, 用户id
        return:
            userprofile: dict, 用户信息; None, 获取用户信息失败
        '''
        userprofile = None
        try:
            ret = ThriftClient(self.server, ApolloServer).call('findUserProfileByid', int(userid))
            userprofile = self._userprofile_dict(ret)
        except:
            log.debug(traceback.format_exc())
            userprofile = None
        log.debug('userprofile: %s' % userprofile)

        return userprofile

    def user_by_ids(self,useridlist):
        '''
        获取用户集的一些基本信息
        params:
            userlist :list ,用户id list
        '''
        users_ret = None
        try:
            q = UserQuery(uids=useridlist)
            ret = ThriftClient(self.server,ApolloServer).call('findUsers',q)
            users_ret = ret
        except:
            log.debug(traceback.format_exc())
            users_ret = None
        return users_ret

    def userids_by_linkid(self,uid,link_cate):
        '''
        获取商户所属关系
        params:
            userid:str  用户id
        return:
            list :[userid,....]
        '''
        useridlist = []
        try:
            ret = ThriftClient(self.server, ApolloServer).call('getUserRelation',int(uid),link_cate)
            useridlist = ret
        except:
            log.debug(traceback.format_exc())
        return useridlist

    def reverse_userids(self,linkid,link_cate):
        '''
        获取商户的逆所属关系
        params:
            userid:str  用户id
        return:
            list :[userid,....]
        '''
        userids = []
        try:
            userids = ThriftClient(self.server, ApolloServer).call('getUserReverseRelation',int(linkid),link_cate)
        except:
            log.debug(traceback.format_exc())

        return userids

    def set_user_relation(self, userid, relations):
        '''
        获取商户的逆所属关系
        params:
            userid:str  用户id
            relations: list(relations)
        return:
            ret : True, ''
        '''
        relations = relations if isinstance(relations, (types.TupleType, types.ListType)) else  [relations]
        try:
            r = ThriftClient(self.server, ApolloServer).call('setUserRelation', int(userid), relations)
            if not r:
                return True, ''
            else:
                log.debug('r:%s' % r)
                return False,  ','.join(r.values())
        except:
            log.warn(traceback.format_exc())
            raise Exception('设置用户关系失败')

    def check_user_permission(self, uid, code):
        '''
        检验用户权限
        params:
            uid: int, 用户id
            code: str, 权限code
        return:
            True, 有权限; False, 无权限.
        '''
        try:
            r = ThriftClient(self.server, ApolloServer).call('checkUserPermission', int(uid), code)
            return bool(r == 0)
        except:
            log.debug(traceback.format_exc())

    def get_user_cate(self, uid):
        '''
        获取用户所有角色
        params:
            uid: int, userid
        return:
            []
        '''
        r = []
        try:
            r = ThriftClient(self.server, ApolloServer).call('getUserCategory', int(uid), json.dumps({}))
            r = [i.__dict__ for i in r ]
        except:
            log.debug(traceback.format_exc())

        return r
