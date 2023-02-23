# coding = 'utf-8'
'''
Created on 2022年12月13日

@author: autotest
'''
'''
        说明：修改PDCCH符号数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    symbolNumber:符号数--Adaptive/1 Symbol/2 Symbol
        返回：
''' 

import logging

import allure

from BasicService.hms.dlScheduleService import DLScheduleService
from BasicService.hms.duService import DuService
from BasicService.hms.pdcchService import PdcchService
from BasicService.hms.ulScheduleService import ULScheduleService
from UserKeywords.basic.basic import key_get_time, key_wait


def key_modify_pdcch_symbol_number(hmsObj, enbId, symbolNumber='Adaptive'):
    
    with allure.step(key_get_time() +": 修改PDCCH符号数,符号数:"+str(symbolNumber)+'\n'):
        logging.info(key_get_time()+': modify PDCCH symbol number,symbol number:'+str(symbolNumber))
        typeDict = {'Adaptive':'0', '1 Symbol':'1', '2 Symbol':'2'}
        modifyRes = PdcchService().update_pdcch_symbol_number(hmsObj, enbId, typeDict[symbolNumber])
        if modifyRes == True:
            with allure.step(key_get_time() +":PDCCH符号数修改成功。"):
                logging.info(key_get_time()+': PDCCH symbol number modify success!')
        else:
            with allure.step(key_get_time() +":PDCCH符号数修改失败。"):
                logging.warning(key_get_time()+': PDCCH symbol number modify failure!')
        assert modifyRes == True,'修改PDCCH符号数异常，请检查！'
        
'''
        说明：修改PDCCH CCE聚合度
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    cceLevel:CCE聚合度--CCE_4/CCE_8/CCE_16
        返回：
''' 
def key_modify_pdcch_cce_level(hmsObj, enbId, cceLevel='CCE_4'):
    
    with allure.step(key_get_time() +": 修改PDCCH CCE聚合度,聚合度:"+cceLevel+'\n'):
        logging.info(key_get_time()+': modify PDCCH CCE level,CCE level:'+cceLevel)
        typeDict = {'CCE_4':'3', 'CCE_8':'4', 'CCE_16':'5'}
        modifyRes = PdcchService().update_pdcch_cce_level(hmsObj, enbId, typeDict[cceLevel])
        if modifyRes == True:
            with allure.step(key_get_time() +":PDCCH CCE聚合度修改成功。"):
                logging.info(key_get_time()+': PDCCH symbol number modify success!')
        else:
            with allure.step(key_get_time() +":PDCCH CCE聚合度修改失败。"):
                logging.warning(key_get_time()+': PDCCH CCE level modify failure!')
        assert modifyRes == True,'修改PDCCH CCE聚合度异常，请检查！'
        
'''
        说明：修改PDSCH下行调制解调参数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    mcs:调制参数
        返回：
''' 
def key_modify_pdsch_dl_mcs(hmsObj, enbId, switch, mcs=28):
    
    with allure.step(key_get_time() +": 修改PDSCH下行调制解调参数,mcs值:"+str(mcs)+'\n'):
        logging.info(key_get_time()+': modify PDSCH DL mcs, mcs value:'+str(mcs))
        modifySwitchRes = DLScheduleService().modify_du_dl_amc_switch(hmsObj, enbId, switch)
        if modifySwitchRes == True:
            modifyMcsRes = DLScheduleService().modify_du_dl_mcs(hmsObj, enbId, mcs)
            if modifyMcsRes == True:
                with allure.step(key_get_time() +":PDSCH下行调制解调参数修改成功。"):
                    logging.info(key_get_time()+': PDSCH DL mcs modify success!')
            else:
                with allure.step(key_get_time() +":PDSCH下行调制解调参数修改失败。"):
                    logging.warning(key_get_time()+': PDSCH DL mcs modify failure!')
        assert modifyMcsRes == True,'修改PDSCH下行调制解调参数修改异常，请检查！'
        
'''
        说明：修改PDSCH上行调制解调参数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    mcs:调制参数
        返回：
''' 
def key_modify_pdsch_ul_mcs(hmsObj, enbId, switch, mcs=28):
    
    with allure.step(key_get_time() +": 修改PDSCH上行调制解调参数,mcs值:"+str(mcs)+'\n'):
        logging.info(key_get_time()+': modify PDSCH UL mcs, mcs value:'+str(mcs))
        modifySwitchRes = ULScheduleService().modify_du_ul_amc_switch(hmsObj, enbId, switch)
        if modifySwitchRes == True:
            modifyMcsRes = ULScheduleService().modify_du_ul_mcs(hmsObj, enbId, mcs)
            if modifyMcsRes == True:
                with allure.step(key_get_time() +":PDSCH上行调制解调参数修改成功。"):
                    logging.info(key_get_time()+': PDSCH UL mcs modify success!')
            else:
                with allure.step(key_get_time() +":PDSCH上行调制解调参数修改失败。"):
                    logging.warning(key_get_time()+': PDSCH UL mcs modify failure!')
        assert modifyMcsRes == True,'修改PDSCH上行调制解调参数修改异常，请检查！'
        
'''
        说明：修改PRACH索引
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    index:配置索引
        返回：
''' 
def key_modify_prach_config_index(hmsObj, enbId, index):
    
    with allure.step(key_get_time() +": 修改PRACH配置索引值:"+str(index)+'\n'):
        logging.info(key_get_time()+': modify PRACH configuration index, index value:'+str(index))
        infoDict = DuService().query_du_cell_info(hmsObj, enbId)
        infoDict.update({'prachConfigurationIndex':index})
        modifyRes = DuService().update_du_cell_para(hmsObj, enbId, infoDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":PRACH配置索引参数修改成功。"):
                logging.info(key_get_time()+': PRACH configuration index modify success!')
        else:
            with allure.step(key_get_time() +":PRACH配置索引参数修改失败。"):
                logging.warning(key_get_time()+': PRACH configuration index modify failure!')
            
        assert modifyRes == True,'修改PRACH配置索引参数修改异常，请检查！'
        