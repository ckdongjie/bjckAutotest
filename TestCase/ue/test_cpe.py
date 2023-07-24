# coding = utf-8 
'''
Created on 2022年9月7日

@author: dj
'''
import logging
import os
import sys
import threading

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.attenuator.Attenuator import key_connect_attenuator, \
    key_send_multi_channel, key_read_multi_channel, key_disconnect_attenuator
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.gnb.gnbManager import key_ssh_login_gnb, key_close_aip_channel, \
    key_close_sub6g_channel, key_logout_gnb, key_open_aip_channel, \
    key_open_sub6g_channel
from UserKeywords.hms.CellManager import key_confirm_cell_status, \
    key_deactive_cell, key_active_cell, key_block_cell, key_unblock_cell
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.DuConfigManager import key_modify_du_dl_schedule_switch
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.maintenanceTool.MaintenanceToolManager import key_stop_capture_data, key_network_data_analyse, \
    key_start_save_log, key_close_save_log
from UserKeywords.pdn.pndManager import key_pdn_login, key_pdn_logout
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_cpe_detach, key_cpe_attach, key_confirm_pdu_setup_succ, \
    key_cpe_attach_cell_info, key_reboot_cpe, key_confirm_pdu_setup_fail, \
    key_dl_udp_nr_flow_test, key_dl_tcp_nr_flow_test, key_dl_tcp_wifi_flow_test, \
    key_ul_tcp_nr_flow_test, key_dl_udp_wifi_flow_test, \
    key_ul_tcp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_udl_tcp_nr_flow_test, \
    key_udl_tcp_wifi_flow_test, key_udl_udp_nr_flow_test, \
    key_udl_udp_wifi_flow_test, key_start_ue_log_trace, key_stop_ue_log_trace, \
    key_qxdm_log_save, key_cpe_logout


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


globalPara.init()

