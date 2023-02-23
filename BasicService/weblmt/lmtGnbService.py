'''
Created on 2022年10月27日

@author: dj
'''
import logging

from BasicModel.weblmt.lmtGngModel import LmtGnbModel
from UserKeywords.basic.basic import key_get_time


class LmtGnbService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    '''
                登录weblmt
                参数：
        lmtIp:基站debug ip地址
        lmtPort:weblmt登录端口
    '''     
    def lmtLogin(self, lmtIp, lmtPort='8090'):
        lmt = LmtGnbModel().lmtLogin(lmtIp, lmtPort)    
        return lmt
    
    '''
                在weblmt上复位基站
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtRebootGnb(self, lmtObj):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtRebootGnb()
        if resCode == 200 and resInfo['result']== 'success':
            logging.warning(key_get_time()+': weblmt reboot gnb success')
            return True
        else:
            logging.warning(key_get_time()+': weblmt reboot gnb fail')
            return False
        