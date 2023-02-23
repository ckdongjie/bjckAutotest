# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
from BasicService.hms.diagnosticService import DiagnosticService
'''
        基站复位
        参数：
    serialNumber:基站序列号列表
'''        

import logging

import allure

from UserKeywords.basic.basic import key_get_time

'''
        说明：复位基站
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
    result:复位操作结果
'''
def key_reboot_enb(hmsObj, enbId):
    with allure.step(key_get_time()+": 基站复位\n"):
        logging.info(key_get_time()+': omc reboot gnb')
        resCode, resInfo = DiagnosticService().reboot_enb(hmsObj, enbId)
        if resCode == 200 and resInfo['result'] == '0':
            with allure.step(key_get_time()+": 基站复位成功\n"):
                logging.info(key_get_time()+': reboot success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 基站复位失败，请检查！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': reboot fail, fail info:'+str(resInfo))
                return 'fail'