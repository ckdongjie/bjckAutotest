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
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_cpe_attach, key_confirm_pdu_setup_succ, key_cpe_detach


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
    exptLossRate = BASIC_DATA['ping']['loseRate']
    exptPingAvg = BASIC_DATA['ping']['pingAvg']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
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
            key_confirm_cell_status(hmsObj, enbId, 'available')
            with allure.step('CPE接入并ping包测试'):
                cpe = key_cpe_login()
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
                    lossrate,avg = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
#                     assert int(lossrate) <= exptLossRate, 'nr端口ping包丢包率大于预期，请检查！'
#                     assert float(avg) <= exptPingAvg, 'nr端口ping包平均时延大于预期，请检查！'
#                     lossrate,avg = key_cpe_ping(cpe, pingInterface = pingwifiInterface)
#                     lossrate = lossrate.split('%')[0]
#                     assert int(lossrate) <= exptLossRate, 'wifi端口ping包丢包率大于预期，请检查！'
#                     assert float(avg) <= exptPingAvg, 'wifi端口ping包平均时延大于预期，请检查！'

@allure.story("复位基站正常后ping包_5524")  
@pytest.mark.复位基站正常后ping包_5524
@pytest.mark.run(order=3)
@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade') 
@pytest.mark.parametrize("testNum",RUN_TESTCASE['复位基站正常后ping包_5524'] if RUN_TESTCASE.get('复位基站正常后ping包_5524') else [])
def testRebootGnbAndPing5524(testNum):
    exptLossRate = BASIC_DATA['ping']['loseRate']
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
                    key_wait(20)
                    lossrate = key_cpe_ping(cpe, pingInterface = '')
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'ping包丢包率大于预期，请检查！'
                    key_cpe_detach(cpe)

@allure.story("闭塞小区后复位基站") 
@pytest.mark.闭塞小区后复位基站
@pytest.mark.parametrize("testNum",RUN_TESTCASE['闭塞小区后复位基站'] if RUN_TESTCASE.get('闭塞小区后复位基站') else [])
def testBlockCellAndRebootGnb(testNum):
    exptLossRate = BASIC_DATA['ping']['loseRate']
    exptPingAvg = BASIC_DATA['ping']['pingAvg']
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
                    lossrate,avg = key_cpe_ping(cpe, pingInterface = pingNrInterface)
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'nr端口ping包丢包率大于预期，请检查！'
                    assert float(avg) > exptPingAvg, 'nr端口ping包平均时延大于预期，请检查！'
                    lossrate,avg = key_cpe_ping(cpe, pingInterface = pingwifiInterface)
                    lossrate = lossrate.split('%')[0]
                    assert int(lossrate) <= exptLossRate, 'wifi端口ping包丢包率大于预期，请检查！'
                    assert float(avg) <= exptPingAvg, 'wifi端口ping包平均时延大于预期，请检查！'

if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass