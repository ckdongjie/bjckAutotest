# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
import logging

import allure

from BasicModel.hms.hms import HMS
from BasicService.hms.hmsService import hmsService
from UserKeywords.basic.basic import key_get_time
from BasicService.hms.configService import configService
from TestCaseData.basicConfig import BASIC_DATA

'''
        说明：登录hms
        参数：
    hmsIP:hms ip地址
    hmsPort:hms登录端口
    username:hms登录用户名
    password:hms登录密码
        返回：
    hmsObj:hms对象
'''
def key_login_hms(hmsIp='172.16.2.159', hmsPort='18088', username='root', password='hms123...'):
    hmsIp = BASIC_DATA['hms']['ip'] if not hmsIp else hmsIp
    hmsPort = BASIC_DATA['hms']['port'] if not hmsPort else hmsPort
    username = BASIC_DATA['hms']['username'] if not username else username
    password = BASIC_DATA['hms']['password'] if not password else password
    with allure.step(key_get_time() +": 登录网管\n"):
        logging.info(key_get_time() +": login HMS, ip: "+hmsIp+",username: "+username)
        hmsObj = hmsService(hmsIp, hmsPort).login_hms(username, password)
        logging.info(key_get_time() +": login HMS success!") 
        return hmsObj
            
'''
        说明：hms上查询基站信息
        参数：
    hmsObj:hms对象
    serialNumber:基站sn号
        返回：
    enbId:基站id
    enbName:基站名称
'''
def key_get_enb_info(hmsObj, serialNumber):
    if hmsObj==None:
        hmsObj = HMS()
    with allure.step(key_get_time() +": 查询基站信息\n"):
        logging.info(key_get_time() +": query gnb info")
        enbId, enbName = hmsObj.query_enb_info(serialNumber)
        logging.info(key_get_time() +": enbId/enbName:"+str(enbId)+'/'+enbName)
        return enbId, enbName

'''
        说明：hms上更新时钟源
        参数：
    hmsObj:hms对象
    enbId:基站id
    clockType:时钟源
        返回：
    
'''
def key_update_clock_source(hmsObj, enbId, clockType):
    with allure.step(key_get_time() +": 更新时钟源，类型："+clockType):
        logging.info(key_get_time() +": update clock source, clock type:"+clockType)
        modifyRes = configService().modify_clock_source(hmsObj, enbId, clockType)
        if modifyRes == True:
            with allure.step(key_get_time() +": 更新时钟源成功\n"):
                logging.info(key_get_time()+': update clock source success!')
        else:
            with allure.step(key_get_time() +": 更新时钟源失败\n"):
                logging.warning(key_get_time()+': update clock source failure!')