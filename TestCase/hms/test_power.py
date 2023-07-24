# coding = 'utf-8'
'''
Created on 2023年1月9日
@author: auto
'''
import logging
import random

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_confirm_cell_status
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info, \
    key_update_clock_source
from UserKeywords.power.Power import key_power_off, key_power_on
from UserKeywords.ue.CpeManager import key_cpe_login, key_cpe_attach, \
    key_confirm_pdu_setup_succ, key_cpe_attach_cell_info, key_cpe_ping, \
    key_cpe_detach


@pytest.mark.基站下电上电后CEP接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站下电上电后CEP接入成功率测试'] if RUN_TESTCASE.get('基站下电上电后CEP接入成功率测试') else [])
def testGnbPowerOnAndPowerOff(testNum):
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+': 环境初始化'):
        logging.info(key_get_time()+': setup test environment')
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(3)
        key_cpe_attach(cpe)
        with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
            key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    for i in range (1,testNum+1):
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            key_power_off()
            key_wait(60)
            key_power_on()
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                logging.info(key_get_time()+':power on, wait for 3min')
                key_wait(3*60)
            key_confirm_device_online(hmsObj)
            if isCheckCell == True:
                key_confirm_cell_status(hmsObj, enbId, 'available')
            key_wait(90)
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            cellPci = key_cpe_attach_cell_info(cpe)
            if setupRes=='success' and cellPci != -1:
                AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    if isCheckSuccRate==True:
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
 
@pytest.mark.基站随机上下电压测
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站随机上下电压测'] if RUN_TESTCASE.get('基站随机上下电压测') else [])
def testGnbRandomPowerOnAndPowerOff(testNum):
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+': 环境初始化'):
        logging.info(key_get_time()+': setup test environment')
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(3)
        key_cpe_attach(cpe)
        with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
            key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    for i in range (1,testNum+1):
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            key_power_off()
            key_wait(30)
            key_power_on()
            with allure.step(key_get_time()+':上电过程中随机再执行下电上电操作。'):
                logging.info(key_get_time()+':when the gnb is starting, random execute power off and power on')
                key_wait(random.randint(0,180))
                key_power_off()
                key_wait(30)
                key_power_on()
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                logging.info(key_get_time()+':power on, wait for 3min')
                key_wait(3*60)
            key_confirm_device_online(hmsObj)
            if isCheckCell == True:
                key_confirm_cell_status(hmsObj, enbId, 'available')
            key_wait(90)
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            cellId = key_cpe_attach_cell_info(cpe)
            if setupRes=='success' and cellId != -1:
                AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    if isCheckSuccRate==True:
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
     
@pytest.mark.CPE下电上电后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE下电上电后接入成功率测试'] if RUN_TESTCASE.get('CPE下电上电后接入成功率测试') else [])
def testCpePowerOnAndPowerOff(testNum):
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    for i in range (1,testNum+1):
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            key_power_off()
            key_wait(30)
            key_power_on()
            with allure.step(key_get_time()+':cpe复位成功，等待cpe启动完成！'):
                logging.info(key_get_time()+'cpe reset success, wait for cpe start')
                key_wait(60)
            cpe = key_cpe_login()
            for i in range (1,10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
                else:
                    key_wait(5)
            cellId = key_cpe_attach_cell_info(cpe)
            if setupRes=='success' and cellId != -1:
                AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    if isCheckSuccRate==True:
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
 
@allure.story("整机上下电本地时钟测试") 
@pytest.mark.整机上下电本地时钟测试
def testLocalClockByGnbPowerOnAndOff():
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    isPing = BASIC_DATA['common']['isPing']
    cpe = key_cpe_login()
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_update_clock_source(hmsObj, enbId, 'LOCAL_CLOCK')
    key_wait(10)
    key_power_off()
    key_wait(30)
    key_power_on()
    with allure.step(key_get_time()+':电源上电，等待3分钟。'):
        logging.info(key_get_time()+':power on, wait for 3min')
        key_wait(3*60)
    key_confirm_device_online(hmsObj)
    if isCheckCell == True:
        key_confirm_cell_status(hmsObj, enbId, 'available')
    key_cpe_detach(cpe)
    key_wait(20)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    for i in range (0, 10):
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            break
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    cellId = key_cpe_attach_cell_info(cpe)
    assert cellId != -1,'CPE接入失败，请检查！'
    if isPing == True:
        key_cpe_ping(cpe, pingInterface = pingNrInterface)
        key_cpe_ping(cpe, pingInterface = pingwifiInterface)
    with allure.step(key_get_time()+':恢复基站时钟配置'):
        logging.info(key_get_time()+': recover gnb clock config')
        key_update_clock_source(hmsObj, enbId, 'GPS')
             
@allure.story("整机复位本地时钟测试") 
@pytest.mark.整机复位本地时钟测试
def testLocalClockByGnbReboot():
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    isPing = BASIC_DATA['common']['isPing']
    cpe = key_cpe_login()
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_update_clock_source(hmsObj, enbId, 'LOCAL_CLOCK')
    key_wait(10)
    #复位基站
    key_reboot_enb(hmsObj, enbId)        
    with allure.step(key_get_time()+': 基站复位成功，等待基站重启正常'):
        logging.info(key_get_time()+': reboot success, wait for BS start')
        key_wait(180)
    key_confirm_device_online(hmsObj)
    if isCheckCell == True:
        key_confirm_cell_status(hmsObj, enbId, 'available')
    key_cpe_detach(cpe)
    key_wait(20)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    for i in range (0, 10):
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            break
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    cellId = key_cpe_attach_cell_info(cpe)
    assert cellId != -1,'CPE接入失败，请检查！'
    if isPing == True:
        key_cpe_ping(cpe, pingInterface = pingNrInterface)
        key_cpe_ping(cpe, pingInterface = pingwifiInterface)
    with allure.step(key_get_time()+':恢复基站时钟配置'):
        logging.info(key_get_time()+': recover gnb clock config')
        key_update_clock_source(hmsObj, enbId, 'GPS')
            
if __name__ == '__main__':
    print(random.randint(0,10))
