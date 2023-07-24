# coding = 'utf-8'
'''
Created on 2023年6月28日
@author: dj
'''
import logging
import allure
from BasicService.hms.timeSynService import TimeSynService
from UserKeywords.basic.basic import key_get_time

'''
        说明：修改网管时间同步参数
        参数：
    hmsObj:hms对象
        返回：
    result:操作结果
'''
def key_update_auto_syn_para(hmsObj, server, synTime):
    with allure.step(key_get_time()+": 更新时间同步为自动同步，并配置对应参数"):
        logging.info(key_get_time()+': update auto synchronization para')
        paraDict = {'ntpType':1, 'ntpServerUrl':server, 'ntpInterval':synTime}
        updateRes = TimeSynService().update_gnb_trace_me_para(hmsObj, paraDict)
        if updateRes['result']==True:
            with allure.step(key_get_time()+": 更新时间同步为自动同步参数成功"):
                logging.info(key_get_time()+': update auto synchronization para success')
        else:
            with allure.step(key_get_time()+": 更新时间同步为自动同步参数失败，失败信息："+str(updateRes)):
                logging.info(key_get_time()+': update auto synchronization para failure, failure info:'+str(updateRes))
        assert updateRes['result']==True, '更新时间同步为自动同步参数失败，请检查！'
        
'''
        说明：修改网管时间同步参数
        参数：
    hmsObj:hms对象
        返回：
    result:操作结果
'''
def key_update_manual_syn_para(hmsObj, systemTime):
    with allure.step(key_get_time()+": 更新时间同步为手动同步，并配置对应参数"):
        logging.info(key_get_time()+': update manual synchronization para')
        paraDict = {'ntpType':0, 'ntpTime':systemTime}
        updateRes = TimeSynService().update_gnb_trace_me_para(hmsObj, paraDict)
        if updateRes['result']==True:
            with allure.step(key_get_time()+": 更新时间同步为手动同步参数成功"):
                logging.info(key_get_time()+': update manual synchronization para success')
        else:
            with allure.step(key_get_time()+": 更新时间同步为手动同步参数失败，失败信息："+str(updateRes)):
                logging.info(key_get_time()+': update manual synchronization para failure, failure info:'+str(updateRes))
        assert updateRes['result']==True, '更新时间同步为手动同步参数失败，请检查！'
