# coding = utf-8 
'''
Created on 2023年5月15日

@author: autotest
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
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.maintenanceTool.MaintenanceToolManager import key_stop_capture_data, key_network_data_analyse, \
    key_start_save_log, key_close_save_log
from UserKeywords.pdn.pndManager import key_pdn_login, key_pdn_logout
from UserKeywords.ue.CpeManager import key_start_ue_log_trace, key_stop_ue_log_trace, \
    key_qxdm_log_save
from UserKeywords.ue.MobilePhoneManager import key_get_devices_list, \
    key_set_phone_airplan_model, key_set_phone_no_airplan_model, key_phone_ping, \
    key_get_phone_ip, key_phone_dl_tcp_nr_traffic, key_phone_dl_udp_nr_traffic, \
    key_phone_ul_tcp_nr_traffic, key_phone_ul_udp_nr_traffic, \
    key_phone_udl_tcp_nr_traffic, key_phone_udl_udp_nr_traffic, \
    key_query_access_status, key_phone_dl_tcp_nr_traffic_port_banding, \
    key_phone_ul_tcp_nr_traffic_port_banding, \
    key_phone_dl_udp_nr_traffic_port_banding, \
    key_phone_ul_udp_nr_traffic_port_banding


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

globalPara.init()

@allure.story("手机飞行去飞行后接入成功率测试")
@pytest.mark.手机飞行去飞行后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['手机飞行去飞行后接入成功率测试'] if RUN_TESTCASE.get('手机飞行去飞行后接入成功率测试') else [])
def testAirplaneAndNoAirplaneAccessSuccRate(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    ueLogFilePath = ''
    device = key_get_devices_list()[0]
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        for i in range (1,testNum+1):
            logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                key_set_phone_airplan_model(device)
                with allure.step(key_get_time()+': 手机飞行模式后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_set_phone_no_airplan_model(device)
                with allure.step(key_get_time()+': 手机去飞行模式后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
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
        if ueLogFilePath != '':
            key_qxdm_log_save(ueLogFilePath)
    
@allure.story("基站复位后接入成功率测试_手机终端")
@pytest.mark.run(order=13)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@pytest.mark.基站复位后接入成功率测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站复位后接入成功率测试_手机终端'] if RUN_TESTCASE.get('基站复位后接入成功率测试_手机终端') else [])
def testRebootGnbPhoneAccessSuccRate(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    device = key_get_devices_list()[0]
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
                key_set_phone_airplan_model(device)
                key_wait(5)
                key_set_phone_no_airplan_model(device)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
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
        if ueLogFilePath != '':    
            key_qxdm_log_save(ueLogFilePath)
            
@allure.story("去激活激活小区后接入成功率测试_手机终端")
@pytest.mark.去激活激活小区后接入成功率测试_手机终端
@pytest.mark.run(order=14)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['去激活激活小区后接入成功率测试_手机终端'] if RUN_TESTCASE.get('去激活激活小区后接入成功率测试_手机终端') else [])
def testDeactiveAndActiveCellPhoneAccessSuccRate(testNum):
    AccSuccNum = 0
    ueLogFilePath = ''
    device = key_get_devices_list()[0]
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
                key_set_phone_airplan_model(device)
                key_wait(5)
                key_set_phone_no_airplan_model(device)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
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
    
@allure.story("闭塞解闭塞小区后接入成功率测试_手机终端")
@pytest.mark.闭塞解闭塞小区后接入成功率测试_手机终端
@pytest.mark.run(order=15)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞解闭塞小区后接入成功率测试_手机终端'] if RUN_TESTCASE.get('闭塞解闭塞小区后接入成功率测试_手机终端') else [])
def testBlockAndUnblockPhoneAccessSuccRate(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    device = key_get_devices_list()[0]
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
                key_set_phone_airplan_model(device)
                key_wait(5)
                key_set_phone_no_airplan_model(device)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
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
 
@allure.story("关闭打开通道射频后接入ping测试_手机终端")
@pytest.mark.关闭打开通道射频后接入ping测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭打开通道射频后接入ping测试_手机终端'] if RUN_TESTCASE.get('关闭打开通道射频后接入ping测试_手机终端') else [])
def testCloseChannelAndAttachAndPingTest(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    pdn = key_pdn_login()
    device = key_get_devices_list()[0]
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
                    accStatus = key_query_access_status(device)
                    assert accStatus == '2','终端接入网络失败，请检查 ！'
                #open channel
                with allure.step(key_get_time()+': 打开通道信号，并确认终端上线'):
                    logging.info(key_get_time()+': open channel, make sure cpe is attached')
                    gnb = key_ssh_login_gnb()
                    key_open_aip_channel(gnb)
                    key_open_sub6g_channel(gnb)
                    key_logout_gnb(gnb)
                    key_wait(60)
                    accStatus = key_query_access_status(device)
                    if accStatus == '2':
                        phoneIp = key_get_phone_ip(device)
                        AccSuccNum = AccSuccNum + 1
                        key_phone_ping(phoneIp, pdn)
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
        key_pdn_logout(pdn)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
         
@allure.story("关闭2s后打开通道射频接入ping测试_手机终端")
@pytest.mark.关闭2s后打开通道射频接入ping测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭2s后打开通道射频接入ping测试_手机终端'] if RUN_TESTCASE.get('关闭2s后打开通道射频接入ping测试_手机终端') else [])
def testCloseChannelWait2sPhoneAttachAndPingTest(testNum):
    ueLogFilePath = ''
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    AccSuccNum = 0
    pdn = key_pdn_login()
    device = key_get_devices_list()[0]
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
                accStatus = key_query_access_status(device)
                phoneIp = key_get_phone_ip(device)
                if accStatus == '2':
                    AccSuccNum = AccSuccNum + 1
                    key_phone_ping(phoneIp, pdn)
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
        key_pdn_logout(pdn)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
 
@allure.story("程控衰减近点ping包测试_手机终端")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点ping包测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['程控衰减近点ping包测试_手机终端'] if RUN_TESTCASE.get('程控衰减近点ping包测试_手机终端') else [])
def testAttenuatorNearPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减近点ping包测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            mobilePhonePintTest(testNum)
    finally:
        key_disconnect_attenuator(attenuator)
  
@allure.story("程控衰减远点ping包测试_手机终端")
@pytest.mark.run(order=4)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点ping包测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['程控衰减远点ping包测试_手机终端'] if RUN_TESTCASE.get('程控衰减远点ping包测试_手机终端') else [])
def testAttenuatorFarPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 程控衰减远点ping包测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            mobilePhonePintTest(testNum)
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
         
@allure.story("程控衰减近点tcp上行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp上行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
  
@allure.story("程控衰减近点tcp下行流量测试_手机终端")
@pytest.mark.run(order=6)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp下行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('DL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
  
@allure.story("程控衰减近点tcp上下行流量测试_手机终端")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减近点tcp上下行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UDL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
                assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_disconnect_attenuator(attenuator)
                  
@allure.story("程控衰减远点tcp上行流量测试_手机终端")
@pytest.mark.run(order=8)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp上行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
  
@allure.story("程控衰减远点tcp下行流量测试_手机终端")
@pytest.mark.run(order=9)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp下行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('DL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
  
@allure.story("程控衰减远点tcp上下行流量测试_手机终端")
@pytest.mark.run(order=10)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减远点tcp上下行流量测试_手机终端
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
            avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UDL', 'NR', 'TCP')
            if isCheckTraffic == True:
                assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
                assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
         
@allure.story("程控衰减tcp上下行流量打点测试_手机终端")
@pytest.mark.run(order=11)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.程控衰减tcp上下行流量打点测试_手机终端
def testAttenuatorEachPointUlDlTrafficTest():
    device = key_get_devices_list()[0]
    ueIp = key_get_phone_ip(device)
    pdn = key_pdn_login()
    pdn2 = key_pdn_login()
    ueLogFilePath = ''
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        with allure.step(key_get_time()+': tcp上下行流量打点测试'):
            logging.info(key_get_time()+': set point cell traffic test') 
            trafTh = threading.Thread(target=key_phone_udl_tcp_nr_traffic, args=(device, ueIp, pdn, pdn2))
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
        key_pdn_logout(pdn)
        key_pdn_logout(pdn2)
        attenuator = key_connect_attenuator()
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
         
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
    手机终端 ping包测试
'''
def mobilePhonePintTest(testNum): 
    ueLogFilePath = ''   
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    device = key_get_devices_list()[0]
    AccSuccNum = 0    
    pdn = key_pdn_login()       
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
        for i in range(1, testNum +1):
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                key_set_phone_airplan_model(device)
                with allure.step(key_get_time()+': 手机设置飞行模式后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_set_phone_no_airplan_model(device)
                with allure.step(key_get_time()+': 手机设置去飞行模式后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
                    AccSuccNum = AccSuccNum + 1
                    ueIp = key_get_phone_ip(device)
                    key_phone_ping(ueIp, pdn)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    finally:
        key_pdn_logout(pdn)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)
                        
#小区流量测试    
def cellPhoneTrafficTest(dir='DL', AsType='NR', traType='TCP'):
    ueLogFilePath = ''
    deviceList = key_get_devices_list()
    device = deviceList[0]
    pdn = key_pdn_login()
    pdn2 = key_pdn_login()
    avgDlTraf, avgUlTraf = 0, 0
    key_set_phone_airplan_model(device)
    key_wait(5)
    key_set_phone_no_airplan_model(device)
    key_wait(5)
    accStatus = key_query_access_status(device)
    if accStatus == '2':
        try:
            ueIp = key_get_phone_ip(device)
            sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
            dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
            if dir=='DL':
                if traType=='TCP':
                    if AsType=='NR':
                        avgDlTraf = key_phone_dl_tcp_nr_traffic(device, ueIp, pdn)
                    elif AsType=='WIFI':
                        pass
#                             avgDlTraf = key_dl_tcp_wifi_flow_test(cpe, pdn)
                elif traType=='UDP':
                    if AsType=='NR':
                        avgDlTraf = key_phone_dl_udp_nr_traffic(device, ueIp, pdn)
                    elif AsType=='WIFI':
                        pass
#                             avgDlTraf = key_dl_udp_wifi_flow_test(cpe, pdn)
            elif dir=='UL':
                if traType=='TCP':
                    if AsType=='NR':
                        avgUlTraf = key_phone_ul_tcp_nr_traffic(device, pdn)
                    elif AsType=='WIFI':
                        pass
#                             avgUlTraf = key_ul_tcp_wifi_flow_test(cpe, pdn)
                elif traType=='UDP':
                    if AsType=='NR':
                        avgUlTraf = key_phone_ul_udp_nr_traffic(device, pdn)
                    elif AsType=='WIFI':
                        pass
#                             avgUlTraf = key_ul_udp_wifi_flow_test(cpe, pdn)
            elif dir=='UDL':
                if traType=='TCP':
                    if AsType=='NR':
                        avgDlTraf, avgUlTraf = key_phone_udl_tcp_nr_traffic(device, ueIp, pdn, pdn2)
                    elif AsType=='WIFI':
                        pass
#                             avgDlTraf, avgUlTraf = key_udl_tcp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
                elif traType=='UDP':
                    if AsType=='NR':
                        avgDlTraf, avgUlTraf = key_phone_udl_udp_nr_traffic(device, ueIp, pdn, pdn2)
                    elif AsType=='WIFI':
                        pass
#                             avgDlTraf, avgUlTraf = key_udl_udp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
            key_stop_capture_data()
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
            key_network_data_analyse()
            return avgDlTraf, avgUlTraf
        finally:
            key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
            key_qxdm_log_save(ueLogFilePath)
    else:
        key_pdn_logout(pdn)
        key_pdn_logout(pdn2)
        with allure.step(key_get_time()+': 终端网络接入失败'):
            logging.warning(key_get_time()+': device not access network')
        assert accStatus == '2', '终端网络接入失败，请检查！'
        
#小区流量测试    
def cellTrafficTestIpAndPortBanding(dir='DL', AsType='NR', traType='TCP'):
    ueLogFilePath = ''
    phoneType = BASIC_DATA['phone']['phoneType']
    deviceList = key_get_devices_list()
    device = deviceList[0]
    pdn = key_pdn_login()
    avgDlTraf, avgUlTraf = 0, 0
    key_set_phone_airplan_model(device)
    key_wait(5)
    key_set_phone_no_airplan_model(device)
    key_wait(5)
    accStatus = key_query_access_status(device)
    if accStatus == '2':
        try:
            if phoneType == 'mate30':
                ueIp = BASIC_DATA['phone']['ueIp']
            else:
                ueIp = key_get_phone_ip(device)
            sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
            dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
            if dir=='DL':
                if traType=='TCP':
                    avgDlTraf = key_phone_dl_tcp_nr_traffic_port_banding(device, ueIp, pdn)
                elif traType=='UDP':
                    avgDlTraf = key_phone_dl_udp_nr_traffic_port_banding(device, ueIp, pdn)
            elif dir=='UL':
                if traType=='TCP':
                    avgUlTraf = key_phone_ul_tcp_nr_traffic_port_banding(device, ueIp, pdn)
                elif traType=='UDP':
                    avgUlTraf = key_phone_ul_udp_nr_traffic_port_banding(device, ueIp, pdn)
            key_stop_capture_data()
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
            key_network_data_analyse()
            return avgDlTraf, avgUlTraf
        finally:
            key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
            key_qxdm_log_save(ueLogFilePath)
    else:
        key_pdn_logout(pdn)
        with allure.step(key_get_time()+': 终端网络接入失败'):
            logging.warning(key_get_time()+': device not access network')
        assert accStatus == '2', '终端网络接入失败，请检查！'

'''
    手机终端 ping包测试
'''
def mobilePhonePintTestIpAndPortBanding(testNum): 
    ueLogFilePath = ''   
    phoneType = BASIC_DATA['phone']['phoneType']
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    isCheckSuccRate=BASIC_DATA['attach']['isCheckSuccRate']
    device = key_get_devices_list()[0]
    AccSuccNum = 0    
    pdn = key_pdn_login()       
    try:
        sigSocket, svBasicSocket, svDetailSocket = key_start_save_log()
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace() 
        for i in range(1, testNum +1):
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                key_set_phone_airplan_model(device, phoneType)
                with allure.step(key_get_time()+': 手机设置飞行模式后等待'+str(detachDelay)+'s'):
                    key_wait(detachDelay)
                key_set_phone_no_airplan_model(device, phoneType)
                with allure.step(key_get_time()+': 手机设置去飞行模式后等待'+str(attachDelay)+'s'):
                    key_wait(attachDelay)
                accStatus = key_query_access_status(device)
                if accStatus == '2':
                    AccSuccNum = AccSuccNum + 1
                    if phoneType == 'mate30':
                        ueIp = BASIC_DATA['phone']['ueIp']
                    else:
                        ueIp = key_get_phone_ip(device)
                    key_phone_ping(ueIp, pdn)
        key_stop_capture_data()
        ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService)
        key_network_data_analyse()
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        if isCheckSuccRate==True:
            assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    finally:
        key_pdn_logout(pdn)
        key_close_save_log(sigSocket, svBasicSocket, svDetailSocket)
        key_qxdm_log_save(ueLogFilePath)

