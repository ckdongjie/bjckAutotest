# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''


import logging

import allure

from BasicService.hms.dlScheduleService import DLScheduleService
from BasicService.hms.duService import DuService
from BasicService.hms.pdcchService import PdcchService
from BasicService.hms.pucchService import PucchService
from UserKeywords.basic.basic import key_get_time, key_wait

'''
        说明：修改PUCCH format1 rb数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    rbNumber:format1 rb数
        返回：
'''
def key_modify_pucch_format1_rb_number(hmsObj, enbId, rbNumber):
    
    with allure.step(key_get_time() +": 修改PUCCH format1 rb数，rb数:"+str(rbNumber)+'\n'):
        logging.info(key_get_time()+': modify PUCCH format1 rb number,rb number:'+str(rbNumber))
        modifyRes = PucchService().update_pucch_format1_rb_number(hmsObj, enbId, rbNumber)
        if modifyRes == True:
            with allure.step(key_get_time() +":PUCCH format1 RB数修改成功。"):
                logging.info(key_get_time()+': PUCCH format1 rb number modify success!')
        else:
            with allure.step(key_get_time() +":PUCCH format1 RB数修改失败。"):
                logging.warning(key_get_time()+': PUCCH format1 rb number modify failure!')
        assert modifyRes == True,'修改PUCCH format1 rb数异常，请检查！'
        
'''
        说明：修改PUCCH format3 rb数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    rbNumber:format3 rb数
        返回：
'''
def key_modify_pucch_format3_rb_number(hmsObj, enbId, rbNumber):
    
    with allure.step(key_get_time() +": 修改PUCCH format3 rb数，rb数:"+str(rbNumber)+'\n'):
        logging.info(key_get_time()+': modify PUCCH format3 rb number,rb number:'+str(rbNumber))
        modifyRes = PucchService().update_pucch_format3_rb_number(hmsObj, enbId, rbNumber)
        if modifyRes == True:
            with allure.step(key_get_time() +":PUCCH format3 RB数修改成功。"):
                logging.info(key_get_time()+': PUCCH format3 rb number modify success!')
        else:
            with allure.step(key_get_time() +":PUCCH format3 RB数修改失败。"):
                logging.warning(key_get_time()+': PUCCH format3 rb number modify failure!')
        assert modifyRes == True,'修改PUCCH format3 rb数异常，请检查！'