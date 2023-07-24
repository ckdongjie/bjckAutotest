# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''

import logging
import os

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_wait, key_get_time
from UserKeywords.hms.CellManager import key_confirm_cell_status
from UserKeywords.hms.DeviceManager import key_modiry_device_auto_test_mode
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info
from UserKeywords.hms.SctpManager import key_modify_ipv6_sctp_config
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login, \
    key_confirm_pdu_setup_succ, key_local_pc_ping
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login, key_weblmt_reboot_gnb, key_weblmt_logout, \
    key_weblmt_gnb_info, key_weblmt_clock_cfg, key_weblmt_get_operator_info, key_weblmt_operator_cfg, key_weblmt_export_wifi_log, \
    key_weblmt_export_device_log, key_weblmt_export_chr_log, key_weblmt_export_black_box_log, key_weblmt_test_mode_activated, \
    key_weblmt_ip_enable_switch, key_weblmt_get_ip_address


@pytest.mark.weblmt复位基站正常后ping包
@pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt复位基站正常后ping包'] if RUN_TESTCASE.get('weblmt复位基站正常后ping包') else [])
def testWeblmtRebootGnbAndPing(testNum):
    cellIdList=BASIC_DATA['gnb']['cellIdList']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    pingwifiInterface = BASIC_DATA['cpe']['pingWifiInterface']
    weblmt = key_weblmt_login()
    cpe = key_cpe_login()
    for i in range (testNum):
        logging.info(key_get_time()+': run the test <'+str(i+1)+'> times')
        with allure.step(key_get_time()+'执行第 <'+str(i+1)+'>次测试'):
            key_weblmt_reboot_gnb(weblmt)
            with allure.step('等待基站复位启动'):
                logging.info(key_get_time()+': reboot success, wait for gnb online......')
                key_wait(180)
            for cellId in cellIdList:
                confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
                assert confirmRes == True, '小区状态与预期不一致，请检查！'
            for i in range (0, 10):
                setupRes = key_confirm_pdu_setup_succ(cpe)
                if setupRes == 'success':
                    break
            assert setupRes == 'success','cpe接入失败，请检查！'
            key_wait(5)
            key_cpe_ping(cpe, pingInterface = pingNrInterface)
            key_cpe_ping(cpe, pingInterface = pingwifiInterface)
            key_local_pc_ping(cpe)

@pytest.mark.weblmt登出
def testWeblmtLogOut():
    # 获得WEBMT对象
    weblmt = key_weblmt_login()
    allure.step(key_get_time() + ":weblmt登出")
    logging.warning(key_get_time() + ':weblmt登出')
    key_weblmt_logout(weblmt)

