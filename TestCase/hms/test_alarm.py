'''
Created on 2023年1月10日

@author: dj
'''
import logging
import os
import sys

import allure
import pytest

from TestCase import globalPara
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.gnb.gnbManager import key_login_wifi_exec_command, \
    key_login_nrapp_exec_command, key_ssh_login_gnb, key_logout_gnb, \
    key_serial_login_2160, key_serial_logout_2160, key_exec_command_on_gnb
from UserKeywords.hms.AlarmManager import key_query_active_alarm, \
    key_query_history_alarm
from UserKeywords.hms.CellManager import key_confirm_cell_status, key_block_cell, \
    key_unblock_cell
from UserKeywords.hms.DeviceAlarmParaManager import key_set_temperature_alarm_threshold, \
    key_set_under_voltage_alarm_threshold, key_set_over_voltage_alarm_threshold, \
    key_set_memory_usage_alarm_threshold, key_set_cpu_usage_alarm_threshold
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info
from UserKeywords.hms.NgManager import key_set_ng_value
from UserKeywords.hms.SctpManager import key_modify_ipv6_sctp_config, \
    key_query_ipv6_sctp_config, key_add_ipv6_sctp_config, \
    key_del_ipv6_sctp_config
from UserKeywords.hms.WifiManager import key_get_wifi_cell_status, \
    key_set_wifi_rf_switch, key_get_wifi_heart_status
from UserKeywords.power.Power import key_power_off, key_power_on


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()


@allure.story("当前告警查询") 
@pytest.mark.当前告警查询
@pytest.mark.run(order=2)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
def testQueryActiveAlarm():
    hmsObj = key_login_hms()
    alarmList = key_query_active_alarm(hmsObj)
    with allure.step(key_get_time()+':基站当前告警:'+str(alarmList)):
        logging.info(key_get_time()+': active alarm info:'+str(alarmList))
    
@allure.story("历史告警查询") 
@pytest.mark.历史告警查询
@pytest.mark.parametrize("startTime, endTime",RUN_TESTCASE['历史告警查询'] if RUN_TESTCASE.get('历史告警查询') else [])
def testQueryHistoryAlarm(startTime, endTime):
    hmsObj = key_login_hms()
    with allure.step(key_get_time()+':查询基站历史告警，时间段:'+str(startTime)+'--'+str(endTime)):
        logging.info(key_get_time()+': query history alarm info, time:'+str(startTime)+'--'+str(endTime))
        alarmList = key_query_history_alarm(hmsObj, alarmRaisedStartTime=startTime, alarmRaisedEndTime=endTime)
        with allure.step(key_get_time()+':基站历史告警:'+str(alarmList)):
            logging.info(key_get_time()+': history alarm info:'+str(alarmList))
            
@pytest.mark.wifi小区退服告警上报及恢复
def testWifiCellDownAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
    assert wifiCellStatus == 'Normal','wifi小区状态与预期不一致，请检查！'
    with allure.step(key_get_time()+':触发并确认wifi小区退服告警上报'):
        logging.info(key_get_time()+': wifi cell down alarm report')
        key_set_wifi_rf_switch(hmsObj, enbId, 'off')
        alarmReport = checkAlarmReport(hmsObj, 'WIFI Cell Down')
        assert alarmReport == True, 'WIFI Cell Down告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复wifi小区退服告警上报'):
        logging.info(key_get_time()+': recovery wifi cell down alarm report')
        key_set_wifi_rf_switch(hmsObj, enbId, 'on')
        alarmRecovery = checkAlarmRecovery(hmsObj, 'WIFI Cell Down')
        assert alarmRecovery == True, 'WIFI Cell Down告警未恢复，请检查！'
        
@pytest.mark.wifi小区退服告警及DFS告警上报及恢复
def testWifiCellDownAndDfsAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
    assert wifiCellStatus == 'Normal','wifi小区状态与预期不一致，请检查！'
    with allure.step(key_get_time()+':触发并确认wifi小区退服告警及DFS告警上报'):
        logging.info(key_get_time()+': wifi cell down alarm and DFS alarm report')
        key_login_wifi_exec_command('radartool bangradar')
        alarmReport1 = checkAlarmReport(hmsObj, 'WIFI Cell Down')
        alarmReport2 = checkAlarmReport(hmsObj, 'WIFI DFS')
        assert alarmReport1 == True and alarmReport2 == True, 'WIFI Cell Down告警/DFS告警未上报，请检查！'
        alarmRecovery1 = checkAlarmRecovery(hmsObj, 'WIFI Cell Down')
        alarmRecovery2 = checkAlarmRecovery(hmsObj, 'WIFI DFS')
        assert alarmRecovery1 == True and alarmRecovery2 == True, 'WIFI Cell Down告警/DFS告警未恢复，请检查！'
        
@pytest.mark.wifi板复位
def testRebootWifi():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
    assert wifiCellStatus == 'Normal','wifi小区状态与预期不一致，请检查！'
    with allure.step(key_get_time()+':登录wifi板并执行复位命令'):
        logging.info(key_get_time()+': login wifi and exec reboot')
        key_login_wifi_exec_command('apps_reboot')
        key_wait(2*60)
        for i in range (1, 30):
            wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
            wifiHBStatus = key_get_wifi_heart_status(hmsObj, enbId)
            if wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal':
                break
        assert wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal','预期时间内wifi小区状态或心跳状态未恢复正常，请检查！'
        
@pytest.mark.omc复位基站检查wifi状态
def testRebootGnbAndCheckWifi():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
    assert wifiCellStatus == 'Normal','wifi小区状态与预期不一致，请检查！'
    with allure.step(key_get_time()+':omc复位基站，基站正常后检查wifi状态'):
        logging.info(key_get_time()+': omc reboot gnb, check wifi status when gnb online')
        rebootRes = key_reboot_enb(hmsObj, enbId)
        assert rebootRes == 'success','基站复位操作失败，请检查！'   
        with allure.step(key_get_time()+':等待基站复位启动'):
            logging.info(key_get_time()+': reboot success, wait for gnb online......')
            key_wait(180)
        key_confirm_device_online(hmsObj)
        for i in range (1, 50):
            wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
            wifiHBStatus = key_get_wifi_heart_status(hmsObj, enbId)
            if wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal':
                break
        assert wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal','预期时间内wifi小区状态或心跳状态未恢复正常，请检查！'
        
@pytest.mark.基站掉电复位基站检查wifi状态
def testPowerOffAndOnGnbAndCheckWifi():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
    assert wifiCellStatus == 'Normal','wifi小区状态与预期不一致，请检查！'
    with allure.step(key_get_time()+':基站掉电复位，基站正常后检查wifi状态'):
        logging.info(key_get_time()+': power off/on gnb, check wifi status when gnb online')
        key_power_off()
        key_wait(60)
        key_power_on()
        with allure.step(key_get_time()+':等待基站复位启动'):
            logging.info(key_get_time()+': reboot success, wait for gnb online......')
            key_wait(180)
        key_confirm_device_online(hmsObj)
        for i in range (1, 50):
            wifiCellStatus = key_get_wifi_cell_status(hmsObj, enbId)
            wifiHBStatus = key_get_wifi_heart_status(hmsObj, enbId)
            if wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal':
                break
        assert wifiCellStatus == 'Normal' and wifiHBStatus=='Heartbeat Normal','预期时间内wifi小区状态或心跳状态未恢复正常，请检查！'

