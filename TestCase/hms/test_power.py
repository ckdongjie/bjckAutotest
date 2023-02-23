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
from UserKeywords.power.APS7100 import key_login_aps7100, key_power_off_aps7100, \
    key_power_on_aps7100
from UserKeywords.ue.CpeManager import key_cpe_login, key_cpe_attach, \
    key_confirm_pdu_setup_succ, key_cpe_attach_cell_info, key_cpe_ping, \
    key_cpe_detach


@allure.story("基站上下电测试") 
@pytest.mark.基站上下电测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站上下电测试'] if RUN_TESTCASE.get('基站上下电测试') else [])
def testGnbPowerOnAndPowerOff(testNum):
    serialNumber=BASIC_DATA['gnb']['serialNumberList']
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    cpeIp=BASIC_DATA['cpe']['cpeSshIp']
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
    aps7100 = key_login_aps7100(BASIC_DATA['aps7100']['serialPort'], BASIC_DATA['aps7100']['serialRate'])
    for i in range (1,testNum+1):
        logging.info(key_get_time()+': run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_power_off_aps7100(aps7100)
            key_wait(30)
            key_power_on_aps7100(aps7100)
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                logging.info(key_get_time()+':power on, wait for 3min')
                key_wait(3*60)
            key_confirm_device_online(hmsObj, serialNumber)
            if isCheckCell == True:
                key_confirm_cell_status(hmsObj, enbId, 'available')
            key_wait(90)
            setupRes = key_confirm_pdu_setup_succ(cpe)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
 
@allure.story("基站上下电测试") 
@pytest.mark.基站随机上下电压测
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站随机上下电压测'] if RUN_TESTCASE.get('基站随机上下电压测') else [])
def testGnbRandomPowerOnAndPowerOff(testNum):
    serialNumber=BASIC_DATA['gnb']['serialNumberList']
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    cpeIp=BASIC_DATA['cpe']['cpeSshIp']
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
    aps7100 = key_login_aps7100(BASIC_DATA['aps7100']['serialPort'], BASIC_DATA['aps7100']['serialRate'])
    for i in range (1,testNum+1):
        logging.info(key_get_time()+': run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_power_off_aps7100(aps7100)
            key_wait(30)
            key_power_on_aps7100(aps7100)
            with allure.step(key_get_time()+':上电过程中随机再执行下电上电操作。'):
                logging.info(key_get_time()+':when the gnb is starting, random execute power off and power on')
                key_wait(random.randint(0,180))
                key_power_off_aps7100(aps7100)
                key_wait(30)
                key_power_on_aps7100(aps7100)
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                logging.info(key_get_time()+':power on, wait for 3min')
                key_wait(3*60)
            key_confirm_device_online(hmsObj, serialNumber)
            if isCheckCell == True:
                key_confirm_cell_status(hmsObj, enbId, 'available')
            key_wait(90)
            setupRes = key_confirm_pdu_setup_succ(cpe)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
     
@allure.story("CPE上下电测试")
@pytest.mark.CPE上下电测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE上下电测试'] if RUN_TESTCASE.get('CPE上下电测试') else [])
def testCpePowerOnAndPowerOff(testNum):
    cpeIp=BASIC_DATA['cpe']['cpeSshIp']
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    aps7100 = key_login_aps7100(BASIC_DATA['aps7100']['serialPort'], BASIC_DATA['aps7100']['serialRate'])
    for i in range (1,testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_power_off_aps7100(aps7100)
            key_wait(30)
            key_power_on_aps7100(aps7100)
            with allure.step(key_get_time()+':cpe复位成功，等待cpe启动完成！'):
                logging.info(key_get_time()+'cpe reset success, wait for cpe start')
                key_wait(60)
            for i in range (1,10):
                cpe = key_cpe_login(cpeIp)
                if cpe != None:
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                    else:
                        key_wait(5)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.info(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
 
@allure.story("整机上下电本地时钟测试") 
@pytest.mark.整机上下电本地时钟测试
def testLocalClockByGnbPowerOnAndOff():
    serialNumber=BASIC_DATA['gnb']['serialNumberList']
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    isPing = BASIC_DATA['cpe']['isPing']
    cpe = key_cpe_login(cpeIp)
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
    key_update_clock_source(hmsObj, enbId, 'LOCAL_CLOCK')
    key_wait(10)
    aps7100 = key_login_aps7100(BASIC_DATA['aps7100']['serialPort'], BASIC_DATA['aps7100']['serialRate'])
    key_power_off_aps7100(aps7100)
    key_wait(30)
    key_power_on_aps7100(aps7100)
    with allure.step(key_get_time()+':电源上电，等待3分钟。'):
        logging.info(key_get_time()+':power on, wait for 3min')
        key_wait(3*60)
    key_confirm_device_online(hmsObj, serialNumber)
    if isCheckCell == True:
        key_confirm_cell_status(hmsObj, enbId, 'available')
    key_cpe_detach(cpe)
    key_wait(20)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    if setupRes == 'success':
        cellId = key_cpe_attach_cell_info(cpe, cpeIp)
        assert cellId != -1,'CPE接入失败，请检查！'
        if isPing == True:
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingwifiInterface)
    with allure.step(key_get_time()+':恢复基站时钟配置'):
        logging.info(key_get_time()+': recover gnb clock config')
        key_update_clock_source(hmsObj, enbId, 'GPS')
             
@allure.story("整机复位本地时钟测试") 
@pytest.mark.整机复位本地时钟测试
def testLocalClockByGnbReboot():
    serialNumber=BASIC_DATA['gnb']['serialNumberList']
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    isPing = BASIC_DATA['cpe']['isPing']
    cpe = key_cpe_login(cpeIp)
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
    key_update_clock_source(hmsObj, enbId, 'LOCAL_CLOCK')
    key_wait(10)
    #复位基站
    key_reboot_enb(hmsObj, enbId)        
    with allure.step(key_get_time()+': 基站复位成功，等待基站重启正常'):
        logging.info(key_get_time()+': reboot success, wait for BS start')
        key_wait(180)
    key_confirm_device_online(hmsObj, serialNumber)
    if isCheckCell == True:
        key_confirm_cell_status(hmsObj, enbId, 'available')
    key_cpe_detach(cpe)
    key_wait(20)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    if setupRes == 'success':
        cellId = key_cpe_attach_cell_info(cpe, cpeIp)
        assert cellId != -1,'CPE接入失败，请检查！'
        if isPing == True:
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingwifiInterface)
    with allure.step(key_get_time()+':恢复基站时钟配置'):
        logging.info(key_get_time()+': recover gnb clock config')
        key_update_clock_source(hmsObj, enbId, 'GPS')
            
if __name__ == '__main__':
    print(random.randint(0,10))