@pytest.mark.weblmt基站信息查看
def testWeblmtGnbInformation():
    # 获得WEBMT对象
    weblmt = key_weblmt_login()
    with allure.step(key_get_time() + ":weblmt获取基站信息"):
        logging.info(key_get_time() + ':weblmt获取基站信息')
        # 获取基站信息
        gnbInfo = key_weblmt_gnb_info(weblmt)
        if gnbInfo == False:
            return
        # 基站信息打印
        if gnbInfo['u8BntStatus'] == 0:
            res = "normal"
        else:
            res = "abnormal"
    with allure.step('Dynamic Query->Query Board Status->基站状态\\产品类型\\产品型号\\基站SN号\\WIFI型号\\FPGA-PL型号\\FPGA-PS型号\\D-PHY型号\\C-PHY型号:'
                     +res+'\\'+gnbInfo['as8PdType']+'\\'+gnbInfo['as8PdModelId']+'\\'+gnbInfo['au8BntSeqNo']+'\\'+gnbInfo['as8WifiVersion']
                     +'\\'+gnbInfo['as8FpgaPLVersion']+'\\'+gnbInfo['as8FpgaPLVersion']+'\\'+gnbInfo['as8FpgaPSVersion']
                     +'\\'+gnbInfo['as8PhyVspaVersion']+'\\'+gnbInfo['as8PhyE200Version']):
        logging.info("Dynamic Query->Query Board Status->基站状态: " + res)
        logging.info("Dynamic Query->Query Board Status->产品类型: " + gnbInfo['as8PdType'])
        logging.info("Dynamic Query->Query Board Status->产品型号: " + gnbInfo['as8PdModelId'])
        logging.info("Dynamic Query->Query Board Status->基站SN号: " + gnbInfo['au8BntSeqNo'])
        logging.info("Dynamic Query->Query Board Status->WIFI型号: " + gnbInfo['as8WifiVersion'])
        logging.info("Dynamic Query->Query Board Status->FPGA-PL型号: " + gnbInfo['as8FpgaPLVersion'])
        logging.info("Dynamic Query->Query Board Status->FPGA-PS型号: " + gnbInfo['as8FpgaPSVersion'])
        logging.info("Dynamic Query->Query Board Status->D-PHY型号: " + gnbInfo['as8PhyVspaVersion'])
        logging.info("Dynamic Query->Query Board Status->C-PHY型号: " + gnbInfo['as8PhyE200Version'])
    if gnbInfo['u32ClkClockStatus'] == 0:
        res = "自由震荡"
    elif gnbInfo['u32ClkClockStatus'] == 1:
        res = "快捕"
    elif gnbInfo['u32ClkClockStatus'] == 2:
        res = "锁定"
    elif gnbInfo['u32ClkClockStatus'] == 3:
        res = "保持"
    elif gnbInfo['u32ClkClockStatus'] == 4:
        res = "失锁"
    with allure.step("Dynamic Query->Query Board Status->时钟状态: "+ res):  
        logging.info("Dynamic Query->Query Board Status->时钟状态: " + res)
    with allure.step("Dynamic Query->Query Board Status->运行时间长度: %d hours %d minutes %d seconds" % (
        int(gnbInfo['u32Uptime'] / 3600), int(gnbInfo['u32Uptime'] % 3600 / 60), gnbInfo['u32Uptime'] % 60)):  
        logging.info("Dynamic Query->Query Board Status->运行时间长度: %d hours %d minutes %d seconds" % (
        int(gnbInfo['u32Uptime'] / 3600), int(gnbInfo['u32Uptime'] % 3600 / 60), gnbInfo['u32Uptime'] % 60))
    with allure.step("Dynamic Query->Query Board Status->经纬度: （%f, %f）" % (
    gnbInfo['s32GpsLockedLatitude'] / 1000000, gnbInfo['s32GpsLockedLongitude'] / 1000000)):
        logging.info("Dynamic Query->Query Board Status->经纬度: （%f, %f）" % (
        gnbInfo['s32GpsLockedLatitude'] / 1000000, gnbInfo['s32GpsLockedLongitude'] / 1000000))
    with allure.step("Dynamic Query->Query Board Status->卫星数: " + str(gnbInfo['u32GpsNumberOfSatellites'])):
        logging.info("Dynamic Query->Query Board Status->卫星数: " + str(gnbInfo['u32GpsNumberOfSatellites']))
    with allure.step("Dynamic Query->Query Board Status->高度: %.1f 米" % (gnbInfo['s32GpsElevation'] / 1000.0)):
        logging.info("Dynamic Query->Query Board Status->高度: %.1f 米" % (gnbInfo['s32GpsElevation'] / 1000.0))
    if gnbInfo['u32GpsScanStatus'] == 0:
        res = "Indeterminate"
    elif gnbInfo['u32GpsScanStatus'] == 1:
        res = "InProgress"
    elif gnbInfo['u32GpsScanStatus'] == 2:
        res = "Success"
    elif gnbInfo['u32GpsScanStatus'] == 3:
        res = "Error"
    elif gnbInfo['u32GpsScanStatus'] == 4:
        res = "Error_TIMEOUT"
    with allure.step("Dynamic Query->Query Board Status->GPS同步状态: " + res):
        logging.info("Dynamic Query->Query Board Status->GPS同步状态: " + res)

@pytest.mark.weblmt时钟源配置
def testWeblmtClockSrcCfg():
    ping_interface=BASIC_DATA['cpe']['pingNrInterface']
    cellIdList=BASIC_DATA['gnb']['cellIdList']
    weblmt = key_weblmt_login()
    cpe = key_cpe_login()
    with allure.step(key_get_time() + ":时钟源设置为:本地时钟"):
        logging.info(key_get_time() + ":时钟源设置为:本地时钟")
        # 修改时钟源0:GPS  1:本地时钟
        resInfo = key_weblmt_clock_cfg(weblmt, 1)
        if resInfo == False:
            return
    with allure.step(key_get_time() + ":小区状态检查"):
        logging.info(key_get_time() + ':小区状态检查')
        for cellId in cellIdList:
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'
        key_cpe_ping(cpe, pingInterface=ping_interface)
    with allure.step(key_get_time() + ":时钟源设置为:GPS"):
        logging.info(key_get_time() + ":时钟源设置为:GPS")
        # 修改时钟源0:GPS  1:本地时钟
        resInfo = key_weblmt_clock_cfg(weblmt, 0)
        if resInfo == False:
            return
    with allure.step(key_get_time() + ":小区状态检查"):
        logging.info(key_get_time() + ':小区状态检查')
        for cellId in cellIdList:
            confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
            assert confirmRes == True, '小区状态与预期不一致，请检查！'
        key_cpe_ping(cpe, pingInterface=ping_interface)

@pytest.mark.weblmt获取运营商信息
def testWeblmtGetOperatorInfo():
    weblmt = key_weblmt_login()
    with allure.step(key_get_time() + ":获取运营商信息"):
        logging.info(key_get_time() + ':获取运营商信息')
        resInfo = key_weblmt_get_operator_info(weblmt)
        if resInfo == False:
            return
        with allure.step(key_get_time()+": OperatorName\\Mcc\\Mnc:"+resInfo['data'][0]['OperatorName']+"\\"+resInfo['data'][0]['Mcc']+"\\"+resInfo['data'][0]['Mnc']):
            logging.info(key_get_time() + ":OperatorName : " + resInfo['data'][0]['OperatorName'])
            logging.info(key_get_time() + ":Mcc : " + resInfo['data'][0]['Mcc'])
            logging.info(key_get_time() + ":Mnc : " + resInfo['data'][0]['Mnc'])

@pytest.mark.weblmt运营商配置
@pytest.mark.parametrize("mcc, mnc", RUN_TESTCASE['weblmt运营商配置'] if RUN_TESTCASE.get('weblmt运营商配置') else [])
def testWeblmtOperatorCfg(mcc, mnc):
    weblmt = key_weblmt_login()
    with allure.step(key_get_time() + ":Weblmt PLMN配置，配置值："+str(mcc)+'--'+str(mnc)):
        logging.info(key_get_time() + ':Weblmt PLMN设置：'+str(mcc)+'--'+str(mnc))
        resInfo = key_weblmt_operator_cfg(weblmt, mcc, mnc)
        if resInfo == False:
            return
        # 配置完成后重启基站
        with allure.step(key_get_time() + ": 设置完成后重启基站"):
            logging.info(key_get_time() +": set plmn success and reboot gnb")
            testWeblmtRebootGnbAndPing(1)

@pytest.mark.weblmt导出基站log
def testWeblmtExportLog():
    weblmt = key_weblmt_login()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    logPath = BASE_DIR+'\\AutoTestMain\\lmtLog'
    with allure.step(key_get_time() + ":weblmt导出WIFI log"):
        logging.info(key_get_time() + ':weblmt导出WIFI log')
        resInfo = key_weblmt_export_wifi_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
    with allure.step(key_get_time() + ":weblmt导出基站log"):
        logging.info(key_get_time() + ':weblmt导出基站log')
        resInfo = key_weblmt_export_device_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
    with allure.step(key_get_time() + ":weblmt导出CHR log"):
        logging.info(key_get_time() + ':weblmt导出CHR log')
        resInfo = key_weblmt_export_chr_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
    with allure.step(key_get_time() + ":weblmt导出黑匣子log"):
        logging.info(key_get_time() + ':weblmt导出黑匣子log')
        key_weblmt_export_black_box_log(weblmt, logPath)

@pytest.mark.weblmt自测模式
def testWeblmtTestMode():
    hmsObj = key_login_hms()
    enbId, enbName = key_get_enb_info(hmsObj)
    weblmt = key_weblmt_login()
    with allure.step(key_get_time() + ":OMC基站自测模式关闭时，weblmt执行自测模式激活操作："):
        logging.info(key_get_time() + ':gnb self-test model is close, active self-test model by weblmt')
        with allure.step(key_get_time() + ":OMC关闭基站自测模式"):
            logging.info(key_get_time() + ':OMC关闭基站自测模式')
            res = key_modiry_device_auto_test_mode(hmsObj, 0)
            assert res != False, 'OMC关闭基站自测模式失败，请检查！' 
            with allure.step(key_get_time() + ":weblmt激活自测模式"):
                logging.info(key_get_time() + ':weblmt激活自测模式')
                # 1：激活自测模式，0：停止自测模式
                resInfo = key_weblmt_test_mode_activated(weblmt, 1)
                assert resInfo['result']==0, "weblmt激活自测模结果与预期不一致，请检查！"
    with allure.step(key_get_time() + ":OMC基站自测模式打开时，weblmt执行自测模式激活操作："):
        logging.info(key_get_time() + ':gnb self-test model is open, active self-test model by weblmt')
        with allure.step(key_get_time() + ":OMC打开基站自测模式"):
            logging.info(key_get_time() + ':OMC打开基站自测模式')
            res = key_modiry_device_auto_test_mode(hmsObj, 1)
            assert res != False, 'OMC打开基站自测模式失败，请检查！' 
        with allure.step(key_get_time()+":修改sctp目标ip地址，触发ngap异常"):
            logging.info(key_get_time()+": modify sctp desIp, ngap abnormal")
            key_modify_ipv6_sctp_config(hmsObj, enbId, {'primaryPeerAddress':'193:168:6::145'})
            key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
        with allure.step(key_get_time() + ":weblmt激活自测模式"):
            logging.warning(key_get_time() + ':weblmt激活自测模式')
            # 1：激活自测模式，0：停止自测模式
            resInfo = key_weblmt_test_mode_activated(weblmt, 1)
            assert resInfo['result']==1,"weblmt激活自测模结果与预期不一致，请检查！"
            key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
        with allure.step(key_get_time() + ":weblmt停止自测模式"):
            logging.warning(key_get_time() + ':weblmt停止自测模式')
            # 1：激活自测模式，0：停止自测模式
            resInfo = key_weblmt_test_mode_activated(weblmt, 0)
        with allure.step(key_get_time() + ":OMC关闭基站自测模式"):
            logging.warning(key_get_time() + ':OMC关闭基站自测模式')
            res = key_modiry_device_auto_test_mode(hmsObj, 0)
            assert res != False, 'OMC关闭基站自测模式失败，请检查！' 
            with allure.step(key_get_time()+": 基站自测模式关闭后复位基站，初始化传输参数"):
                logging.info(key_get_time()+": reboot gnb and setup transport paras when close gnb self-test model")
                key_weblmt_reboot_gnb(weblmt)
                key_wait(3*60)
            key_confirm_cell_status(hmsObj, enbId, expectStatus='unavailable')
            with allure.step(key_get_time()+":修改sctp目标ip地址，恢复ngap状态"):
                logging.info(key_get_time()+": modify sctp desIp, recovery ngap status")
                key_modify_ipv6_sctp_config(hmsObj, enbId, {'primaryPeerAddress':'193:168:6::14'})
                key_confirm_cell_status(hmsObj, enbId, expectStatus='available')
        
@pytest.mark.weblmt查看IP地址信息
@pytest.mark.parametrize("ipMode", RUN_TESTCASE['weblmt查看IP地址信息'] if RUN_TESTCASE.get('weblmt查看IP地址信息') else [])
def testWeblmtIpAddressInfo(ipMode):
    weblmt = key_weblmt_login()
    with allure.step(key_get_time() + ":enable %s switch" % ("IPV4" if ipMode == 0 else "IPV6")):
        logging.info(key_get_time() + ":enable %s switch" % ("IPV4" if ipMode == 0 else "IPV6"))
        # 0:IPV4, 1:IPV6
        resInfo = key_weblmt_ip_enable_switch(weblmt, ipMode)
        if resInfo == False:
            return
    with allure.step(key_get_time() + ":get %s address" % ("IPV4" if ipMode == 0 else "IPV6")):
        logging.info(key_get_time() + ":get %s address" % ("IPV4" if ipMode == 0 else "IPV6"))
        # 获取IP地址，0：IPV4， 1：IPV6
        resInfo = key_weblmt_get_ip_address(weblmt, ipMode)
        if resInfo == False:
            return
    with allure.step(key_get_time()+": 基站ip地址信息："+resInfo['data'][0]['IPAddress']):
        logging.info(key_get_time() + ':IP address: ' + resInfo['data'][0]['IPAddress'])

if __name__ == "__main__":
    testWeblmtExportLog("E:\\autotestpath\\")