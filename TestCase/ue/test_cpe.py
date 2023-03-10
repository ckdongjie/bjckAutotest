# coding = 'utf-8'
from distutils.core import setup
'''
Created on 2022年11月1日

@author: dj

'''

import logging

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.attenuator.Attenuator import key_connect_attenuator, \
    key_send_multi_channel, key_read_multi_channel
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_block_cell, key_unblock_cell, \
    key_confirm_cell_status, key_deactive_cell, key_active_cell
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.DuConfigManager import key_modify_du_ul_schedule_type, \
    key_modify_du_dl_schedule_switch, key_modify_du_ul_schedule_switch
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info
from UserKeywords.pdn.pndManager import key_pdn_login, key_pdn_logout
from UserKeywords.ue.CpeManager import key_cpe_detach, key_cpe_attach, \
    key_cpe_attach_cell_info, key_reboot_cpe, key_cpe_login, \
    key_confirm_pdu_setup_succ, key_dl_udp_nr_flow_test, \
    key_dl_tcp_nr_flow_test, key_ul_tcp_nr_flow_test, key_dl_tcp_wifi_flow_test, \
    key_ul_tcp_wifi_flow_test, key_dl_udp_wifi_flow_test, \
    key_ul_udp_nr_flow_test, key_ul_udp_wifi_flow_test, key_cpe_ping
globalPara.init()

@allure.story("CPE注册去注册后接入成功率测试")
@pytest.mark.CPE注册去注册后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE注册去注册后接入成功率测试'] if RUN_TESTCASE.get('CPE注册去注册后接入成功率测试') else [])
def testDetachAndAttachAccessSuccRate(testNum, cpeIp=BASIC_DATA['cpe']['cpeSshIp'], attachDelay=BASIC_DATA['attach']['attachDelay'], detachDelay=BASIC_DATA['attach']['detachDelay']):
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
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
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))
        
@allure.story("CPE复位后接入成功率测试")
@pytest.mark.CPE复位后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['CPE复位后接入成功率测试'] if RUN_TESTCASE.get('CPE复位后接入成功率测试') else [])
def testRebootCpeAccessSuccRate(testNum, cpeIp=BASIC_DATA['cpe']['cpeSshIp'], attachDelay=BASIC_DATA['attach']['attachDelay'], detachDelay=BASIC_DATA['attach']['detachDelay']):
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    for i in range (1,testNum+1):
        logging.warning(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            key_reboot_cpe(cpe)
            with allure.step(key_get_time()+':cpe复位成功，等待cpe启动完成！'):
                logging.warning(key_get_time()+'cpe reset success, wait for cpe start')
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
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))

      
@allure.story("基站复位后接入成功率测试")
@pytest.mark.run(order=4)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@pytest.mark.基站复位后接入成功率测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站复位后接入成功率测试'] if RUN_TESTCASE.get('基站复位后接入成功率测试') else [])
def testRebootGnbAccessSuccRate(testNum, serialNumber=BASIC_DATA['gnb']['serialNumberList'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], attachDelay=BASIC_DATA['attach']['attachDelay'], detachDelay=BASIC_DATA['attach']['detachDelay']):
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    key_cpe_attach(cpe)
    with allure.step(key_get_time()+': CPE注册后等待'+str(attachDelay)+'s'):
        key_wait(attachDelay)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    assert setupRes == 'success','pdu建立失败，请检查 ！'
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
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
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))

  
@allure.story("去激活激活小区后接入成功率测试")
@pytest.mark.去激活激活小区后接入成功率测试
@pytest.mark.run(order=5)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['去激活激活小区后接入成功率测试'] if RUN_TESTCASE.get('去激活激活小区后接入成功率测试') else [])
def testDeactiveAndActiveCellAccessSuccRate(testNum, serialNumber=BASIC_DATA['gnb']['serialNumberList'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], attachDelay=BASIC_DATA['attach']['attachDelay'], detachDelay=BASIC_DATA['attach']['detachDelay']):
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
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
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))

          
@allure.story("闭塞解闭塞小区后接入成功率测试")
@pytest.mark.闭塞解闭塞小区后接入成功率测试
@pytest.mark.run(order=6)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞解闭塞小区后接入成功率测试'] if RUN_TESTCASE.get('闭塞解闭塞小区后接入成功率测试') else [])
def testBlockAndUnblockCellAccessSuccRate(testNum, serialNumber=BASIC_DATA['gnb']['serialNumberList'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], attachDelay=BASIC_DATA['attach']['attachDelay'], detachDelay=BASIC_DATA['attach']['detachDelay']):
    AccSuccNum = 0
    cpe = key_cpe_login(cpeIp)
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
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
                cellId = key_cpe_attach_cell_info(cpe, cpeIp)
                assert cellId != -1,'CPE接入失败，请检查！'
            AccSuccNum = AccSuccNum + 1
    with allure.step(key_get_time()+': CPE接入成功率:'+str(AccSuccNum)+'/'+str(testNum)):
        logging.warning(key_get_time()+': CPE access success rate:'+str(AccSuccNum)+'/'+str(testNum))

