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
from UserKeywords.pdn.pndManager import key_pdn_login, key_pdn_logout
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_cpe_detach, key_cpe_attach, key_confirm_pdu_setup_succ, \
    key_cpe_attach_cell_info, key_reboot_cpe, key_confirm_pdu_setup_fail, \
    key_dl_udp_nr_flow_test, key_dl_tcp_nr_flow_test, key_dl_tcp_wifi_flow_test, \
    key_ul_tcp_nr_flow_test, key_dl_udp_wifi_flow_test, \
    key_ul_tcp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_udl_tcp_nr_flow_test, \
    key_udl_tcp_wifi_flow_test, key_udl_udp_nr_flow_test, \
    key_udl_udp_wifi_flow_test


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
    AccSuccNum = 0
    cpe = key_cpe_login()
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
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
         
@allure.story("CPE复位后接入成功率测试")
@pytest.mark.CPE复位后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE复位后接入成功率测试'] if RUN_TESTCASE.get('CPE复位后接入成功率测试') else [])
def testRebootCpeAccessSuccRate(testNum):
    exptSuccRate = BASIC_DATA['attach']['succRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
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
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
       
@allure.story("基站复位后接入成功率测试")
@pytest.mark.run(order=13)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@pytest.mark.基站复位后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站复位后接入成功率测试'] if RUN_TESTCASE.get('基站复位后接入成功率测试') else [])
def testRebootGnbAccessSuccRate(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    for i in range (1,testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_reboot_enb(hmsObj, enbId)
            with allure.step(key_get_time()+': 基站复位成功，等待基站重启正常'):
                logging.info(key_get_time()+': reboot success, wait for BS start')
                key_wait(180)
            key_confirm_cell_status(hmsObj, enbId, 'available')
            key_wait(90)
            setupRes = key_confirm_pdu_setup_succ(cpe)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
            
@allure.story("去激活激活小区后接入成功率测试")
@pytest.mark.去激活激活小区后接入成功率测试
@pytest.mark.run(order=14)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['去激活激活小区后接入成功率测试'] if RUN_TESTCASE.get('去激活激活小区后接入成功率测试') else [])
def testDeactiveAndActiveCellAccessSuccRate(testNum):
    AccSuccNum = 0
    cpe = key_cpe_login()
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    exptSuccRate = BASIC_DATA['attach']['succRate']
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
            setupRes = key_confirm_pdu_setup_succ(cpe)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
           
@allure.story("闭塞解闭塞小区后接入成功率测试")
@pytest.mark.闭塞解闭塞小区后接入成功率测试
@pytest.mark.run(order=15)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞解闭塞小区后接入成功率测试'] if RUN_TESTCASE.get('闭塞解闭塞小区后接入成功率测试') else [])
def testBlockAndUnblockCellAccessSuccRate(testNum):
    exptSuccRate = BASIC_DATA['attach']['succRate']
    AccSuccNum = 0
    cpe = key_cpe_login()
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj)
    for i in range (1,testNum+1):
        logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_block_cell(hmsObj, enbId)
            with allure.step(key_get_time()+':闭塞小区成功，等待5s'):
                logging.warning(key_get_time()+':block cell success, wait for 5s')
                key_wait(5)
            key_unblock_cell(hmsObj, enbId)
            key_confirm_cell_status(hmsObj, enbId, 'available')
            setupRes = key_confirm_pdu_setup_succ(cpe)
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
 
@allure.story("关闭打开通道射频后CPE接入ping测试")
@pytest.mark.关闭打开通道射频后CPE接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭打开通道射频后CPE接入ping测试'] if RUN_TESTCASE.get('关闭打开通道射频后CPE接入ping测试') else [])
def testCloseChannelAndAttachAndPingTest(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    exptLossRate = BASIC_DATA['ping']['loseRate']
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
                key_cpe_attach(cpe)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellId = key_cpe_attach_cell_info(cpe)
                    assert cellId != -1,'CPE接入失败，请检查！'
                    AccSuccNum = AccSuccNum + 1
                    lossrate = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        gnb = key_ssh_login_gnb()
        key_open_aip_channel(gnb)
        key_open_sub6g_channel(gnb)
        key_logout_gnb(gnb)
         
@allure.story("关闭2s后打开通道射频CPE接入ping测试")
@pytest.mark.关闭2s后打开通道射频CPE接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['关闭2s后打开通道射频CPE接入ping测试'] if RUN_TESTCASE.get('关闭2s后打开通道射频CPE接入ping测试') else [])
def testCloseChannelWait2SAttachAndPingTest(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    exptLossRate = BASIC_DATA['ping']['loseRate']
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
                setupRes = key_confirm_pdu_setup_succ(cpe)
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellId = key_cpe_attach_cell_info(cpe)
                    assert cellId != -1,'CPE接入失败，请检查！'
                    AccSuccNum = AccSuccNum + 1
                    lossrate = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        gnb = key_ssh_login_gnb()
        key_open_aip_channel(gnb)
        key_open_sub6g_channel(gnb)
        key_logout_gnb(gnb)
 
@allure.story("设置程控衰减极值恢复后接入ping测试")
@pytest.mark.设置程控衰减极值恢复后接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['设置程控衰减极值恢复后接入ping测试'] if RUN_TESTCASE.get('设置程控衰减极值恢复后接入ping测试') else [])
def testAttMaxAttachAndPingTest(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    exptLossRate = BASIC_DATA['ping']['loseRate']
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
                key_cpe_attach(cpe)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellId = key_cpe_attach_cell_info(cpe)
                    assert cellId != -1,'CPE接入失败，请检查！'
                    AccSuccNum = AccSuccNum + 1
                    lossrate = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
         
@allure.story("设置程控衰减极值等待2秒恢复后接入ping测试")
@pytest.mark.设置程控衰减极值等待2秒恢复后接入ping测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['设置程控衰减极值等待2秒恢复后接入ping测试'] if RUN_TESTCASE.get('设置程控衰减极值等待2秒恢复后接入ping测试') else [])
def testAttMaxWait2AttachAndPingTest(testNum):
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    exptLossRate = BASIC_DATA['ping']['loseRate']
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
                key_cpe_attach(cpe)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                assert setupRes == 'success','pdu建立失败，请检查 ！'
                if setupRes == 'success':
                    cellId = key_cpe_attach_cell_info(cpe)
                    assert cellId != -1,'CPE接入失败，请检查！'
                    AccSuccNum = AccSuccNum + 1
                    lossrate = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
        with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
            logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
    except:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
 
@allure.story("UDP下行流量测试")
@pytest.mark.UDP下行流量测试
def testDlUdpFlowTest():
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_udp_nr_flow_test(cpe, pdn)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
     
@allure.story("TCP下行流量测试_动态调度")
@pytest.mark.TCP下行流量测试_动态调度
def testDlTcpFlowTest_DynamicScheduling():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
#        修改调度类型为动态调度
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_tcp_nr_flow_test(cpe, pdn)
            key_wait(10)
            key_dl_tcp_wifi_flow_test(cpe, pdn)
            key_cpe_detach(cpe)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
                key_cpe_detach(cpe)
            assert setupRes == 'success', 'cpe接入失败，请检查！'
    key_pdn_logout(pdn)
 
@allure.story("TCP下行流量测试_预调度")
@pytest.mark.TCP下行流量测试_预调度
def testDlTcpFlowTest_PreScheduling():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    #修改下行预调试开关
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'open')
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_tcp_nr_flow_test(cpe, pdn)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
    #修改下行预调试开关
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
     
