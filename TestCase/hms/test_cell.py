# coding = utf-8 
'''
Created on 2022年9月7日

@author: dj
'''
import logging
import os
import sys
from time import sleep

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_confirm_cell_status, key_block_cell, \
    key_unblock_cell, key_active_cell, key_deactive_cell
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_confirm_pdu_setup_succ, key_local_pc_ping, key_cpe_logout


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


@pytest.mark.parametrize("testNum",RUN_TESTCASE['反复闭塞解闭塞小区并ping包测试'] if RUN_TESTCASE.get('反复闭塞解闭塞小区并ping包测试') else [])    
@pytest.mark.反复闭塞解闭塞小区并ping包测试
def testUnBlockAndBlockCellPingStatus(testNum):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    cpe = key_cpe_login()
    for i in range (1, testNum+1):
        with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            key_block_cell(hmsObj, enbId)
            sleep(20)
            key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
            sleep(20)
            key_unblock_cell(hmsObj, enbId)
            sleep(20)
            key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            assert setupRes == 'success','cpe接入失败，请检查！'
            key_wait(5)
            key_cpe_ping(cpe, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pingInterface = pingwifiInterface)
            key_local_pc_ping(cpe)
    key_cpe_logout(cpe)
            
@pytest.mark.parametrize("testNum",RUN_TESTCASE['反复去激活激活小区并ping包测试'] if RUN_TESTCASE.get('反复去激活激活小区并ping包测试') else [])    
@pytest.mark.反复去激活激活小区并ping包测试
def testDeactiveAndActiveCellPingStatus(testNum):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    cpe = key_cpe_login()
    for i in range (1, testNum+1):
        with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            key_deactive_cell(hmsObj, enbId)
            sleep(20)
            key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
            sleep(20)
            key_active_cell(hmsObj, enbId)
            sleep(20)
            key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            assert setupRes == 'success','cpe接入失败，请检查！'
            key_wait(5)
            key_cpe_ping(cpe, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pingInterface = pingwifiInterface)
            key_local_pc_ping(cpe)
    key_cpe_logout(cpe)
            
                          
if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass