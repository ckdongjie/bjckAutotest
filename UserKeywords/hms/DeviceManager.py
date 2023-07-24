# coding = 'utf-8'
'''
Created on 2022年10月20日
@author: dj

'''


import logging

import allure

from BasicService.hms.deviceManagerService import deviceManagerService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time


def key_confirm_device_online(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 确认基站是在线状态\n"):
        logging.info(key_get_time()+': confirm if gnb is online')
        enbStatus = deviceManagerService().query_device_online(hmsObj, serialNumber)
        if enbStatus == 'online':
            with allure.step(key_get_time()+": 基站在线"):
                logging.info(key_get_time()+': gnb is online')
        else:
            with allure.step(key_get_time()+": 基站断链"):
                logging.warning(key_get_time()+': gnb is offline')
        assert enbStatus == 'online',key_get_time()+':基站断链，请检查！'

'''
        确认基站在线状态与预期一致
        参数：
    serialNumber:基站序列号
    expectStatus:预期状态
        返回：
'''
def key_confirm_device_status_same_as_expect(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], expectStatus='online'):
    with allure.step(key_get_time()+": 确认基站在线状态与预期一致\n"):
        logging.info(key_get_time()+': confirm if gnb status is same as expect,expect status: '+expectStatus)
        isSame = deviceManagerService().query_device_status_same_as_expect(hmsObj, serialNumber, expectStatus)
        if isSame == True:
            with allure.step(key_get_time()+": 基站状态与预期一致"):
                logging.info(key_get_time()+': gnb status is same as expect!')
        else:
            with allure.step(key_get_time()+": 基站状态与预期不一致"):
                logging.warning(key_get_time()+': gnb status is not same as expect!')
        assert isSame == True,key_get_time()+':基站在线状态与预期不一致，请检查！'

'''
    说明：设置基站自测模式
    参数：
        hmsObj:hms对象
        serialNumber:基站序列号
        testMode:自测模式0：关闭，1：打开
    返回：
'''
def key_modiry_device_auto_test_mode(hmsObj, testMode=1, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 设置基站自测模式\n"):
        logging.info(key_get_time()+': set auto test mode: ' + "open" if testMode==1 else "close")
        resInfo = deviceManagerService().set_auto_test_mode(hmsObj, serialNumber, testMode)
        return resInfo