@allure.story("UDP下行流量测试")
@pytest.mark.UDP下行流量测试
def testDlUdpFlowTest():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
    
@allure.story("TCP下行流量测试_动态调度")
@pytest.mark.TCP下行流量测试_动态调度
def testDlTcpFlowTest_DynamicScheduling():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    wifiPort = BASIC_DATA['flow']['wifiPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
#        修改调度类型为动态调度
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            key_wait(10)
            key_dl_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
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
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    #修改下行预调试开关
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'open')
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
    #修改下行预调试开关
    key_modify_du_dl_schedule_switch(hmsObj, enbId, 'close')
    
@allure.story("TCP上行流量测试")
@pytest.mark.TCP上行流量测试
def testUlTcpFlowTest():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            key_ul_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
            
@allure.story("近点ping包测试")
@pytest.mark.近点ping包测试
def testNearPointPingTest():
    attenuatorPort = BASIC_DATA['attenuator']['serialPort']
    attenuatorRate = BASIC_DATA['attenuator']['serialRate']
    attenuator = key_connect_attenuator(attenuatorPort, attenuatorRate)
    key_send_multi_channel(attenuator, '1,2,3,4', 20)

#设置程控值，使snrp为-70左右    
def setNearPoint():
    attenuatorPort = BASIC_DATA['attenuator']['serialPort']
    attenuatorRate = BASIC_DATA['attenuator']['serialRate']
    attenuator = key_connect_attenuator(attenuatorPort, attenuatorRate)
    key_send_multi_channel(attenuator, '1,2,3,4', 0)
    key_read_multi_channel(attenuator, '1,2,3,4') 

#设置程控值，使snrp为-100左右        
def setFarPoint():
    attenuatorPort = BASIC_DATA['attenuator']['serialPort']
    attenuatorRate = BASIC_DATA['attenuator']['serialRate']
    attenuator = key_connect_attenuator(attenuatorPort, attenuatorRate)
    key_send_multi_channel(attenuator, '1,2,3,4', 20)
    key_read_multi_channel(attenuator, '1,2,3,4') 
    
#接入ping包测试    
def cellPingTest(AsType='NR'):
    pdnIp=BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    with allure.step('CPE接入并ping包测试'):
        cpe = key_cpe_login(cpeIp, cpeUser, cpePass)
        attachRes = key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if attachRes == 'OK':
            if setupRes == 'success':
                with allure.step(key_get_time()+': cpe接入成功'):
                    logging.warning(key_get_time()+': cpe attach sussess')
            else:
                with allure.step(key_get_time()+': cpe接入失败'):
                    logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success','cpe接入失败，请检查！'
            if AsType=='NR':
                key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            elif AsType=='WIFI':
                key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingwifiInterface)
                       
#小区流量测试    
def cellTrafficTest(dir='DL', AsType='NR', traType='TCP'):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    attachRes = key_cpe_attach(cpe)
    setupRes = key_confirm_pdu_setup_succ(cpe)
    if attachRes == 'OK':
        if setupRes == 'success':
            with allure.step(key_get_time()+': cpe接入成功'):
                logging.info(key_get_time()+': cpe attach sussess')
            if dir=='DL':
                if traType=='TCP':
                    if AsType=='NR':
                        key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                    elif AsType=='WIFI':
                        key_dl_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                elif traType=='UDP':
                    if AsType=='NR':
                        key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                    elif AsType=='WIFI':
                        key_dl_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            elif dir=='UL':
                if traType=='TCP':
                    if AsType=='NR':
                        key_ul_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                    elif AsType=='WIFI':
                        key_ul_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                elif traType=='UDP':
                    if AsType=='NR':
                        key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                    elif AsType=='WIFI':
                        key_ul_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
        else:
            with allure.step(key_get_time()+': cpe接入失败'):
                logging.warning(key_get_time()+': cpe attach failure')
            assert setupRes == 'success', 'cpe接入失败，请检查！'
                
    
        