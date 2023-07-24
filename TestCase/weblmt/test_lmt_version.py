# coding = 'utf-8'
'''
Created on 2022年12月28日
@author: autotest
'''

import logging
import os
import threading

import allure
import pytest

from TestCase import globalPara
from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time
from UserKeywords.basic.basic import key_wait
from UserKeywords.basic.xmlManager import key_read_xml_root_value
from UserKeywords.gnb.gnbManager import key_ssh_login_gnb, \
    key_query_gps_md5_value, key_query_nrsys_version, key_upgrade_cpld_version, \
    key_gnb_copy_file, key_query_cpld_version_info, key_query_gnb_cpu_ratio
from UserKeywords.hms.VersionManager import key_download_gkg_to_local, \
    key_get_newest_version
from UserKeywords.pdn.pndManager import key_pdn_login
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_confirm_pdu_setup_succ, key_dl_udp_nr_flow_test, \
    key_dl_udp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_dl_tcp_nr_flow_test, \
    key_dl_tcp_wifi_flow_test, key_ul_tcp_nr_flow_test, \
    key_ul_tcp_wifi_flow_test, key_cpe_logout
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login, \
    key_weblmt_reboot_gnb
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_upload_version, \
    key_weblmt_query_upload_result, key_weblmt_active_version, \
    key_weblmt_query_version_info, key_weblmt_query_version_package_info
from UserKeywords.weblmt.WeblmtXmlManager import key_export_xml_file, \
    key_upload_xml_to_weblmt, key_import_xml_to_gnb


