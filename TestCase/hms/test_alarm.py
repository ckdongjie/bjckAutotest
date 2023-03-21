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
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time
from UserKeywords.hms.AlarmManager import key_query_active_alarm, \
    key_query_history_alarm
from UserKeywords.hms.HmsManager import key_login_hms


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
    alarmList = key_query_history_alarm(hmsObj, alarmRaisedStartTime=startTime, alarmRaisedEndTime=endTime)
    with allure.step(key_get_time()+':基站历史告警:'+str(alarmList)):
        logging.info(key_get_time()+': history alarm info:'+str(alarmList))
            
# if __name__ == '__main__':
#     TestAlarm().testQueryHistoryAlarm('2023-01-29 14:31:00', '2023-01-30 14:31:00')