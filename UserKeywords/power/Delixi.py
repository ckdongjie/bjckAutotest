'''
Created on 2023年4月10日

@author: autotest
'''
import logging

import allure

from BasicService.power import DelixiService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time


def key_login_delixi(serialPort=BASIC_DATA['power']['serialPort'], serialRate=BASIC_DATA['power']['serialRate']):
    with allure.step(key_get_time() +":串口登录程控电源:"+serialPort+','+str(serialRate)):
        logging.info(key_get_time()+':login delixi by serial:'+serialPort+','+str(serialRate))
        delixi = DelixiService().login_serial(serialPort, serialRate)
        return delixi
    
'''
    说明：登出程控电源
    参数：
    aps7100:程控电源接口对象
'''
def key_logout_delixi(delixi):
    with allure.step(key_get_time() +":串口登出程控电源"):
        logging.info(key_get_time()+':logout delixi')
        DelixiService().logout_serial(delixi)
    
'''
    说明：启动程控电源开关
    参数：
    aps7100:程控电源接口对象
'''
def key_power_on_delixi(delixi):
    with allure.step(key_get_time() +":启动程控电源开关"):
        logging.info(key_get_time()+':delixi power on')
        ponRes = DelixiService().power_on(delixi)
        logging.info(key_get_time()+': delixi power on result:'+ponRes)
'''
    说明：关闭程控电源开关
    参数：
    aps7100:程控电源接口对象
'''
def key_power_off_delixi(delixi):
    with allure.step(key_get_time() +":关闭程控电源开关"):
        logging.info(key_get_time()+':delixi power off')
        poffRes = DelixiService().power_off(delixi)
        logging.info(key_get_time()+': delixi power off result:'+delixi)