@pytest.mark.黑匣子中记录mbuf信息
@pytest.mark.parametrize("testNum",RUN_TESTCASE['黑匣子中记录mbuf信息'] if RUN_TESTCASE.get('黑匣子中记录mbuf信息') else [])
def testMubfInfoInBlackBox(testNum):
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, 'available')
    for num in range (1, testNum+1):
        logging.info(key_get_time()+':run the test <'+str(num)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(num)+'次测试'):
            key_login_nrapp_exec_command('g_kni_set_mbuf_addr_flag 1')
            with allure.step(key_get_time()+':等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
            key_confirm_device_online(hmsObj)
            key_confirm_cell_status(hmsObj, enbId, 'available')

@pytest.mark.Emmc使用超限告警
@pytest.mark.parametrize("testNum",RUN_TESTCASE['Emmc使用超限告警'] if RUN_TESTCASE.get('Emmc使用超限告警') else [])
def testEmmcEndOfLifeAlarm(testNum):
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    alarmExit = False
    alarmList = key_query_active_alarm(hmsObj)
    if 'eMMC reserved block Usage Over Threshold' in str(alarmList):
        alarmExit = True
    assert alarmExit == True,'预期告警不存在，请检查！'
    for num in range (1, testNum+1):
        logging.info(key_get_time()+':run the test <'+str(num)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(num)+'次测试'):
            alarmExit = False
            rebootRes = key_reboot_enb(hmsObj, enbId)
            assert rebootRes == 'success','基站复位操作失败，请检查！'   
            with allure.step(key_get_time()+':等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
                key_confirm_device_online(hmsObj)
            key_confirm_cell_status(hmsObj, enbId, 'available')
            for i in range (1,240):
                alarmList = key_query_active_alarm(hmsObj)
                if 'eMMC reserved block Usage Over Threshold' in str(alarmList):
                    alarmExit = True
                    break
                else:
                    key_wait(5)
            assert alarmExit == True,'预期告警不存在，请检查！'

@pytest.mark.SCTP异常告警上报及恢复
def testSctpAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    primaryPeerAddress_back = key_query_ipv6_sctp_config(hmsObj, enbId, 'primaryPeerAddress')
    paraDict = {'primaryPeerAddress': "193:168:6::145"}
    with allure.step(key_get_time()+':触发并确认SCTP告警上报'):
        logging.info(key_get_time()+': sctp alarm report')
        key_modify_ipv6_sctp_config(hmsObj, enbId, paraDict)
        alarmReport = checkAlarmReport(hmsObj, 'SCTP link fault alarm')
        assert alarmReport == True, 'SCTP告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复SCTP告警上报'):
        logging.info(key_get_time()+': recovery sctp alarm report')
        paraDict['primaryPeerAddress'] = primaryPeerAddress_back
        key_modify_ipv6_sctp_config(hmsObj, enbId, paraDict)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'SCTP link fault alarm')
        assert alarmRecovery == True, 'SCTP告警未恢复，请检查！'
        
@pytest.mark.DU小区闭塞告警上报及恢复
def testDuCellBlockAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    with allure.step(key_get_time()+':触发并确认DU小区闭塞告警上报'):
        logging.info(key_get_time()+': du cell block alarm report')
        key_block_cell(hmsObj, enbId)
        alarmReport = checkAlarmReport(hmsObj, 'NR DU Cell Block')
        assert alarmReport == True, 'DU小区闭塞告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复DU小区闭塞告警上报'):
        logging.info(key_get_time()+': recovery du cell block alarm report')
        key_unblock_cell(hmsObj, enbId)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'NR DU Cell Block')
        assert alarmRecovery == True, 'du cell block告警未恢复，请检查！'
        
@pytest.mark.基站退服告警上报及恢复
def testGnbOutOfServiceAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    with allure.step(key_get_time()+':触发并确认基站退服告警上报'):
        logging.info(key_get_time()+': gnb out of service alarm report')
        key_block_cell(hmsObj, enbId)
        alarmReport = checkAlarmReport(hmsObj, 'gNodeB Out of Service')
        assert alarmReport == True, '基站退服告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站退服告警上报'):
        logging.info(key_get_time()+': recovery gnb out of service alarm report')
        key_unblock_cell(hmsObj, enbId)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'gNodeB Out of Service')
        assert alarmRecovery == True, '基站退服告警未恢复，请检查！'
        
