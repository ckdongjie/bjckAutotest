# coding = 'utf-8'
'''
Created on 2023年6月27日
@author: autotest

'''



import logging
import allure
from BasicService.hms.deviceAlarmParaService import DevAlarmParaService
from UserKeywords.basic.basic import key_get_time

'''
        设置温度阈值
'''
def key_set_temperature_alarm_threshold(hmsObj, enbId, tempAlarmThr):
    paraDict = {'tempAlarmThld':tempAlarmThr}
    with allure.step(key_get_time()+":设置基站温度阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify temperature alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站温度阈值成功\n"):
                logging.info(key_get_time()+': temperature alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站温度阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': temperature alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站温度阈值失败，请检查！'
        
'''
        设置基站低压阈值
'''
def key_set_under_voltage_alarm_threshold(hmsObj, enbId, underVoltAlarmThr):
    paraDict = {'busVolAlarmLowThld':underVoltAlarmThr}
    with allure.step(key_get_time()+":设置基站低压阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify under voltage alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站低压阈值成功\n"):
                logging.info(key_get_time()+': under voltage alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站低压阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': under voltage alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站低压阈值失败，请检查！'
        
'''
        设置基站高压阈值
'''
def key_set_over_voltage_alarm_threshold(hmsObj, enbId, overVoltAlarmThr):
    paraDict = {'busVolAlarmHighThld':overVoltAlarmThr}
    with allure.step(key_get_time()+":设置基站高压阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify over voltage alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站高压阈值成功\n"):
                logging.info(key_get_time()+': over voltage alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站高压阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': over voltage alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站高压阈值失败，请检查！'
        
'''
        设置基站内存使用率阈值
'''
def key_set_memory_usage_alarm_threshold(hmsObj, enbId, memoryUsageAlarmThr):
    paraDict = {'memUsageAlarmThld':memoryUsageAlarmThr}
    with allure.step(key_get_time()+":设置基站内存使用率阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify memory usage alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站内存使用率阈值成功\n"):
                logging.info(key_get_time()+': memory usage alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站内存使用率阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': memory usage alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站内存使用率阈值失败，请检查！'
        
'''
        设置基站cpu使用率阈值
'''
def key_set_cpu_usage_alarm_threshold(hmsObj, enbId, cpuUsageAlarmThr):
    paraDict = {'cpuUsageAlarmThld':cpuUsageAlarmThr}
    with allure.step(key_get_time()+":设置基站cpu使用率阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify cpu usage alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站cpu使用率阈值成功\n"):
                logging.info(key_get_time()+': cpu usage alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站cpu使用率阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': cpu usage alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站cpu使用率阈值失败，请检查！'
        
'''
        设置基站驻波比阈值
'''
def key_set_vswr_alarm_threshold(hmsObj, enbId, vswrAlarmThld):
    paraDict = {'vswrAlarmThld':vswrAlarmThld}
    with allure.step(key_get_time()+":设置基站驻波比阈值，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify vswr alarm threshold, params:'+str(paraDict))
        updateRes = DevAlarmParaService().update_dev_alarm_para(hmsObj, str(enbId), paraDict)
        if updateRes['result'] == '0':
            with allure.step(key_get_time()+":设置基站驻波比阈值成功\n"):
                logging.info(key_get_time()+': vswr alarm threshold modify success!')
        else:
            with allure.step(key_get_time()+":设置基站驻波比阈值失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': vswr alarm threshold modify fail, fail info:'+str(updateRes))
        assert updateRes['result'] == '0','设置基站驻波比阈值失败，请检查！'

'''
        读取设备告警阈值
'''
def key_get_dev_alarm_para(hmsObj, enbId):
    with allure.step(key_get_time()+":查询设备告警阈值参数"):
        logging.info(key_get_time()+': query device alarm para')
        devAlarmPara = DevAlarmParaService().query_dev_alarm_para(hmsObj, str(enbId))
        return devAlarmPara