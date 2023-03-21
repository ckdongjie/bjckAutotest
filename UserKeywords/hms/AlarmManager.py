# codint = 'utf-8'
'''
Created on 2023年1月10日

@author: dj

'''


import logging

import allure

from BasicService.hms.alarmService import AlarmService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
    功能：查询当前告警
    参数：
    hmsObj:网管对象
    serialNumber:基站序列号
    tryNum:尝试次数
'''
def key_query_active_alarm(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], tryNum=3):
    with allure.step(key_get_time()+':基站当前告警查询'):
        logging.info(key_get_time()+': query gnb active alarm')
    for i in range (tryNum):
        syncRes = AlarmService().sync_alarm(hmsObj, serialNumber)
        if syncRes == 'true':
            break
    alarmList = AlarmService().query_active_alarm(hmsObj, serialNumber)
    return alarmList

'''
    功能：查询历史告警
    参数：
    hmsObj:网管对象
    serialNumber:基站序列号
    alarmRaisedStartTime:告警上报时间
    alarmRaisedEndTime:告警恢复时间
    tryNum:尝试次数
'''
def key_query_history_alarm(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], alarmRaisedStartTime='', alarmRaisedEndTime='', tryNum=3):
    with allure.step(key_get_time()+':基站历史告警查询'):
        logging.info(key_get_time()+': query gnb history alarm')
    for i in range (tryNum):
        syncRes = AlarmService().sync_alarm(hmsObj, serialNumber)
        if syncRes == 'true':
            break
    alarmList = AlarmService().query_history_alarm(hmsObj, serialNumber, alarmRaisedStartTime, alarmRaisedEndTime)
    return alarmList

'''
    功能：当前告警校验-黑名单
    参数：
    hmsObj:网管对象
    serialNumber:基站序列号
    alarmBlackList:告警黑名单
'''
def key_check_active_alarm_with_black_list(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], alarmBlackList=BASIC_DATA['alarm']['activeBlackList']):
    alarmList = key_query_active_alarm(hmsObj, serialNumber)
    findBlackAlarm = False
    for alarmInfo in alarmList:
        alarmName = alarmInfo['specificProblem']
        if alarmName in alarmBlackList:
            findBlackAlarm = True
            break
    return findBlackAlarm

'''
    功能：当前告警校验-白名单
    参数：
    hmsObj:网管对象
    serialNumber:基站序列号
    alarmBlackList:告警黑名单
'''
def key_check_active_alarm_with_white_list(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], alarmWhiteList=BASIC_DATA['alarm']['activeWhiteList']):
    alarmList = key_query_active_alarm(hmsObj, serialNumber)
    notFindAlarm = False
    for alarmName in alarmWhiteList:
        if alarmName not in alarmList:
            notFindAlarm = True
            break
    return notFindAlarm