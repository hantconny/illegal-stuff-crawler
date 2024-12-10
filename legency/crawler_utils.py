# -*- coding:utf-8 -*-
import time


def get_local_time(utc_ts_):
    """
    返回当地时间，而不是UTC时间
    :param utc_ts_:
    :return:
    """
    local_struct_time = time.localtime(utc_ts_)
    return time.strftime('%Y-%m-%d %H:%M:%S', local_struct_time)
