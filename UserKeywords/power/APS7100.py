# coding = 'utf-8'
'''
Created on 2023年1月5日

@author: autotest
'''
'''
    说明：登录程控电源
    参数：
    serialPort:程控电源串口号
    serialRate:程控电源串口速率
'''

import logging

import allure

from BasicService.power.APS7100Service import APS7100Service
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time


def key_login_aps7100(serialPort=BASIC_DATA['power']['serialPort'], serialRate=BASIC_DATA['power']['serialRate']):
    with allure.step(key_get_time() +":串口登录程控电源:"+serialPort+','+str(serialRate)):
        logging.info(key_get_time()+':login aps7100 by serial:'+serialPort+','+str(serialRate))
        aps7100 = APS7100Service().login_serial(serialPort, serialRate)
        return aps7100
    
'''
    说明：登出程控电源
    参数：
    aps7100:程控电源接口对象
'''
def key_logout_aps7100(aps7100):
    with allure.step(key_get_time() +":串口登出程控电源"):
        logging.info(key_get_time()+':logout aps7100')
        APS7100Service().logout_serial(aps7100)
    
'''
    说明：启动程控电源开关
    参数：
    aps7100:程控电源接口对象
'''
def key_power_on_aps7100(aps7100):
    with allure.step(key_get_time() +":启动程控电源开关"):
        logging.info(key_get_time()+':aps7100 power on')
        ponRes = APS7100Service().power_on(aps7100)
        logging.info(key_get_time()+': aps7100 power on result:'+ponRes)
#         assert ponRes == 'PON','程控电源启动失败，请检查！'
'''
    说明：关闭程控电源开关
    参数：
    aps7100:程控电源接口对象
'''
def key_power_off_aps7100(aps7100):
    with allure.step(key_get_time() +":关闭程控电源开关"):
        logging.info(key_get_time()+':aps7100 power off')
        poffRes = APS7100Service().power_off(aps7100)
        logging.info(key_get_time()+': aps7100 power off result:'+poffRes)
#         assert poffRes == 'POFF','程控电源关闭失败，请检查！'
        
'''
    说明：读取程控电源设置电压值
    参数：
    aps7100:程控电源接口对象
'''
def key_read_set_vol_aps7100(aps7100):
    with allure.step(key_get_time() +":读取程控电源设置电压值"):
        logging.info(key_get_time()+':read aps7100 set vol')
        setVol = APS7100Service().read_set_power_vol(aps7100)
        logging.info(key_get_time()+': aps7100 set vol:'+setVol)


if __name__ == '__main__':
    aps7100 = key_login_aps7100('COM7', 9600)
    key_read_set_vol_aps7100(aps7100)
    key_logout_aps7100(aps7100)