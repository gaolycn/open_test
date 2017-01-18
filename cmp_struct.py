#coding: utf-8

import os, sys
import traceback
import types

class CmpStructure(object):
    def cmp_object(self, o1, o2):
        if type(o1) != type(o2):
            return False
        if isinstance(o1, types.DictType):
            return self.cmp_dict(o1, o2)
        elif isinstance(o1, (types.ListType, types.TupleType)):
            return self.cmp_list(o1, o2)
        else:
            return True

    def cmp_list(self, lst1, lst2):
        for i in range(0, min(len(lst1), len(lst2))):
            if not self.cmp_object(lst1[i], lst2[i]):
                return False
        if len(lst1) == len(lst2):
            return True
        #后续元素的类型必须相同
        if len(lst1) > len(lst2):
            last_e = lst1[max(len(lst2)-1, 0)]
            for i in range(len(lst2), len(lst1)):
                if not self.cmp_object(last_e, lst1[i]):
                    return False
        else:
            last_e = lst2[max(len(lst1)-1, 0)] 
            for i in range(len(lst1), len(lst2)):
                if not self.cmp_object(last_e, lst2[i]):
                    return False
        return True

    def cmp_dict(self, dict1, dict2):
        for k in dict1: 
            if k not in dict2 or not self.cmp_object(dict1[k], dict2[k]):
                return False 
        return True 

if __name__ == '__main__':
    o1 = {'respcd': '0000', 'respmsg': 'caller error', 'data': {}}
    o2 = {'respcd': '', 'respmsg': '', 'data': {}}
    print CmpStructure().cmp_object(o1, o2)

    o1 = {'respcd': '0000', 'respmsg': 'caller error', 'data': {'order_info': [{'order_id': 1234}, {'drder_id': 1234}]}}
    o2 = {'respcd': '', 'respmsg': '', 'data': {'order_info': [{'order_id': 0}]}}
    print CmpStructure().cmp_object(o1, o2)
