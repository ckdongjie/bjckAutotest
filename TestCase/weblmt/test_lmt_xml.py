# coding = 'utf-8'
'''
Created on 2022年11月11日
@author: dj
'''

from datetime import datetime
import logging
import os
import threading

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.basic.xmlManager import key_read_xml_root_value, \
    key_modify_xml_root_value, key_modify_xml_record_value, \
    key_read_xml_record_value, key_rename_xml_file
from UserKeywords.gnb.gnbManager import key_query_gnb_cpu_ratio
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.hms.VersionManager import key_download_gkg_to_local, \
    key_upload_xml_file_from_gnb_to_hms, key_download_xml_file_to_local, \
    key_upload_xml_from_local_to_hms, key_download_xml_from_hms_to_gnb
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_active_version
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_query_upload_result
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_upload_version
from UserKeywords.weblmt.WeblmtXmlManager import key_export_xml_file, \
    key_upload_xml_to_weblmt, key_import_xml_to_gnb


@allure.story("weblmt配置文件导出导入压力测试")
@pytest.mark.welmt配置文件导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['welmt配置文件导出导入测试'] if RUN_TESTCASE.get('welmt配置文件导出导入测试') else [])
def testDownloadXmlAndUploadXmlOnWeblmt(testNum):
    xmlFileName='BntCfgFile'
    cellIdList = BASIC_DATA['gnb']['cellIdList']
    with allure.step('weblmt配置文件导出导入压力测试'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                weblmt = key_weblmt_login()
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
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
                    for cellId in cellIdList:
                        confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
                        assert confirmRes == True, '小区状态与预期不一致，请检查！'

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号为空
def testImportXmlSnIsNone():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_SN号为空'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':''}
        key_modify_xml_root_value(valueDir, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        
@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号过短
def testImportXmlSnIsShort():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_SN号过短'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，sn长度过短
        valueDir = {'sn':'902272840'}
        key_modify_xml_root_value(valueDir, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号过长
def testImportXmlSnIsLong():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_SN号过长'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':'902272840123123'}
        key_modify_xml_root_value(valueDir, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
                                
@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_SN号为非法值
def testImportXmlSnIsAbnormal():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_SN号为非法值'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'sn':'#￥%……##￥'}
        key_modify_xml_root_value(valueDir, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, xmlFileName, staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)

@allure.story("weblmt配置文件导出导入异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_Tac为非法值
def testImportXmlTacIsAbnormal():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_Tac为非法值'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName, )
        staType = versionName.split('_')[0]
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        modifyContext = '&*^'
        key_modify_xml_record_value(xmlTreePath, modifyContext, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes != 'success','配置数据导入结果与预期不一致，请检查！'
        
@pytest.mark.welmt配置文件导入时查询cpu利用率
@pytest.mark.parametrize("testNum",RUN_TESTCASE['welmt配置文件导入时查询cpu利用率'] if RUN_TESTCASE.get('welmt配置文件导入时查询cpu利用率') else [])
def testImportXmlAndQueryCpuRatioByWeblmt(testNum):
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导入时查询cpu利用率'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                weblmt = key_weblmt_login()
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #数据同步
                t0 = threading.Thread(target=key_import_xml_to_gnb,args=(weblmt, staType))
                t1 = threading.Thread(target=key_query_gnb_cpu_ratio, args=(14, 30))
                t0.start()
                t1.start()
                t0.join()
                t1.join()
                with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
                    logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
                    key_wait(240)
                    
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_Tac值修改
@pytest.mark.parametrize("tacSetValue",RUN_TESTCASE['welmt配置文件导出导入异常测试_Tac值修改'] if RUN_TESTCASE.get('welmt配置文件导出导入异常测试_Tac值修改') else [])
def testImportXmlTacValureModify(tacSetValue):
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_Tac值修改'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        oldValure = key_read_xml_record_value(xmlTreePath, xmlFileName)
        key_modify_xml_record_value(xmlTreePath, str(tacSetValue), xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        curValure = key_read_xml_record_value(xmlTreePath, xmlFileName)    
        assert curValure == str(tacSetValue), '修改后的参数与预期不一致，请检查！'
        with allure.step(key_get_time()+':恢复基站参数'):
            logging.info(key_get_time()+': recover gnb config')
            key_modify_xml_record_value(xmlTreePath, oldValure, xmlFileName)
            #上传xml文件到网管
            uploadRes =key_upload_xml_to_weblmt(weblmt)
            assert uploadRes == 'yes','配置数据上传失败，请检查！'
            #数据同步
            importRes = key_import_xml_to_gnb(weblmt, staType=staType)
            assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
            with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
                logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
                key_wait(180)
        
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_Tac值越界
@pytest.mark.parametrize("tacSetValue",RUN_TESTCASE['welmt配置文件导出导入异常测试_Tac值越界'] if RUN_TESTCASE.get('welmt配置文件导出导入异常测试_Tac值越界') else [])
def testImportXmlTacValureAbnormal(tacSetValue):
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_Tac值修改'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/TA_Configuration/t_tapara[@record="1"]/Tac'
        key_modify_xml_record_value(xmlTreePath, str(tacSetValue), xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes != 'success','配置数据导入结果与预期不一致，请检查！'
        
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_版本号异常
def testImportXmlAndVersionAbnormal():
    xmlFileName='BntCfgFile'
    with allure.step('welmt配置文件导出导入异常测试_版本号异常'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，sn设置为空
        valueDir = {'version':'BS5514_V1.20.25'}
        versionNum = key_read_xml_root_value('version', xmlFileName)
        key_modify_xml_root_value(valueDir, xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        curVersionNum = key_read_xml_root_value('version', xmlFileName)
        assert versionNum == curVersionNum, '版本号与预期不一致，请检查！'
        
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt升级前后执行配置文件导出导入测试
def testExpAndImpXmlBeforAndAfterUpgradeVersion():
    xmlFileName='BntCfgFile'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    rollbackVersion = BASIC_DATA['version']['recoverVersion']
    with allure.step(key_get_time()+': welmt升级前执行配置文件导出导入测试'):
        logging.info(key_get_time()+': weblmt export and import xml before upgrade')
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+': 数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
    with allure.step(key_get_time()+': welmt升级版本'):
        logging.info(key_get_time()+': weblmt upgrade version')        
        if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
            key_download_gkg_to_local(upgradeVersion)
        key_weblmt_upload_version(weblmt, upgradeVersion)
        key_weblmt_query_upload_result(weblmt, upgradeVersion)
        key_weblmt_active_version(weblmt, upgradeVersion)
        with allure.step(key_get_time()+': 版本激活成功，等待基站复位重启'):
            logging.info(key_get_time()+': version active success, wait for gnb reboot')
            key_wait(5*60)    
    with allure.step(key_get_time()+': welmt升级后执行配置文件导出导入测试'):
        logging.info(key_get_time()+': weblmt export and import xml after upgrade')
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+': 数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)        
    with allure.step(key_get_time()+': 恢复基站版本'):
        logging.info(key_get_time()+': recovery gnb version')        
        if os.path.exists(localPath+'\\'+rollbackVersion+'.zip') == False:
            key_download_gkg_to_local(rollbackVersion)
        key_weblmt_upload_version(weblmt, rollbackVersion)
        key_weblmt_query_upload_result(weblmt, rollbackVersion)
        key_weblmt_active_version(weblmt, rollbackVersion)
        with allure.step(key_get_time()+': 版本激活成功，等待基站复位重启'):
            logging.info(key_get_time()+': version active success, wait for gnb reboot')
            key_wait(5*60)    
            
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt导入omc导出的xml
def testOmcExpXmlAndWeblmtImpXml():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    xmlSavePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time()+': omc导出xml'):
        logging.info(key_get_time()+': omc export xml')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        #配置上载
        key_upload_xml_file_from_gnb_to_hms(hmsObj)
        #下载xml文件到本地
        fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId, xmlSavePath)
    with allure.step(key_get_time()+': weblmt导入xml'):
        logging.info(key_get_time()+': weblmt import xml')
        
        weblmt = key_weblmt_login()
        versionName = key_read_xml_root_value('version', filename)
        staType = versionName.split('_')[0]
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt, xmlSavePath, filename=filename)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
            
@allure.story("配置文件导入导出异常测试")
@pytest.mark.omc导入welmt导出的xml
def testWeblmtExpXmlAndOmcImpXml():
    xmlFileName='BntCfgFile'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    xmlSavePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    sn = BASIC_DATA['gnb']['serialNumberList']
    nowtime = datetime.now()
    timeStr = nowtime.strftime('%Y%m%d%H%M%S')
    newFileName = 'test_'+sn+'_'+timeStr+'.cfg'
    with allure.step(key_get_time()+': weblmt导出xml'):
        logging.info(key_get_time()+': weblmt export xml')
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt, xmlSavePath)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        key_rename_xml_file(newFileName, xmlFileName, xmlSavePath)
    with allure.step(key_get_time()+': omc导入xml'):
        logging.info(key_get_time()+': omc import xml')
        hmsObj = key_login_hms()
        #上传xml文件到网管
        key_upload_xml_from_local_to_hms(hmsObj, newFileName, fileSize, localPath=xmlSavePath)
        #数据同步
        synRes = key_download_xml_from_hms_to_gnb(hmsObj, newFileName)
        assert synRes == True,key_get_time()+': 配置数据同步状态与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
            
@allure.story("配置文件导入导出异常测试")
@pytest.mark.welmt配置文件导出导入异常测试_wifi发射功率修改
@pytest.mark.parametrize("WifiTxPower",RUN_TESTCASE['welmt配置文件导出导入异常测试_wifi发射功率修改'] if RUN_TESTCASE.get('welmt配置文件导出导入异常测试_wifi发射功率修改') else [])
def testImportXmlWifiValureModify(WifiTxPower):
    xmlFileName='BntCfgFile'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    xmlSavePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step('welmt配置文件导出导入异常测试_wifi发射功率修改'):
        weblmt = key_weblmt_login()
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt, xmlFileName)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        versionName = key_read_xml_root_value('version', xmlFileName)
        staType = versionName.split('_')[0]
        #修改配置文件，tac设置为非法值
        xmlTreePath = './/gNodeB_Function/t_gnbfunction/WiFi_Management/t_wifi[@record="1"]/WifiTxPower'
        oldValure = key_read_xml_record_value(xmlTreePath, xmlFileName)
        key_modify_xml_record_value(xmlTreePath, str(WifiTxPower), xmlFileName)
        #上传xml文件到网管
        uploadRes =key_upload_xml_to_weblmt(weblmt, xmlFileName)
        assert uploadRes == 'yes','配置数据上传失败，请检查！'
        #数据同步
        importRes = key_import_xml_to_gnb(weblmt, staType=staType)
        assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
            logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
            key_wait(180)
        #下载xml文件到本地
        fileSize = key_export_xml_file(weblmt, xmlFileName)
        assert fileSize != 0,'配置文件导出失败，请检查！'
        curValure = key_read_xml_record_value(xmlTreePath, xmlFileName)    
        assert curValure == str(WifiTxPower), '修改后的参数与预期不一致，请检查！'
        with allure.step(key_get_time()+':恢复基站参数'):
            logging.info(key_get_time()+': recover gnb config')
            key_modify_xml_record_value(xmlTreePath, oldValure, xmlFileName)
            #上传xml文件到网管
            uploadRes =key_upload_xml_to_weblmt(weblmt, xmlFileName)
            assert uploadRes == 'yes','配置数据上传失败，请检查！'
            #数据同步
            importRes = key_import_xml_to_gnb(weblmt, staType=staType)
            assert importRes == 'success','配置数据导入结果与预期不一致，请检查！'
            with allure.step(key_get_time()+':数据导入成功，等待基站复位重启......'):
                logging.info(key_get_time()+': import xml success, wait for gnb reboot......')
                key_wait(180)
                
if __name__ == '__main__':
    weblmt = key_weblmt_login()
    cellId = 1
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    key_download_gkg_to_local(upgradeVersion)
    