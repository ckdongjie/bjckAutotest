# coding = utf-8 
'''
Created on 2022年9月5日

'''
from datetime import datetime
import logging
import os
import sys
from time import sleep
import pytest
#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time

def login_main():
    print('***********************************************************************')
    print('*                         AutoTest Tool                               *') 
    print('*                                                                     *')
    print('*                                            --author:bjcktech@2022   *')
    print('***********************************************************************')
    testcaseMasks = ''
    markList = RUN_TESTCASE.keys()
    for mark in markList:
        testcaseMasks = testcaseMasks + mark + ' or '
    return testcaseMasks[0:-4]

def new_dir(path):
    nowtime = datetime.now()
    nowtime.strftime('%Y-%m-%d_%H-%M-%S')
    timeStr = (str(nowtime).split('.')[0]).replace(' ','-').replace(':','-')
    reportDir = path+'\\report_'+timeStr
    if not os.path.exists(reportDir):
        os.mkdir(reportDir)
        return reportDir
    

if __name__ == '__main__':
    runTestMark = login_main()
     
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    xmlDir = BASE_DIR+'\\target\\allure-results'
    
    #清空xml数据
    delCmd = 'rd /s/Q '+xmlDir
    os.popen(delCmd)
    sleep(5)
    os.mkdir(xmlDir)
    
    pytest.main(['-s', '-v', BASE_DIR+'/autotestPro/TestCase', '-m', runTestMark,'--alluredir', BASE_DIR+'/target/allure-results', '--junitxml',BASE_DIR+'/target/test-reports/result.xml'])
#----------------------------------------------------------------------------------------------------------------------
#     生成测试报告 
#     allure generate --clean E:\autotestPro\AutoTestMain\report\xml -o E:\autotestPro\AutoTestMain\report\html2
#----------------------------------------------------------------------------------------------------------------------
    reportDir = new_dir(BASE_DIR+'\\autotestPro\\AutoTestMain\\report')
    logging.warning(key_get_time()+': generate test report: '+reportDir)
    genReportCmd = 'allure generate --clean '+xmlDir+' -o '+reportDir
    os.popen(genReportCmd)

    #打开测试报告
    #allure open E:\autotestPro\AutoTestMain\report\html2
    