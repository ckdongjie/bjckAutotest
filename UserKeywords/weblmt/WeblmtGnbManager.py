# coding = 'utf-8'
from BasicModel.weblmt.weblmt import WebLmt
'''
Created on 2022年10月27日

@author: dj
'''

import logging

import allure

from BasicService.weblmt.lmtGnbService import LmtGnbService
from UserKeywords.basic.basic import key_get_time

'''
        说明：weblmt上复位基站
        参数：
    lmtObj:weblmt对象
'''
def key_weblmt_reboot_gnb(lmtObj):
    with allure.step(key_get_time() +": weblmt上复位基站："+lmtObj.ip+'\n'):
        logging.info(key_get_time()+': weblmt reboot gnb: '+lmtObj.ip)
        rebootRes = LmtGnbService().lmtRebootGnb(lmtObj)
        assert rebootRes == True, 'weblmt复位基站操作失败，请检查！'

'''
        说明：登录weblmt
        参数：
    lmtIp:weblmt ip地址
    lmtPort:weblmt端口号
'''        
def key_weblmt_login(lmtIp, lmtPort='8090'):
    with allure.step(key_get_time()+': 登录weblmt, ip:'+lmtIp):
        logging.info(key_get_time()+': login weblmt, ip: '+lmtIp)
        lmt = LmtGnbService().lmtLogin(lmtIp, lmtPort)
        return lmt
    
if __name__ == '__main__':
    key_weblmt_reboot_gnb('172.16.2.153', '8090')