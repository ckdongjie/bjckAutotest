# coding = 'utf-8'
'''
Created on 2022年12月28日

@author: autotest
'''

import logging
import os

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time
from UserKeywords.basic.basic import key_wait
from UserKeywords.gnb.gnbManager import key_ssh_login_gnb, \
    key_query_gps_md5_value, key_query_nrsys_version
from UserKeywords.hms.VersionManager import key_download_gkg_to_local
from UserKeywords.pdn.pndManager import key_pdn_login
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_cpe_attach, key_confirm_pdu_setup_succ, key_dl_udp_nr_flow_test, \
    key_dl_udp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_ul_udp_wifi_flow_test, key_dl_tcp_nr_flow_test, \
    key_dl_tcp_wifi_flow_test, key_ul_tcp_nr_flow_test, \
    key_ul_tcp_wifi_flow_test, key_cpe_logout
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login
from UserKeywords.weblmt.WeblmtVersionManager import key_weblmt_upload_version, \
    key_weblmt_query_upload_result, key_weblmt_active_version, \
    key_weblmt_query_version_info


@allure.feature("weblmt版本管理")
@allure.story("weblmt基站相关测试用例：基站升级回退")
class TestWeblmtGnb():
    
    @pytest.mark.weblmt版本升级回退
    @pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt版本升级回退'] if RUN_TESTCASE.get('weblmt版本升级回退') else [])
    def testWeblmtUpgradeAndRollback(self, testNum, weblmtIp=BASIC_DATA['weblmt']['ip'], cellId=0, cpePcIp=BASIC_DATA['flow']['cpePcIp'], pdnIp=BASIC_DATA['pdn']['pdnIp'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], ping_interface=BASIC_DATA['cpe']['pingNrInterface'], log_save_path=BASIC_DATA['ping']['logSavePath']):
        upgradeVersion = BASIC_DATA['version']['upgradeVersion']
        rollbackVersion = BASIC_DATA['version']['recoverVersion']
        localPath = BASIC_DATA['version']['versionSavePath']
        isCheckVerDetail = BASIC_DATA['VerDetail']['isCheckVerDetail']
        isAttach = BASIC_DATA['cpe']['isAttach']
        isPing = BASIC_DATA['cpe']['isPing']
        isFlow = BASIC_DATA['cpe']['isFlow']
        isCheckCell = BASIC_DATA['version']['isCheckCell']
        gnbSshIp = BASIC_DATA['weblmt']['ip']
        gnbSshUser = BASIC_DATA['gnb']['username']
        gnbSshPass = BASIC_DATA['gnb']['password']
        weblmt = key_weblmt_login(weblmtIp)
        
        for i in range (1, testNum+1):
            logging.info(key_get_time()+':run the test '+str(i)+' times')
            with allure.step(key_get_time()+'执行第 '+str(i)+'次测试'):
                if os.path.exists(localPath+'\\'+upgradeVersion+'.zip') == False:
                    key_download_gkg_to_local(upgradeVersion, localPath)
                key_weblmt_upload_version(weblmt, upgradeVersion, localPath)
                key_weblmt_query_upload_result(weblmt, upgradeVersion)
                key_weblmt_active_version(weblmt, upgradeVersion)
                with allure.step(key_get_time()+':版本激活成功，等待基站复位重启'):
                    logging.info(key_get_time()+':version active success, wait for gnb reboot')
                    key_wait(300)
                if isCheckCell == True:
                    cellRes = key_weblmt_confirm_cell_status(weblmt, cellId=0, expectStatus='available')
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
                            if checkWifiVer == curWifiVer and checkFpgaPlVer == checkFpgaPlVer and checkFpgaPsVer == checkFpgaPsVer and checkDPhyVer == checkDPhyVer and checkCPhyVer == checkCPhyVer and checkCpldVer == checkCpldVer:
                                with allure.step(key_get_time()+':小版本信息检查正确，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                                    logging.info(key_get_time()+': version detail check success, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                                break
                            else:
                                with allure.step(key_get_time()+':小版本信息检查与预期不一致，等待10s后再次查询，版本详情[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer):
                                    logging.warning(key_get_time()+': version detail check abnormal, wait for 10s, version info[wifi/fpgapl/fpgaps/dphy/cphy/cpld]: '+curWifiVer+'/'+curFpgaPlVer+'/'+curFpgaPsVer+'/'+curDPhyVer+'/'+curCPhyVer+'/'+curCpldVer)
                            key_wait(10)
#                         #assert checkWifiVer == curWifiVer and checkFpgaPlVer == checkFpgaPlVer and checkFpgaPsVer == checkFpgaPsVer and checkDPhyVer == checkDPhyVer and checkCPhyVer == checkCPhyVer and checkCpldVer == checkCpldVer,'小版本信息校验不通过，请检查！'
                        gnb = key_ssh_login_gnb(gnbSshIp, gnbSshUser, gnbSshPass)
                        curGpsVer = key_query_gps_md5_value(gnb)
                        curUbootVer, curNrsysVer = key_query_nrsys_version(gnb)
                        if curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer:
                            with allure.step(key_get_time()+':小版本信息检查正确，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                                logging.info(key_get_time()+': version detail check success, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
                        else:
                            with allure.step(key_get_time()+':小版本信息检查与预期不一致，版本详情[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer):
                                logging.warning(key_get_time()+': version detail check abnormal, version info[gps/nrsys]: '+curGpsVer+'/'+curNrsysVer)
#                         #assert curGpsVer == checkGpsVer and curNrsysVer == checkNrsysVer,'gps/nrsys版本检查不通过，请检查！'
                self.CellBusinessManager(isAttach, isPing, isFlow)
                self.weblmtRollbackVersion(weblmt, rollbackVersion, localPath)
    
    '''
    weblmt版本回退
        参数：
        weblmt:weblmt对象
        rollbackVersion:回退版本号
        localPath:版本包存放目录
    '''
    def weblmtRollbackVersion(self, weblmt, rollbackVersion, localPath):
        with allure.step(key_get_time()+':weblmt上回退版本包'):
            logging.info(key_get_time()+': rollback version on weblmt')
            if os.path.exists(localPath+'\\'+rollbackVersion+'.zip')  == False:
                key_download_gkg_to_local(rollbackVersion, localPath)
            key_weblmt_upload_version(weblmt, rollbackVersion, localPath)
            key_weblmt_query_upload_result(weblmt, rollbackVersion)
            key_weblmt_active_version(weblmt, rollbackVersion)
            with allure.step(key_get_time()+':版本激活成功，等待基站复位重启'):
                logging.info(key_get_time()+':version active success, wait for gnb reboot')
                key_wait(300)
    '''
          终端业务测试
        参数：
        isAttach:是否接入测试
        isPing:是否ping包测试
        isFlow:是否流量测试
    '''
    def CellBusinessManager(self, isAttach, isPing, isFlow):
        cpeIp = BASIC_DATA['cpe']['cpeSshIp']
        cpeUser = BASIC_DATA['cpe']['cpeUsername']
        cpePass = BASIC_DATA['cpe']['cpePassword']
        pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
        pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
        pdnIp = BASIC_DATA['pdn']['pdnIp']
        if isAttach:
            with allure.step(key_get_time()+': 执行cpe业务测试'):
                logging.warning(key_get_time()+': exec cpe business test')
                cpe = key_cpe_login(cpeIp, cpeUser, cpePass)
                attachRes = key_cpe_attach(cpe)
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if attachRes == 'OK':
                    if setupRes == 'success':
                        with allure.step(key_get_time()+': cpe接入成功'):
                            logging.warning(key_get_time()+': cpe attach sussess')
                    else:
                        with allure.step(key_get_time()+': cpe接入失败'):
                            logging.warning(key_get_time()+': cpe attach failure')
                    #assert setupRes == 'success','cpe接入失败，请检查！'
                    if isPing == True:
                        key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
                        key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingwifiInterface)
                    if isFlow:
                        with allure.step(key_get_time()+': 小区流量测试'):
                            logging.warning(key_get_time()+': start cell flow test.')
                            cpePcIp = BASIC_DATA['flow']['cpePcIp']
                            iperfPath = BASIC_DATA['flow']['iperfLocalPath']
                            pdnIp = BASIC_DATA['pdn']['pdnIp']
                            enbDebugIp = BASIC_DATA['weblmt']['ip']
                            pcIp = BASIC_DATA['flow']['localPcIp']
                            pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
                            pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
                            pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
                            nrPort = BASIC_DATA['flow']['nrPort']
                            wifiPort = BASIC_DATA['flow']['wifiPort']
                            spanTime = BASIC_DATA['flow']['spanTime']
                            type = BASIC_DATA['flow']['type']
                            dir = BASIC_DATA['flow']['dir']
                            pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
                            logging.warning(key_get_time()+': ue flow test')
                            if type == 'UDP':
                                if dir == 'DL':
                                    key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_dl_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                elif dir == 'UL':
                                    key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_ul_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                else:
                                    key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_dl_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                    key_wait(30)
                                    key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_ul_udp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                            if type == 'TCP':
                                if dir == 'DL':
                                    key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_dl_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                elif dir == 'UL':
                                    key_ul_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_ul_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                else:
                                    key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_dl_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)
                                    key_wait(30)
                                    key_ul_tcp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
                                    key_wait(20)
                                    key_ul_tcp_wifi_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=wifiPort, spanTime=spanTime)  
                key_cpe_logout(cpe)