@pytest.mark.小区退服告警上报及恢复
def testCellUnavailableAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    with allure.step(key_get_time()+':触发并确认小区退服告警上报'):
        logging.info(key_get_time()+': cell unavailable alarm report')
        key_block_cell(hmsObj, enbId)
        alarmReport = checkAlarmReport(hmsObj, 'NR Cell Unavailable')
        assert alarmReport == True, '小区退服告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复小区退服告警上报'):
        logging.info(key_get_time()+': recovery cell unavailable alarm report')
        key_unblock_cell(hmsObj, enbId)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'NR Cell Unavailable')
        assert alarmRecovery == True, '小区退服告警未恢复，请检查！'
        
@pytest.mark.Ng故障告警上报及恢复
def testNgFaultAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    with allure.step(key_get_time()+':触发并确认Ng故障告警上报'):
        logging.info(key_get_time()+': NG fault alarm report')
        addParaDict = {"assID":"2","primaryPeerAddress":"193:168:6::145"}
        key_add_ipv6_sctp_config(hmsObj, enbId, addParaDict)
        key_set_ng_value(hmsObj, enbId, addParaDict['assID'])
        alarmReport = checkAlarmReport(hmsObj, 'gNodeB NG Fault')
        assert alarmReport == True, 'NG故障告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复NG故障告警上报'):
        logging.info(key_get_time()+': recovery ng fault alarm report')
        key_set_ng_value(hmsObj, enbId, "1")
        key_del_ipv6_sctp_config(hmsObj, enbId, "2")
        alarmRecovery = checkAlarmRecovery(hmsObj, 'gNodeB NG Fault')
        assert alarmRecovery == True, 'NG故障告警未恢复，请检查！'
        
@pytest.mark.SSH登录告警上报及恢复
def testSshLoginAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
    with allure.step(key_get_time()+':触发并确认用户SSH登录告警上报'):
        logging.info(key_get_time()+': user ssh login alarm report')
        gnb = key_ssh_login_gnb()
        alarmReport = checkAlarmReport(hmsObj, 'Debug User Login through SSH')
        assert alarmReport == True, 'ssh登录告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复SSH登录告警上报'):
        logging.info(key_get_time()+': recovery ssh login alarm report')
        key_exec_command_on_gnb(gnb, 'exit')
        key_logout_gnb(gnb)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Debug User Login through SSH')
        assert alarmRecovery == True, 'ssh登录告警未恢复，请检查！'
        
@pytest.mark.串口登录基站告警上报及恢复
def testSerialLoginAlarmReportAndRecovery():
    with allure.step(key_get_time()+':触发并确认串口登录告警上报'):
        logging.info(key_get_time()+': Serial login alarm report')
        serial = key_serial_login_2160()
        alarmReport = checkAlarmReport(hmsObj, 'Debug User Login through Serial Port')
        assert alarmReport == True, '串口登录告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复串口登录告警上报'):
        logging.info(key_get_time()+': recovery serial login alarm report')
        key_serial_logout_2160(serial)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Debug User Login through Serial Port')
        assert alarmRecovery == True, '串口登录告警未恢复，请检查！'
        
@pytest.mark.基站下电告警上报及恢复
def testGnbPowerOffAlarmReportAndRecovery():
    with allure.step(key_get_time()+':触发并确认基站下电告警上报'):
        logging.info(key_get_time()+': power drop alarm report')
        key_power_off()
        alarmReport = checkAlarmReport(hmsObj, 'Power Drop')
        assert alarmReport == True, '基站下电告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站下电告警上报'):
        logging.info(key_get_time()+': recovery power drop alarm report')
        key_power_on()
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Power Drop')
        assert alarmRecovery == True, '基站下电告警未恢复，请检查！' 
        
@pytest.mark.基站过温告警上报及恢复
def testGnbTemperatureHighAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+':触发并确认基站过温告警上报'):
        logging.info(key_get_time()+': temperature high alarm report')
        key_set_temperature_alarm_threshold(hmsObj, enbId, 60)
        alarmReport = checkAlarmReport(hmsObj, 'Temperature High')
        assert alarmReport == True, '基站过温告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站过温告警上报'):
        logging.info(key_get_time()+': recovery temperature high alarm report')
        key_set_temperature_alarm_threshold(hmsObj, enbId, 100)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Temperature High')
        assert alarmRecovery == True, '基站过温告警未恢复，请检查！' 
        
