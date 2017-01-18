# coding: utf-8

import json
from bs4 import BeautifulSoup
import logging

from qfcommon.thriftclient.qf_wxmp import QFMP
from qfcommon.thriftclient.qf_wxmp.ttypes import MPError
from qfcommon.thriftclient.qf_wxmp.ttypes import PageQuery
from qfcommon.thriftclient.qf_wxmp.ttypes import KFMsgType, KFMsg
from qfcommon.thriftclient.qf_wxmp.ttypes import Reply, ReplyType, ReplyQuery

from qfcommon.base.tools import thrift_callex
from qfcommon.qfpay.qfresponse import QFRET

log = logging.getLogger()


MP_ENABLE  = 1  # 公众号的状态为启用
MP_DISABLE = 0  # 公众号的状态为不启用

class LocationKey(object):
    MASTER_KEY = 'location'         # 欢迎消息, 欢迎消息只是一个框架，只有头与尾，具体内容是下面的信息
    SALE_KEY   = 'location-sale'    # 欢迎消息中的特卖
    COUPON_KEY = 'location-coupon'  # 欢迎消息中的红包
    ADV_KEY    = 'location-adv'     # 欢迎消息中的广告

    _KEYS = (MASTER_KEY, SALE_KEY, COUPON_KEY, ADV_KEY)

    _KEY_TO_WEIGHT = {
        MASTER_KEY: 100,
        SALE_KEY  : 80,
        COUPON_KEY: 70,
        ADV_KEY   : 90,
    }

    def __contains__(self, key):
        return key in self._KEYS

    def __str__(self):
        return str(self.KEYS)
    __repr__ = __str__

    def key2weight(self, key):
        '''获取key默认对应的权重'''
        if key not in self:
            log.warn('key is invalid:%s', key)
            return 1
        return self._KEY_TO_WEIGHT[key]

LOCATION_KEY = LocationKey()



class MPClient(object):
    '''连接公众号服务的客户端'''
    LOCATION_SEPARATOR = '{content}'

    def __init__(self, server, appid, openid=''):
        self.server = server
        self.appid  = appid
        self.openid = openid

    def msg_send(self, msg_type, msg):
        req_args = KFMsg()
        req_args.appid       = self.appid
        req_args.openid      = self.openid
        req_args.msg_type    = msg_type
        req_args.msg_content = json.dumps(msg)
        return thrift_callex(self.server, QFMP, 'msg_send', req_args)

    def msg_send_text(self, content):
        '''发送文本消息'''
        send_msg = {
            'content': content,
        }
        return self.msg_send(KFMsgType.TEXT, send_msg)

    def msg_send_img(self, media_id):
        '''发送图片消息'''
        send_msg = {
            'media_id': media_id
        }
        return self.msg_send(KFMsgType.IMAGE, send_msg)

    def msg_send_voice(self, media_id):
        '''发送语音消息'''
        send_msg = {
            'media_id': media_id
        }
        return self.msg_send(KFMsgType.VOICE, send_msg)

    def msg_send_video(self, media_id, thumb_media_id='', title='', description=''):
        '''
            发送视频消息
            media_id      : 视频的id
            thumb_media_id: 缩略图的媒体ID, 非必传
            title         : 视频消息的标题, 非必传
            description   : 视频消息的描述, 非必传
        '''
        send_msg = {
            'media_id'      : media_id,
            'thumb_media_id': thumb_media_id,
            'title'         : title,
            'description'   : description,
        }
        return self.msg_send(KFMsgType.VIDEO, send_msg)

    def msg_send_music(self, musicurl, hqmusicurl, thumb_media_id, title='', description=''):
        '''
            发送音乐消息
            musicurl      : 音乐的链接
            hqmusicurl    : 高品质音乐链接，wifi环境优先使用该链接播放音乐
            thumb_media_id: 缩略图的媒体ID
            title         : 音乐消息的标题, 非必传
            description   : 音乐消息的描述, 非必传
        '''
        send_msg = {
            'title'         : title,
            'description'   : description,
            'musicurl'      : musicurl,
            'hqmusicurl'    : hqmusicurl,
            'thumb_media_id': thumb_media_id,
        }
        return self.msg_send(KFMsgType.MUSIC, send_msg)

    def msg_send_news(self, urls, picurls, titles, descriptions):
        '''
            发送图文消息, 点击跳转到外链
            url         : 图文消息被点击后跳转的链接
            description : 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图640*320，小图80*80
            title       : 图文消息的标题, 非必传
            description : 图文消息的描述, 非必传
            以前4个元素，如果需要发送多个，
        '''
        NEWS_NUM = 8
        send_msg = []
        if not isinstance(titles, (list, tuple)) or \
                not isinstance(descriptions, (list, tuple)) or \
                not isinstance(urls, (list, tuple)) or \
                not isinstance(picurls, (list, tuple)):
            log.warn('titles or descriptions or urls or picurls type is invalid. titles:%s descriptions:%s urls:%s picurls:%s',
                titles, descriptions, urls, picurls)
            raise MPError(QFRET.PARAMERR, 'param type is invalid')
        if len(titles) != len(descriptions) != len(urls) != len(picurls):
            log.warn('titles, descriptions, urls, picurls len isnot eq. titles:%s descriptions:%s urls:%s picurls:%s',
                titles, descriptions, urls, picurls)
            raise MPError(QFRET.PARAMERR, 'param len is invalid')
        params_num = len(titles)
        if params_num > NEWS_NUM or params_num <= 0:
            log.warn('0 < param num <= 8. param num:%d', params_num)
            raise MPError(QFRET.PARAMERR, 'param len is invalid')
        for i in range(params_num):
            item = {
                'title'      : titles[i],
                'description': descriptions[i],
                'url'        : urls[i],
                'picurl'     : picurls[i],
            }
            send_msg.append(item)
        return self.msg_send(KFMsgType.NEWS_LINK, send_msg)

    def msg_send_mpnews(self, media_id):
        '''发送图文消息, 点击跳转到图文消息页面'''
        send_msg = {
            'media_id': media_id
        }
        return self.msg_send(KFMsgType.NEWS_ID, send_msg)

    def msg_send_card(self, card_id, code):
        '''
            发送卡券消息
            card_id : 卡券id
            code    : 卡券code
        '''
        # 如果这里出现异常，直接抛出去，调用方需要捕获
        card_ext = thrift_callex(self.server, QFMP, 'card_ext', self.appid, card_id, code)
        send_msg = {
            'card_id' : card_id,
            'card_ext': card_ext,
        }
        return self.msg_send(KFMsgType.WXCARD, send_msg)

    def reply_save_location(self, key, title='', tail='', link='', weight=-1, content='', status=MP_ENABLE):
        '''
            保存地理位置的文本回复
            key: LocationKey的类变量
            title: 消息的头
            tail: 消息的尾
            link: 消息的尾如果是个链接，则给出链接地址, 如果tail不存在，则link无意义
            weight: 消息的权重, 如果有多个消息，可能会显示消息个数, 权重值越高，越优先显示
            如果这里出现异常，直接抛出去，调用方需要捕获
        '''
        # 验证key
        key = key.lower()   # key必须是小写
        if key not in LOCATION_KEY:
            log.warn('key is invalid:%s', key)
            return -1
        # 获取默认的权重
        if weight <= 0:
            weight = LOCATION_KEY.key2weight(key)
        # 转换消息尾
        if tail and link:
            new_tail = '<a href="%s">%s</a>' % (link, tail)
        else:
            new_tail = tail
        #log.debug('title:%s  new_tail:%s', title, tail)
        if title or new_tail:
            push_txt = title + self.LOCATION_SEPARATOR + new_tail
        else:
            push_txt = None
        # 拼接请求参数
        req_args = Reply()
        req_args.appid = self.appid
        req_args.mp_key = key
        req_args.push_type = ReplyType.TEXT
        req_args.push_txt = push_txt
        req_args.content = content
        req_args.status = status
        req_args.weight = weight
        # 请求
        log.debug('req_args:%s', req_args)
        resp_data = thrift_callex(self.server, QFMP, 'reply_save', req_args)
        log.info('resp_data:%s', resp_data)
        return resp_data

    def reply_query_location(self, key=None, page_curr=1, page_size=20):
        '''
            地理位置的文本回复
            key:  LocationKey的类变量
            page_curr: 分页查询时的页数
            page_size: 分页查询时每页显示的数量
            如果这里出现异常，直接抛出去，调用方需要捕获
            返回结果中，extitle, extail, exlink开头，为解析push_txt后的数据
        '''
        #log.debug('key:%s', key)
        if isinstance(key, str):
            key = [key, ]
        if not key:
            key = LOCATION_KEY._KEYS
        # 拼接请求参数
        page = PageQuery()
        page.num  = page_curr
        page.size = page_size
        req_args  = ReplyQuery()
        req_args.appid   = self.appid
        req_args.mp_keys = key
        req_args.page    = page
        # 请求
        log.debug('req_args:%s', req_args)
        resp_data = thrift_callex(self.server, QFMP, 'reply_query', req_args)
        log.info('resp_data:%s', resp_data)
        # 解析数据
        # 如果是文本推送，拆分成title, tail, link
        for item in resp_data.data:
            # 默认的值
            item.extitle = ''   
            item.extail  = ''
            item.exlink  = ''
            if item.push_type != ReplyType.TEXT:
                continue
            # 文本推送，解析推送内容
            push_txt_item = item.push_txt.split(self.LOCATION_SEPARATOR)
            item_cnt = len(push_txt_item)
            if item_cnt == 1:
                item.extitle = push_txt_item[0]
            elif item_cnt == 2:
                item.extitle = push_txt_item[0]
                if push_txt_item[1]:
                    # 解析html数据
                    soup = BeautifulSoup(push_txt_item[1], 'html.parser')
                    a_tag = soup.a
                    if a_tag:
                        item.extail = a_tag.text
                        item.exlink = a_tag['href']
                        # thrift请求，返回值都是utf-8，所以这里也把编码统一为utf-8
                        if isinstance(item.extail, unicode):
                            item.extail = item.extail.encode('utf-8')
                        if isinstance(item.exlink, unicode):
                            item.exlink = item.exlink.encode('utf-8')
                    else:
                        item.extail = push_txt_item[1]
        return resp_data




