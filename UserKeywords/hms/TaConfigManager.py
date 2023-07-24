# coding='utf-8'
'''
Created on 2023年6月6日
@author: dj

'''
import logging
import allure
from BasicService.hms.taService import TaService
from UserKeywords.basic.basic import key_get_time

'''
        设置tac参数值
'''
def key_set_tac_value(hmsObj, enbId, tacValue):
    paraDict = {'tac':tacValue}
    with allure.step(key_get_time()+":修改ta配置参数，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify ta config, params:'+str(paraDict))
        updateRes = TaService().modify_ta_info(hmsObj, str(enbId), paraDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":ta参数修改成功\n"):
                logging.info(key_get_time()+': ta config modify success!')
        else:
            with allure.step(key_get_time()+":ta参数修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': ta config modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','ta参数修改失败，请检查！'

'''
        读取tac配置值
'''
def key_get_tac_value(hmsObj, enbId):
    with allure.step(key_get_time()+":查询ta参数值"):
        logging.info(key_get_time()+': query ta config value')
        taInfo = TaService().query_ta_config_info(hmsObj, str(enbId))
        return taInfo['tac']