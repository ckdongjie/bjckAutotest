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
    key_modify_xml_record_value
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.hms.VersionManager import  key_upload_xml_file_from_gnb_to_hms, \
    key_download_xml_file_to_local, key_upload_xml_from_local_to_hms, \
    key_download_xml_from_hms_to_gnb


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()

@pytest.mark.skipif(globalPara.get_upgrade_status()==True, reason='No Newest Version Upgrade')  
@allure.story("基站配置文件导出导入测试")
@pytest.mark.run(order=7)
@pytest.mark.配置文件导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['配置文件导出导入测试'] if RUN_TESTCASE.get('配置文件导出导入测试') else [])
def testDownloadXmlAndUploadXml(testNum, serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], isCheckData=BASIC_DATA['version']['isCheckData']):
    with allure.step('基站配置文件导入导出测试'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, isCheckData)
                #数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
                with allure.step(key_get_time()+':数据同步成功，等待基站复位重启......'):
                    logging.info(key_get_time()+': syn xml success, wait for gnb reboot......')
                    key_wait(180)
                key_confirm_device_online(hmsObj, serialNumber)
            key_wait(30)

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN为空
def testUploadXmlSnIsNone(serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], checkData=BASIC_DATA['version']['isCheckData']):
    with allure.step('SN号为空时，配置文件导入'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
        #修改配置文件，sn设置为空
        valueDir = {'sn':''}
        key_modify_xml_root_value(xmlSavePath+'\\'+filename, valueDir)
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, checkData)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
        assert synRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        key_wait(30)
    
@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN长度过短
def testUploadXmlSnIsShort(serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], checkData=BASIC_DATA['version']['isCheckData']):
    with allure.step('SN号过短时，配置文件导入'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'902272840'}
        key_modify_xml_root_value(xmlSavePath+'\\'+filename, valueDir)
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, checkData)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
        assert synRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        key_wait(30)

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN长度过长
def testUploadXmlSnIsLong(serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], checkData=BASIC_DATA['version']['isCheckData']):
    with allure.step('SN号过长时，配置文件导入'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'90227284000811'}
        key_modify_xml_root_value(xmlSavePath+'\\'+filename, valueDir)
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, checkData)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
        assert synRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        key_wait(30)               
                                
@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_SN非法值
def testUploadXmlSnIsAbnormal(serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], checkData=BASIC_DATA['version']['isCheckData']):
    with allure.step('SN配置非法值时，配置文件导入'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
        #修改配置文件，sn设置为空
        valueDir = {'sn':'&&##abc'}
        key_modify_xml_root_value(xmlSavePath+'\\'+filename, valueDir)
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, checkData)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
        assert synRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        key_wait(30)

@allure.story("配置文件导入导出异常测试")
@pytest.mark.配置文件导出导入测试_Tac值异常
def testUploadXmlTacIsAbnormal(serialNumber=BASIC_DATA['gnb']['serialNumberList'], xmlSavePath=BASIC_DATA['version']['xmlSavePath'], checkData=BASIC_DATA['version']['isCheckData']):
    with allure.step('tac配置异常值时，配置文件导入'):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj, serialNumber)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
        #修改配置文件，tac设置为非法值
#             xmlTreePath = './/gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        modifyContext = '&*^'
        key_modify_xml_record_value(xmlSavePath+'\\'+filename, xmlTreePath, modifyContext)
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, xmlSavePath, filename, fileSize, checkData)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, serialNumber, filename)
        assert synRes == False,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        key_wait(30)


