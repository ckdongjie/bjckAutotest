# coding = 'utf-8'
'''
Created on 2022年11月11日

@author: dj


'''

import logging

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.basic.xmlManager import key_read_xml_root_value, \
    key_modify_xml_root_value, key_modify_xml_record_value
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login
from UserKeywords.weblmt.WeblmtXmlManager import key_export_xml_file, \
    key_upload_xml_to_weblmt, key_import_xml_to_gnb
    
@allure.story("weblmt配置文件导入导出压力测试")
@pytest.mark.welmt配置文件导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['welmt配置文件导出导入测试'] if RUN_TESTCASE.get('welmt配置文件导出导入测试') else [])
def testDownloadXmlAndUploadXmlOnWeblmt(testNum):
    xmlFileName='BntCfgFile'
    cellId=0
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    with allure.step('weblmt配置文件导出导入压力测试'):
        weblmt = key_weblmt_login()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                #下载xml文件到本地
                exportRes = key_export_xml_file(weblmt)
                assert exportRes == 'success','配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlSavePath+'\\'+xmlFileName, )
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #数据同步
                importRes = key_import_xml_to_gnb(weblmt, staType=staType)
                assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
                with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
                    logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
                    key_wait(180)
                with allure.step(key_get_time()+':基站重启完成，确认小区状态正常'):
                    logging.info(key_get_time()+': gnb reboot success, confirm cell status is available.')
                    confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
                    assert confirmRes == True, '小区状态与预期不一致，请检查！'

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号为空
def testImportXmlSnIsNone():
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    xmlFileName='BntCfgFile'
    cellId=0
    with allure.step('welmt配置文件导出导入异常测试_SN号为空'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        exportRes = key_export_xml_file(weblmt)
        assert exportRes == 'success','配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value(xmlSavePath+'\\'+xmlFileName, 'version')
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':''}
        key_modify_xml_root_value(xmlSavePath+'\\'+xmlFileName, valueDir)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt, xmlSavePath, xmlFileName)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        with allure.step(key_get_time()+':基站重启完成，确认小区状态正常'):
            logging.info(key_get_time()+': gnb reboot success, confirm cell status is available.')
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'
        
@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号过短
def testImportXmlSnIsShort():
    xmlFileName='BntCfgFile'
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    cellId=0
    with allure.step('welmt配置文件导出导入异常测试_SN号过短'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        exportRes = key_export_xml_file(weblmt)
        assert exportRes == 'success','配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value(xmlSavePath+'\\'+xmlFileName, 'version')
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':'902272840'}
        key_modify_xml_root_value(xmlSavePath+'\\'+xmlFileName, valueDir)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        with allure.step(key_get_time()+':基站重启完成，确认小区状态正常'):
            logging.info(key_get_time()+': gnb reboot success, confirm cell status is available.')
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号过长
def testImportXmlSnIsLong():
    xmlFileName='BntCfgFile'
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    cellId=0
    with allure.step('welmt配置文件导出导入异常测试_SN号过长'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        exportRes = key_export_xml_file(weblmt)
        assert exportRes == 'success','配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value(xmlSavePath+'\\'+xmlFileName, 'version')
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':'902272840123123'}
        key_modify_xml_root_value(xmlSavePath+'\\'+xmlFileName, valueDir)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        with allure.step(key_get_time()+':基站重启完成，确认小区状态正常'):
            logging.info(key_get_time()+': gnb reboot success, confirm cell status is available.')
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'
                                
@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号为非法值
def testImportXmlSnIsAbnormal():
    xmlFileName='BntCfgFile'
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    cellId=0
    with allure.step('welmt配置文件导出导入异常测试_SN号为非法值'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        exportRes = key_export_xml_file(weblmt)
        assert exportRes == 'success','配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value(xmlSavePath+'\\'+xmlFileName, 'version')
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':'#￥%……##￥'}
        key_modify_xml_root_value(xmlSavePath+'\\'+xmlFileName, valueDir)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, xmlFileName, staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        with allure.step(key_get_time()+':基站重启完成，确认小区状态正常'):
            logging.info(key_get_time()+': gnb reboot success, confirm cell status is available.')
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_Tac为非法值
def testImportXmlTacIsAbnormal():
    xmlFileName='BntCfgFile'
    xmlSavePath=BASIC_DATA['version']['xmlSavePath']
    with allure.step('welmt配置文件导出导入异常测试_Tac为非法值'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        exportRes = key_export_xml_file(weblmt)
        assert exportRes == 'success','配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value(xmlSavePath+'\\'+xmlFileName, 'version')
        staType = versionName.split('_')[0]
        #修改配置文件，tac设置为非法值
#             xmlTreePath = './/gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        modifyContext = '&*^'
        key_modify_xml_record_value(xmlSavePath+'\\'+xmlFileName, xmlTreePath, modifyContext)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes != 'success','配置数据导入结果与预期不一致，请检查！'