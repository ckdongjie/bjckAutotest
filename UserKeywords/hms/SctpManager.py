# coding = 'utf-8'
from BasicService.hms.sctpService import SctpService
'''
Created on 2023年1月13日

@author: autotest

'''
from UserKeywords.basic.basic import key_get_time
import logging
import allure


'''
        修改ipv6 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
    paraDict:参数字典
        返回：
    modifyRes:修改结果
'''
def key_modify_ipv6_sctp_config(hmsObj, enbId, paraDict):
    with allure.step(key_get_time()+":修改ipv6 sctp参数，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify ipv6 sctp, params:'+str(paraDict))
        SctpService().realtime_query_ipv6_sctp_info(hmsObj, str(enbId))
        updateRes = SctpService().modify_ipv6_sctp_info(hmsObj, str(enbId), paraDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":ipv6 sctp参数修改成功\n"):
                logging.info(key_get_time()+': ipv6 sctp modify success!')
        else:
            with allure.step(key_get_time()+":ipv6 sctp参数修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': ipv6 sctp modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','ipv6 sctp参数修改失败，请检查！'
