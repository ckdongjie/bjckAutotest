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
        
'''
        删除ipv6 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
    assID:sctp id
        返回：
    delRes:删除结果
'''
def key_del_ipv6_sctp_config(hmsObj, enbId, assID):
    with allure.step(key_get_time()+":删除ipv6 sctp参数，id："+str(assID)):
        logging.info(key_get_time()+': delete ipv6 sctp, id:'+str(assID))
        delRes = SctpService().del_ipv6_sctp_info(hmsObj, str(enbId), assID)
        if delRes == '0':
            with allure.step(key_get_time()+":ipv6 sctp参数删除成功\n"):
                logging.info(key_get_time()+': ipv6 sctp delete success!')
        else:
            with allure.step(key_get_time()+":ipv6 sctp参数删除失败，失败信息："+str(delRes)):
                logging.warning(key_get_time()+': ipv6 sctp delete fail, fail info:'+str(delRes))
        assert delRes == '0','ipv6 sctp参数删除失败，请检查！'

'''
        查询ipv6 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
        返回：
    queryRes:修改结果
'''
def key_query_ipv6_sctp_config(hmsObj, enbId, queryKey):
    with allure.step(key_get_time()+":查询ipv6 sctp参数"):
        logging.info(key_get_time()+': query ipv6 sctp info')
        SctpService().realtime_query_ipv6_sctp_info(hmsObj, str(enbId))
        queryRes = SctpService().query_ipv6_sctp_info(hmsObj, str(enbId))
        return queryRes[0][queryKey]
    
'''
        新增ipv6 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
    paraDict:参数字典
        返回：
    addRes:新增结果
'''
def key_add_ipv6_sctp_config(hmsObj, enbId, paraDict):
    with allure.step(key_get_time()+":新增ipv6 sctp参数，参数："+str(paraDict)):
        logging.info(key_get_time()+': 新增 ipv6 sctp, params:'+str(paraDict))
        addRes = SctpService().add_ipv6_sctp_info(hmsObj, str(enbId), paraDict)
        if addRes == '0':
            with allure.step(key_get_time()+":ipv6 sctp参数增加成功\n"):
                logging.info(key_get_time()+': ipv6 sctp add success!')
        else:
            with allure.step(key_get_time()+":ipv6 sctp参数增加失败，失败信息："+str(addRes)):
                logging.warning(key_get_time()+': ipv6 sctp add fail, fail info:'+str(addRes))
        assert addRes == '0','ipv6 sctp参数增加失败，请检查！'
    
'''
        修改ipv4 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
    paraDict:参数字典
        返回：
    modifyRes:修改结果
'''
def key_modify_ipv4_sctp_config(hmsObj, enbId, paraDict):
    with allure.step(key_get_time()+":修改ipv4 sctp参数，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify ipv4 sctp, params:'+str(paraDict))
        SctpService().realtime_query_ipv4_sctp_info(hmsObj, str(enbId))
        updateRes = SctpService().modify_ipv4_sctp_info(hmsObj, str(enbId), paraDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":ipv4 sctp参数修改成功\n"):
                logging.info(key_get_time()+': ipv4 sctp modify success!')
        else:
            with allure.step(key_get_time()+":ipv4 sctp参数修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': ipv4 sctp modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','ipv4 sctp参数修改失败，请检查！'

'''
        查询ipv6 sctp参数
        参数：
    serialNumber:基站序列号
    enbId:基站Id
        返回：
    queryRes:修改结果
'''
def key_query_ipv4_sctp_config(hmsObj, enbId, queryKey):
    with allure.step(key_get_time()+":查询ipv4 sctp参数"):
        logging.info(key_get_time()+': query ipv4 sctp info')
        SctpService().realtime_query_ipv4_sctp_info(hmsObj, str(enbId))
        queryRes = SctpService().query_ipv4_sctp_info(hmsObj, str(enbId))
        return queryRes[queryKey]
