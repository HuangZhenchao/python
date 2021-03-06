#! /usr/bin/env python  

_global_dict = {}

def set_global_value(key,value):
    """ 定义一个全局变量 """
    global _global_dict
    _global_dict[key] = value


def get_global_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    global _global_dict
    try:
        return _global_dict[key]
    except KeyError:
        return defValue