# coding = utf-8 
'''
Created on 2022年9月5日

@author: dj
'''
import logging
import os
import sys

import allure
import pytest

from TestCase import globalPara
from TestCase.hms.test_alarm import testQueryHistoryAlarm
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.basic.xmlManager import key_read_xml_root_value
from UserKeywords.gnb.gnbManager import key_ssh_login_gnb, \
    key_query_gps_md5_value, key_query_nrsys_version, key_forbid_dpdk0, \
    key_unforbid_dpdk0, key_open_log_print_switch, key_capture_package_on_gnb, \
    key_upgrade_cpld_version, key_gnb_copy_file, key_logout_gnb, \
    key_query_gnb_cpu_ratio
from UserKeywords.hms.CellManager import key_confirm_cell_status, key_block_cell, \
    key_unblock_cell
from UserKeywords.hms.DeviceManager import key_confirm_device_online
from UserKeywords.hms.DiagnosticManager import key_reboot_enb
from UserKeywords.hms.HmsManager import key_get_enb_info, key_login_hms
from UserKeywords.hms.UserManager import key_add_user
from UserKeywords.hms.VersionManager import key_query_package_exist, \
    key_download_version, key_active_version, key_query_version_info, \
    key_download_gkg_to_local, key_upload_version_to_hms, \
    key_query_download_status, key_query_active_status, \
    key_upload_version_to_hms_if_version_no_exit, key_rollback_version, \
    key_query_rollback_status, key_query_version_info_from_device, \
    key_get_newest_version, key_upload_xml_file_from_gnb_to_hms, \
    key_download_xml_file_to_local, key_upload_xml_from_local_to_hms, \
    key_download_xml_from_hms_to_gnb, key_query_fail_xml_file, \
    key_delete_fail_xml_file, key_create_polic_upgrade_task, \
    key_query_polic_upgrade_task_info
from UserKeywords.pdn.pndManager import key_pdn_login
from UserKeywords.power.APS7100 import key_login_aps7100, key_power_on_aps7100, \
    key_power_off_aps7100, key_logout_aps7100
from UserKeywords.power.Delixi import key_login_delixi, key_logout_delixi, \
    key_power_off_delixi, key_power_on_delixi
from UserKeywords.power.Power import key_power_off, key_power_on
from UserKeywords.ue.CpeManager import key_cpe_login, key_confirm_pdu_setup_succ, \
    key_cpe_ping, key_cpe_logout, key_dl_udp_nr_flow_test, \
    key_dl_udp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_dl_tcp_nr_flow_test, \
    key_dl_tcp_wifi_flow_test, key_ul_tcp_nr_flow_test, \
    key_ul_tcp_wifi_flow_test, key_local_pc_ping
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_upload_version, \
    key_weblmt_query_upload_result, key_weblmt_active_version
from UserKeywords.weblmt.WeblmtXmlManager import key_export_xml_file, \
    key_upload_xml_to_weblmt, key_import_xml_to_gnb


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()

@allure.story("冒烟测试—版本升级") 
@pytest.mark.基站版本冒烟测试_OMC升级最新版本
@pytest.mark.run(order=1)
def testVersionSmoke():
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    cellIdList = BASIC_DATA['gnb']['cellIdList']
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    #查询基站运行版本号
    key_query_version_info_from_device(hmsObj)
    verInfoDict = key_query_version_info(hmsObj)
    curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
    with allure.step(key_get_time()+':当前运行的版本号: '+curVersion):
        logging.info(key_get_time()+': current version: '+curVersion)
    #查询版本库中是否有最新版本
    newestVerNum = key_get_newest_version(curVersion)
    if newestVerNum != '':
        key_upload_version_to_hms_if_version_no_exit(hmsObj, newestVerNum)
        startTime = key_get_time()
        downRes = key_download_version(hmsObj, softVersion=newestVerNum)
        assert downRes == 'success', '版本下载执行失败，请检查！'
        downStatus = key_query_download_status(hmsObj, enbName)
        assert downStatus == 'success','基站版本下载失败，请检查！'
        activeRes = key_active_version(hmsObj)
        assert activeRes == 'success', '版本激活失败，请检查！'
        activeStatus = key_query_active_status(hmsObj, enbName)
        assert activeStatus == 'success','基站版本激活失败，请检查！'
        with allure.step(key_get_time()+':版本激活成功，等待基站复位重启（3min）'):
            logging.info(key_get_time()+': active success, gnb will auto reboot, wait for 3min......')
            key_wait(180) #基站激活复位，等待3min
        key_confirm_device_online(hmsObj)
        with allure.step(key_get_time()+':确认版本升级成功，校验升级后版本号是否正确'):
            for activeNum in range (0, 10):
                key_query_version_info_from_device(hmsObj)
                verInfoDict = key_query_version_info(hmsObj)   
                curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
                if curVersion == newestVerNum:
                    break
                else:
                    key_wait(5)
            #查询基站运行版本号
            with allure.step(key_get_time()+':当前运行的版本号: '+curVersion):
                logging.info(key_get_time()+': current version: '+curVersion)
            assert curVersion == newestVerNum,'激活后基站版本校验失败，请检查！'
        #设置版本升级状态
        globalPara.set_upgrade_status(True)
        endTime = key_get_time()
        #check cell status 
        if isCheckCell:
            for cellId in cellIdList:
                key_confirm_cell_status(hmsObj, enbId, expectStatus='available', cellId=cellId)
        #gnb alarm
        testQueryHistoryAlarm(startTime, endTime) 

'''
      终端业务测试
    参数：
    isAttach:是否接入测试
    isPing:是否ping包测试
    isFlow:是否流量测试
'''
def CellBusinessManager(isAttach, isPing, isTraffic):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    pingType = BASIC_DATA['ping']['pingType']#pc/cpe
    if isAttach:
        with allure.step(key_get_time()+': 执行cpe业务测试'):
            logging.info(key_get_time()+': exec cpe business test')
            cpe = key_cpe_login()
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            assert setupRes == 'success','cpe接入失败，请检查！'
            key_wait(5)
            if isPing == True:
                if pingType == 'cpe':
                    key_cpe_ping(cpe, pingInterface = pingNrInterface)
                    key_cpe_ping(cpe, pingInterface = pingwifiInterface)
                elif pingType == 'pc':
                    key_local_pc_ping(cpe)
                else:
                    key_cpe_ping(cpe, pingInterface = pingNrInterface)
                    key_cpe_ping(cpe, pingInterface = pingwifiInterface)
                    key_local_pc_ping(cpe)
            if isTraffic:
                with allure.step(key_get_time()+': 小区流量测试'):
                    logging.info(key_get_time()+': cell traffic test')
                    type = BASIC_DATA['traffic']['type']
                    dir = BASIC_DATA['traffic']['dir']
                    pdn = key_pdn_login()
                    if type == 'UDP':
                        if dir == 'DL':
                            key_dl_udp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_dl_udp_wifi_flow_test(cpe, pdn)
                        elif dir == 'UL':
                            key_ul_udp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_ul_udp_wifi_flow_test(cpe, pdn)
                        else:
                            key_dl_udp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_dl_udp_wifi_flow_test(cpe, pdn)
                            key_wait(30)
                            key_ul_udp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_ul_udp_wifi_flow_test(cpe, pdn)
                    if type == 'TCP':
                        if dir == 'DL':
                            key_dl_tcp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_dl_tcp_wifi_flow_test(cpe, pdn)
                        elif dir == 'UL':
                            key_ul_tcp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_ul_tcp_wifi_flow_test(cpe, pdn)
                        else:
                            key_dl_tcp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_dl_tcp_wifi_flow_test(cpe, pdn)
                            key_wait(30)
                            key_ul_tcp_nr_flow_test(cpe, pdn)
                            key_wait(20)
                            key_ul_tcp_wifi_flow_test(cpe, pdn)  
            key_cpe_logout(cpe)
                
@allure.story("基站版本管理压力测试") 
@pytest.mark.基站版本升级回退测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本升级回退测试'] if RUN_TESTCASE.get('基站版本升级回退测试') else [])
def testUpgradeAndRollbackVersion(testNum):
    with allure.step(key_get_time()+':压力测试：基站版本升级回退'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+' 次升级回退测试'):
                VersionManager()
                
@allure.story("基站版本管理压力测试") 
@pytest.mark.基站cpld版本升级回退测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站cpld版本升级回退测试'] if RUN_TESTCASE.get('基站cpld版本升级回退测试') else [])
def testUpgradeAndRollbackCpldVersion(testNum):
    with allure.step(key_get_time()+':压力测试：基站CPLD版本升级回退'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+' 次升级回退测试'):
                VersionManager(isRollCpld=True)

@allure.story("基站版本管理压力测试") 
@pytest.mark.基站cpld版本升级回退测试且更新Bootmisc
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站cpld版本升级回退测试且更新Bootmisc'] if RUN_TESTCASE.get('基站cpld版本升级回退测试且更新Bootmisc') else [])
def testUpgradeAndRollbackCpldVersionUpdateBootmisc(testNum):
    with allure.step(key_get_time()+':压力测试：基站CPLD版本升级回退'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+' 次升级回退测试'):
                VersionManager(isRollCpld=True, isUpdateBootmisc=True)
            
@allure.story("基站版本管理压力测试") 
@pytest.mark.V4基站cpld版本升级回退测试且更新Bootmisc
@pytest.mark.parametrize("testNum",RUN_TESTCASE['V4基站cpld版本升级回退测试且更新Bootmisc'] if RUN_TESTCASE.get('V4基站cpld版本升级回退测试且更新Bootmisc') else [])
def testV4UpgradeAndRollbackCpldVersionUpdateBootmisc(testNum):
    with allure.step(key_get_time()+':压力测试：基站CPLD版本升级回退'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+' 次升级回退测试'):
                VersionManager(isRollCpld=True, isUpdateBootmisc=True, gnbType='V4')
                
@allure.story("基站版本管理压力测试") 
@pytest.mark.基站版本升级回退_配置导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本升级回退_配置导出导入测试'] if RUN_TESTCASE.get('基站版本升级回退_配置导出导入测试') else [])
def testUpgradeAndRollbackVersionAndExportAndImportXml(testNum):
    with allure.step(key_get_time()+':压力测试：基站版本升级回退&&配置导出导入测试'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次升级回退测试'):
                VersionManager(isRollCpld=False, isXmlTest=True)
        
'''
    单次基站升级回退测试
    step1:登录网管
    step2:查询目标版本包是否存在，不存在则从版本库中下载版本到网管上
    step3:下载版本，并确认版本下载成功
    step4:激活版本，并确认版本升级成功
    step5:查询升级后小区状态
'''
def VersionManager(isRollCpld=False, isXmlTest=False, isUpdateBootmisc=False, isLogAndCapture=False, gnbType='V2'):
    hmsObj = key_login_hms()
    isDownAgain = BASIC_DATA['version']['isDownAgain']
    cellIdList = BASIC_DATA['gnb']['cellIdList']
    softVersion = BASIC_DATA['version']['upgradeVersion']
    isCheckVerDetail = BASIC_DATA['VerDetail']['isCheckVerDetail']
    isCheckRollVerDetail = BASIC_DATA['VerDetail']['isCheckRollVerDetail']
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    isAttach = BASIC_DATA['common']['isAttach']
    isPing = BASIC_DATA['common']['isPing']
    isFlow = BASIC_DATA['common']['isTraffic']
    recoverVersion = BASIC_DATA['version']['recoverVersion']
    gnbType = BASIC_DATA['common']['gnbType']
    enbId, enbName = key_get_enb_info(hmsObj)
    verInfoDict = key_query_version_info(hmsObj)
    bakVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
    isExist = key_query_package_exist(hmsObj)
    if isExist == False:
        fileSize = key_download_gkg_to_local()
        key_upload_version_to_hms(hmsObj, fileSize)
    if isLogAndCapture == True:
        openEnbLogAndCaptureData()
    downRes = key_download_version(hmsObj)
    assert downRes == 'success', '版本下载执行失败，请检查！'
    downStatus = key_query_download_status(hmsObj, enbName)
    assert downStatus == 'success','版本下载任务执行失败，请检查！'
    key_query_version_info_from_device(hmsObj)
    activeRes = key_active_version(hmsObj)
    assert activeRes == 'success', '版本激活执行失败，请检查！'
    activeStatus = key_query_active_status(hmsObj, enbName)
    assert activeStatus != 'fail','版本激活任务执行失败，请检查！'
    if activeStatus == 'activing':
        activeTimeoutScene(softVersion)
    with allure.step(key_get_time()+':版本激活任务执行成功，等待基站复位重启（3min）'):
        logging.info(key_get_time()+': version active success, gnb will auto reboot, wait for 3min......')
        key_wait(180) #基站激活复位，等待3min
    key_confirm_device_online(hmsObj)
    if isLogAndCapture == True:
        openEnbLogAndCaptureData()
    with allure.step(key_get_time()+':确认版本升级成功，校验升级后版本号是否正确'):
        logging.info(key_get_time()+': confirm if the current version is same as the upgrade version')
        for i in range (0, 5):
            key_query_version_info_from_device(hmsObj)
            verInfoDict = key_query_version_info(hmsObj)   
            curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
            if curVersion == softVersion:
                break
            else:
                key_wait(5)
        with allure.step(key_get_time()+':当前运行版本：'+curVersion):
            logging.info(key_get_time()+': current version:'+curVersion)
        assert curVersion == softVersion,'基站版本激活后基站版本号校验失败，请检查！'
        if isCheckVerDetail == True:
            checkUpgradeVersionInfo(hmsObj)
    if isCheckCell:
        for cellId in cellIdList:
            key_confirm_cell_status(hmsObj, enbId, 'available', cellId=cellId)
    key_wait(60)
    #业务测试
    CellBusinessManager(isAttach, isPing, isFlow)     
    #回退版本包
    with allure.step(key_get_time()+':回退基站版本：'+bakVersion):
        logging.info(key_get_time()+': rollback gnb version:'+bakVersion)
    rollRes = key_rollback_version(hmsObj)
    assert rollRes == 'success','版本回退执行失败，请检查！'
    #检查回退任务状态
    rollStatus = key_query_rollback_status(hmsObj, enbName)
    assert rollStatus != 'fail','回退任务执行失败，请检查！'
    if rollStatus == 'rollbacking':
        rollbackTimeoutScene(bakVersion)
    else:
        with allure.step(key_get_time()+':等待基站回退复位启动'):
            logging.info(key_get_time()+': version rollback success, wait for gnb online')
            key_wait(180)
            key_confirm_device_online(hmsObj)
            if isLogAndCapture == True:
                openEnbLogAndCaptureData()
        with allure.step(key_get_time()+':确认版本回退成功，校验回退后版本号是否正确'):
            logging.info(key_get_time()+': confirm if the current version is same as the rollback version')
            for roll in range (0, 5):
                key_query_version_info_from_device(hmsObj)
                verInfoDict = key_query_version_info(hmsObj)   
                curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
                if curVersion == bakVersion:
                    break
                else:
                    key_wait(5)
            with allure.step(key_get_time()+':当前运行版本：'+curVersion):
                logging.info(key_get_time()+': current version:'+curVersion)
            assert curVersion == bakVersion,'版本回退后基站版本号校验失败，请检查！'
        if isCheckRollVerDetail == True:
            checkRollbackVersionInfo(hmsObj)
    if isDownAgain == True: 
        downloadVersionAgain(hmsObj,recoverVersion, enbName)
    if isRollCpld == True:
        if gnbType == 'V2':
            rollCpldVersion(hmsObj,'BS5514_MBb_mbcl_2021092701.jed', '/home', 'V2', '219271')
        else:
            rollCpldVersion(hmsObj,'BS5514_MBbV4_mbcl__2022040801.sbit', '/root', 'V4', '22481', gnbType=gnbType)
    if isUpdateBootmisc == True:
        replaceBootmisc()
    if isXmlTest==True:
        exportAndImportXml(hmsObj)


'''
    开启基站log记录，并抓包
'''
def openEnbLogAndCaptureData():
    gnb = key_ssh_login_gnb()
    #打开基站log记录开关
    key_open_log_print_switch(gnb)
    #启动基站抓包
    key_capture_package_on_gnb(gnb, filePath='/')
    key_logout_gnb(gnb)
    
'''
    更新bootmisc.sh文件
'''
def replaceBootmisc():
    gnb = key_ssh_login_gnb()
    key_gnb_copy_file(gnb, '/home/bootmisc.sh', '/etc/init.d/bootmisc.sh')
    key_logout_gnb(gnb)
    
'''
    回退cpld版本
'''
def rollCpldVersion(hmsObj,cpldFileName, cpldFilePath, enbType, checkVersion, gnbType='V2'):
    powerType = BASIC_DATA['power']['powerType']
    #手工更新cpld版本
    gnb = key_ssh_login_gnb()
    key_upgrade_cpld_version(gnb, cpldFileName, cpldFilePath, enbType)
    with allure.step(key_get_time()+':cpld升级后基站复位，等待3分钟。'):
        key_wait(3*60)
    if gnbType == 'V2':
        with allure.step(key_get_time()+':程控电源控制基站上电下电。'):
            powerOnAndOff(powerType)
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                key_wait(3*60)
    key_confirm_device_online(hmsObj)
    key_query_version_info_from_device(hmsObj)
    verInfoDict = key_query_version_info(hmsObj)
    curCpldVer = verInfoDict['rows'][0]['mu']['cpldVersion']
    if curCpldVer == checkVersion:
        logging.info(key_get_time()+': cpld manual rollback success!')
    else:
        logging.info(key_get_time()+': cpld manual rollback failure, current version:'+curCpldVer)

'''
        程控电源下电上电
'''            
def powerOnAndOff(powerType):
    if powerType == 'aps7001':
        aps7100 = key_login_aps7100()
        key_power_off_aps7100(aps7100)
        key_wait(60)
        key_power_on_aps7100(aps7100)
        key_logout_aps7100(aps7100)
    else:
        delixi = key_login_delixi()
        key_power_off_delixi(delixi)
        key_wait(60)
        key_power_on_delixi(delixi)
        key_logout_delixi(delixi)
    
'''
        再次执行版本下载
'''
def downloadVersionAgain(hmsObj,recoverVersion, enbName):
    with allure.step(key_get_time()+':下载中间版本，恢复环境'):
        logging.warning(key_get_time()+': download other version')
        downRes = key_download_version(hmsObj, softVersion=recoverVersion)
        assert downRes == 'success', '版本下载执行失败，请检查！'
        downStatus = key_query_download_status(hmsObj, enbName)
        assert downStatus == 'success','基站版本下载失败，请检查！'
        key_query_version_info_from_device(hmsObj)
        key_query_version_info(hmsObj)
        
'''
                配置文件导出导入测试
'''
def exportAndImportXml(hmsObj):
    enbId, enbName = key_get_enb_info(hmsObj)
    with allure.step('基站配置文件导入导出测试'):
        logging.info(key_get_time()+': xml file export and import test')
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
        key_confirm_cell_status(hmsObj, enbId, expectStatus='available')          
            
'''
                检查升级后小版本信息是否正确
'''
def checkUpgradeVersionInfo(hmsObj):
    with allure.step(key_get_time()+':确认版本升级后wifi等小版本信息是否正确'):
        logging.info(key_get_time()+':confirm if the upgrade version detail is correct.')
        checkWifiVer = BASIC_DATA['VerDetail']['checkWifiVer']
        checkFpgaPlVer = BASIC_DATA['VerDetail']['checkFpgaPlVer']
        checkFpgaPsVer = BASIC_DATA['VerDetail']['checkFpgaPsVer']
        checkDPhyVer = BASIC_DATA['VerDetail']['checkDPhyVer']
        checkCPhyVer = BASIC_DATA['VerDetail']['checkCPhyVer']
        checkCpldVer = BASIC_DATA['VerDetail']['checkCpldVer']
        checkGpsVer = BASIC_DATA['VerDetail']['checkGpsVer']
        checkNrsysVer = BASIC_DATA['VerDetail']['checkNrsysVer']
        checkAipVer = BASIC_DATA['VerDetail']['checkAipVer']
        with allure.step(key_get_time()+':确认wifi等小版本信息是否正确'):
            for i in range(1,30):
                key_query_version_info_from_device(hmsObj)
                verInfoDict = key_query_version_info(hmsObj)
                curWifiVer = verInfoDict['rows'][0]['mu']['wifiVersion']
                curFpgaPlVer = verInfoDict['rows'][0]['mu']['fpgaPLVersion']
                curFpgaPsVer = verInfoDict['rows'][0]['mu']['fpgaPSVersion']
                curDPhyVer = verInfoDict['rows'][0]['mu']['dPhyVersion']
                curCPhyVer = verInfoDict['rows'][0]['mu']['cPhyVersion']
                curCpldVer = verInfoDict['rows'][0]['mu']['cpldVersion']
                curAipVer = verInfoDict['rows'][0]['mu']['aipVersion']
                if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer and checkAipVer == curAipVer:
                    with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer):
                        logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer)
                    break
                else:
                    with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer):
                        logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer)
                key_wait(10)
            assert checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer and checkAipVer == curAipVer,'小版本信息校验不通过，请检查！'
            gnb = key_ssh_login_gnb()
            curGpsVer = key_query_gps_md5_value(gnb)
            curUbootVer, curNrsysVer = key_query_nrsys_version(gnb)
            if curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                    logging.info(key_get_time()+': version detail check success, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                    logging.warning(key_get_time()+': version detail check abnormal, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
            assert curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer,'gps/nrsys版本检查不通过，请检查！'

'''
                检查升级后小版本信息是否正确
'''
def checkRollbackVersionInfo(hmsObj):
    with allure.step(key_get_time()+':确认版本回退后wifi等小版本信息是否正确'):
        logging.info(key_get_time()+':confirm if the rollback version detail is correct.')
        checkWifiVer = BASIC_DATA['VerDetail']['checkRollWifiVer']
        checkFpgaPlVer = BASIC_DATA['VerDetail']['checkRollFpgaPlVer']
        checkFpgaPsVer = BASIC_DATA['VerDetail']['checkRollFpgaPsVer']
        checkDPhyVer = BASIC_DATA['VerDetail']['checkRollDPhyVer']
        checkCPhyVer = BASIC_DATA['VerDetail']['checkRollCPhyVer']
        checkCpldVer = BASIC_DATA['VerDetail']['checkRollCpldVer']
        checkGpsVer = BASIC_DATA['VerDetail']['checkRollGpsVer']
        checkNrsysVer = BASIC_DATA['VerDetail']['checkRollNrsysVer']
        checkUbootVer = BASIC_DATA['VerDetail']['checkRollUbootVer']
        checkAipVer = BASIC_DATA['VerDetail']['checkRollAipVer']
            
        for i in range(1,30):
            key_query_version_info_from_device(hmsObj)
            verInfoDict = key_query_version_info(hmsObj)
            curWifiVer = verInfoDict['rows'][0]['mu']['wifiVersion']
            curFpgaPlVer = verInfoDict['rows'][0]['mu']['fpgaPLVersion']
            curFpgaPsVer = verInfoDict['rows'][0]['mu']['fpgaPSVersion']
            curDPhyVer = verInfoDict['rows'][0]['mu']['dPhyVersion']
            curCPhyVer = verInfoDict['rows'][0]['mu']['cPhyVersion']
            curCpldVer = verInfoDict['rows'][0]['mu']['cpldVersion']
            curAipVer = verInfoDict['rows'][0]['mu']['aipVersion']
            if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer and checkAipVer == curAipVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer):
                    logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer)
                break
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer):
                    logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer+'/'+curAipVer)
            key_wait(10)
        assert checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer and checkAipVer == curAipVer,'小版本信息校验不通过，请检查！'
        gnb = key_ssh_login_gnb()
        curGpsVer = key_query_gps_md5_value(gnb)
        curUbootVer, curNrsysVer = key_query_nrsys_version(gnb)
        if checkNrsysVer != '':
            if curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                    logging.info(key_get_time()+': version detail check success, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                    logging.warning(key_get_time()+': version detail check abnormal, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
            assert curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer,'gps/nrsys版本检查不通过，请检查！'
        else:
            if curGpsVer == checkGpsVer and curUbootVer == checkUbootVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[gps/uboot]: '+curGpsVer+'/'+curUbootVer):
                    logging.info(key_get_time()+': version detail check success, version info[gps/uboot]: '+curGpsVer+'/'+curUbootVer)
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，版本详情[gps/uboot]: '+curGpsVer+'/'+curUbootVer):
                    logging.warning(key_get_time()+': version detail check abnormal, version info[gps/uboot]: '+curGpsVer+'/'+curUbootVer)
            assert curGpsVer == checkGpsVer and curUbootVer == checkUbootVer,'gps/nrsys版本检查不通过，请检查！'
'''
            版本激活超时异常场景
'''
def activeTimeoutScene(upgradeVersion):
    hmsObj = key_login_hms()
    with allure.step(key_get_time()+':基站激活消息丢失，等待30分钟，等待网管任务超时！'):
        key_wait(60*30)
    key_query_version_info_from_device(hmsObj)
    verInfoDict = key_query_version_info(hmsObj)   
    curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
    if curVersion == upgradeVersion :
        logging.info(key_get_time()+': enb version active success, continue test')
    else:
        logging.warning(key_get_time()+': enb version active failure, curVersion:'+curVersion+', expcetVersion:'+upgradeVersion)
    assert curVersion == upgradeVersion, '基站版本升级失败，请检查！'
    
'''
            版本回退超时异常场景
'''
def rollbackTimeoutScene(rollbackVersion):
    hmsObj = key_login_hms()
    with allure.step(key_get_time()+':基站回退消息丢失，等待30分钟，等待网管任务超时！'):
        key_wait(60*30)
    key_query_version_info_from_device(hmsObj)
    verInfoDict = key_query_version_info(hmsObj)   
    curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
    if curVersion == rollbackVersion:
        logging.info(key_get_time()+': enb version rollback success, continue test')
    else:
        logging.warning(key_get_time()+': enb version rollback failure, curVersion:'+curVersion+', expectVersion:'+rollbackVersion)
    assert curVersion == rollbackVersion, '基站版本回退失败，请检查！'

@pytest.mark.基站版本包下载过程中查询CPU利用率
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包下载过程中查询CPU利用率'] if RUN_TESTCASE.get('基站版本包下载过程中查询CPU利用率') else [])
def testQueryCpuDuringDownloadVersion(testNum):
    with allure.step('基站版本包下载过程中查询CPU利用率'):
        logging.info(key_get_time()+'query gnb cpu use rate during download version')
        recoverVersion=BASIC_DATA['version']['recoverVersion']
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        gnb = key_ssh_login_gnb()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                #查询cpu利用率
                key_query_gnb_cpu_ratio(gnb, coreNum=14, queryNum=30)
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                with allure.step(key_get_time()+':基站版本恢复'):
                    logging.info(key_get_time()+': recover gnb version')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'

@allure.story("基站版本管理异常测试")        
@pytest.mark.基站版本包下载过程中基站断链x秒
@pytest.mark.parametrize("testNum, waitTime",RUN_TESTCASE['基站版本包下载过程中基站断链x秒'] if RUN_TESTCASE.get('基站版本包下载过程中基站断链x秒') else [])
def testGnbOfflineDuringDownloadVersion(testNum, waitTime):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中基站断链'+str(waitTime)+'s'):
        logging.info(key_get_time()+'gnb off line '+str(waitTime)+'s when gnb version download')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        gnb = key_ssh_login_gnb()
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #禁用dpdk0网卡
                    key_forbid_dpdk0(gnb)
                    key_wait(waitTime)
                    key_unforbid_dpdk0(gnb)
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    with allure.step(key_get_time()+':基站版本恢复'):
                        logging.info(key_get_time()+': recover gnb version')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run exception! recover gnb version')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中再次执行版本下载
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中再次执行版本下载'] if RUN_TESTCASE.get('基站版本下载过程中再次执行版本下载') else [])
def testRepeatDownloadVersion(testNum):
    softVersion2=BASIC_DATA['version']['upgradeVersion2']
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中再次执行版本下载'):
        logging.info(key_get_time()+': download gnb version during version downloading')
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    key_upload_version_to_hms_if_version_no_exit(hmsObj, softVersion=softVersion2)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #再次执行版本下载
                    reDownloadRes = key_download_version(hmsObj, softVersion=softVersion2)
                    assert reDownloadRes == 'fail','版本重复下载执行异常，请检查！'
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    with allure.step(key_get_time()+':基站版本恢复'):
                        logging.info(key_get_time()+': recover gnb version')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run exception! recover gnb version')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中执行版本激活
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中执行版本激活'] if RUN_TESTCASE.get('基站版本下载过程中执行版本激活') else [])
def testActiveDuringDownloadVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中执行版本激活'):
        logging.info(key_get_time()+': activing gnb version during version downloading')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #执行版本激活
                    key_wait(2)
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'fail','版本下载过程中执行版本激活操作异常，请检查！'
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    with allure.step(key_get_time()+':基站版本恢复'):
                        logging.info(key_get_time()+': recover gnb version')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run exception! recover gnb version')
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中执行版本回退
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中执行版本回退'] if RUN_TESTCASE.get('基站版本下载过程中执行版本回退') else [])
def testRollbackDuringDownloadVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中执行版本回退'):
        logging.info(key_get_time()+': rollback gnb version during version downloading')
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #执行版本回退
                    key_wait(2)
                    activeRes = key_rollback_version(hmsObj)
                    assert activeRes == 'fail','版本下载过程中执行版本回退操作异常，请检查！'
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    with allure.step(key_get_time()+':基站版本恢复'):
                        logging.info(key_get_time()+': recover gnb version')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run exception! recover gnb version')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中omc复位基站
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中omc复位基站'] if RUN_TESTCASE.get('基站版本下载过程中omc复位基站') else [])
def testOmcRebootDuringDownloadVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中omc复位基站'):
        logging.info(key_get_time()+': reboot gnb by omc during version downloading')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #执行基站复位
                    rebootRes = key_reboot_enb(hmsObj, enbId)
                    assert rebootRes == 'success','基站复位操作异常，请检查！'
                    with allure.step(key_get_time()+':等待基站复位启动'):
                        logging.info(key_get_time()+': wait for gnb online')
                        key_wait(180)
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'downloading','基站版本下载状态与预期不一致，请检查！'
                    with allure.step(key_get_time()+':等待30分钟后基站下载任务超时'):
                        logging.info(key_get_time()+': wait for download task timeout(30min)')
                        key_wait(1800)
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'fail','基站版本下载状态与预期不一致，请检查！'
                    with allure.step(key_get_time()+':基站版本恢复'):
                        logging.info(key_get_time()+': recover gnb version')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run exception! recover gnb version')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)         

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中基站断链x秒
@pytest.mark.parametrize("testNum, waitTime",RUN_TESTCASE['基站版本包激活过程中基站断链x秒'] if RUN_TESTCASE.get('基站版本包激活过程中基站断链x秒') else [])
def testGnbOfflineDuringActiveVersion(testNum, waitTime):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本激活过程中基站断链'+str(waitTime)+'s'):
        logging.info(key_get_time()+': gnb off line '+str(waitTime)+'s during version activing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        gnb = key_ssh_login_gnb()
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #禁用dpdk0网卡
                key_forbid_dpdk0(gnb)
                key_wait(waitTime)
                key_unforbid_dpdk0(gnb)
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务状态与预期不一致，请检查！'
                with allure.step(key_get_time()+': 等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                with allure.step(key_get_time()+':基站版本恢复'):
                    logging.info(key_get_time()+': recover gnb version')
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+': 等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中下载版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中下载版本'] if RUN_TESTCASE.get('基站版本包激活过程中下载版本') else [])
def testDownloadDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中下载版本'):
        logging.info(key_get_time()+': download gnb version during version activing')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #激活过程中执行版本下载
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'fail','版本下载执行状态与预期不一致，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    with allure.step(key_get_time()+':基站版本恢复'):
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.info(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                isRoll = False
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    while(isRoll==False):
                        activeStatus = key_query_active_status(hmsObj, enbName)
                        if activeStatus == 'success' or activeStatus == 'fail':
                            isRoll = True
                        else:
                            key_wait(30)
                    if isRoll == True:       
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.warning(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中激活版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中激活版本'] if RUN_TESTCASE.get('基站版本包激活过程中激活版本') else [])
def testActiveDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中激活版本'):
        logging.info(key_get_time()+': active gnb version during version activing')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #激活过程中执行版本激活
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'fail','版本激活执行状态与预期不一致，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    with allure.step(key_get_time()+':基站版本恢复'):
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.info(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                isRoll = False
                with allure.step('运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
                    while(isRoll==False):
                        activeStatus = key_query_active_status(hmsObj, enbName)
                        if activeStatus == 'success' or activeStatus == 'fail':
                            isRoll = True
                        else:
                            key_wait(30)
                    if isRoll == True:       
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step('等待基站回退复位启动'):
                            logging.warning(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中回退版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中回退版本'] if RUN_TESTCASE.get('基站版本包激活过程中回退版本') else [])
def testRollbackDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中回退版本'):
        logging.info(key_get_time()+': rollback gnb version during version activing')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #激活过程中执行版本激活
                    logging.info(key_get_time()+': during the activing status, rollback version again')
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'fail','版本回退执行状态与预期不一致，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    key_confirm_device_online(hmsObj)
                    with allure.step(key_get_time()+':基站版本恢复'):
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.info(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                isRoll = False
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
                    while(isRoll==False):
                        activeStatus = key_query_active_status(hmsObj, enbName)
                        if activeStatus == 'success' or activeStatus == 'fail':
                            isRoll = True
                        else:
                            key_wait(30)
                    if isRoll == True:       
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.warning(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包回退过程中下载版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包回退过程中下载版本'] if RUN_TESTCASE.get('基站版本包回退过程中下载版本') else [])
def testDownloadDuringRollbackVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包回退过程中下载版本'):
        logging.info(key_get_time()+': download gnb version during version rollbacking')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    #回退版本包
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    #回退过程中执行版本下载
                    logging.info(key_get_time()+': during the rollbacking status, download version again')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'fail','版本下载执行状态与预期不一致，请检查！'
                    #检查回退任务状态
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    with allure.step(key_get_time()+':备用版本包更新'):
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包回退过程中回退版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包回退过程中回退版本'] if RUN_TESTCASE.get('基站版本包回退过程中回退版本') else [])
def testRollbackDuringRollbackVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包回退过程中下载版本'):
        logging.info(key_get_time()+': rollback gnb version during version rollbacking')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    #回退版本包
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    #回退过程中执行版本下载
                    logging.info(key_get_time()+': query the rollback task status, rollback version again')
                    rollbackRes = key_rollback_version(hmsObj)
                    assert rollbackRes == 'fail','版本回退执行状态与预期不一致，请检查！'
                    #检查回退任务状态
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    with allure.step(key_get_time()+':备用版本包更新'):
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中修改基站参数
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中修改基站参数'] if RUN_TESTCASE.get('基站版本下载过程中修改基站参数') else [])
def testModifyParasDuringDownloadVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中修改基站参数'):
        logging.info(key_get_time()+': modify config paras during version downloading')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #执行参数修改
                    key_block_cell(hmsObj, enbId)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载状态与预期不一致，请检查！'
                    with allure.step(key_get_time()+':基站版本及参数恢复'):
                        #执行参数修改
                        key_unblock_cell(hmsObj, enbId)
                        #确认参数修改生效
                        key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本及参数'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载状态与预期不一致，请检查！'
                    #执行参数修改
                    key_unblock_cell(hmsObj, enbId)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)         

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中修改参数
@pytest.mark.parametrize("testNum,waitTime",RUN_TESTCASE['基站版本包激活过程中修改参数'] if RUN_TESTCASE.get('基站版本包激活过程中修改参数') else [])
def testModifyParamDuringActiveVersion(testNum, waitTime):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中修改参数'):
        logging.info(key_get_time()+': modify config paras during version activing')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    key_upload_version_to_hms_if_version_no_exit(hmsObj, recoverVersion)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #激活等待
                    with allure.step(key_get_time()+':基站激活后等待:'+str(waitTime)+'s'):
                        logging.info(key_get_time()+': active exec success, wait for '+str(waitTime)+'s')
                        key_wait(waitTime)
                    #激活过程中修改基站参数
                    key_block_cell(hmsObj, enbId)
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    key_confirm_device_online(hmsObj)
                    #确认参数修改生效
                    with allure.step(key_get_time()+':确认参数修改生效'):
                        if waitTime == 0:
                            key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                        else:
                            key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                    with allure.step(key_get_time()+':基站版本恢复'):
                        rollRes = key_rollback_version(hmsObj)
                        assert rollRes == 'success','版本回退执行失败，请检查！'
                        rollStatus = key_query_rollback_status(hmsObj, enbName)
                        assert rollStatus == 'success','回退任务失败，请检查！'
                        with allure.step(key_get_time()+':等待基站回退复位启动'):
                            logging.info(key_get_time()+': rollback success, wait for gnb online')
                            key_wait(300)
                        key_confirm_device_online(hmsObj)
                        #执行参数修改
                        key_unblock_cell(hmsObj, enbId)
                        #确认参数修改生效
                        key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
 
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包回退过程中修改参数
@pytest.mark.parametrize("testNum,waitTime",RUN_TESTCASE['基站版本包回退过程中修改参数'] if RUN_TESTCASE.get('基站版本包回退过程中修改参数') else [])
def testModifyParamDuringRollbackVersion(testNum, waitTime):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包回退过程中修改参数'):
        logging.info(key_get_time()+': modify config paras during version rollbacking')
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    key_upload_version_to_hms_if_version_no_exit(hmsObj, recoverVersion)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    key_confirm_device_online(hmsObj)
                    #回退版本包
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    #回退等待
                    with allure.step(key_get_time()+':基站回退后等待:'+str(waitTime)+'s'):
                        logging.info(key_get_time()+': rollback exec success, wait for '+str(waitTime)+'s')
                        key_wait(waitTime)
                    #回退过程中修改基站参数
                    key_block_cell(hmsObj, enbId)
                    #检查回退任务状态
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    key_confirm_device_online(hmsObj)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
                    with allure.step(key_get_time()+':恢复基站版本'):
                        downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                        assert downloadRes == 'success','版本下载执行失败，请检查！'
                        downStatus = key_query_download_status(hmsObj, enbName)
                        assert downStatus == 'success','基站版本下载失败，请检查！'
                        key_query_version_info_from_device(hmsObj)
                        key_query_version_info(hmsObj)
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step(key_get_time()+':运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                
@allure.story("基站版本管理异常测试")
@pytest.mark.不同用户对同一基站进行版本操作
@pytest.mark.parametrize("testNum",RUN_TESTCASE['不同用户对同一基站进行版本操作'] if RUN_TESTCASE.get('不同用户对同一基站进行版本操作') else [])
def testDiffUserVersionUpgradeAndRollback(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：不同用户对同一基站进行版本操作'):
        logging.info(key_get_time()+': operate gnb by different user')
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                    #新增用户并用新用户登录网管
                    key_add_user(hmsObj, 'auto','auto2022@123')
                    hmsObj2 = key_login_hms(username='auto',password='auto2022@123')
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    #root用户下载版本
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #auto用户下载版本
                    logging.info(key_get_time()+': auto user exec download')
                    autoDownloadRes = key_download_version(hmsObj2, user='auto')
                    assert autoDownloadRes == 'fail','auto用户版本下载执行结果与预期不一致，请检查！'
                    #检查root用户下载任务状态
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    #激活版本包
                    activeRes = key_active_version(hmsObj)
                    assert activeRes == 'success','版本激活执行失败，请检查！'
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'success','激活任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站激活复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    #回退版本包
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    #回退过程中修改基站参数
                    key_block_cell(hmsObj, enbId)
                    #检查回退任务状态
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step('运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+': run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中复位基站
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中复位基站'] if RUN_TESTCASE.get('基站版本下载过程中复位基站') else [])
def testRebootGnbDuringDownloadVersion(testNum):
    with allure.step('异常测试：基站版本下载过程中复位基站'):
        logging.info(key_get_time()+': reboot gnb during version downloading')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #复位基站
                    key_reboot_enb(hmsObj, enbId)
                    with allure.step(key_get_time()+':基站复位，等待3分钟后基站建链'):
                        key_wait(180)
                        key_confirm_device_online(hmsObj)
                    downStatus = key_query_download_status(hmsObj, enbName)
                    if downStatus == 'downloading':
                        with allure.step(key_get_time()+':基站版本下载正在执行，等待30分钟后下载任务超时'):
                            logging.info(key_get_time()+':download task is running, wait for 30 mins')
                            key_wait(30*60)
        except:
            logging.warning(key_get_time()+': reboot gnb during gnb download version exec abnormal!')
            
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本下载过程中掉电复位基站
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本下载过程中掉电复位基站'] if RUN_TESTCASE.get('基站版本下载过程中掉电复位基站') else [])
def testPowerOffGnbDuringDownloadVersion(testNum):
    with allure.step('异常测试：基站版本下载过程中掉电复位基站'):
        logging.info(key_get_time()+': power off/on gnb during version downloading')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #复位基站
                    key_power_off()
                    key_wait(60)
                    key_power_on()
                    with allure.step(key_get_time()+':基站复位，等待3分钟后基站建链'):
                        key_wait(180)
                        key_confirm_device_online(hmsObj)
                    downStatus = key_query_download_status(hmsObj, enbName)
                    if downStatus == 'downloading':
                        with allure.step(key_get_time()+':基站版本下载正在执行，等待30分钟后下载任务超时'):
                            logging.info(key_get_time()+': download task is running, wait for 30 mins')
                            key_wait(30*60)
        except:
            logging.warning(key_get_time()+': reboot gnb during gnb download version exec abnormal!')

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中omc导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中omc导入xml'] if RUN_TESTCASE.get('基站版本包激活过程中omc导入xml') else [])
def testImpXmlDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中omc导入xml'):
        logging.info(key_get_time()+': omc import xml during version activing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                key_wait(3)
                #激活过程中执行数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
                dataId = key_query_fail_xml_file(hmsObj)
                assert dataId != '', 'xml导入结果与预期不一致，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务失败，请检查！'
                with allure.step(key_get_time()+':等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                with allure.step(key_get_time()+':基站版本恢复'):
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    key_delete_fail_xml_file(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.omc导入xml过程中激活基站版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['omc导入xml过程中激活基站版本'] if RUN_TESTCASE.get('omc导入xml过程中激活基站版本') else [])
def testActiveVersionDuringImpXml(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：omc导入xml过程中激活基站版本'):
        logging.info(key_get_time()+': active gnb version during xml importing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #执行数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
                dataId = key_query_fail_xml_file(hmsObj)
                assert dataId != '', 'xml导入结果与预期不一致，请检查！'
                #激活版本包
                key_active_version(hmsObj, tryNum=1)
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'false' or activeStatus == 'activing','激活任务状态与预期不一致，请检查！'
                if activeStatus == 'false':
                    with allure.step(key_get_time()+':等待基站复位启动'):
                        logging.info(key_get_time()+': wait for gnb online')
                        key_wait(300)
                    key_confirm_device_online(hmsObj)
                if activeStatus == 'activing':
                    key_wait(16*60)
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'false','激活任务状态与预期不一致，请检查！'
                with allure.step(key_get_time()+':基站版本恢复'):
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_delete_fail_xml_file(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中weblmt导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中weblmt导入xml'] if RUN_TESTCASE.get('基站版本包激活过程中weblmt导入xml') else [])
def testWeblmtImpXmlDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：基站版本包激活过程中weblmt导入xml'):
        logging.info(key_get_time()+': weblmt import xml during version activing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                weblmt = key_weblmt_login()
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                key_wait(10)
                #激活过程中执行数据同步
                importRes = key_import_xml_to_gnb(weblmt, staType=staType)
                assert importRes != 'success','配置数据导入结果与预期不一致，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务失败，请检查！'
                with allure.step(key_get_time()+':等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                with allure.step(key_get_time()+':基站版本恢复'):
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包回退过程中omc导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包回退过程中omc导入xml'] if RUN_TESTCASE.get('基站版本包回退过程中omc导入xml') else [])
def testImpXmlDuringRollbackVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包回退过程中omc导入xml'):
        logging.info(key_get_time()+': omc import xml during version rollbacking')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务失败，请检查！'
                with allure.step(key_get_time()+':等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                with allure.step(key_get_time()+':基站版本恢复'):
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    key_wait(3)
                    #回退过程中执行数据同步
                    key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
                    dataId = key_query_fail_xml_file(hmsObj)
                    assert dataId != '', 'xml导入结果与预期不一致，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    key_delete_fail_xml_file(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.omc导入xml过程中执行版本回退
@pytest.mark.parametrize("testNum",RUN_TESTCASE['omc导入xml过程中执行版本回退'] if RUN_TESTCASE.get('omc导入xml过程中执行版本回退') else [])
def testRollbackVersionDuringImpXml(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：omc导入xml过程中执行版本回退'):
        logging.info(key_get_time()+': rollback gnb version during xml importing by omc')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务失败，请检查！'
                with allure.step(key_get_time()+':等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                #-------------------------weblmt----------------------------------
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                with allure.step(key_get_time()+':基站版本恢复'):
                    #回退过程中执行数据同步
                    key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
                    dataId = key_query_fail_xml_file(hmsObj)
                    assert dataId != '', 'xml导入结果与预期不一致，请检查！'
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus != 'success','回退任务执行结果与预期不一致，请检查！'
                    if rollStatus == 'rollbacking':
                        with allure.step(key_get_time()+':回退任务执行中，等待任务超时失败'):
                            logging.info(key_get_time()+': rollback task is running, wait for timeout')
                            key_wait(30*60)
                    else:
                        with allure.step(key_get_time()+':等待基站复位启动'):
                            logging.info(key_get_time()+': wait for gnb online')
                            key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务执行结果与预期不一致，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    key_delete_fail_xml_file(hmsObj)
                    
                        
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包回退过程中weblmt导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包回退过程中weblmt导入xml'] if RUN_TESTCASE.get('基站版本包回退过程中weblmt导入xml') else [])
def testWeblmtImpXmlDuringRollbackVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：基站版本包激活过程中weblmt导入xml'):
        logging.info(key_get_time()+': weblmt import xml during version rollbacking')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                weblmt = key_weblmt_login()
                logging.info(key_get_time()+': run the test <'+str(i)+'> times')
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务失败，请检查！'
                with allure.step(key_get_time()+':等待基站激活复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                with allure.step(key_get_time()+':基站版本恢复'):
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    key_wait(10)
                    #激活过程中执行数据同步
                    importRes = key_import_xml_to_gnb(weblmt, staType=staType)
                    assert importRes != 'success','配置数据导入结果与预期不一致，请检查！'
                    rollStatus = key_query_rollback_status(hmsObj, enbName)
                    assert rollStatus == 'success','回退任务失败，请检查！'
                    with allure.step(key_get_time()+':等待基站回退复位启动'):
                        logging.info(key_get_time()+': rollback success, wait for gnb online')
                        key_wait(300)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.omc导入xml时weblmt激活版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['omc导入xml时weblmt激活版本'] if RUN_TESTCASE.get('omc导入xml时weblmt激活版本') else [])
def testWeblmtActiveDuringOmcImport(testNum):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    recoverVersion = BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：omc导入xml时weblmt激活版本'):
        logging.info(key_get_time()+': weblmt active gnb version during omc xml importing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            weblmt = key_weblmt_login()
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                
                #检查地址是否保存升级版本包
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local()
                #weblmt上传版本
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                key_weblmt_query_upload_result(weblmt, upgradeVersion)
                #执行数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, filename)
                key_wait(10)
                dataId = key_query_fail_xml_file(hmsObj)
                assert dataId == '', 'xml导入结果与预期不一致，请检查！'  
                #weblmt激活版本
                key_weblmt_active_version(weblmt, upgradeVersion)  
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(180)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                with allure.step(key_get_time()+':恢复weblmt版本上传状态'):
                    logging.info(key_get_time()+': recovery weblmt version upload status')
                    key_weblmt_upload_version(weblmt, recoverVersion, localPath)
                    key_weblmt_query_upload_result(weblmt, recoverVersion)
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.weblmt激活版本时omc导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt激活版本时omc导入xml'] if RUN_TESTCASE.get('weblmt激活版本时omc导入xml') else [])
def testOmcImportDuringWeblmtActive(testNum):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    recoverVersion = BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：weblmt激活版本时omc导入xml'):
        logging.info(key_get_time()+': omc import xml during weblmt activing version')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            weblmt = key_weblmt_login()
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                #配置上载
                key_upload_xml_file_from_gnb_to_hms(hmsObj)
                #下载xml文件到本地
                fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
                #上传xml文件到网管
                key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
                #检查地址是否保存升级版本包
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local()
                #weblmt上传版本
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                key_weblmt_query_upload_result(weblmt, upgradeVersion)
                #weblmt激活版本
                activeRes = key_weblmt_active_version(weblmt, upgradeVersion)  
                key_wait(5)
                #执行数据同步
                key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
                dataId = key_query_fail_xml_file(hmsObj)
                assert dataId != '', 'xml导入结果与预期不一致，请检查！'  
                with allure.step(key_get_time()+':版本激活成功，等待基站复位启动'):
                    logging.info(key_get_time()+': active success, wait for gnb online')
                    key_wait(240)
                    #确认基站在线
                    key_confirm_device_online(hmsObj)
                    key_delete_fail_xml_file(hmsObj)
                with allure.step(key_get_time()+':恢复基站版本'):
                    logging.info(key_get_time()+': recover gnb version')
                    #weblmt上传版本
                    key_weblmt_upload_version(weblmt, recoverVersion, localPath)
                    key_weblmt_query_upload_result(weblmt, recoverVersion)
                    #weblmt激活版本
                    key_weblmt_active_version(weblmt, recoverVersion)  
                    with allure.step(key_get_time()+':版本激活成功，等待基站复位启动'):
                        logging.info(key_get_time()+': active success, wait for gnb online')
                        key_wait(240)
                        #确认基站在线
                        key_confirm_device_online(hmsObj)
                    
                    
@allure.story("基站版本管理异常测试")
@pytest.mark.weblmt导入xml时omc激活版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt导入xml时omc激活版本'] if RUN_TESTCASE.get('weblmt导入xml时omc激活版本') else [])
def testActiveVerDuringWeblmtImpXml(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：weblmt导入xml时omc激活版本'):
        logging.info(key_get_time()+': omc active gnb version during weblmt xml importing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            weblmt = key_weblmt_login()
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #------------------------------------
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #执行数据同步
                key_import_xml_to_gnb(weblmt, staType=staType)
                key_wait(5)
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus != 'success','激活任务状态与预期不一致，请检查！'
                
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                if activeStatus == 'activing':
                    with allure.step(key_get_time()+':版本激活任务进入超时等待状态，等待30分钟后任务超时失败'):
                        logging.info(key_get_time()+': active task is running, wait for 30 minutes')
                        key_wait(30*60)
                with allure.step(key_get_time()+':更新下载版本信息'):
                    logging.info(key_get_time()+': update download version')
                    key_upload_version_to_hms_if_version_no_exit(hmsObj, softVersion=recoverVersion)
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'

@allure.story("基站版本管理异常测试")
@pytest.mark.weblmt导入xml时omc回退版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt导入xml时omc回退版本'] if RUN_TESTCASE.get('weblmt导入xml时omc回退版本') else [])
def testRollbackVerDuringWeblmtImpXml(testNum):
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：weblmt导入xml时omc激活版本'):
        logging.info(key_get_time()+': omc rollback gnb version during weblmt xml importing')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        for i in range (1,testNum+1):
            weblmt = key_weblmt_login()
            logging.info(key_get_time()+': run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                key_upload_version_to_hms_if_version_no_exit(hmsObj)
                downloadRes = key_download_version(hmsObj)
                assert downloadRes == 'success','版本下载执行失败，请检查！'
                downStatus = key_query_download_status(hmsObj, enbName)
                assert downStatus == 'success','基站版本下载失败，请检查！'
                #激活版本包
                activeRes = key_active_version(hmsObj)
                assert activeRes == 'success','版本激活执行失败，请检查！'
                #等待激活任务完成
                activeStatus = key_query_active_status(hmsObj, enbName)
                assert activeStatus == 'success','激活任务状态与预期不一致，请检查！'
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)
                #-----------------weblmt xml-------------------
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #执行数据同步
                key_import_xml_to_gnb(weblmt, staType=staType)
                key_wait(5)
                rollRes = key_rollback_version(hmsObj)
                assert rollRes == 'success','版本回退执行失败，请检查！'
                rollStatus = key_query_rollback_status(hmsObj, enbName)
                assert rollStatus != 'success','版本回退执行状态与预期不一致，请检查！'
                if rollStatus == 'rollbacking':
                    with allure.step(key_get_time()+':版本回退任务进入超时等待状态，等待30分钟后任务超时失败'):
                        logging.info(key_get_time()+': rollback task is running, wait for 30 minutes')
                        key_wait(30*60)
                else:
                    with allure.step(key_get_time()+':等待基站复位启动'):
                        logging.info(key_get_time()+': wait for gnb online')
                        key_wait(300)
                rollRes = key_rollback_version(hmsObj)
                assert rollRes == 'success','版本回退执行失败，请检查！'
                rollStatus = key_query_rollback_status(hmsObj, enbName)
                assert rollStatus == 'success','版本回退执行状态与预期不一致，请检查！'
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(300)
                #确认基站在线
                key_confirm_device_online(hmsObj)

@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包升级前后omc导出导入xml
def testUpgradeVersionAndImpXml():
    with allure.step('异常测试：基站版本包升级前后omc导出导入xml'):
        logging.info(key_get_time()+': omc export/import xml before version upgrade and rollback')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        with allure.step(key_get_time()+':版本升级前执行配置数据导出导入'):
            logging.info(key_get_time()+': export xml and import before upgrade')
            key_upload_version_to_hms_if_version_no_exit(hmsObj)
            #配置上载
            key_upload_xml_file_from_gnb_to_hms(hmsObj)
            #下载xml文件到本地
            fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
            #上传xml文件到网管
            key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
            #执行数据同步
            key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
            dataId = key_query_fail_xml_file(hmsObj)
            assert dataId != '', 'xml导入结果与预期不一致，请检查！'
            key_wait(3*60)
            key_confirm_device_online(hmsObj)
        with allure.step(key_get_time()+':版本升级'):
            logging.info(key_get_time()+': upgrade version')    
            downloadRes = key_download_version(hmsObj)
            assert downloadRes == 'success','版本下载执行失败，请检查！'
            downStatus = key_query_download_status(hmsObj, enbName)
            assert downStatus == 'success','基站版本下载失败，请检查！'
            #激活版本包
            activeRes = key_active_version(hmsObj)
            assert activeRes == 'success','版本激活执行失败，请检查！'
            #等待激活任务完成
            activeStatus = key_query_active_status(hmsObj, enbName)
            assert activeStatus == 'success','激活任务失败，请检查！'
            with allure.step(key_get_time()+':等待基站激活复位启动'):
                logging.info(key_get_time()+': active success, wait for gnb online')
                key_wait(300)
            #确认基站在线
            key_confirm_device_online(hmsObj)
        with allure.step(key_get_time()+':版本升级后执行配置数据导出导入'):
            logging.info(key_get_time()+': export xml and import after upgrade')
            key_upload_version_to_hms_if_version_no_exit(hmsObj)
            #配置上载
            key_upload_xml_file_from_gnb_to_hms(hmsObj)
            #下载xml文件到本地
            fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
            #上传xml文件到网管
            key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
            #执行数据同步
            key_download_xml_from_hms_to_gnb(hmsObj, filename, tryNum=1)
            dataId = key_query_fail_xml_file(hmsObj)
            assert dataId != '', 'xml导入结果与预期不一致，请检查！'
            key_wait(3*60)
            key_confirm_device_online(hmsObj)
        with allure.step(key_get_time()+':基站版本恢复'):
            rollRes = key_rollback_version(hmsObj)
            assert rollRes == 'success','版本回退执行失败，请检查！'
            rollStatus = key_query_rollback_status(hmsObj, enbName)
            assert rollStatus == 'success','回退任务失败，请检查！'
            with allure.step(key_get_time()+':等待基站回退复位启动'):
                logging.info(key_get_time()+': rollback success, wait for gnb online')
                key_wait(300)
            #确认基站在线
            key_confirm_device_online(hmsObj)
            
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包升级后omc导出导入升级前xml
def testUpgradeVersionAndImpOldXml():
    with allure.step('异常测试：基站版本包升级后omc导出导入升级前xml'):
        logging.info(key_get_time()+': omc import low version xml after version upgrade')
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        with allure.step(key_get_time()+':版本升级前执行配置数据导出'):
            logging.info(key_get_time()+': export xml before upgrade')
            key_upload_version_to_hms_if_version_no_exit(hmsObj)
            #配置上载
            key_upload_xml_file_from_gnb_to_hms(hmsObj)
            #下载xml文件到本地
            fileSize, filename = key_download_xml_file_to_local(hmsObj, enbId)
        with allure.step(key_get_time()+':版本升级'):
            logging.info(key_get_time()+': upgrade version')    
            downloadRes = key_download_version(hmsObj)
            assert downloadRes == 'success','版本下载执行失败，请检查！'
            downStatus = key_query_download_status(hmsObj, enbName)
            assert downStatus == 'success','基站版本下载失败，请检查！'
            #激活版本包
            activeRes = key_active_version(hmsObj)
            assert activeRes == 'success','版本激活执行失败，请检查！'
            #等待激活任务完成
            activeStatus = key_query_active_status(hmsObj, enbName)
            assert activeStatus == 'success','激活任务失败，请检查！'
            with allure.step(key_get_time()+':等待基站激活复位启动'):
                logging.info(key_get_time()+': active success, wait for gnb online')
                key_wait(300)
            #确认基站在线
            key_confirm_device_online(hmsObj)
        with allure.step(key_get_time()+':版本升级后执行配置数据导入'):
            logging.info(key_get_time()+': import xml after upgrade')
            #上传xml文件到网管
            uploadRes = key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize)
            assert uploadRes == False, 'xml文件上传结果与预期不一致，请检查！'
        with allure.step(key_get_time()+':基站版本恢复'):
            rollRes = key_rollback_version(hmsObj)
            assert rollRes == 'success','版本回退执行失败，请检查！'
            rollStatus = key_query_rollback_status(hmsObj, enbName)
            assert rollStatus == 'success','回退任务失败，请检查！'
            with allure.step(key_get_time()+':等待基站回退复位启动'):
                logging.info(key_get_time()+': rollback success, wait for gnb online')
                key_wait(300)
            #确认基站在线
            key_confirm_device_online(hmsObj)

@pytest.mark.基站策略升级压测
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站策略升级压测'] if RUN_TESTCASE.get('基站策略升级压测') else [])
def testGnbPolicyUpgrade(testNum):
    gnbSerList = BASIC_DATA['polSoft']['gnbSerList']
    activeVersion = BASIC_DATA['polSoft']['activeVersion']
    rollVersion = BASIC_DATA['polSoft']['rollVersion']
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    gnbType = BASIC_DATA['common']['gnbType']
    isRoll = BASIC_DATA['polSoft']['isRoll']
    with allure.step(key_get_time()+':基站版本策略升级测试'):
        for i in range (1,testNum+1):
            with allure.step(key_get_time()+'执行第 '+str(i)+'次版本策略升级测试'):
                logging.info(key_get_time()+': run the active test <'+str(i)+'> times')
                one_time_gnb_policy_upgrade(activeVersion, gnbSerList, isCheckCell, gnbType)
            if isRoll == True:
                with allure.step(key_get_time()+'执行第 '+str(i)+'次版本策略回退测试'):
                    logging.info(key_get_time()+':run the rollback test <'+str(i)+'> times')
                    one_time_gnb_policy_upgrade(rollVersion, gnbSerList, isCheckCell, gnbType)
                    
'''
    执行单次策略升级任务
'''               
def one_time_gnb_policy_upgrade(activeVersion, gnbSerList, isCheckCell, gnbType):                
    hmsObj = key_login_hms()
    policyName = key_create_polic_upgrade_task(hmsObj, softVersion=activeVersion)
    isExeced = monitor_policy_task_status(hmsObj, policyName)
    if isExeced == True:
        for gnbSer in gnbSerList:
            key_confirm_device_online(hmsObj, serialNumber=gnbSer)
            enbId, enbName = key_get_enb_info(hmsObj, serialNumber=gnbSer)
            with allure.step(key_get_time()+':校验升级后版本号是否正确'):
                logging.info(key_get_time()+': confirm if the current version is same as the upgrade version')
                for num in range (0, 5):
                    key_query_version_info_from_device(hmsObj, serialNumber=gnbSer)
                    verInfoDict = key_query_version_info(hmsObj, serialNumber=gnbSer)   
                    curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
                    if curVersion == activeVersion:
                        break
                    else:
                        key_wait(5)
                with allure.step(key_get_time()+':当前运行版本：'+curVersion):
                    logging.info(key_get_time()+': current version:'+curVersion)
                assert curVersion == activeVersion,'激活后基站版本校验失败，请检查！'
            if isCheckCell == True:
                with allure.step(key_get_time()+':查询nr小区状态'):
                    logging.info(key_get_time()+': query nr cell status')
                    key_confirm_cell_status(hmsObj, enbId, 'available', cellId=1)
                if gnbType == 'BS5524':
                    #mmw cell
                    with allure.step(key_get_time()+':查询mmw小区状态'):
                        logging.info(key_get_time()+': query mmw cell status')
                        key_confirm_cell_status(hmsObj, enbId, 'available', cellId=2)   
    else:
        with allure.step(key_get_time()+':版本策略任务执行异常'):
            logging.info(key_get_time()+': version policy task exec failure')
    assert isExeced == True, '版本策略任务执行异常，请检查!'
    
'''
    监听任务状态
'''                       
def monitor_policy_task_status(hmsObj, policyName):
    isExeced = False
    for wait in range (1, 20):
        queryResList = key_query_polic_upgrade_task_info(hmsObj)
        for taskInfo in queryResList:
            if taskInfo['policyName']== policyName:
                if taskInfo['executeOrNot']== 0:
                    logging.info(key_get_time()+'task not start, wait for 60s')
                    key_wait(60)
                if taskInfo['executeOrNot']== 2:
                    logging.info(key_get_time()+'task is running, wait for 60s')
                    key_wait(60)
                if taskInfo['executeOrNot']== 1:
                    logging.info(key_get_time()+'task exec success')
                    isExeced = True
                    break
        if isExeced == True:            
            break
    return isExeced
            
if __name__ == "__main__":
#     pytest.main(['-s', '-vv', 'test_version.py'])
    print(key_get_time())