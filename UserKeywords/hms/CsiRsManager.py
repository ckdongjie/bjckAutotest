# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest

'''
 

import logging

import allure

from BasicService.hms.csiRsService import CsiRsService
from UserKeywords.basic.basic import key_get_time

'''
        说明：修改trs周期
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    trsPeriod:trs周期
        返回：
'''
def key_update_trs_period(hmsObj, enbId, trsPeriod):
    with allure.step(key_get_time() +": 修改trs周期，周期值:"+trsPeriod+'\n'):
        logging.info(key_get_time()+': modify trs period, trs period value:'+trsPeriod)
        modifyRes = CsiRsService().update_trs_period(hmsObj, enbId, trsPeriod)
        if modifyRes == True:
            with allure.step(key_get_time() +":trs周期修改成功。"):
                logging.info(key_get_time()+':trs period modify success!')
        else:
            with allure.step(key_get_time() +":trs周期修改失败。"):
                logging.warning(key_get_time()+':trs period modify failure!')
            
        assert modifyRes == True,'trs周期修改异常，请检查！'

'''
        说明：修改csi report quantity参数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    csiReportQuantiry:csi报告量
        返回：
'''
def key_update_csi_report_quantity(hmsObj, enbId, csiReportQuantiry):
    with allure.step(key_get_time() +": 修改csi报告量，报告量:"+csiReportQuantiry+'\n'):
        logging.info(key_get_time()+': modify csi report quantity, report quantity:'+csiReportQuantiry)
        modifyRes = CsiRsService().update_csi_report_quantity(hmsObj, enbId, csiReportQuantiry)
        if modifyRes == True:
            with allure.step(key_get_time() +":csi报告量修改成功。"):
                logging.info(key_get_time()+':csi report quantity modify success!')
        else:
            with allure.step(key_get_time() +":csi报告量修改失败。"):
                logging.warning(key_get_time()+':csi report quantity modify failure!')
            
        assert modifyRes == True,'csi报告量修改异常，请检查！'
