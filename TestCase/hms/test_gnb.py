# coding = utf-8 
'''
Created on 2022年9月7日

@author: dj
'''
import logging
import os
import sys

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_confirm_cell_status, key_block_cell, \
    key_unblock_cell
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.DiagnosticManager import key_reboot_enb, key_gnb_ping_diag, \
    key_get_ping_diag_result, key_gnb_trace_route_diag, \
    key_get_trace_route_diag_result
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms, \
    key_get_enb_ip
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_confirm_pdu_setup_succ, key_cpe_detach, key_cpe_logout


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()

@allure.story("复位基站正常后ping包")  
@pytest.mark.复位基站正常后ping包
@pytest.mark.run(order=12)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.parametrize("testNum",RUN_TESTCASE['复位基站正常后ping包'] if RUN_TESTCASE.get('复位基站正常后ping包') else [])
def testRebootGnbAndPing(testNum):
    hmsObj=key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    for i in range (1,testNum+1):
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            rebootRes = key_reboot_enb(hmsObj, enbId)
            assert rebootRes == 'success','基站复位操作失败，请检查！'   
            with allure.step(key_get_time()+':等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
            key_confirm_device_online(hmsObj)
            key_confirm_cell_status(hmsObj, enbId, 'available')
            with allure.step('CPE接入并ping包测试'):
                cpe = key_cpe_login()
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                assert setupRes == 'success','cpe接入失败，请检查！'
                key_wait(5)
                key_cpe_ping(cpe, pingInterface = '')
                key_cpe_logout(cpe)

@allure.story("复位基站正常后ping包_5524")  
@pytest.mark.复位基站正常后ping包_5524
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.parametrize("testNum",RUN_TESTCASE['复位基站正常后ping包_5524'] if RUN_TESTCASE.get('复位基站正常后ping包_5524') else [])
def testRebootGnbAndPing5524(testNum):
    hmsObj=key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    for i in range (1,testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            rebootRes = key_reboot_enb(hmsObj, enbId)
            assert rebootRes == 'success','基站复位操作失败，请检查！'   
            with allure.step(key_get_time()+':等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
            key_confirm_device_online(hmsObj)
            with allure.step(key_get_time()+':查询nr小区状态'):
                logging.info(key_get_time()+': query nr cell status')
                key_confirm_cell_status(hmsObj, enbId, 'available', cellId=1)
            #mmw cell
            with allure.step(key_get_time()+':查询mmw小区状态'):
                logging.info(key_get_time()+': query mmw cell status')
                key_confirm_cell_status(hmsObj, enbId, 'available', cellId=2)
            with allure.step('CPE接入并ping包测试'):
                cpe = key_cpe_login()
                key_cpe_detach(cpe)
                key_wait(2)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                assert setupRes == 'success','cpe接入失败，请检查！'
                key_wait(5)
                key_cpe_ping(cpe, pingInterface = '')
                key_cpe_detach(cpe)

@allure.story("闭塞小区后复位基站") 
@pytest.mark.闭塞小区后复位基站
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞小区后复位基站'] if RUN_TESTCASE.get('闭塞小区后复位基站') else [])
def testBlockCellAndRebootGnb(testNum):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    hmsObj=key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    for i in range (1,testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_block_cell(hmsObj, enbId)
            key_wait(2)
            rebootRes = key_reboot_enb(hmsObj, enbId)
            assert rebootRes == 'success','基站复位操作失败，请检查！'
            with allure.step(key_get_time()+':等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
            key_confirm_device_online(hmsObj)
            key_confirm_cell_status(hmsObj, enbId, 'unavailable')
            with allure.step(key_get_time()+':恢复小区状态'):
                key_unblock_cell(hmsObj, enbId)
                key_wait(2)
            key_confirm_cell_status(hmsObj, enbId, 'available')
            with allure.step('CPE接入并ping包测试'):
                cpe = key_cpe_login()
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                assert setupRes == 'success','cpe接入失败，请检查！'
                key_wait(5)
                key_cpe_ping(cpe, pingInterface = pingNrInterface)
                key_cpe_ping(cpe, pingInterface = pingwifiInterface)
                    
@allure.story("基站诊断测试") 
@pytest.mark.基站ping包诊断测试
@pytest.mark.parametrize("pingTimes",RUN_TESTCASE['基站ping包诊断测试'] if RUN_TESTCASE.get('基站ping包诊断测试') else [])                    
def testPingDiagnosis(pingTimes):
    hmsObj=key_login_hms()
    with allure.step(key_get_time()+'执行基站ping诊断测试'):
        logging.info(key_get_time()+':exec gnb ping diagnosis')
        enbIp = key_get_enb_ip(hmsObj)
        clientId = key_gnb_ping_diag(hmsObj, pingTimes, enbIp)
        key_get_ping_diag_result(hmsObj, pingTimes, clientId)
                    
@allure.story("基站诊断测试") 
@pytest.mark.基站跟踪路由诊断测试
def testTraceRouteDiagnosis():
    hmsObj=key_login_hms()
    with allure.step(key_get_time()+'执行基站跟踪路由诊断测试'):
        logging.info(key_get_time()+':exec gnb trace route diagnosis')
        enbIp = key_get_enb_ip(hmsObj)
        clientId = key_gnb_trace_route_diag(hmsObj, enbIp)
        key_get_trace_route_diag_result(hmsObj, clientId)

if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass