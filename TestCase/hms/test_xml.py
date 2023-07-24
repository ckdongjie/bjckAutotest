# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj
'''
#获取父目录

import logging
import os
import sys

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.basic.xmlManager import key_modify_xml_root_value, \
    key_modify_xml_record_value, key_read_xml_record_value, \
    key_read_xml_root_value
from UserKeywords.gnb.gnbManager import key_query_gnb_cpu_ratio, \
    key_ssh_login_gnb
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.hms.TaConfigManager import key_get_tac_value, \
    key_set_tac_value
from UserKeywords.hms.VersionManager import  key_upload_xml_file_from_gnb_to_hms, \
    key_download_xml_file_to_local, key_upload_xml_from_local_to_hms, \
    key_download_xml_from_hms_to_gnb, key_download_xml_from_hms_to_gnb_imediate, \
    key_query_fail_xml_file, key_delete_fail_xml_file


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()

@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@allure.story("基站配置文件导出导入测试")
@pytest.mark.run(order=7)
@pytest.mark.配置文件导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['配置文件导出导入测试'] if RUN_TESTCASE.get('配置文件导出导入测试') else [])
def testDownloadXmlAndUploadXml(testNum, ):
    with allure.step('基站配置文件导入导出测试'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                #数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, filename)
                with allure.step(key_get_time()+':数据同步成功，等待基站复位重启......'):
                    logging.info(key_get_time()+': syn xml success, wait for gnb reboot......')
                    key_wait(180)
                key_confirm_device_online(hmsObj)
            key_wait(30)

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN为空
def testUploadXmlSnIsNone():
    with allure.step('SN号为空时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，sn设置为空
        valueDir = {'sn':''}
        key_modify_xml_root_value(valueDir, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
    
@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN长度过短
def testUploadXmlSnIsShort():
    with allure.step('SN号过短时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'902272840'}
        key_modify_xml_root_value(valueDir, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN长度过长
def testUploadXmlSnIsLong():
    with allure.step('SN号过长时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'90227284000811'}
        key_modify_xml_root_value(valueDir, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'             
                                
@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN非法值
def testUploadXmlSnIsAbnormal():
    with allure.step('SN配置非法值时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'&&##abc'}
        key_modify_xml_root_value(valueDir, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_Tac值异常
def testUploadXmlTacIsAbnormal():
    with allure.step('tac配置异常值时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        modifyContext = '&*^'
        key_modify_xml_record_value(xmlTreePath, modifyContext, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        
@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_Tac值修改
@pytest.mark.parametrize("tacSetValue",RUN_TESTCASE['配置文件导出导入测试_Tac值修改'] if RUN_TESTCASE.get('配置文件导出导入测试_Tac值修改') else [])
def testUploadXmlTacValureModify(tacSetValue):
    with allure.step('tac配置修改，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        omcReadValue = key_read_xml_record_value(xmlTreePath, filename)
        key_modify_xml_record_value(xmlTreePath, str(tacSetValue), filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == True,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        #数据同步
        key_download_xml_from_hms_to_gnb(hmsObj, filename)
        key_wait(20)
        dataId = key_query_fail_xml_file(hmsObj)
        assert dataId == '','配置数据同步失败，请检查！'
        with allure.step(key_get_time()+':数据同步成功，等待基站复位重启......'):
            logging.info(key_get_time()+': syn xml success, wait for gnb reboot......')
            key_wait(180)
        key_confirm_device_online(hmsObj)
        tacValue = key_get_tac_value(hmsObj, enbId)
        assert tacValue == tacSetValue, '网管查询tac值与xml导入的配置值不一致，请检查！'
        with allure.step(key_get_time()+':恢复tac参数配置'):
            logging.info(key_get_time()+': recover tac config')
            key_set_tac_value(hmsObj, enbId, int(omcReadValue))

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_Tac值超界
@pytest.mark.parametrize("tacSetValue",RUN_TESTCASE['配置文件导出导入测试_Tac值超界'] if RUN_TESTCASE.get('配置文件导出导入测试_Tac值超界') else [])
def testUploadXmlTacValureModify1(tacSetValue):
    with allure.step('tac配置修改，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        key_modify_xml_record_value(xmlTreePath, str(tacSetValue), filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
           
@pytest.mark.配置文件导入查询cpu利用率
@pytest.mark.parametrize("testNum",RUN_TESTCASE['配置文件导入查询cpu利用率'] if RUN_TESTCASE.get('配置文件导入查询cpu利用率') else [])
def testQueryCpuRatioAndImportXml(testNum):
    with allure.step('基站配置文件导入时CPU利用率查询'):
        logging.info(key_get_time()+': query cpu ratio when import xml')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                #数据同步
                key_download_xml_from_hms_to_gnb_imediate(hmsObj, filename)
                gnb = key_ssh_login_gnb()
                key_query_gnb_cpu_ratio(gnb, coreNum=14, queryNum=30)
                with allure.step(key_get_time()+':数据同步成功，等待基站复位重启......'):
                    logging.info(key_get_time()+': syn xml success, wait for gnb reboot......')
                    key_wait(180)
                key_confirm_device_online(hmsObj)
                key_wait(30)

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_版本号异常
def testUploadXmlVersionIsAbnormal():
    with allure.step('版本号异常时，配置文件导入'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        key_delete_fail_xml_file(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        oldVersion = key_read_xml_root_value('version', filename)
        #修改配置文件，sn设置为空
        valueDir = {'version':'BS5514_V1.20.24'}
        key_modify_xml_root_value(valueDir, filename)
        #上传xml文件到网管
        uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
        assert uploadRes != False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        #数据同步
        key_download_xml_from_hms_to_gnb_imediate(hmsObj, filename)
        with allure.step(key_get_time()+':数据同步成功，等待基站复位重启......'):
            logging.info(key_get_time()+': syn xml success, wait for gnb reboot......')
            key_wait(180)
            key_confirm_device_online(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        key_wait(20)
        dataId = key_query_fail_xml_file(hmsObj)
        assert dataId == '','配置数据同步失败，请检查！'
        #下载xml文件到本地
        fileSize, filenameModify = key_download_xml_file_to_local(hmsObj, enbId)
        curVersion = key_read_xml_root_value('version', filenameModify)
        assert oldVersion == curVersion, '版本号信息与预期不一致，请检查！'
