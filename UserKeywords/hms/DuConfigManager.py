'''
Created on 2022年12月9日

@author: autotest
'''
      

import logging

import allure

from BasicService.hms.duService import DuService
from UserKeywords.basic.basic import key_get_time, key_wait

'''
        说明：修改DU下行预调度开关
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    switch:预调度开关
        返回：
''' 
def key_modify_du_dl_schedule_switch(hmsObj, enbId, switch='open'):
    with allure.step(key_get_time() +": 修改DU下行预调度开关,开关状态:"+switch+'\n'):
        logging.info(key_get_time()+': modify DU dl pre-scheduling switch,switch status:'+switch)
        switchDict = {'open':'1', 'close':'0'}
        paraDict = {'dlPreSchdTestSwitch':switchDict[switch]}
        modifyRes = DuService().update_du_dl_schedule_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU下行预调度开关修改成功。"):
                logging.info(key_get_time()+': DU dl pre-scheduling switch modify success!')
        else:
            with allure.step(key_get_time() +":DU下行预调度开关修改失败。"):
                logging.warning(key_get_time()+': DU dl pre-scheduling switch modify failure!')
        assert modifyRes == True,'小区状态与预期状态不符，请检查！'
        
'''
        说明：修改DU上行预调度开关
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    switch:预调度开关
        返回：
''' 
def key_modify_du_ul_schedule_switch(hmsObj, enbId, switch='open'):
    with allure.step(key_get_time() +": 修改DU上行预调度开关,开关状态:"+switch+'\n'):
        logging.info(key_get_time()+': modify DU ul pre-scheduling switch,switch status:'+switch)
        switchDict = {'open':'1', 'close':'0'}
        paraDict = {'ulPreSchdTestSwitch':switchDict[switch]}
        modifyRes = DuService().update_du_ul_schedule_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU上行预调度开关修改成功。"):
                logging.info(key_get_time()+': DU ul pre-scheduling switch modify success!')
        else:
            with allure.step(key_get_time() +":DU上行预调度开关修改失败。"):
                logging.warning(key_get_time()+': DU ul pre-scheduling switch modify failure!')
        assert modifyRes == True,'修改DU上行预调度开关异常，请检查！'
        
'''
        说明：修改DU上行预调度类型
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    scheduleType:调度类型
        返回：
''' 
def key_modify_du_ul_schedule_type(hmsObj, enbId, scheduleType='Static'):
    with allure.step(key_get_time() +": 修改DU上行预调度类型,调度类型:"+scheduleType+'\n'):
        logging.info(key_get_time()+': modify DU ul pre-scheduling type,schedule type:'+scheduleType)
        typeDict = {'Static':'1', 'Dynamic':'0'}
        paraDict = {'ulPreSchdType':typeDict[scheduleType]}
        modifyRes = DuService().update_du_ul_schedule_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU上行调度类型修改成功。"):
                logging.info(key_get_time()+': DU ul schedule type modify success!')
        else:
            with allure.step(key_get_time() +":DU上行调度类型修改失败。"):
                logging.warning(key_get_time()+': DU ul schedule type modify failure!')
        assert modifyRes == True,'修改DU上行预调度类型异常，请检查！'
        
'''
        说明：修改DU小区SSB发射功率
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    scheduleType:调度类型
        返回：
''' 
def key_modify_du_cell_epre(hmsObj, enbId, epre):
    with allure.step(key_get_time() +":修改DU小区SSB发射功率，设置值:"+str(epre)+'\n'):
        logging.info(key_get_time()+':modify DU cell epre, value: '+str(epre))
        paraDict = {'epre':str(epre)}
        modifyRes = DuService().update_du_cell_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU小区SSB发射功率修改成功。"):
                logging.info(key_get_time()+':DU cell epre modify success!')
        else:
            with allure.step(key_get_time() +":DU小区SSB发射功率修改失败。"):
                logging.warning(key_get_time()+': DU cell epre modify failure!')
        assert modifyRes == True,'DU小区SSB发射功率修改异常，请检查！'
        
'''
        说明：修改DU小区SSB周期和smtc周期
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    ssbPeriod:ssb周期
    smtcPeriod:smtc周期
        返回：
''' 
def key_modify_ssb_period(hmsObj, enbId, ssbPeriod, smtcPeriod):
    with allure.step(key_get_time() +":修改SSB周期和smtc周期，参数值:"+ssbPeriod+','+smtcPeriod+'\n'):
        logging.info(key_get_time()+':modify SSB period, parameter: '+ssbPeriod+','+smtcPeriod)
        ssbPeriodDict = {'MS5':'0','MS10':'1','MS20':'2','MS40':'3','MS80':'4','MS160':'5'}
        smtcPeriodDict = {'MS5':'0','MS10':'1','MS20':'2','MS40':'3','MS80':'4','MS160':'5'}
        paraDict = {'ssbPeriodicityServingCell':ssbPeriodDict[ssbPeriod], 'smtcPeriod':smtcPeriodDict[smtcPeriod]}
        modifyRes = DuService().update_du_cell_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU小区SSB周期和smtc周期修改成功。"):
                logging.info(key_get_time()+':DU cell ssb period and smtc period modify success!')
        else:
            with allure.step(key_get_time() +":DU小区SSB周期和smtc周期修改失败。"):
                logging.warning(key_get_time()+': DU cell ssb period and smtc period modify failure!')
        assert modifyRes == True,'DU小区SSB周期和smtc周期修改异常，请检查！'
        
'''
        说明：修改DU小区SSB频域位置
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    ssbFreqPos:ssb频域位置
        返回：
''' 
def key_modify_ssb_frequency_position(hmsObj, enbId, ssbFreqPos):
    with allure.step(key_get_time() +":修改SSB频域位置，参数值:"+ssbFreqPos+'\n'):
        logging.info(key_get_time()+':modify SSB frequency position, parameter: '+ssbFreqPos)
        
        paraDict = {'ssbFreqPos':str(ssbFreqPos)}
        modifyRes = DuService().update_du_cell_para(hmsObj, enbId, paraDict)
        if modifyRes == True:
            with allure.step(key_get_time() +":DU小区SSB频域位置修改成功。"):
                logging.info(key_get_time()+':DU cell ssb frequency position modify success!')
        else:
            with allure.step(key_get_time() +":DU小区SSB频域位置修改失败。"):
                logging.warning(key_get_time()+': DU cell ssb frequency position modify failure!')
        assert modifyRes == True,'DU小区SSB频域位置修改异常，请检查！'
        
