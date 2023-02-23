# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
from UserKeywords.ue.CpeManager import key_cpe_ping

'''

import logging

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time
from UserKeywords.basic.basic import key_wait
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_reboot_gnb, \
    key_weblmt_login


@allure.feature("weblmt基站管理")
@allure.story("weblmt基站相关测试用例：基站复位")
class TestWeblmtGnb():
    
    @pytest.mark.weblmt复位基站正常后ping包
    @pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt复位基站正常后ping包'] if RUN_TESTCASE.get('weblmt复位基站正常后ping包') else [])
    def testWeblmtRebootGnbAndPing(self, testNum, weblmtIp=BASIC_DATA['weblmt']['ip'],cellId=0, cpePcIp=BASIC_DATA['flow']['cpePcIp'], pdnIp=BASIC_DATA['pdn']['pdnIp'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], ping_interface=BASIC_DATA['cpe']['pingNrInterface'], log_save_path=BASIC_DATA['ping']['logSavePath']):
        weblmt = key_weblmt_login(weblmtIp)
        cpe = key_cpe_login(cpeIp)
        for i in range (testNum):
            logging.info(key_get_time()+':run the test '+str(i+1)+' times')
            with allure.step(key_get_time()+'执行第 '+str(i+1)+'次测试'):
                key_weblmt_reboot_gnb(weblmt)
                with allure.step('等待基站复位启动'):
                    logging.info(key_get_time()+': reboot success, wait for gnb online......')
                    key_wait(180)
                confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
                assert confirmRes == True, '小区状态与预期不一致，请检查！'
                key_cpe_ping(cpe, cpePcIp=cpePcIp, pdnIp=pdnIp, cpeIp=cpeIp, ping_interface=ping_interface, log_save_path=log_save_path)