@pytest.mark.基站低压告警上报及恢复
def testGnbLowVoltAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+':触发并确认基站低压告警上报'):
        logging.info(key_get_time()+': low voltage alarm report')
        key_set_under_voltage_alarm_threshold(hmsObj, enbId, 12)
        alarmReport = checkAlarmReport(hmsObj, 'Voltage Abnormal')
        assert alarmReport == True, '基站低压告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站低压告警上报'):
        logging.info(key_get_time()+': recovery low voltage alarm report')
        key_set_under_voltage_alarm_threshold(hmsObj, enbId, 10)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Voltage Abnormal')
        assert alarmRecovery == True, '基站低压告警未恢复，请检查！'     
        
@pytest.mark.基站过压告警上报及恢复
def testGnbHighVoltAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+':触发并确认基站过压告警上报'):
        logging.info(key_get_time()+': high voltage alarm report')
        key_set_over_voltage_alarm_threshold(hmsObj, enbId, 11)
        alarmReport = checkAlarmReport(hmsObj, 'Voltage Abnormal')
        assert alarmReport == True, '基站过压告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站过压告警上报'):
        logging.info(key_get_time()+': recovery high voltage alarm report')
        key_set_over_voltage_alarm_threshold(hmsObj, enbId, 14)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Voltage Abnormal')
        assert alarmRecovery == True, '基站过压告警未恢复，请检查！'    
        
@pytest.mark.基站内存使用率过高告警上报及恢复
def testGnbMemoryUsageHighAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+':触发并确认基站内存使用率过高告警上报'):
        logging.info(key_get_time()+': memory usage high alarm report')
        key_set_memory_usage_alarm_threshold(hmsObj, enbId, 0)
        alarmReport = checkAlarmReport(hmsObj, 'Memory Usage Over Threshold')
        assert alarmReport == True, '基站内存使用率过高告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站内存使用率过高告警上报'):
        logging.info(key_get_time()+': recovery memory usage high alarm report')
        key_set_memory_usage_alarm_threshold(hmsObj, enbId, 90)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'Memory Usage Over Threshold')
        assert alarmRecovery == True, '基站内存使用率过高告警未恢复，请检查！' 
        
@pytest.mark.基站CPU使用率过高告警上报及恢复
def testGnbCpuUsageHighAlarmReportAndRecovery():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step(key_get_time()+':触发并确认基站CPU使用率过高告警上报'):
        logging.info(key_get_time()+': cpu usage high alarm report')
        key_set_cpu_usage_alarm_threshold(hmsObj, enbId, 0)
        alarmReport = checkAlarmReport(hmsObj, 'CPU Usage Over Threshold')
        assert alarmReport == True, '基站内存使用率过高告警未上报，请检查！'
    key_wait(5)
    with allure.step(key_get_time()+':恢复基站CPU使用率过高告警上报'):
        logging.info(key_get_time()+': recovery cpu usage high alarm report')
        key_set_cpu_usage_alarm_threshold(hmsObj, enbId, 90)
        alarmRecovery = checkAlarmRecovery(hmsObj, 'CPU Usage Over Threshold')
        assert alarmRecovery == True, '基站CPU使用率过高告警未恢复，请检查！' 
        
def checkAlarmReport(hmsObj, alarmName, tryNum=30):
    alarmReport = False
    for i in range (1, tryNum+1):
        alarmList = key_query_active_alarm(hmsObj)
        if alarmName in str(alarmList):
            alarmReport = True
            break
        else:
            key_wait(5)
    return alarmReport

def checkAlarmRecovery(hmsObj, alarmName, tryNum=30):
    alarmRecovery = False
    for i in range (1, tryNum+1):
        alarmList = key_query_active_alarm(hmsObj)
        if alarmName not in str(alarmList):
            alarmRecovery = True
            break
        else:
            key_wait(5)
    return alarmRecovery
        
        
if __name__ == '__main__':
    hmsObj = key_login_hms()
    alarmList = key_query_active_alarm(hmsObj)
    print(alarmList)