@allure.story("TCP上行流量测试")
@pytest.mark.TCP上行流量测试
def testUlTcpFlowTest():
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_ul_tcp_nr_flow_test(cpe, pdn)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
             
@allure.story("近点ping包测试")
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点ping包测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['近点ping包测试'] if RUN_TESTCASE.get('近点ping包测试') else [])
def testNearPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 近点ping包测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cpePintTest(testNum)
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("远点ping包测试")
@pytest.mark.run(order=4)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点ping包测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['远点ping包测试'] if RUN_TESTCASE.get('远点ping包测试') else [])
def testFarPointPingTest(testNum):
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点ping包测试'):
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
 
@allure.story("近点tcp上行流量测试")
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp上行流量测试
def testNearPointUlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 近点tcp上行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('UL', 'NR', 'TCP')
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("近点tcp下行流量测试")
@pytest.mark.run(order=6)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp下行流量测试
def testNearPointDlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 近点tcp下行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('DL', 'NR', 'TCP')
    finally:
        key_disconnect_attenuator(attenuator)
 
@allure.story("近点tcp上下行流量测试")
@pytest.mark.run(order=7)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.近点tcp上下行流量测试
def testNearPointUlDlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 近点tcp上下行流量测试'):
            logging.info(key_get_time()+': near point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在近点'):
                logging.info(key_get_time()+': set attenuator, make RF power at near point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 0)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('UDL', 'NR', 'TCP')
    finally:
        key_disconnect_attenuator(attenuator)
                 
@allure.story("远点tcp上行流量测试")
@pytest.mark.run(order=8)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp上行流量测试
def testFarPointUlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp上行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('UL', 'NR', 'TCP')
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
 
@allure.story("远点tcp下行流量测试")
@pytest.mark.run(order=9)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp下行流量测试
def testFarPointDlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp下行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('DL', 'NR', 'TCP')
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
 
@allure.story("远点tcp上下行流量测试")
@pytest.mark.run(order=10)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.远点tcp上下行流量测试
def testFarPointUlDlTrafficTest():
    try:
        attenuator = key_connect_attenuator()
        with allure.step(key_get_time()+': 远点tcp上下行流量测试'):
            logging.info(key_get_time()+': far point ping test') 
            with allure.step(key_get_time()+': 设置程控衰减，使射频信号在远点'):
                logging.info(key_get_time()+': set attenuator, make RF power at far point') 
                key_send_multi_channel(attenuator, '1,2,3,4', 20)
                key_read_multi_channel(attenuator, '1,2,3,4')
            cellTrafficTest('UDL', 'NR', 'TCP')
    finally:
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        
@allure.story("tcp上下行流量打点测试")
@pytest.mark.run(order=11)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.tcp上下行流量打点测试
def testEachPointUlDlTrafficTest():
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    cpe2 = key_cpe_login()
    pdn2 = key_pdn_login()
    try:
        with allure.step(key_get_time()+': tcp上下行流量打点测试'):
            logging.info(key_get_time()+': set point cell traffic test') 
            trafTh = threading.Thread(target=key_udl_tcp_nr_flow_test, args=(cpe, cpe2, pdn, pdn2))
            attTh = threading.Thread(target=cyclicSetPoint,args=(4,))
            trafTh.start()
            key_wait(30)
            attTh.start()
            trafTh.join()
            attTh.join()
    finally:
        attenuator = key_connect_attenuator()
        key_send_multi_channel(attenuator, '1,2,3,4', 0)
        key_read_multi_channel(attenuator, '1,2,3,4')
        key_disconnect_attenuator(attenuator)
        
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
    attachDelay=BASIC_DATA['attach']['attachDelay']
    detachDelay=BASIC_DATA['attach']['detachDelay']
    exptSuccRate = BASIC_DATA['attach']['succRate']
    exptLossRate = BASIC_DATA['ping']['loseRate']
    exptPingAvg = BASIC_DATA['ping']['pingAvg']
    cpe = key_cpe_login()
    AccSuccNum = 0            
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
            assert setupRes == 'success','pdu建立失败，请检查 ！'
            if setupRes == 'success':
                cellId = key_cpe_attach_cell_info(cpe)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
            lossrate,avg = key_cpe_ping(cpe, pingInterface = '')
            lossrate = lossrate.split('%')[0]
            assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
            assert float(avg) <= exptPingAvg, 'ping包平均时延大于预期，请检查！'
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
    assert (AccSuccNum/testNum)*100 >= exptSuccRate, '接入成功率小于预期，请检查！'
                        
#小区流量测试    
def cellTrafficTest(dir='DL', AsType='NR', traType='TCP'):
    cpe = key_cpe_login()
    pdn = key_pdn_login()
    cpe2 = key_cpe_login()
    pdn2 = key_pdn_login()
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            if dir=='DL':
                if traType=='TCP':
                    if AsType=='NR':
                        key_dl_tcp_nr_flow_test(cpe, pdn)
                    elif AsType=='WIFI':
                        key_dl_tcp_wifi_flow_test(cpe, pdn)
                elif traType=='UDP':
                    if AsType=='NR':
                        key_dl_udp_nr_flow_test(cpe, pdn)
                    elif AsType=='WIFI':
                        key_dl_udp_wifi_flow_test(cpe, pdn)
            elif dir=='UL':
                if traType=='TCP':
                    if AsType=='NR':
                        key_ul_tcp_nr_flow_test(cpe, pdn)
                    elif AsType=='WIFI':
                        key_ul_tcp_wifi_flow_test(cpe, pdn)
                elif traType=='UDP':
                    if AsType=='NR':
                        key_ul_udp_nr_flow_test(cpe, pdn)
                    elif AsType=='WIFI':
                        key_ul_udp_wifi_flow_test(cpe, pdn)
            elif dir=='UDL':
                if traType=='TCP':
                    if AsType=='NR':
                        key_udl_tcp_nr_flow_test(cpe, cpe2, pdn, pdn2)
                    elif AsType=='WIFI':
                        key_udl_tcp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
                elif traType=='UDP':
                    if AsType=='NR':
                        key_udl_udp_nr_flow_test(cpe, cpe2, pdn, pdn2)
                    elif AsType=='WIFI':
                        key_udl_udp_wifi_flow_test(cpe, cpe2, pdn, pdn2)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'

if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass