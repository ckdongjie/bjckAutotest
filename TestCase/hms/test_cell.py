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
from UserKeywords.basic.basic import key_get_time
from UserKeywords.hms.CellManager import key_confirm_cell_status, key_block_cell, \
    key_unblock_cell, key_active_cell, key_deactive_cell
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)


@pytest.mark.parametrize("testNum",RUN_TESTCASE['反复闭塞解闭塞小区并ping包测试'] if RUN_TESTCASE.get('反复闭塞解闭塞小区并ping包测试') else [])    
@pytest.mark.反复闭塞解闭塞小区并ping包测试
def testUnBlockAndBlockCellPingStatus(testNum):
    serialNumber=BASIC_DATA['gnb']['serialNumberList']
    pdnIp=BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
    cpe = key_cpe_login(cpeIp, cpeUser, cpePass)
    for i in range (1, testNum+1):
        with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step('闭塞小区状态'):
            key_block_cell(hmsObj, enbId)
        sleep(20)
        with allure.step('确认小区状态为不可用状态'):
            key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
        sleep(20)
        with allure.step('解闭塞小区状态'):
            key_unblock_cell(hmsObj, enbId)
        sleep(20)
        with allure.step('确认小区状态为可用状态'):
            key_confirm_cell_status(hmsObj, enbId, expectStatus='available') 
        with allure.step('cpe ping包测试'):
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingwifiInterface)
            
                          
if __name__ == "__main__":
    pytest.main(['-s', '-vv', 'test_cell.py'])
    pass