@allure.story("CPE注册去注册后接入成功率测试")
@pytest.mark.CPE注册去注册后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE注册去注册后接入成功率测试'] if RUN_TESTCASE.get('CPE注册去注册后接入成功率测试') else [])
def testDetachAndAttachAccessSuccRate(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    ueLogFilePath = ''
    cpe = key_cpe_login()
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_cpe_detach(cpe)
                with allure.step(key_get_time()+': CPE去注册后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_cpe_attach(cpe)
                with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                cellPci = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellPci != -1:
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
        key_cpe_logout(cpe)
        if ueLogFilePath != '':
            key_qxdm_log_save(ueLogFilePath)
    

@allure.story("CPE复位后接入成功率测试")
@pytest.mark.CPE复位后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE复位后接入成功率测试'] if RUN_TESTCASE.get('CPE复位后接入成功率测试') else [])
def testCpeRebootAccessSuccRate(testNum):
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_reboot_cpe(cpe)
                with allure.step(key_get_time()+':cpe复位成功，等待cpe启动完成！'):
                    logging.warning(key_get_time()+'cpe reset success, wait for cpe start')
                    key_wait(60)
                for i in range (1,10):
                    cpe = key_cpe_login()
                    if cpe != None:
                        setupRes = key_confirm_pdu_setup_succ(cpe)
                        if setupRes == 'success':
                            break
                        else:
                            key_wait(5)
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
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
        key_cpe_logout(cpe)
        if ueLogFilePath != '':
            key_qxdm_log_save(ueLogFilePath)
    
@allure.story("基站复位后CPE接入成功率测试")
@pytest.mark.run(order=13)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@pytest.mark.基站复位后CPE接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站复位后CPE接入成功率测试'] if RUN_TESTCASE.get('基站复位后CPE接入成功率测试') else [])
def testRebootGnbAccessSuccRate(testNum):
    ueLogFilePath = ''
    attachDelay=BASIC_DATA['attach']['attachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    for i in range (0, 10):
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            break
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_reboot_enb(hmsObj, enbId)
                with allure.step(key_get_time()+': 基站复位成功，等待基站重启正常'):
                    logging.info(key_get_time()+': reboot success, wait for BS start')
                    key_wait(180)
                key_confirm_cell_status(hmsObj, enbId, 'available')
                key_wait(90)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
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
        key_cpe_logout(cpe)
        if ueLogFilePath != '':    
            key_qxdm_log_save(ueLogFilePath)
            
@allure.story("去激活激活小区后CPE接入成功率测试")
@pytest.mark.去激活激活小区后CPE接入成功率测试
@pytest.mark.run(order=14)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['去激活激活小区后CPE接入成功率测试'] if RUN_TESTCASE.get('去激活激活小区后CPE接入成功率测试') else [])
def testDeactiveAndActiveCellAccessSuccRate(testNum):
    AccSuccNum = 0
    ueLogFilePath = ''
    cpe = key_cpe_login()
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
                with allure.step(key_get_time()+':去激活小区成功，等待5min'):
                    logging.warning(key_get_time()+':deactive success, wait for 5min')
                    key_wait(5*60)
                key_active_cell(hmsObj, enbId)
                key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                key_wait(30)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
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
        key_cpe_logout(cpe)
    
@allure.story("闭塞解闭塞小区后接入成功率测试")
@pytest.mark.闭塞解闭塞小区后接入成功率测试
@pytest.mark.run(order=15)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞解闭塞小区后接入成功率测试'] if RUN_TESTCASE.get('闭塞解闭塞小区后接入成功率测试') else [])
def testBlockAndUnblockAccessSuccRate(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
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
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellPci = key_cpe_attach_cell_info(cpe)
                    assert cellPci != -1,'CPE接入失败，请检查！'
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
        key_cpe_logout(cpe)
 
@allure.story("关闭打开通道射频后CPE接入ping测试")
@pytest.mark.关闭打开通道射频后CPE接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭打开通道射频后CPE接入ping测试'] if RUN_TESTCASE.get('关闭打开通道射频后CPE接入ping测试') else [])
def testCloseChannelAndAttachAndPingTest(testNum):
    ueLogFilePath = ''
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    with allure.step(key_get_time()+'环境初始化'):
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(detachDelay)
        key_cpe_attach(cpe)
        key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #close channel
                with allure.step(key_get_time()+': 关闭通道信号，并确认终端掉线'):
                    logging.info(key_get_time()+': close channel, make sure cpe is detached')
                    gnb = key_ssh_login_gnb()
                    key_close_aip_channel(gnb)
                    key_close_sub6g_channel(gnb)
                    key_logout_gnb(gnb)
                    key_wait(60)
                    setupRes = key_confirm_pdu_setup_fail(cpe)
                    assert setupRes == 'failure','pdu建立未掉线，请检查 ！'
                #open channel
                with allure.step(key_get_time()+': 打开通道信号，并确认终端上线'):
                    logging.info(key_get_time()+': open channel, make sure cpe is attached')
                    gnb = key_ssh_login_gnb()
                    key_open_aip_channel(gnb)
                    key_open_sub6g_channel(gnb)
                    key_logout_gnb(gnb)
                    key_wait(60)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
                    AccSuccNum = AccSuccNum + 1
                    key_cpe_ping(cpe, pingInterface = '')
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        gnb = key_ssh_login_gnb()
        key_open_aip_channel(gnb)
        key_open_sub6g_channel(gnb)
        key_logout_gnb(gnb)
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
         
@allure.story("关闭2s后打开通道射频CPE接入ping测试")
@pytest.mark.关闭2s后打开通道射频CPE接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭2s后打开通道射频CPE接入ping测试'] if RUN_TESTCASE.get('关闭2s后打开通道射频CPE接入ping测试') else [])
def testCloseChannelWait2SAttachAndPingTest(testNum):
    ueLogFilePath = ''
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    with allure.step(key_get_time()+'环境初始化'):
        logging.info(key_get_time()+': device setup')
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(detachDelay)
        key_cpe_attach(cpe)
        key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #close channel
                with allure.step(key_get_time()+': 关闭通道信号，并确认终端掉线'):
                    logging.info(key_get_time()+': close channel, make sure cpe is detached')
                    gnb = key_ssh_login_gnb()
                    key_close_aip_channel(gnb)
                    key_close_sub6g_channel(gnb)
                    key_logout_gnb(gnb)
                with allure.step(key_get_time()+': 等待2秒'):
                    logging.info(key_get_time()+': wait for 2s')
                    key_wait(2)
                #open channel
                with allure.step(key_get_time()+': 打开通道信号，并确认终端上线'):
                    logging.info(key_get_time()+': open channel, make sure cpe is attached')
                    gnb = key_ssh_login_gnb()
                    key_open_aip_channel(gnb)
                    key_open_sub6g_channel(gnb)
                    key_logout_gnb(gnb)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
                    AccSuccNum = AccSuccNum + 1
                    key_cpe_ping(cpe, pingInterface = '')
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        gnb = key_ssh_login_gnb()
        key_open_aip_channel(gnb)
        key_open_sub6g_channel(gnb)
        key_logout_gnb(gnb)
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        
@allure.story("设置程控衰减极值恢复后接入ping测试")
@pytest.mark.设置程控衰减极值恢复后接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['设置程控衰减极值恢复后接入ping测试'] if RUN_TESTCASE.get('设置程控衰减极值恢复后接入ping测试') else [])
def testAttMaxAttachAndPingTest(testNum):
    ueLogFilePath = ''
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    with allure.step(key_get_time()+'环境初始化'):
        attenuator = key_connect_attenuator()
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(detachDelay)
        key_cpe_attach(cpe)
        key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #att max
                with allure.step(key_get_time()+': 设置程控衰减到最大值，并确认终端掉线'):
                    logging.info(key_get_time()+': set attenuator max, make sure cpe is detached')
                    key_send_multi_channel(attenuator, '1,2,3,4', 110)
                    key_read_multi_channel(attenuator, '1,2,3,4')
                    key_wait(20)
                    setupRes = key_confirm_pdu_setup_fail(cpe)
                    assert setupRes == 'failure','pdu建立未掉线，请检查 ！'
                #att 0
                with allure.step(key_get_time()+': 恢复程控衰减值，并确认终端上线'):
                    logging.info(key_get_time()+': open channel, make sure cpe is attached')
                    key_send_multi_channel(attenuator, '1,2,3,4', 0)
                    key_read_multi_channel(attenuator, '1,2,3,4')
                    key_wait(20)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellId = key_cpe_attach_cell_info(cpe)
                    assert cellId != -1,'CPE接入失败，请检查！'
                    AccSuccNum = AccSuccNum + 1
                    key_cpe_ping(cpe, pingInterface = '')
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        
@allure.story("设置程控衰减极值等待2秒恢复后接入ping测试")
@pytest.mark.设置程控衰减极值等待2秒恢复后接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['设置程控衰减极值等待2秒恢复后接入ping测试'] if RUN_TESTCASE.get('设置程控衰减极值等待2秒恢复后接入ping测试') else [])
def testAttMaxWait2AttachAndPingTest(testNum):
    ueLogFilePath = ''
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    with allure.step(key_get_time()+'环境初始化'):
        logging.info(key_get_time()+': device setup')
        attenuator = key_connect_attenuator()
        cpe = key_cpe_login()
        key_cpe_detach(cpe)
        key_wait(detachDelay)
        key_cpe_attach(cpe)
        key_wait(attachDelay)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        assert setupRes == 'success','pdu建立失败，请检查 ！'
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #att max
                with allure.step(key_get_time()+': 设置程控衰减到最大值，并确认终端掉线'):
                    logging.info(key_get_time()+': set attenuator max, make sure cpe is detached')
                    key_send_multi_channel(attenuator, '1,2,3,4', 110)
                    key_read_multi_channel(attenuator, '1,2,3,4')
                with allure.step(key_get_time()+': 程控衰减设置后等待2秒'):
                    logging.info(key_get_time()+': set att and wait 2s')
                    key_wait(2)
                #att 0
                with allure.step(key_get_time()+': 恢复程控衰减值，并确认终端上线'):
                    logging.info(key_get_time()+': open channel, make sure cpe is attached')
                    key_send_multi_channel(attenuator, '1,2,3,4', 0)
                    key_read_multi_channel(attenuator, '1,2,3,4')
                    key_wait(20)
                for i in range (0, 10):
                    setupRes = key_confirm_pdu_setup_succ(cpe)
                    if setupRes == 'success':
                        break
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
                    AccSuccNum = AccSuccNum + 1
                    key_cpe_ping(cpe, pingInterface = '')
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
 
@allure.story("UDP下行流量测试")
@pytest.mark.UDP下行流量测试
def testDlUdpFlowTest():
    ueLogFilePath = ''
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        cpe = cpeLoginAndAttach()
        pdn = key_pdn_login()
        key_dl_udp_nr_flow_test(cpe, pdn)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_pdn_logout(pdn)
     
@allure.story("TCP下行流量测试_动态调度")
@pytest.mark.TCP下行流量测试_动态调度
def testDlTcpFlowTest_DynamicScheduling():
    ueLogFilePath = ''
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
#        修改调度类型为动态调度
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        cpe = cpeLoginAndAttach()
        pdn = key_pdn_login()
        key_dl_tcp_nr_flow_test(cpe, pdn)
        key_wait(10)
        key_dl_tcp_wifi_flow_test(cpe, pdn)
        key_cpe_detach(cpe)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_pdn_logout(pdn)
 
@allure.story("TCP下行流量测试_预调度")
@pytest.mark.TCP下行流量测试_预调度
def testDlTcpFlowTest_PreScheduling():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    #修改下行预调试开关
    ueLogFilePath = ''
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'open')
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        cpe = cpeLoginAndAttach()
        pdn = key_pdn_login()
        key_dl_tcp_nr_flow_test(cpe, pdn)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_pdn_logout(pdn)
    #修改下行预调试开关
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
     
@allure.story("TCP上行流量测试")
@pytest.mark.TCP上行流量测试
def testUlTcpFlowTest():
    ueLogFilePath = ''
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        cpe = cpeLoginAndAttach()
        pdn = key_pdn_login()
        key_ul_tcp_nr_flow_test(cpe, pdn)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_pdn_logout(pdn)
             
@allure.story("程控衰减近点ping包测试")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点ping包测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['程控衰减近点ping包测试'] if RUN_TESTCASE.get('程控衰减近点ping包测试') else [])
def testAttenuatorNearPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减近点ping包测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cpePintTest(testNum)
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("程控衰减远点ping包测试")
@pytest.mark.run(order=4)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点ping包测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['程控衰减远点ping包测试'] if RUN_TESTCASE.get('程控衰减远点ping包测试') else [])
def testAttenuatorFarPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减远点ping包测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cpePintTest(testNum)
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        
@allure.story("程控衰减近点tcp上行流量测试")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp上行流量测试
def testAttenuatorNearPointUlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减近点tcp上行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("程控衰减近点tcp下行流量测试")
@pytest.mark.run(order=6)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp下行流量测试
def testAttenuatorNearPointDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减近点tcp下行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("程控衰减近点tcp上下行流量测试")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp上下行流量测试
def testAttenuatorNearPointUlDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 近点tcp上下行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
                assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
                 
@allure.story("程控衰减远点tcp上行流量测试")
@pytest.mark.run(order=8)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp上行流量测试
def testAttenuatorFarPointUlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp上行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
 
@allure.story("程控衰减远点tcp下行流量测试")
@pytest.mark.run(order=9)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp下行流量测试
def testAttenuatorFarPointDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp下行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
 
@allure.story("程控衰减远点tcp上下行流量测试")
@pytest.mark.run(order=10)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp上下行流量测试
def testAttenuatorFarPointUlDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
    expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp上下行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
                assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        
@allure.story("程控衰减tcp上下行流量打点测试")
@pytest.mark.run(order=11)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减tcp上下行流量打点测试
def testAttenuatorEachPointUlDlTrafficTest():
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    cpe2 = key_cpe_login()
    pdn2 = key_pdn_login()
    ueLogFilePath = ''
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        with allure.step(key_get_time()+': tcp上下行流量打点测试'):
            logging.info(key_get_time()+': set point cell traffic test') 
            trafTh = threading.Thread(target=key_udl_tcp_nr_flow_test, args=(cpe, cpe2, pdn, pdn2))
            attTh = threading.Thread(target=cyclicSetPoint,args=(4,))
            trafTh.start()
            key_wait(30)
            attTh.start()
            trafTh.join()
            attTh.join()
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
    finally:
        attenuator = key_connect_attenuator()
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_cpe_logout(cpe2)
        key_pdn_logout(pdn)
        key_pdn_logout(pdn2)
        
'''
            程控衰减打点测试
'''
def cyclicSetPoint(cycNum):
    attenuator = key_connect_attenuator()
    for num in range(0, cycNum):
        with allure.step(key_get_time()+': 循环打点程控衰减'):
            logging.info(key_get_time()+': cyclic set attenuator') 
            if num % 2 == 0:
                stepAdd = True
                counter = 0
            else:
                stepAdd = False
                counter = 25
            if stepAdd == True:
                while counter < 25:
                    with allure.step(key_get_time()+': 设置程控衰减，值：'+str(counter)):
                        logging.info(key_get_time()+': set attenuator:'+str(counter)) 
                        counter = counter+1
                        key_wait(1)
            else:
                while counter > 0:
                    with allure.step(key_get_time()+': 设置程控衰减，值：'+str(counter)):
                        logging.info(key_get_time()+': set attenuator:'+str(counter)) 
                        counter = counter-1
                        key_wait(1)
    key_disconnect_attenuator(attenuator)            

'''
    cpe ping包测试
'''
def cpePintTest(testNum): 
    ueLogFilePath = ''   
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    cpe = key_cpe_login()
    AccSuccNum = 0           
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
        for i in range(1, testNum +1):
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                key_cpe_detach(cpe)
                with allure.step(key_get_time()+': CPE去注册后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_cpe_attach(cpe)
                with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                cellId = key_cpe_attach_cell_info(cpe)
                if setupRes == 'success' and cellId != -1:
                    AccSuccNum = AccSuccNum + 1
                    key_cpe_ping(cpe, pingInterface = '')
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
        key_cpe_logout(cpe)

'''
    1 登录cpe
    2 执行detach
    3 等待3s
    4 执行attach
    5 确认接入成功
'''
def cpeLoginAndAttach():
    cpe = key_cpe_login()
    key_cpe_detach(cpe)
    key_wait(3)
    key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe, tryNum=500)
    assert setupRes == 'success', 'cpe接入失败，请检查！'
    return cpe

#小区流量测试    
def cellTrafficTest(dir='DL', AsType='NR', traType='TCP'):
    ueLogFilePath = ''
    cpe,cpe2,pdn,pdn2 = None,None,None,None
    avgDlTraf, avgUlTraf = 0, 0
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
        cpe = cpeLoginAndAttach()
        pdn = key_pdn_login()
        if dir=='DL':
            if traType=='TCP':
                if AsType=='NR':
                    avgDlTraf = key_dl_tcp_nr_flow_test(cpe, pdn)
                elif AsType=='WIFI':
                    avgDlTraf = key_dl_tcp_wifi_flow_test(cpe, pdn)
            elif traType=='UDP':
                if AsType=='NR':
                    avgDlTraf = key_dl_udp_nr_flow_test(cpe, pdn)
                elif AsType=='WIFI':
                    avgDlTraf = key_dl_udp_wifi_flow_test(cpe, pdn)
        elif dir=='UL':
            if traType=='TCP':
                if AsType=='NR':
                    avgUlTraf = key_ul_tcp_nr_flow_test(cpe, pdn)
                elif AsType=='WIFI':
                    avgUlTraf = key_ul_tcp_wifi_flow_test(cpe, pdn)
            elif traType=='UDP':
                if AsType=='NR':
                    avgUlTraf = key_ul_udp_nr_flow_test(cpe, pdn)
                elif AsType=='WIFI':
                    avgUlTraf = key_ul_udp_wifi_flow_test(cpe, pdn)
        elif dir=='UDL':
            cpe2 = cpeLoginAndAttach()
            pdn2 = key_pdn_login()
            if traType=='TCP':
                if AsType=='NR':
                    avgDlTraf, avgUlTraf = key_udl_tcp_nr_flow_test(cpe, cpe2, pdn, pdn2)
                elif AsType=='WIFI':
                    avgDlTraf, avgUlTraf = key_udl_tcp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
            elif traType=='UDP':
                if AsType=='NR':
                    avgDlTraf, avgUlTraf = key_udl_udp_nr_flow_test(cpe, cpe2, pdn, pdn2)
                elif AsType=='WIFI':
                    avgDlTraf, avgUlTraf = key_udl_udp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        return avgDlTraf, avgUlTraf
    finally:
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
        key_cpe_logout(cpe)
        key_cpe_logout(cpe2)
        key_pdn_logout(pdn)
        key_pdn_logout(pdn2)
    

