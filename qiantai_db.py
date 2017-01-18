#coding: utf-8

from qfcommon.base import dbpool
from qfcommon.base.dbpool import with_database
import sys,os
HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HOME))
import qiantai_config

dbpool.install(qiantai_config.DATABASE)

class test:

    @with_database('qiantai')
    def get_customer(self):
        where = {
            'app_code':qiantai_config.TEST_APP['app_code'],
        }
        appid =self.db.select_one('app', fields='id', where=where)
        where1 = {
                'app_id':str(appid['id']),
                }
        ret = self.db.select('customer', where=where1, fields='`balance`,`out_user`', other = 'LIMIT 10')
        if not ret :
            return "error"
        return ret 

    @with_database('qf_open')
    def get_cate_info(self,id):
        where = {
            'id': id,
        }
        ret = self.db.select_one('cate', fields='`name`,`descr`,`available`', where=where)
        if not ret :
            return "error"
        return ret 
    @with_database('qf_open')
    def del_goods_info(self):
        where = {
            'name': ('like','商品%'),
        }
        ret = self.db.delete('goods',  where=where)
        if not ret :
            return "error"
        return ret 
    
    @with_database('qf_open')
    def del_cate_info(self):
        where = {
            'name': ('like','商品%'),
        }
        ret = self.db.delete('cate',  where=where)
        if not ret :
            return "error"
        return ret 

    @with_database('qf_open')
    def get_goods_info(self,id):
        where = {
            'id': id,
        }
        ret = self.db.select_one('goods', fields='`name`,`descr`', where=where)
        if not ret :
            return "error"
        return ret 

if __name__ == '__main__':
    test1 = test()
    #mobile = '13911659430'
    test1.del_goods_info()
