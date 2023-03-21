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
from UserKeywords.gnb.gnbManager import key_ssh_login_gnb, \
    key_query_gps_md5_value, key_query_nrsys_version, key_forbid_dpdk0, \
    key_unforbid_dpdk0, key_open_log_print_switch, key_capture_package_on_gnb, \
    key_upgrade_cpld_version
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
    key_download_xml_from_hms_to_gnb
from UserKeywords.pdn.pndManager import key_pdn_login
from UserKeywords.power.APS7100 import key_login_aps7100, key_power_on_aps7100, \
    key_power_off_aps7100
from UserKeywords.ue.CpeManager import key_cpe_login, key_confirm_pdu_setup_succ, \
    key_cpe_attach, key_cpe_ping, key_cpe_logout, key_dl_udp_nr_flow_test, \
    key_dl_udp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_dl_tcp_nr_flow_test, \
    key_dl_tcp_wifi_flow_test, key_ul_tcp_nr_flow_test, \
    key_ul_tcp_wifi_flow_test


#获取父目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
globalPara.init()

@allure.story("冒烟测试——版本升级") 
@pytest.mark.基站版本冒烟测试
@pytest.mark.run(order=1)
def testVersionSmoke():
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    isAttach = BASIC_DATA['cpe']['isAttach']
    isPing = BASIC_DATA['cpe']['isPing']
    isTraffic = BASIC_DATA['cpe']['isFlow']
    
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
            assert curVersion == newestVerNum,'激活后基站版本校验失败，请检查！'
        #设置版本升级状态
        globalPara.set_upgrade_status(True)
        endTime = key_get_time()
        #check cell status 
        if isCheckCell:
            key_confirm_cell_status(hmsObj, enbId, 'available')
        #gnb alarm
        logging.info('--------------------------------------------------')
        logging.info('              new version alarm test              ')
        logging.info('--------------------------------------------------')
        testQueryHistoryAlarm(startTime, endTime)
        #cell traffic
        logging.info('--------------------------------------------------')
        logging.info('              new version traffic test            ')
        logging.info('--------------------------------------------------')  
        CellBusinessManager(isAttach, isPing, isTraffic)  

'''
      终端业务测试
    参数：
    isAttach:是否接入测试
    isPing:是否ping包测试
    isFlow:是否流量测试
'''
def CellBusinessManager(isAttach, isPing, isFlow):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    if isAttach:
        with allure.step(key_get_time()+': 执行cpe业务测试'):
            logging.info(key_get_time()+': exec cpe business test')
            cpe = key_cpe_login()
            attachRes = key_cpe_attach(cpe)
            setupRes = key_confirm_pdu_setup_succ(cpe)
            if attachRes == 'OK':
                if setupRes == 'success':
                    with allure.step(key_get_time()+': cpe接入成功'):
                        logging.info(key_get_time()+': cpe attach sussess')
                else:
                    with allure.step(key_get_time()+': cpe接入失败'):
                        logging.warning(key_get_time()+': cpe attach failure')
                #assert setupRes == 'success','cpe接入失败，请检查！'
                if isPing == True:
                    key_cpe_ping(cpe, pingInterface = pingNrInterface)
                    key_cpe_ping(cpe, pingInterface = pingwifiInterface)
                if isFlow:
                    with allure.step(key_get_time()+': 小区流量测试'):
                        type = BASIC_DATA['flow']['type']
                        dir = BASIC_DATA['flow']['dir']
                        pdn = key_pdn_login()
                        logging.info(key_get_time()+': ue traffic test')
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
    isDownAgin = BASIC_DATA['version']['isDownAgain']
    with allure.step(key_get_time()+':压力测试：基站版本升级回退\n'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+'run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+' 次升级回退测试'):
                VersionManager(isDownAgain=isDownAgin)
                
@allure.story("基站版本管理压力测试") 
@pytest.mark.基站cpld版本升级回退测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站cpld版本升级回退测试'] if RUN_TESTCASE.get('基站cpld版本升级回退测试') else [])
def testUpgradeAndRollbackCpldVersion(testNum):
    isDownAgin = BASIC_DATA['version']['isDownAgain']
    with allure.step(key_get_time()+':压力测试：基站CPLD版本升级回退\n'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+'run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+' 次升级回退测试'):
                VersionManager(isDownAgain=isDownAgin, isRollCpld=True)
                
@allure.story("基站版本管理压力测试") 
@pytest.mark.基站版本升级回退_配置导出导入测试
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本升级回退_配置导出导入测试'] if RUN_TESTCASE.get('基站版本升级回退_配置导出导入测试') else [])
def testUpgradeAndRollbackVersionAndExportAndImportXml(testNum):
    isDownAgin = BASIC_DATA['version']['isDownAgain']
    with allure.step(key_get_time()+':压力测试：基站版本升级回退&&配置导出导入测试\n'):
        for i in range (1,testNum+1):
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次升级回退测试'):
                VersionManager(isDownAgain=isDownAgin, isRollCpld=False, isXmlTest=True)
        

'''
    单次基站升级回退测试
    step1:登录网管
    step2:查询目标版本包是否存在，不存在则从版本库中下载版本到网管上
    step3:下载版本，并确认版本下载成功
    step4:激活版本，并确认版本升级成功
    step5:查询升级后小区状态
'''
def VersionManager(isDownAgain=False, isRollCpld=False, isXmlTest=False):
    hmsObj = key_login_hms()
    softVersion = BASIC_DATA['version']['upgradeVersion']
    isCheckVerDetail = BASIC_DATA['VerDetail']['isCheckVerDetail']
    isCheckRollVerDetail = BASIC_DATA['VerDetail']['isCheckRollVerDetail']
    isCheckCell = BASIC_DATA['version']['isCheckCell']
    isAttach = BASIC_DATA['cpe']['isAttach']
    isPing = BASIC_DATA['cpe']['isPing']
    isFlow = BASIC_DATA['cpe']['isFlow']
    recoverVersion = BASIC_DATA['version']['recoverVersion']
    enbId, enbName = key_get_enb_info(hmsObj)
    gnb = key_ssh_login_gnb()
    verInfoDict = key_query_version_info(hmsObj)
    bakVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
    isExist = key_query_package_exist(hmsObj)
    if isExist == False:
        fileSize = key_download_gkg_to_local()
        key_upload_version_to_hms(hmsObj, fileSize)
    #打开基站log记录开关
    key_open_log_print_switch(gnb)
#         启动基站抓包
    key_capture_package_on_gnb(gnb, filePath='/')
    downRes = key_download_version(hmsObj)
    assert downRes == 'success', '版本下载执行失败，请检查！'
    downStatus = key_query_download_status(hmsObj, enbName)
    assert downStatus == 'success','基站版本下载失败，请检查！'
    key_query_version_info_from_device(hmsObj)
    activeRes = key_active_version(hmsObj)
    assert activeRes == 'success', '版本激活失败，请检查！'
    activeStatus = key_query_active_status(hmsObj, enbName)
    assert activeStatus == 'success','基站版本激活失败，请检查！'
    if activeStatus == 'activing':
        activeTimeoutScene(softVersion)
    with allure.step(key_get_time()+':版本激活成功，等待基站复位重启（3min）'):
        logging.info(key_get_time()+': active success, gnb will auto reboot, wait for 3min......')
        key_wait(180) #基站激活复位，等待3min
    key_confirm_device_online(hmsObj)
    with allure.step(key_get_time()+':确认版本升级成功，校验升级后版本号是否正确'):
        for activeNum in range (0, 10):
            key_query_version_info_from_device(hmsObj)
            verInfoDict = key_query_version_info(hmsObj)   
            curVersion = verInfoDict['rows'][0]['enbInfo']['softVersion']
            if curVersion == softVersion:
                break
            else:
                key_wait(5)
        assert curVersion == softVersion,'激活后基站版本校验失败，请检查！'
        if isCheckVerDetail == True:
            checkUpgradeVersionInfo(hmsObj)
    if isCheckCell:
        key_confirm_cell_status(hmsObj, enbId, 'available')
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
    assert rollStatus == 'success','回退任务失败，请检查！'
    if rollStatus == 'rollbacking':
        rollbackTimeoutScene(bakVersion)
    else:
        with allure.step(key_get_time()+':等待基站回退复位启动'):
            logging.info(key_get_time()+': rollback success, wait for gnb online')
            key_wait(180)
            key_confirm_device_online(hmsObj)
            if isCheckRollVerDetail == True:
                checkRollbackVersionInfo(hmsObj)
    if isDownAgain == True: 
        with allure.step(key_get_time()+':下载中间版本，恢复环境'):
            logging.warning(key_get_time()+': download other version')
            downRes = key_download_version(hmsObj, softVersion=recoverVersion)
            assert downRes == 'success', '版本下载执行失败，请检查！'
            downStatus = key_query_download_status(hmsObj, enbName)
            assert downStatus == 'success','基站版本下载失败，请检查！'
            key_query_version_info_from_device(hmsObj)
            key_query_version_info(hmsObj)
    if isRollCpld == True:
        #手工更新cpld版本
        gnb = key_ssh_login_gnb()
        key_upgrade_cpld_version(gnb, 'BS5514_MBb_mbcl_2021092701.jed', '/home', 'V2')
        with allure.step(key_get_time()+':cpld升级后基站复位，等待3分钟。'):
            key_wait(3*60)
        with allure.step(key_get_time()+':程控电源控制基站上电下电。'):
            aps7100 = key_login_aps7100()
            key_power_off_aps7100(aps7100)
            key_wait(60)
            key_power_on_aps7100(aps7100)
            with allure.step(key_get_time()+':电源上电，等待3分钟。'):
                key_wait(3*60)
            key_confirm_device_online(hmsObj)
            key_query_version_info_from_device(hmsObj)
            verInfoDict = key_query_version_info(hmsObj)
            curCpldVer = verInfoDict['rows'][0]['mu']['cpldVersion']
            if curCpldVer == '219271':
                logging.info(key_get_time()+': cpld manual rollback success!')
            else:
                logging.info(key_get_time()+': cpld manual rollback failure, current version:'+curCpldVer)
    if isXmlTest==True:
        exportAndImportXml(hmsObj)

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
        key_confirm_cell_status(hmsObj, enbId, 'available')          
            
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
            if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                    logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                break
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                    logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
            key_wait(10)
        assert checkWifiVer == curWifiVer and checkFpgaPlVer == checkFpgaPlVer and checkFpgaPsVer == checkFpgaPsVer and checkDPhyVer == checkDPhyVer and checkCPhyVer == checkCPhyVer and checkCpldVer == checkCpldVer,'小版本信息校验不通过，请检查！'
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
            if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                    logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                break
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                    logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
            key_wait(10)
        assert checkWifiVer == curWifiVer and checkFpgaPlVer == checkFpgaPlVer and checkFpgaPsVer == checkFpgaPsVer and checkDPhyVer == checkDPhyVer and checkCPhyVer == checkCPhyVer and checkCpldVer == checkCpldVer,'小版本信息校验不通过，请检查！'
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

@allure.story("基站版本管理异常测试")        
@pytest.mark.基站版本包下载过程中基站断链x秒
@pytest.mark.parametrize("testNum, waitTime",RUN_TESTCASE['基站版本包下载过程中基站断链x秒'] if RUN_TESTCASE.get('基站版本包下载过程中基站断链x秒') else [])
def testGnbOfflineDuringDownloadVersion(testNum, waitTime):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本下载过程中基站断链'+str(waitTime)+'s'):
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        gnb = key_ssh_login_gnb()
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+'run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    logging.info(key_get_time()+': download version to enb')
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
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    key_upload_version_to_hms_if_version_no_exit(hmsObj, softVersion2)
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
@pytest.mark.parametrize("testNum, waitTime, errorOmcIp",RUN_TESTCASE['基站版本包激活过程中基站断链x秒'] if RUN_TESTCASE.get('基站版本包激活过程中基站断链x秒') else [])
def testGnbOfflineDuringActiveVersion(testNum, waitTime, errorOmcIp):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本激活过程中基站断链'+str(waitTime)+'s'):
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        gnb = key_ssh_login_gnb()
        try:
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
                    #禁用dpdk0网卡
                    key_forbid_dpdk0(gnb)
                    key_wait(waitTime)
                    key_unforbid_dpdk0(gnb)
                    #等待激活任务完成
                    activeStatus = key_query_active_status(hmsObj, enbName)
                    assert activeStatus == 'activing','激活任务状态与预期不一致，请检查！'
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
        finally:
            with allure.step(key_get_time()+':运行异常'):
                logging.warning(key_get_time()+': process exec exception!')
                           
    
@allure.story("基站版本管理异常测试")
@pytest.mark.基站版本包激活过程中下载版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['基站版本包激活过程中下载版本'] if RUN_TESTCASE.get('基站版本包激活过程中下载版本') else [])
def testDownloadDuringActiveVersion(testNum):
    recoverVersion=BASIC_DATA['version']['recoverVersion']
    with allure.step('异常测试：基站版本包激活过程中下载版本'):
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
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
                    #回退版本包
                    rollRes = key_rollback_version(hmsObj)
                    assert rollRes == 'success','版本回退执行失败，请检查！'
                    #回退过程中执行版本下载
                    logging.info(key_get_time()+': during the rollbacking status, download version again')
                    downloadRes = key_download_version(hmsObj)
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
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
#                         key_login_hms()
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
                    logging.info(key_get_time()+': during the rollbacking status, rollback version again')
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
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                    key_upload_version_to_hms_if_version_no_exit(hmsObj)
                    downloadRes = key_download_version(hmsObj)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    #执行参数修改
                    key_block_cell(hmsObj, enbId)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId,'unavailable')
                    #版本下载状态查询
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载状态与预期不一致，请检查！'
                    with allure.step(key_get_time()+':基站版本及参数恢复'):
                        #执行参数修改
                        key_unblock_cell(hmsObj, enbId)
                        #确认参数修改生效
                        key_confirm_cell_status(hmsObj, enbId,'available')
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
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载状态与预期不一致，请检查！'
                    #执行参数修改
                    key_unblock_cell(hmsObj, enbId)
                    #确认参数修改生效
                    key_confirm_cell_status(hmsObj, enbId,'available')
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
                        key_confirm_cell_status(hmsObj, enbId,'unavailable')
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
                        key_confirm_cell_status(hmsObj, enbId,'available')
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
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
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
        abnormal = True
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
                    key_confirm_cell_status(hmsObj, enbId,'available')
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
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
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
        abnormal = True
        hmsObj = key_login_hms()
        enbId, enbName = key_get_enb_info(hmsObj)
        try:
            for i in range (1,testNum+1):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
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
                    key_confirm_cell_status(hmsObj, enbId,'available')
            abnormal = False
        finally:
            if abnormal == True:
                with allure.step('运行异常，恢复基站版本'):
                    logging.warning(key_get_time()+':run abnormal, recover gnb version and config')
                    downloadRes = key_download_version(hmsObj, softVersion=recoverVersion)
                    assert downloadRes == 'success','版本下载执行失败，请检查！'
                    downStatus = key_query_download_status(hmsObj, enbName)
                    assert downStatus == 'success','基站版本下载失败，请检查！'
                    key_query_version_info_from_device(hmsObj)
                    key_query_version_info(hmsObj)
    
        
if __name__ == "__main__":
#     pytest.main(['-s', '-vv', 'test_version.py'])
    print(key_get_time())