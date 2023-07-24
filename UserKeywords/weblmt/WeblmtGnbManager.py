# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj

'''
'''
        说明：weblmt上复位基站
        参数：
    lmtObj:weblmt对象
'''

import logging

import allure
from TestCaseData.basicConfig import BASIC_DATA
from BasicModel.weblmt.weblmt import WebLmt
from BasicService.weblmt.lmtGnbService import LmtGnbService
from UserKeywords.basic.basic import key_get_time


def key_weblmt_reboot_gnb(lmtObj):
    with allure.step(key_get_time() +": weblmt上复位基站："+lmtObj.ip+'\n'):
        logging.info(key_get_time()+': weblmt reboot gnb: '+lmtObj.ip)
        rebootRes = LmtGnbService().lmtRebootGnb(lmtObj)
        assert rebootRes == True, 'weblmt复位基站操作失败，请检查！'

'''
        说明：登录weblmt
        参数：
    lmtIp:weblmt ip地址
    lmtPort:weblmt端口号
'''        
def key_weblmt_login(lmtIp=BASIC_DATA['weblmt']['ip'], lmtPort=BASIC_DATA['weblmt']['port']):
    with allure.step(key_get_time()+': 登录weblmt, ip:'+lmtIp):
        logging.info(key_get_time()+': login weblmt, ip: '+lmtIp)
        lmt = LmtGnbService().lmtLogin(lmtIp, lmtPort)
        return lmt

'''
说明：weblmt登出
参数：weblmt对象
'''
def key_weblmt_logout(lmtObj):
    with allure.step(key_get_time() + ": %s weblmt登出\n" %(lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt logout\n" % (lmtObj.ip))
        gnbInfo = LmtGnbService().lmtLogOut(lmtObj)
        return gnbInfo

'''
说明：获取基站信息
参数：weblmt对象
'''
def key_weblmt_gnb_info(lmtObj):
    with allure.step(key_get_time() + ": %s weblmt查看基站信息\n" %(lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt get gnb information\n" % (lmtObj.ip))
        gnbInfo = LmtGnbService().lmtGetGnbInfo(lmtObj)
        return gnbInfo

'''
说明：时钟源配置
参数：weblmt对象、时钟源类型
'''
def key_weblmt_clock_cfg(lmtObj, clockMode):
    with allure.step(key_get_time() + ": %s weblmt时钟源配置\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt clock source config\n" % (lmtObj.ip))
        resInfo = LmtGnbService().lmtClockSrcCfg(lmtObj, clockMode)
        return resInfo
'''
说明：获取运营商信息
参数：WEBLMT对象
'''
def key_weblmt_get_operator_info(lmtObj):
    with allure.step(key_get_time() + ": %s weblmt获取运营商信息\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt get operator information\n" % (lmtObj.ip))
        resInfo = LmtGnbService().lmtGetOperatorInfo(lmtObj)
        return resInfo

'''
说明：运营商信息配置
参数：WEBLMT对象、MNC、MCC
'''
def key_weblmt_operator_cfg(lmtObj, mcc, mnc):
    with allure.step(key_get_time() + ": %s weblmt运营商信息配置\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt operator config\n" % (lmtObj.ip))
        resInfo = LmtGnbService().lmtOperatorCfg(lmtObj, mcc, mnc)
        return resInfo

'''
说明：导出基站WifiLog
参数：WEBLMT对象、log路径
'''
def key_weblmt_export_wifi_log(lmtObj, logPath):
    with allure.step(key_get_time() + ": %s weblmt导出基站WiFiLog\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt export BTS WiFi log\n" % (lmtObj.ip))
        res = LmtGnbService().lmtExportWifiLog(lmtObj, logPath)
        return res

'''
说明：导出基站DeviceLog
参数：WEBLMT对象、log路径
'''
def key_weblmt_export_device_log(lmtObj, logPath):
    with allure.step(key_get_time() + ": %s weblmt导出基站DeviceLog\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt export BTS device log\n" % (lmtObj.ip))
        res = LmtGnbService().lmtExportDeviceLog(lmtObj, logPath)
        return res

'''
说明：导出基站CHRLog
参数：WEBLMT对象、log路径
'''
def key_weblmt_export_chr_log(lmtObj, logPath):
    with allure.step(key_get_time() + ": %s weblmt导出基站CHRLog\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt export BTS chr log\n" % (lmtObj.ip))
        res = LmtGnbService().lmtExportCHRLog(lmtObj, logPath)
        return res

'''
说明：导出基站BlackBoxLog
参数：WEBLMT对象、log路径
'''
def key_weblmt_export_black_box_log(lmtObj, logPath):
    with allure.step(key_get_time() + ": %s weblmt导出基站BlackBoxLog\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt export BTS black box log\n" % (lmtObj.ip))
        res = LmtGnbService().lmtExportBlackBoxLog(lmtObj, logPath)
        return res

'''
说明：激活自测模式
参数：WEBLMT对象
'''
def key_weblmt_test_mode_activated(lmtObj, testMode):
    with allure.step(key_get_time() + ": %s weblmt激活自测模式\n" % (lmtObj.ip)):
        logging.warning(key_get_time() + ": %s weblmt test mode set %s\n" % (lmtObj.ip, "open" if testMode==1 else "close"))
        resInfo = LmtGnbService().lmtTestModeActivated(lmtObj, testMode)
        if resInfo['result'] == 0:
            with allure.step(key_get_time()+": weblmt激活自测模式失败"):
                logging.warning(key_get_time() + ":weblmt active auto test mode fail")
        elif resInfo['result'] == 1:
            with allure.step(key_get_time()+": weblmt激活自测模式成功"):
                logging.info(key_get_time() + ":weblmt active auto test mode success")
        return resInfo

'''
说明：打开IPV4/V6使能开关
参数：WEBLMT对象、log路径
'''
def key_weblmt_ip_enable_switch(lmtObj, ipMode):
    with allure.step(key_get_time() + ": %s weblmt打开%s使能开关\n" % (lmtObj.ip, "IPV4" if ipMode==0 else "IPV6")):
        logging.warning(key_get_time() + ": %s weblmt open %s enable switch\n" % (lmtObj.ip, "IPV4" if ipMode==0 else "IPV6"))
        res = LmtGnbService().lmtIpEnableSwitch(lmtObj, ipMode)
        return res

'''
说明：导出基站BlackBoxLog
参数：WEBLMT对象、log路径
'''
def key_weblmt_get_ip_address(lmtObj, ipMode):
    with allure.step(key_get_time() + ": %s weblmt获取%s地址\n" % (lmtObj.ip, "IPV4" if ipMode==0 else "IPV6")):
        logging.warning(key_get_time() + ": %s weblmt get %s address\n" % (lmtObj.ip, "IPV4" if ipMode==0 else "IPV6"))
        res = LmtGnbService().lmtGetIpAddress(lmtObj, ipMode)
        return res