@allure.story("近点ping包测试_手机终端")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点ping包测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['近点ping包测试_手机终端'] if RUN_TESTCASE.get('近点ping包测试_手机终端') else [])
def testNearPointPingTest(testNum):
    with allure.step(key_get_time()+': 近点ping包测试'):
        logging.info(key_get_time()+': near point ping test') 
        mobilePhonePintTest(testNum)
            
@allure.story("远点ping包测试_手机终端")
@pytest.mark.run(order=4)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点ping包测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['远点ping包测试'] if RUN_TESTCASE.get('远点ping包测试') else [])
def testFarPointPingTest(testNum):
    with allure.step(key_get_time()+': 程控衰减远点ping包测试'):
        logging.info(key_get_time()+': far point ping test') 
        mobilePhonePintTest(testNum)
            
 
@allure.story("近点tcp上行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp上行流量测试_手机终端
def testNearPointUlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    with allure.step(key_get_time()+': 近点tcp上行流量测试'):
        logging.info(key_get_time()+': near point tcp ul traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
 
@allure.story("近点tcp下行流量测试_手机终端")
@pytest.mark.run(order=6)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp下行流量测试_手机终端
def testNearPointDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': 近点tcp下行流量测试'):
        logging.info(key_get_time()+': near point tcp dl traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('DL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
            
 
@allure.story("近点tcp上下行流量测试_手机终端")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp上下行流量测试_手机终端
def testNearPointUlDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': 近点tcp上下行流量测试'):
        logging.info(key_get_time()+': near point tcp ul&dl traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UDL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
            
                 
@allure.story("远点tcp上行流量测试_手机终端")
@pytest.mark.run(order=8)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp上行流量测试_手机终端
def testFarPointUlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
    with allure.step(key_get_time()+': 远点tcp上行流量测试'):
        logging.info(key_get_time()+': far point tcp ul traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
        
@allure.story("远点tcp下行流量测试_手机终端")
@pytest.mark.run(order=9)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp下行流量测试_手机终端
def testFarPointDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
    with allure.step(key_get_time()+': 远点tcp下行流量测试'):
        logging.info(key_get_time()+': far point tcp dl traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('DL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
 
@allure.story("远点tcp上下行流量测试_手机终端")
@pytest.mark.run(order=10)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp上下行流量测试_手机终端
def testFarPointUlDlTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expFarDlTcpTraf = BASIC_DATA['traffic']['expFarDlTcpTraf']
    expFarUlTcpTraf = BASIC_DATA['traffic']['expFarUlTcpTraf']
    with allure.step(key_get_time()+': 远点tcp上下行流量测试'):
        logging.info(key_get_time()+': far point tcp ul&dl traffic test') 
        avgDlTraf, avgUlTraf = cellPhoneTrafficTest('UDL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expFarDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
            assert avgUlTraf >= expFarUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'

@allure.story("iperf端口绑定场景tcp上行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.iperf端口绑定场景tcp上行流量测试_手机终端
def testIperfPortBandingUlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlTcpTraf = BASIC_DATA['traffic']['expNearUlTcpTraf']
    with allure.step(key_get_time()+': iperf端口绑定场景tcp上行流量测试'):
        logging.info(key_get_time()+': iperf port banding, tcp ul traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTestIpAndPortBanding('UL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlTcpTraf, 'tcp上行流量测试结果不及预期，请检查！'
 
@allure.story("iperf端口绑定场景tcp下行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.iperf端口绑定场景tcp下行流量测试_手机终端
def testIperfPortBandingDlTcpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlTcpTraf = BASIC_DATA['traffic']['expNearDlTcpTraf']
    with allure.step(key_get_time()+': iperf端口绑定场景tcp上行流量测试'):
        logging.info(key_get_time()+': iperf port banding, tcp ul traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTestIpAndPortBanding('DL', 'NR', 'TCP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlTcpTraf, 'tcp下行流量测试结果不及预期，请检查！'
            
@allure.story("iperf端口绑定场景udp上行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.iperf端口绑定场景udp上行流量测试_手机终端
def testIperfPortBandingUlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearUlUdpTraf = BASIC_DATA['traffic']['expNearUlUdpTraf']
    with allure.step(key_get_time()+': iperf端口绑定场景tcp上行流量测试'):
        logging.info(key_get_time()+': iperf port banding, tcp ul traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTestIpAndPortBanding('UL', 'NR', 'UDP')
        if isCheckTraffic == True:
            assert avgUlTraf >= expNearUlUdpTraf, 'udp上行流量测试结果不及预期，请检查！'
 
@allure.story("iperf端口绑定场景tcp下行流量测试_手机终端")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.iperf端口绑定场景udp下行流量测试_手机终端
def testIperfPortBandingDlUdpTrafficTest():
    isCheckTraffic = BASIC_DATA['traffic']['isCheckTraffic']
    expNearDlUdpTraf = BASIC_DATA['traffic']['expNearDlUdpTraf']
    with allure.step(key_get_time()+': iperf端口绑定场景tcp上行流量测试'):
        logging.info(key_get_time()+': iperf port banding, tcp dl traffic test') 
        avgDlTraf, avgUlTraf = cellTrafficTestIpAndPortBanding('DL', 'NR', 'UDP')
        if isCheckTraffic == True:
            assert avgDlTraf >= expNearDlUdpTraf, 'udp下行流量测试结果不及预期，请检查！'
            
@allure.story("iperf端口绑定场景ping包测试_手机终端")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点ping包测试_手机终端
@pytest.mark.parametrize("testNum",RUN_TESTCASE['近点ping包测试_手机终端'] if RUN_TESTCASE.get('近点ping包测试_手机终端') else [])
def testIperfPortBandingPingTest(testNum):
    with allure.step(key_get_time()+': iperf端口绑定场景ping包测试'):
        logging.info(key_get_time()+': iperf port banding, ping test') 
        mobilePhonePintTestIpAndPortBanding(testNum)
        
if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass