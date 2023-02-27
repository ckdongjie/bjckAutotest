# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
from UserKeywords.ue.CpeManager import key_cpe_ping

'''

import logging

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time
from UserKeywords.basic.basic import key_wait
from UserKeywords.ue.CpeManager import key_cpe_ping, key_cpe_login
from UserKeywords.weblmt.WeblmtCellManager import key_weblmt_confirm_cell_status
from UserKeywords.weblmt.WeblmtGnbManager import *
from UserKeywords.hms.HmsManager import key_login_hms
from UserKeywords.hms.DeviceManager import key_confirm_device_status_same_as_expect


@allure.feature("weblmt基站管理")
@allure.story("weblmt基站相关测试用例：基站复位")
class TestWeblmtGnb():
    
    @pytest.mark.weblmt复位基站正常后ping包
    @pytest.mark.parametrize("testNum",RUN_TESTCASE['weblmt复位基站正常后ping包'] if RUN_TESTCASE.get('weblmt复位基站正常后ping包') else [])
    def testWeblmtRebootGnbAndPing(self, testNum, weblmtIp=BASIC_DATA['weblmt']['ip'],cellId=0, cpePcIp=BASIC_DATA['flow']['cpePcIp'], pdnIp=BASIC_DATA['pdn']['pdnIp'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'], ping_interface=BASIC_DATA['cpe']['pingNrInterface'], log_save_path=BASIC_DATA['ping']['logSavePath']):
        weblmt = key_weblmt_login(weblmtIp)
        cpe = key_cpe_login(cpeIp)
        for i in range (testNum):
            logging.info(key_get_time()+':run the test '+str(i+1)+' times')
            with allure.step(key_get_time()+'执行第 '+str(i+1)+'次测试'):
                key_weblmt_reboot_gnb(weblmt)
                with allure.step('等待基站复位启动'):
                    logging.info(key_get_time()+': reboot success, wait for gnb online......')
                    key_wait(180)
                confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
                assert confirmRes == True, '小区状态与预期不一致，请检查！'
                key_cpe_ping(cpe, cpePcIp=cpePcIp, pdnIp=pdnIp, cpeIp=cpeIp, ping_interface=ping_interface, log_save_path=log_save_path)

    @pytest.mark.weblmt登出
    def testWeblmtLogOut(self, weblmtIp=BASIC_DATA['weblmt']['ip']):
        # 获得WEBMT对象
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":weblmt登出")
        logging.warning(key_get_time() + ':weblmt登出')
        key_weblmt_logout(weblmt)

    @pytest.mark.weblmt基站信息查看
    def testWeblmtGnbInformation(self, weblmtIp=BASIC_DATA['weblmt']['ip']):
        # 获得WEBMT对象
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":weblmt获取基站信息")
        logging.warning(key_get_time() + ':weblmt获取基站信息')
        # 获取基站信息
        gnbInfo = key_weblmt_gnb_info(weblmt)
        if gnbInfo == False:
            return
        # 基站信息打印
        if gnbInfo['u8BntStatus'] == 0:
            res = "normal"
        else:
            res = "abnormal"
        logging.warning("Dynamic Query->Query Board Status->基站状态: " + res)
        logging.warning("Dynamic Query->Query Board Status->产品类型: " + gnbInfo['as8PdType'])
        logging.warning("Dynamic Query->Query Board Status->产品型号: " + gnbInfo['as8PdModelId'])
        logging.warning("Dynamic Query->Query Board Status->基站SN号: " + gnbInfo['au8BntSeqNo'])
        logging.warning("Dynamic Query->Query Board Status->WIFI型号: " + gnbInfo['as8WifiVersion'])
        logging.warning("Dynamic Query->Query Board Status->FPGA-PL型号: " + gnbInfo['as8FpgaPLVersion'])
        logging.warning("Dynamic Query->Query Board Status->FPGA-PS型号: " + gnbInfo['as8FpgaPSVersion'])
        logging.warning("Dynamic Query->Query Board Status->D-PHY型号: " + gnbInfo['as8PhyVspaVersion'])
        logging.warning("Dynamic Query->Query Board Status->C-PHY型号: " + gnbInfo['as8PhyE200Version'])
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
        logging.warning("Dynamic Query->Query Board Status->时钟状态: " + res)
        logging.warning("Dynamic Query->Query Board Status->运行时间长度: %d hours %d minutes %d seconds" % (
        int(gnbInfo['u32Uptime'] / 3600), int(gnbInfo['u32Uptime'] % 3600 / 60), gnbInfo['u32Uptime'] % 60))
        logging.warning("Dynamic Query->Query Board Status->经纬度: （%f, %f）" % (
        gnbInfo['s32GpsLockedLatitude'] / 1000000, gnbInfo['s32GpsLockedLongitude'] / 1000000))
        logging.warning("Dynamic Query->Query Board Status->卫星数: " + str(gnbInfo['u32GpsNumberOfSatellites']))
        logging.warning("Dynamic Query->Query Board Status->高度: %.1f 米" % (gnbInfo['s32GpsElevation'] / 1000.0))
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
        logging.warning("Dynamic Query->Query Board Status->GPS同步状态: " + res)

    @pytest.mark.weblmt时钟源配置
    @pytest.mark.parametrize("clkSrc", RUN_TESTCASE['weblmt时钟源配置'] if RUN_TESTCASE.get('weblmt时钟源配置') else [])
    def testWeblmtClockSrcCfg(self, clkSrc, weblmtIp=BASIC_DATA['weblmt']['ip'], cellId=0, cpePcIp=BASIC_DATA['flow']['cpePcIp'],
                              pdnIp=BASIC_DATA['pdn']['pdnIp'], cpeIp=BASIC_DATA['cpe']['cpeSshIp'],
                              ping_interface=BASIC_DATA['cpe']['pingNrInterface'],
                              log_save_path=BASIC_DATA['ping']['logSavePath']):
        weblmt = key_weblmt_login(weblmtIp)
        cpe = key_cpe_login(cpeIp)
        allure.step(key_get_time() + ":时钟源设置为%s" % ("GPS" if clkSrc==0 else "本地时钟"))
        logging.warning(key_get_time() + ":时钟源设置为%s" % ("GPS" if clkSrc==0 else "本地时钟"))
        # 修改时钟源0:GPS  1:本地时钟
        resInfo = key_weblmt_clock_cfg(weblmt, clkSrc)
        if resInfo == False:
            return
        allure.step(key_get_time() + ":小区状态检查")
        logging.warning(key_get_time() + ':小区状态检查')
        confirmRes = key_weblmt_confirm_cell_status(weblmt, cellId, expectStatus='available')
        allure.step(key_get_time() + ":CPE ping业务")
        logging.warning(key_get_time() + ':CPE ping业务')
        key_cpe_ping(cpe, cpePcIp=cpePcIp, pdnIp=pdnIp, cpeIp=cpeIp, ping_interface=ping_interface,
                     log_save_path=log_save_path)

    @pytest.mark.weblmt获取运营商信息
    def testWeblmtGetOperatorInfo(self, weblmtIp=BASIC_DATA['weblmt']['ip']):
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":获取运营商信息")
        logging.warning(key_get_time() + ':获取运营商信息')
        resInfo = key_weblmt_get_operator_info(weblmt)
        if resInfo == False:
            return
        logging.warning(key_get_time() + ":OperatorName : " + resInfo['data'][0]['OperatorName'])
        logging.warning(key_get_time() + ":Mcc : " + resInfo['data'][0]['Mcc'])
        logging.warning(key_get_time() + ":Mnc : " + resInfo['data'][0]['Mnc'])

    @pytest.mark.weblmt运营商配置
    @pytest.mark.parametrize("mcc, mnc", RUN_TESTCASE['weblmt运营商配置'] if RUN_TESTCASE.get('weblmt运营商配置') else [])
    def testWeblmtOperatorCfg(self, mcc, mnc, weblmtIp=BASIC_DATA['weblmt']['ip']):
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":Weblmt PLMN配置")
        logging.warning(key_get_time() + ':Weblmt PLMN设置')
        resInfo = key_weblmt_operator_cfg(weblmt, mcc, mnc)
        if resInfo == False:
            return
        # 配置完成后重启基站
        allure.step(key_get_time() + ": 设置完成后重启基站")
        self.testWeblmtRebootGnbAndPing(1)

    @pytest.mark.weblmt导出基站log
    @pytest.mark.parametrize("logPath", RUN_TESTCASE['weblmt导出基站log'] if RUN_TESTCASE.get('weblmt导出基站log') else [])
    def testWeblmtExportLog(self, logPath, weblmtIp=BASIC_DATA['weblmt']['ip']):
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":weblmt导出WIFI log")
        logging.warning(key_get_time() + ':weblmt导出WIFI log')
        resInfo = key_weblmt_export_wifi_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
        allure.step(key_get_time() + ":weblmt导出基站log")
        logging.warning(key_get_time() + ':weblmt导出基站log')
        resInfo = key_weblmt_export_device_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
        allure.step(key_get_time() + ":weblmt导出CHR log")
        logging.warning(key_get_time() + ':weblmt导出CHR log')
        resInfo = key_weblmt_export_chr_log(weblmt, logPath)
        if resInfo == False:
            return
        key_wait(1)
        allure.step(key_get_time() + ":weblmt导出黑匣子log")
        logging.warning(key_get_time() + ':weblmt导出黑匣子log')
        key_weblmt_export_black_box_log(weblmt, logPath)

    @pytest.mark.weblmt自测模式
    @pytest.mark.parametrize("serialNumber", RUN_TESTCASE['weblmt自测模式'] if RUN_TESTCASE.get('weblmt自测模式') else [])
    def testWeblmtTestMode(self, serialNumber, weblmtIp=BASIC_DATA['weblmt']['ip']):
        hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
        allure.step(key_get_time() + ":OMC关闭基站自测模式")
        logging.warning(key_get_time() + ':OMC关闭基站自测模式')
        res = key_confirm_device_status_same_as_expect(hmsObj, serialNumber, 0)
        if res == False:
            return
        allure.step(key_get_time() + ":weblmt激活自测模式")
        logging.warning(key_get_time() + ':weblmt激活自测模式')
        weblmt = key_weblmt_login(weblmtIp)
        # 1：激活自测模式，0：停止自测模式
        resInfo = key_weblmt_test_mode_activated(weblmt, 1)
        if resInfo['result'] == 0:
            logging.warning(key_get_time() + ":weblmt active auto test mode fail")
        elif resInfo['result'] == 1:
            logging.warning(key_get_time() + ":weblmt active auto test mode success")

        allure.step(key_get_time() + ":OMC打开基站自测模式")
        logging.warning(key_get_time() + ':OMC打开基站自测模式')
        res = key_confirm_device_status_same_as_expect(hmsObj, serialNumber, 1)
        if res == False:
            return
        allure.step(key_get_time() + ":weblmt激活自测模式")
        logging.warning(key_get_time() + ':weblmt激活自测模式')
        # 1：激活自测模式，0：停止自测模式
        resInfo = key_weblmt_test_mode_activated(weblmt, 1)
        if resInfo['result'] == 0:
            logging.warning(key_get_time() + ":weblmt active auto test mode fail")
        elif resInfo['result'] == 1:
            logging.warning(key_get_time() + ":weblmt active auto test mode success")

        allure.step(key_get_time() + ":weblmt停止自测模式")
        logging.warning(key_get_time() + ':weblmt停止自测模式')
        # 1：激活自测模式，0：停止自测模式
        resInfo = key_weblmt_test_mode_activated(weblmt, 0)
        if resInfo['result'] == 0:
            logging.warning(key_get_time() + ":weblmt unactive auto test mode fail")
        elif resInfo['result'] == 1:
            logging.warning(key_get_time() + ":weblmt unactive auto test mode success")

    @pytest.mark.weblmt查看IP地址信息
    @pytest.mark.parametrize("ipMode", RUN_TESTCASE['weblmt查看IP地址信息'] if RUN_TESTCASE.get('weblmt查看IP地址信息') else [])
    def testWeblmtIpAddressInfo(self, ipMode, weblmtIp=BASIC_DATA['weblmt']['ip']):
        weblmt = key_weblmt_login(weblmtIp)
        allure.step(key_get_time() + ":enable %s switch" % ("IPV4" if ipMode == 0 else "IPV6"))
        logging.warning(key_get_time() + ":enable %s switch" % ("IPV4" if ipMode == 0 else "IPV6"))
        # 0:IPV4, 1:IPV6
        resInfo = key_weblmt_ip_enable_switch(weblmt, ipMode)
        if resInfo == False:
            return
        allure.step(key_get_time() + ":get %s address" % ("IPV4" if ipMode == 0 else "IPV6"))
        logging.warning(key_get_time() + ":get %s address" % ("IPV4" if ipMode == 0 else "IPV6"))
        # 获取IP地址，0：IPV4， 1：IPV6
        resInfo = key_weblmt_get_ip_address(weblmt, ipMode)
        if resInfo == False:
            return
        logging.warning(key_get_time() + ':IP address: ' + resInfo['data'][0]['IPAddress'])

if __name__ == "__main__":
    TestWeblmtGnb().testWeblmtExportLog("E:\\autotestpath\\")