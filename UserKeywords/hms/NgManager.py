'''
Created on 2023年6月12日
@author: dj
'''
'''
        设置tac参数值
'''

import logging

import allure

from BasicService.hms.ngInterfaceService import NgInterfaceService
from UserKeywords.basic.basic import key_get_time


def key_set_ng_value(hmsObj, enbId, ngInterfaceInstanceId):
    paraDict = {'assId':ngInterfaceInstanceId}
    with allure.step(key_get_time()+":引用SCTP实例，参数："+str(paraDict)):
        logging.info(key_get_time()+': sctp instance id, params:'+str(paraDict))
        updateRes = NgInterfaceService().modify_ng_info(hmsObj, str(enbId), paraDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":ng参数修改成功\n"):
                logging.info(key_get_time()+': ng config modify success!')
        else:
            with allure.step(key_get_time()+":ng参数修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': ng config modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','ng参数修改失败，请检查！'

'''
        读取ng配置值
'''
def key_get_ng_value(hmsObj, enbId):
    with allure.step(key_get_time()+":查询ng参数值"):
        logging.info(key_get_time()+': query ng config value')
        ngInfo = NgInterfaceService().query_ng_config_info(hmsObj, str(enbId))
        return ngInfo