@pytest.mark.weblmt版本升级回退
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt版本升级回退'] if RUN_TESTCASE.get('weblmt版本升级回退') else [])
def testWeblmtUpgradeAndRollback(testNum):
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    rollbackVersion = BASIC_DATA['version']['recoverVersion']
    isCheckVerDetail = BASIC_DATA['VerDetail']['isCheckVerDetail']
    isAttach = BASIC_DATA['common']['isAttach']
    isPing = BASIC_DATA['common']['isPing']
    isFlow = BASIC_DATA['common']['isTraffic']
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    ueType = BASIC_DATA['common']['ueType']
    isRollback = BASIC_DATA['version']['isRollback']
    weblmt = key_weblmt_login()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    for i in range (1, testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                key_download_gkg_to_local(upgradeVersion)
            key_weblmt_upload_version(weblmt, upgradeVersion)
            key_weblmt_query_upload_result(weblmt, upgradeVersion)
            key_weblmt_active_version(weblmt, upgradeVersion)
            with allure.step(key_get_time()+':版本激活成功，等待基站复位重启'):
                logging.info(key_get_time()+':version active success, wait for gnb reboot')
                key_wait(5*60)
            if isCheckCell == True:
                cellRes = key_weblmt_confirm_cell_status(weblmt, cellId=1, expectStatus='available', tryNum=100)
                assert cellRes == True, '小区状态校验失败，请检查！'
            if isCheckVerDetail == True:
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
                        verInfoDict = key_weblmt_query_version_info(weblmt)
                        curWifiVer = verInfoDict['as8WifiVersion']
                        curFpgaPlVer = verInfoDict['as8FpgaPLVersion']
                        curFpgaPsVer = verInfoDict['as8FpgaPSVersion']
                        curDPhyVer = verInfoDict['as8PhyVspaVersion']
                        curCPhyVer = verInfoDict['as8PhyE200Version']
                        curCpldVer = verInfoDict['as8CpldVersion']
                        if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer:
                            with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                                logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                            break
                        else:
                            with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                                logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                        key_wait(5)
                    assert checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer,'小版本信息校验不通过，请检查！'
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
            if ueType == 'CPE':
                CellBusinessManagerCpe(isAttach, isPing, isFlow)
            if isRollback == True:
                weblmtRollbackVersion(weblmt, rollbackVersion, localPath, isRollCpld=False)
            else:
                break
            
@pytest.mark.weblmt最新分支版本升级
def testWeblmtUpgradeNewestVersion():
    isCheckCell = BASIC_DATA['common']['isCheckCell']
    weblmt = key_weblmt_login()
    curVersion, backPkg = key_weblmt_query_version_package_info(weblmt)
    #查询版本库中是否有最新版本
    newestVerNum = key_get_newest_version(curVersion)
    if newestVerNum != '':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
        localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
        if os.path.exists(localPath+'\\'+newestVerNum+'.zip')  == False:
            key_download_gkg_to_local(newestVerNum)
        key_weblmt_upload_version(weblmt, newestVerNum)
        key_weblmt_query_upload_result(weblmt, newestVerNum)
        key_weblmt_active_version(weblmt, newestVerNum)
        with allure.step(key_get_time()+':版本激活成功，等待基站复位重启'):
            logging.info(key_get_time()+':version active success, wait for gnb reboot')
            key_wait(5*60)
        if isCheckCell == True:
            cellRes = key_weblmt_confirm_cell_status(weblmt, cellId=1, expectStatus='available', tryNum=100)
            assert cellRes == True, '小区状态校验失败，请检查！'
        #设置版本升级状态
        globalPara.set_upgrade_status(True)
                
'''
weblmt版本回退
    参数：
    weblmt:weblmt对象
    rollbackVersion:回退版本号
    localPath:版本包存放目录
'''
def weblmtRollbackVersion(weblmt, rollbackVersion, localPath, isRollCpld=False):
    isCheckRollVerDetail = BASIC_DATA['VerDetail']['isCheckRollVerDetail']
    with allure.step(key_get_time()+':weblmt上回退版本包'):
        logging.info(key_get_time()+': rollback version on weblmt')
        if os.path.exists(localPath+'\\'+rollbackVersion+'.zip')  == False:
            key_download_gkg_to_local(rollbackVersion)
        key_weblmt_upload_version(weblmt, rollbackVersion)
        key_weblmt_query_upload_result(weblmt, rollbackVersion)
        key_weblmt_active_version(weblmt, rollbackVersion)
        with allure.step(key_get_time()+':版本激活成功，等待基站复位重启'):
            logging.info(key_get_time()+':version active success, wait for gnb reboot')
            key_wait(5*60)
    if isRollCpld == True:
        #手工更新cpld版本
        gnb = key_ssh_login_gnb()
        key_upgrade_cpld_version(gnb, 'BS5514_MBb_mbcl_2021092701.jed', '/home', 'V2')
        with allure.step(key_get_time()+':cpld升级后基站复位，等待3分钟。'):
            key_wait(5*60)
#         with allure.step(key_get_time()+':程控电源控制基站上电下电。'):
#             with allure.step(key_get_time()+':电源上电，等待3分钟。'):
#                 key_wait(5*60)
#             verInfoDict = key_weblmt_query_version_info(weblmt)
#             curCpldVer = verInfoDict['as8CpldVersion']
#             if curCpldVer == '219271':
#                 logging.info(key_get_time()+': cpld manual rollback success!')
#             else:
#                 logging.info(key_get_time()+': cpld manual rollback failure, current version:'+curCpldVer)
        gnb = key_ssh_login_gnb()
        key_query_cpld_version_info(gnb)
        key_gnb_copy_file(gnb, '/home/bootmisc.sh', '/etc/init.d/bootmisc.sh')
    if isCheckRollVerDetail == True:
        rollbackVersionCheck()

def rollbackVersionCheck():
    checkWifiVer = BASIC_DATA['VerDetail']['checkRollWifiVer']
    checkFpgaPlVer = BASIC_DATA['VerDetail']['checkRollFpgaPlVer']
    checkFpgaPsVer = BASIC_DATA['VerDetail']['checkRollFpgaPsVer']
    checkDPhyVer = BASIC_DATA['VerDetail']['checkRollDPhyVer']
    checkCPhyVer = BASIC_DATA['VerDetail']['checkRollCPhyVer']
    checkCpldVer = BASIC_DATA['VerDetail']['checkRollCpldVer']
    checkGpsVer = BASIC_DATA['VerDetail']['checkRollGpsVer']
    checkNrsysVer = BASIC_DATA['VerDetail']['checkRollNrsysVer']
    checkUbootVer = BASIC_DATA['VerDetail']['checkRollUbootVer']
                
    weblmt = key_weblmt_login()
    with allure.step(key_get_time()+':确认wifi等小版本信息是否正确'):
        for i in range(1,30):
            verInfoDict = key_weblmt_query_version_info(weblmt)
            curWifiVer = verInfoDict['as8WifiVersion']
            curFpgaPlVer = verInfoDict['as8FpgaPLVersion']
            curFpgaPsVer = verInfoDict['as8FpgaPSVersion']
            curDPhyVer = verInfoDict['as8PhyVspaVersion']
            curCPhyVer = verInfoDict['as8PhyE200Version']
            curCpldVer = verInfoDict['as8CpldVersion']
            if checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer:
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'):
                    logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/')
                break
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'):
                    logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/')
            key_wait(5)
        assert checkWifiVer == curWifiVer and checkFpgaPlVer == curFpgaPlVer and checkFpgaPsVer == curFpgaPsVer and checkDPhyVer == curDPhyVer and checkCPhyVer == curCPhyVer and checkCpldVer == curCpldVer,'小版本信息校验不通过，请检查！'
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
                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[gps/uboot]: '+curGpsVer+'/'+curNrsysVer):
                    logging.info(key_get_time()+': version detail check success, version info[gps/uboot]: '+curGpsVer+'/'+curUbootVer)
            else:
                with allure.step(key_get_time()+':小版本信息检查与预期不一致，版本详情[gps/uboot]: '+curGpsVer+'/'+curNrsysVer):
                    logging.warning(key_get_time()+': version detail check abnormal, version info[gps/uboot]: '+curGpsVer+'/'+curUbootVer)
                    assert curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer,'gps/uboot版本检查不通过，请检查！'
'''
      终端业务测试
    参数：
    isAttach:是否接入测试
    isPing:是否ping包测试
    isFlow:是否流量测试
'''
def CellBusinessManagerCpe(isAttach, isPing, isFlow):
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    if isAttach:
        with allure.step(key_get_time()+': 执行cpe业务测试'):
            logging.info(key_get_time()+': exec cpe business test')
            cpe = key_cpe_login()
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            assert setupRes == 'success', 'cpe接入失败，请检查！'
            if isPing == True:
                key_wait(5)
                key_cpe_ping(cpe, pingInterface = pingNrInterface)
                key_cpe_ping(cpe, pingInterface = pingwifiInterface)
            if isFlow:
                with allure.step(key_get_time()+': 小区流量测试'):
                    type = BASIC_DATA['traffic']['type']
                    dir = BASIC_DATA['traffic']['dir']
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

@pytest.mark.weblmt版本下载过程中查询cpu利用率
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt版本下载过程中查询cpu利用率'] if RUN_TESTCASE.get('weblmt版本下载过程中查询cpu利用率') else [])
def testWeblmtDownloadAndQueryCpuRatio(testNum):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    recoverVersion = BASIC_DATA['version']['recoverVersion']
    weblmt = key_weblmt_login()
    uploadAgain = False
    for i in range (1, testNum+1):
        logging.info(key_get_time()+':run the test <'+str(i)+'> times')
        with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
            if uploadAgain == False:
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local()
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                t1 = threading.Thread(target=key_query_gnb_cpu_ratio, args=(14, 30))
                t2 = threading.Thread(target=key_weblmt_query_upload_result, args=(weblmt, upgradeVersion))
                uploadAgain = True
            else:
                if os.path.exists(localPath+'\\'+recoverVersion+'.zip') == False:
                    key_download_gkg_to_local()
                key_weblmt_upload_version(weblmt, recoverVersion, localPath)
                t1 = threading.Thread(target=key_query_gnb_cpu_ratio, args=(14, 30))
                t2 = threading.Thread(target=key_weblmt_query_upload_result, args=(weblmt, recoverVersion))
                uploadAgain = False
            t2.start()
            t1.start()
            
            t2.join()
            t1.join()
            
            #版本包多次上传会失败，复位基站初始化
            key_weblmt_reboot_gnb(weblmt)
            with allure.step('等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(240)

@allure.story("基站版本管理异常测试")
@pytest.mark.weblmt导入xml时weblmt激活版本
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt导入xml时weblmt激活版本'] if RUN_TESTCASE.get('weblmt导入xml时weblmt激活版本') else [])
def testActiveVerDuringWeblmtImpXml(testNum):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：weblmt导入xml时weblmt激活版本'):
        for i in range (1,testNum+1):
            weblmt = key_weblmt_login()
            logging.info(key_get_time()+':run the test <'+str(i)+'> times')
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                #------------------weblmt xml------------------
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #------------------weblmt version------------------
                #检查地址是否保存升级版本包
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local()
                #weblmt上传版本
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                key_weblmt_query_upload_result(weblmt, upgradeVersion)
                #执行数据同步
                importRes = key_import_xml_to_gnb(weblmt, staType=staType)
                assert importRes == 'success','weblmt执行数据同步失败,请检查!' 
                key_wait(5)
                #weblmt激活版本
                activeRes = key_weblmt_active_version(weblmt, upgradeVersion)  
                assert activeRes == False, 'weblmt上激活版本包状态与预期不一致，请检查！'
                
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(300)

@allure.story("基站版本管理异常测试")
@pytest.mark.weblmt激活时weblmt导入xml
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt激活时weblmt导入xml'] if RUN_TESTCASE.get('weblmt激活时weblmt导入xml') else [])
def testWeblmtImpXmlDuringActiveVer(testNum):
#     localPath= BASIC_DATA['version']['versionSavePath']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    upgradeVersion = BASIC_DATA['version']['upgradeVersion']
    upgradeVersion2 = BASIC_DATA['version']['upgradeVersion2']
    xmlFileName='BntCfgFile'
    with allure.step('异常测试：weblmt激活时weblmt导入xml'):
        for i in range (1,testNum+1):
            with allure.step(key_get_time()+':执行第 '+str(i)+'次测试'):
                logging.info(key_get_time()+':run the test <'+str(i)+'> times')
                #------------------weblmt xml------------------
                weblmt = key_weblmt_login()
                #下载xml文件到本地
                fileSize = key_export_xml_file(weblmt)
                assert fileSize != 0,'配置文件导出失败，请检查！'
                versionName = key_read_xml_root_value('version', xmlFileName)
                staType = versionName.split('_')[0]
                #上传xml文件到网管
                uploadRes =key_upload_xml_to_weblmt(weblmt)
                assert uploadRes == 'yes','配置数据上传失败，请检查！'
                #------------------weblmt version------------------
                #检查地址是否保存升级版本包
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local()
                #weblmt上传版本
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                key_weblmt_query_upload_result(weblmt, upgradeVersion)
                #weblmt激活版本
                activeRes = key_weblmt_active_version(weblmt, upgradeVersion)  
#                 assert activeRes == True, 'weblmt上激活版本包状态与预期不一致，请检查！'
                key_wait(5)
                #执行数据同步
                importRes = key_import_xml_to_gnb(weblmt, staType=staType)
                assert importRes != 'success','weblmt执行数据同步失败,请检查!' 
                with allure.step(key_get_time()+':等待基站复位启动'):
                    logging.info(key_get_time()+': wait for gnb online')
                    key_wait(300)
                with allure.step(key_get_time()+':回退基站版本'):
                    weblmt = key_weblmt_login()
                    logging.info(key_get_time()+': rollback gnb version')
                    #检查地址是否保存升级版本包
                    if os.path.exists(localPath+'\\'+upgradeVersion2+'.zip') == False:
                        key_download_gkg_to_local()
                    #weblmt上传版本
                    key_weblmt_upload_version(weblmt, upgradeVersion2, localPath)
                    key_weblmt_query_upload_result(weblmt, upgradeVersion2)
                    #weblmt激活版本
                    key_weblmt_active_version(weblmt, upgradeVersion2)  
                    with allure.step(key_get_time()+':等待基站复位启动'):
                        logging.info(key_get_time()+': wait for gnb online')
                        key_wait(300)
                    weblmt = key_weblmt_login()
                    key_weblmt_reboot_gnb(weblmt)
                    key_wait(300)