@allure.story("ping包测试_CPE")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.ping包测试_CPE
@pytest.mark.parametrize("testNum",RUN_TESTCASE['ping包测试_CPE'] if RUN_TESTCASE.get('ping包测试_CPE') else [])
def testNearPointPingTest(testNum):
    with allure.step(key_get_time()+': cpe ping包测试'):
        logging.info(key_get_time()+': cpe ping test') 
        cpePintTest(testNum)
 
@allure.story("NR上行TCP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR上行TCP流量测试_CPE
def testCpeNrUlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    with allure.step(key_get_time()+': NR上行TCP流量测试'):
        logging.info(key_get_time()+': NR UL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlTcpTraf, 'NR上行TCP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI上行TCP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI上行TCP流量测试_CPE
def testCpeWifiUlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    with allure.step(key_get_time()+': WIFI上行TCP流量测试'):
        logging.info(key_get_time()+': WIFI UL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'WIFI', 'TCP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlTcpTraf, 'WIFI上行TCP流量测试结果不及预期，请检查！'
            
@allure.story("NR下行TCP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR下行TCP流量测试_CPE
def testCpeNrDlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': NR下行TCP流量测试'):
        logging.info(key_get_time()+': NR DL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'NR下行TCP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI下行TCP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI下行TCP流量测试_CPE
def testCpeWifiDlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': WIFI下行TCP流量测试'):
        logging.info(key_get_time()+': WIFI DL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'WIFI', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'WIFI下行TCP流量测试结果不及预期，请检查！'

@allure.story("NR上下行TCP流量测试_CPE")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR上下行TCP流量测试_CPE
def testNrUlDlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': NR上下行TCP流量测试'):
        logging.info(key_get_time()+': NR UL&DL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'NR下行TCP流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expNearUlTcpTraf, 'NR上行TCP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI上下行TCP流量测试_CPE")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI上下行TCP流量测试_CPE
def testWifiUlDlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': WIFI上下行TCP流量测试'):
        logging.info(key_get_time()+': WIFI UL&DL TCP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'WIFI', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'WIFI下行TCP流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expNearUlTcpTraf, 'WIFI上行TCP流量测试结果不及预期，请检查！'
            
@allure.story("NR上行UDP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR上行UDP流量测试_CPE
def testCpeNrUlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlUdpTraf = BASIC_DATA['traffic']['expNearUlUdpTraf']
    with allure.step(key_get_time()+': NR上行UDP流量测试'):
        logging.info(key_get_time()+': NR UL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'UDP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlUdpTraf, 'NR上行UDP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI上行UDP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI上行UDP流量测试_CPE
def testCpeWifiUlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlUdpTraf = BASIC_DATA['traffic']['expNearUlUdpTraf']
    with allure.step(key_get_time()+': WIFI上行UDP流量测试'):
        logging.info(key_get_time()+': WIFI UL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'WIFI', 'UDP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlUdpTraf, 'WIFI上行UDP流量测试结果不及预期，请检查！'
            
@allure.story("NR下行UDP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR下行UDP流量测试_CPE
def testCpeNrDlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlUdpTraf = BASIC_DATA['traffic']['expNearDlUdpTraf']
    with allure.step(key_get_time()+': NR下行UDP流量测试'):
        logging.info(key_get_time()+': NR DL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'UDP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlUdpTraf, 'NR下行UDP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI下行UDP流量测试_CPE")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI下行UDP流量测试_CPE
def testCpeWifiDlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlUdpTraf = BASIC_DATA['traffic']['expNearDlUdpTraf']
    with allure.step(key_get_time()+': WIFI下行UDP流量测试'):
        logging.info(key_get_time()+': WIFI DL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'WIFI', 'UDP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlUdpTraf, 'WIFI下行UDP流量测试结果不及预期，请检查！'

@allure.story("NR上下行UDP流量测试_CPE")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.NR上下行UDP流量测试_CPE
def testNrUlDlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlUdpTraf = BASIC_DATA['traffic']['expNearUlUdpTraf']
    expNearDlUdpTraf = BASIC_DATA['traffic']['expNearDlUdpTraf']
    with allure.step(key_get_time()+': NR上下行UDP流量测试'):
        logging.info(key_get_time()+': NR UL&DL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'UDP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlUdpTraf, 'NR下行UDP流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expNearUlUdpTraf, 'NR上行UDP流量测试结果不及预期，请检查！'
            
@allure.story("WIFI上下行UDP流量测试_CPE")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.WIFI上下行UDP流量测试_CPE
def testWifiUlDlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlUdpTraf = BASIC_DATA['traffic']['expNearUlUdpTraf']
    expNearDlUdpTraf = BASIC_DATA['traffic']['expNearDlUdpTraf']
    with allure.step(key_get_time()+': WIFI上下行UDP流量测试'):
        logging.info(key_get_time()+': WIFI UL&DL UDP traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'WIFI', 'UDP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlUdpTraf, 'WIFI下行UDP流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expNearUlUdpTraf, 'WIFI上行UDP流量测试结果不及预期，请检查！'

# @allure.story("近点udp上行nr流量测试")
# @pytest.mark.run(order=5)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.近点udp上行nr流量测试
# def testNearPointUlUdpNrTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
#     with allure.step(key_get_time()+': 近点tcp上行流量测试'):
#         logging.info(key_get_time()+': near point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'UDP')
#         if isCheckTraffic == True:
#             assert avgUlTraf >= expNearUlTcpTraf, 'udp上行nr流量测试结果不及预期，请检查！'
#  
# @allure.story("近点tcp下行nr流量测试")
# @pytest.mark.run(order=6)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.近点tcp下行nr流量测试
# def testNearPointDlTcpNrTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
#     with allure.step(key_get_time()+': 近点tcp下行流量测试'):
#         logging.info(key_get_time()+': near point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'TCP')
#         if isCheckTraffic == True:
#             assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
#             
# @allure.story("近点tcp下行wifi流量测试")
# @pytest.mark.run(order=6)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.近点tcp下行wifi流量测试
# def testNearPointDlTcpWifiTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
#     with allure.step(key_get_time()+': 近点tcp下行流量测试'):
#         logging.info(key_get_time()+': near point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'WIFI', 'TCP')
#         if isCheckTraffic == True:
#             assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
#             
#  
# @allure.story("近点tcp上下行流量测试")
# @pytest.mark.run(order=7)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.近点tcp上下行流量测试
# def testNearPointUlDlTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
#     expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
#     with allure.step(key_get_time()+': 近点tcp上下行流量测试'):
#         logging.info(key_get_time()+': near point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'TCP')
#         if isCheckTraffic == True:
#             assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
#             assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
#             
#                  
# @allure.story("远点tcp上行流量测试")
# @pytest.mark.run(order=8)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.远点tcp上行流量测试
# def testFarPointUlTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
#     with allure.step(key_get_time()+': 远点tcp上行流量测试'):
#         logging.info(key_get_time()+': far point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('UL', 'NR', 'TCP')
#         if isCheckTraffic == True:
#             assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
#         
# @allure.story("远点tcp下行流量测试")
# @pytest.mark.run(order=9)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.远点tcp下行流量测试
# def testFarPointDlTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
#     with allure.step(key_get_time()+': 远点tcp下行流量测试'):
#         logging.info(key_get_time()+': far point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('DL', 'NR', 'TCP')
#         if isCheckTraffic == True:
#             assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
#             
#  
# @allure.story("远点tcp上下行流量测试")
# @pytest.mark.run(order=10)
# @pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
# @pytest.mark.远点tcp上下行流量测试
# def testFarPointUlDlTrafficTest():
#     isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
#     expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
#     expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
#     with allure.step(key_get_time()+': 远点tcp上下行流量测试'):
#         logging.info(key_get_time()+': far point ping test') 
#         avgDlTraf, avgUlTraf = cellTrafficTest('UDL', 'NR', 'TCP')
#         if isCheckTraffic == True:
#             assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
#             assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
            
if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass