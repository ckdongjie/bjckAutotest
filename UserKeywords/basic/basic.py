# coding = 'utf-8'
'''
Created on 2022年10月17日

@author: dj
'''
'''
    获取当前时间，以记录log
'''

from datetime import datetime
import logging
from time import sleep

import allure


def key_get_time():
    nowtime = datetime.now()
    nowtime.strftime('%Y-%m-%d %H:%M:%S')
    timeStr = str(nowtime).split('.')[0]
    return timeStr

'''
    操作等待
    sec:等待时间，单位：秒
'''
def key_wait(sec):
    with allure.step(key_get_time() +": 等待 "+str(sec)+"s......\n"):
        logging.info(key_get_time()+': wait for '+str(sec)+'s......')
        sleep(sec)
