# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
'''
        基站复位
        参数：
    serialNumber:基站序列号列表
'''        
'''
        说明：复位基站
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
    result:复位操作结果
'''

import logging

import allure

from BasicService.hms.diagnosticService import DiagnosticService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info, \
    key_get_enb_ip


def key_reboot_enb(hmsObj, enbId):
    with allure.step(key_get_time()+": 基站复位\n"):
        logging.info(key_get_time()+': omc reboot gnb')
        resCode, resInfo = DiagnosticService().reboot_enb(hmsObj, enbId)
        if resCode == 200 and resInfo['result'] == '0':
            with allure.step(key_get_time()+": 基站复位成功\n"):
                logging.info(key_get_time()+': reboot success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 基站复位失败，请检查！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': reboot fail, fail info:'+str(resInfo))
                return 'fail'
            
'''
        说明：基站ping诊断
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
    result:复位操作结果
'''
def key_gnb_ping_diag(hmsObj, pingTimes, gnbIp):
    with allure.step(key_get_time()+": 基站ping包诊断\n"):
        logging.info(key_get_time()+': gnb ping diagnosis')
        clientId, resInfo = DiagnosticService().gnb_ping_diag(hmsObj, pingTimes, gnbIp)
        if resInfo['result'] == True:
            with allure.step(key_get_time()+": 基站ping诊断执行成功\n"):
                logging.info(key_get_time()+': ping diagnosis exec success!')
        else:
            with allure.step(key_get_time()+": 基站ping诊断执行失败！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': ping diagnosis exec fail, fail info:'+str(resInfo))
        return clientId
            
'''
        说明：获取基站ping诊断结果
        参数：
    hmsObj:hms对象
    pingTimes:ping包次数
    clientId:客户端id
        返回：
    result:操作结果
'''
def key_get_ping_diag_result(hmsObj, pingTimes, clientId):
    with allure.step(key_get_time()+": 获取基站ping包诊断结果\n"):
        logging.info(key_get_time()+': get gnb ping diagnosis result')
        diagInfo = DiagnosticService().get_gnb_ping_diag_res(hmsObj, pingTimes, clientId)
        with allure.step(key_get_time()+": 基站ping诊断结果："+diagInfo):
            logging.info(key_get_time()+': ping diagnosis exec result:'+diagInfo)
            
'''
        说明：基站跟踪路由诊断
        参数：
    hmsObj:hms对象
    gnbIp:基站ip
        返回：
    result:复位操作结果
'''
def key_gnb_trace_route_diag(hmsObj, gnbIp):
    with allure.step(key_get_time()+": 基站跟踪路由诊断\n"):
        logging.info(key_get_time()+': gnb trace route diagnosis')
        clientId, resInfo = DiagnosticService().gnb_trace_route_diag(hmsObj, gnbIp)
        if resInfo['result'] == True:
            with allure.step(key_get_time()+": 基站跟踪路由诊断执行成功\n"):
                logging.info(key_get_time()+': trace route diagnosis exec success!')
        else:
            with allure.step(key_get_time()+": 基站跟踪路由诊断执行失败！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': trace route diagnosis exec fail, fail info:'+str(resInfo))
        return clientId
            
'''
        说明：获取基站跟踪路由诊断结果
        参数：
    hmsObj:hms对象
    clientId:客户端id
        返回：
    result:操作结果
'''
def key_get_trace_route_diag_result(hmsObj, clientId):
    with allure.step(key_get_time()+": 获取基站跟踪路由诊断结果\n"):
        logging.info(key_get_time()+': get gnb trace route diagnosis result')
        diagInfo = DiagnosticService().get_gnb_trace_route_diag_res(hmsObj, clientId)
        with allure.step(key_get_time()+": 基站跟踪路由诊断结果："+diagInfo):
            logging.info(key_get_time()+': trace route diagnosis exec result:'+diagInfo)
            
'''
        说明：修改信令跟踪任务参数
        参数：
    hmsObj:hms对象
    clientId:客户端id
        返回：
    result:操作结果
'''
def key_update_trace_me_para(hmsObj, startTime, endTime, dataReportSwitch, sn=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 更新基站信令踪路参数"):
        logging.info(key_get_time()+': update gnb trace route me para')
        paraDict = {'startTime':startTime, 'endTime':endTime, 'switchState':dataReportSwitch}
        updateRes = DiagnosticService().update_gnb_trace_me_para(hmsObj, sn, paraDict)
        if updateRes['result']==1:
            with allure.step(key_get_time()+": 更新基站信令踪路参数成功"):
                logging.info(key_get_time()+': update trace me para success')
        else:
            with allure.step(key_get_time()+": 更新基站信令踪路参数失败，失败信息："+str(updateRes)):
                logging.info(key_get_time()+': update trace me para failure, failure info:'+str(updateRes))
        assert updateRes['result']==1, '更新基站信令踪路参数失败，请检查！'
            
if __name__ == '__main__':
    hmsObj = key_login_hms()
    enbIp = key_get_enb_ip(hmsObj)
    clientId = key_gnb_trace_route_diag(hmsObj, enbIp)
    key_get_trace_route_diag_result(hmsObj, clientId)