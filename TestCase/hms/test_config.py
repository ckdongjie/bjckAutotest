# coding = 'utf-8'
'''
Created on 2022年11月7日

@author: dj
'''

import logging

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.AlarmManager import key_check_active_alarm_with_black_list, \
    key_check_active_alarm_with_white_list
from UserKeywords.hms.CellManager import key_confirm_cell_status
from UserKeywords.hms.ConfigManager import key_modify_omc_url
from UserKeywords.hms.DeviceManager import key_confirm_device_online, \
    key_confirm_device_status_same_as_expect
from UserKeywords.hms.DuConfigManager import key_modify_du_cell_epre
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms, \
    key_update_clock_source
from UserKeywords.hms.SctpManager import key_modify_ipv6_sctp_config

@allure.story("OMC IP地址修改")
@pytest.mark.更新omcIp地址_地址正确且基站已注册
@pytest.mark.parametrize("testNum",RUN_TESTCASE['更新omcIp地址_地址正确且基站已注册'] if RUN_TESTCASE.get('更新omcIp地址_地址正确且基站已注册') else [])
def testUpdateOmcIpScence1(testNum):
    hmsIp2=BASIC_DATA['hms']['ip2']
    oldOmcIp=BASIC_DATA['hms']['omcIp']
    newOmcIp=BASIC_DATA['hms']['omcIp2']
    with allure.step('更新omc ip地址测试：修改地址正确且基站在新网管已经注册'):
        souHmsObj=key_login_hms()
        souEnbId, souEnbName = key_get_enb_info(souHmsObj)
        desHmsObj=key_login_hms(hmsIp2)
        desEnbId, desEnbName = key_get_enb_info(desHmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_confirm_device_online(souHmsObj)
                key_modify_omc_url(souHmsObj, souEnbId, newOmcIp)
                with allure.step(key_get_time()+': omc ip修改生效，等待60s检查基站状态'):
                    key_wait(60)
                key_confirm_device_status_same_as_expect(souHmsObj, expectStatus='offline')
                #登录另一个omc系统，确认基站在线
                key_confirm_device_online(desHmsObj)
                with allure.step(key_get_time()+': 恢复基站参数'):
                    key_modify_omc_url(desHmsObj, desEnbId, oldOmcIp)
                with allure.step(key_get_time()+': omc ip修改生效，等待10s检查基站状态'):
                    key_wait(60)
                key_confirm_device_status_same_as_expect(desHmsObj, expectStatus='offline')
        
@allure.story("OMC IP地址修改")
@pytest.mark.更新omcIp地址_地址正确但基站未注册
@pytest.mark.parametrize("testNum",RUN_TESTCASE['更新omcIp地址_地址正确但基站未注册'] if RUN_TESTCASE.get('更新omcIp地址_地址正确但基站未注册') else [])
def testUpdateOmcIpScence2(testNum):
    oldOmcIp=BASIC_DATA['hms']['omcIp']
    newOmcIp=BASIC_DATA['hms']['omcIp2']
    with allure.step('更新omc ip地址测试：修改地址正确但基站在新网管未注册'):
        souHmsObj=key_login_hms()
        souEnbId, souEnbName = key_get_enb_info(souHmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_confirm_device_online(souHmsObj)
                key_modify_omc_url(souHmsObj, souEnbId, newOmcIp)
                with allure.step(key_get_time()+': 新网管上基站未注册，等待2分钟后omc ip地址回退'):
                    key_wait(120)
                key_confirm_device_status_same_as_expect(souHmsObj, expectStatus='online')
                key_modify_omc_url(souHmsObj, souEnbId, oldOmcIp)
                
@allure.story("OMC IP地址修改")
@pytest.mark.更新omcIp地址_地址错误
@pytest.mark.parametrize("testNum",RUN_TESTCASE['更新omcIp地址_地址错误'] if RUN_TESTCASE.get('更新omcIp地址_地址错误') else [])
def testUpdateOmcIpScence3(testNum):
    oldOmcIp=BASIC_DATA['hms']['omcIp']
    newOmcIp=BASIC_DATA['hms']['erroromcIp']
    with allure.step('更新omc ip地址测试：修改地址正确但基站在新网管未注册'):
        souHmsObj=key_login_hms()
        souEnbId, souEnbName = key_get_enb_info(souHmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_confirm_device_online(souHmsObj)
                key_modify_omc_url(souHmsObj, souEnbId, newOmcIp)
                with allure.step(key_get_time()+': omc ip修改生效，等待10s检查基站状态'):
                    key_wait(60)
                key_confirm_device_status_same_as_expect(souHmsObj, expectStatus='offline')
                with allure.step(key_get_time()+': 目标omc ip地址错误，等待3分钟后omc ip地址回退'):
                    key_wait(180)
                key_modify_omc_url(souHmsObj, souEnbId, oldOmcIp)

@allure.story("SSB发射功率修改")
@pytest.mark.SSB发射功率修改
@pytest.mark.parametrize("epre",RUN_TESTCASE['SSB发射功率修改'] if RUN_TESTCASE.get('SSB发射功率修改') else [])
def testModifyDuCellEpre(epre):
    with allure.step('SSB发射功率修改，修改值：'+str(epre)):
        logging.info(key_get_time()+': modify du cell epre, value:'+str(epre))
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        #修改小区epre
        key_modify_du_cell_epre(hmsObj, enbId, epre)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        
@allure.story("本地时钟和GPS切换测试")
@pytest.mark.本地时钟和GPS切换测试
def testClockSourceConfig():
    with allure.step('时钟源切换测试'):
        logging.info(key_get_time()+': clock source config test')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        #修改时钟类型为本地时钟
        key_update_clock_source(hmsObj, enbId, 'LOCAL_CLOCK')
        key_wait(30)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        #修改时钟类型为本地时钟
        key_update_clock_source(hmsObj, enbId, 'GPS')
        key_wait(30)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')

@allure.story("SCTP目标端口号修改")
@pytest.mark.SCTP目标端口号修改
def testSctpRemotePortConfig():
    with allure.step('SCTP目标端口号修改测试'):
        logging.info(key_get_time()+': sctp remote port modify test')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        #修改sctp远端端口
        key_modify_ipv6_sctp_config(hmsObj, enbId, {'remotePort':'38418'})
        key_wait(10)
        alarmWhiteList = ['NR Cell Unavailable', 'gNodeB Out of Service', 'gNodeB NG Fault', 'SCTP link fault alarm']
        key_check_active_alarm_with_white_list(hmsObj, alarmWhiteList=alarmWhiteList)
        #确认小区状态不正常
        key_confirm_cell_status(hmsObj, enbId, 'unavailable')
        #修改sctp远端端口
        key_modify_ipv6_sctp_config(hmsObj, enbId, {'remotePort':'38412'})
        key_wait(10)
        alarmBlackList = ['NR Cell Unavailable', 'gNodeB Out of Service', 'gNodeB NG Fault', 'SCTP link fault alarm']
        key_check_active_alarm_with_black_list(hmsObj, alarmBlackList=alarmBlackList)
        #确认小区状态不正常
        key_confirm_cell_status(hmsObj, enbId, 'available')