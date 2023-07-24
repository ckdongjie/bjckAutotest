'''
Created on 2023年5月15日

@author: autotest
'''
import logging

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_deactive_cell, key_active_cell, \
    key_confirm_cell_status, key_block_cell, key_unblock_cell
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info
from UserKeywords.maintenanceTool.MaintenanceToolManager import key_start_save_log, \
    key_stop_capture_data, key_network_data_analyse, key_close_save_log
from UserKeywords.ue.CpeManager import key_start_ue_log_trace, \
    key_stop_ue_log_trace, key_qxdm_log_save
from UserKeywords.ue.Mate30Manager import key_login_mate30, key_mate30_detach, \
    key_mate30_attach, key_query_attach_info, key_logout_mate30


@allure.story("Mate30注册去注册后接入成功率测试")
@pytest.mark.Mate30注册去注册后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['Mate30注册去注册后接入成功率测试'] if RUN_TESTCASE.get('Mate30注册去注册后接入成功率测试') else [])
def testMate30DetachAndAttachAccessSuccRate(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    ueLogFilePath = ''
    mate30 = key_login_mate30()
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_mate30_detach(mate30)
                with allure.step(key_get_time()+': CPE去注册后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_mate30_attach(mate30)
                with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                attachStatus, cellInfo = key_query_attach_info(mate30)
                if attachStatus != '-1':
                    AccSuccNum = AccSuccNum + 1
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': Mate30接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': Mate30 access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    finally:
        key_logout_mate30(mate30)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        if ueLogFilePath != '':
            key_qxdm_log_save(ueLogFilePath)
        
@allure.story("去激活激活小区后mate30接入成功率测试")
@pytest.mark.去激活激活小区后mate30接入成功率测试
@pytest.mark.run(order=14)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['去激活激活小区后mate30接入成功率测试'] if RUN_TESTCASE.get('去激活激活小区后mate30接入成功率测试') else [])
def testDeactiveAndActiveMate30AccessSuccRate(testNum):
    AccSuccNum = 0
    ueLogFilePath = ''
    mate30 = key_login_mate30()
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_deactive_cell(hmsObj, enbId)
                with allure.step(key_get_time()+':去激活小区成功，等待5s'):
                    logging.warning(key_get_time()+':deactive success, wait for 5s')
                    key_wait(5)
                key_active_cell(hmsObj, enbId)
                key_confirm_cell_status(hmsObj, enbId, 'available')
                key_wait(30)
                attachStatus, cellInfo = key_query_attach_info(mate30)
                if attachStatus != '-1':
                    AccSuccNum = AccSuccNum + 1
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
               
@allure.story("闭塞解闭塞小区后Mate30接入成功率测试")
@pytest.mark.闭塞解闭塞小区后Mate30接入成功率测试
@pytest.mark.run(order=15)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞解闭塞小区后Mate30接入成功率测试'] if RUN_TESTCASE.get('毫米波的 V2.00.20版本') else [])
def testBlockAndUnblockCellMate30AccessSuccRate(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    mate30 = key_login_mate30()
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj)
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_block_cell(hmsObj, enbId)
                with allure.step(key_get_time()+':闭塞小区成功，等待5s'):
                    logging.warning(key_get_time()+':block cell success, wait for 5s')
                    key_wait(5)
                key_unblock_cell(hmsObj, enbId)
                key_confirm_cell_status(hmsObj, enbId, 'available')
                attachStatus, cellInfo = key_query_attach_info(mate30)
                if attachStatus != '-1':
                    AccSuccNum = AccSuccNum + 1
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': Mate30接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': Mate30 access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)