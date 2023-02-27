'''
Created on 2022年10月27日

@author: dj
'''
import logging

from BasicModel.weblmt.lmtGngModel import LmtGnbModel
from UserKeywords.basic.basic import key_get_time


class LmtGnbService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    '''
                登录weblmt
                参数：
        lmtIp:基站debug ip地址
        lmtPort:weblmt登录端口
    '''     
    def lmtLogin(self, lmtIp, lmtPort='8090'):
        lmt = LmtGnbModel().lmtLogin(lmtIp, lmtPort)    
        return lmt
    
    '''
                在weblmt上复位基站
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtRebootGnb(self, lmtObj):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtRebootGnb()
        if resCode == 200 and resInfo['result']== 'success':
            logging.warning(key_get_time()+': weblmt reboot gnb success')
            return True
        else:
            logging.warning(key_get_time()+': weblmt reboot gnb fail')
            return False

    '''
    说明：weblmt登出
    参数：WEBLMT对象
    '''
    def lmtLogOut(self, lmtObj):
        resCode = LmtGnbModel(lmtObj).lmtLogOut()
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt logout success')
            return True
        else:
            logging.warning(key_get_time() + ': weblmt logout fail')
            return False

    '''
    说明：获取基站信息
    参数：WEBLMT对象
    '''
    def lmtGetGnbInfo(self, lmtObj):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtGetGnbInfo()
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt get gnb information success')
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt get gnb information fail')
            return False
    '''
    说明：时钟源配置
    参数：WEBLMT对象、时钟源对象
    '''
    def lmtClockSrcCfg(self, lmtObj, clockMode):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtClockSrcCfg(clockMode)
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt clock source config success')
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt clock source config fail')
            return False

    '''
    说明：获取运营商信息
    参数：WEBLMT对象
    '''
    def lmtGetOperatorInfo(self, lmtObj):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtGetOperatorInfo()
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt get operator information success')
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt get operator information fail')
            return False

    '''
    说明：运营商信息配置
    参数：WEBLMT对象、MNC、MCC
    '''
    def lmtOperatorCfg(self, lmtObj, mcc, mnc):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtOperatorCfg(mcc, mnc)
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt operator config success')
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt operator config fail')
            return False

    '''
    说明：导出基站WifiLog
    参数：WEBLMT对象、log路径
    '''
    def lmtExportWifiLog(self, lmtObj, logPath):
        res = LmtGnbModel(lmtObj).lmtExportWifiLog(logPath)
        if res != False:
            logging.warning(key_get_time() + ': weblmt export wifi log success')
            return True
        else:
            logging.warning(key_get_time() + ': weblmt export wifi log fail')
            return False

    '''
        说明：导出基站DeviceLog
        参数：WEBLMT对象、log路径
        '''
    def lmtExportDeviceLog(self, lmtObj, logPath):
        res = LmtGnbModel(lmtObj).lmtExportDeviceLog(logPath)
        if res != False:
            logging.warning(key_get_time() + ': weblmt export device log success')
            return True
        else:
            logging.warning(key_get_time() + ': weblmt export device log fail')
            return False

    '''
        说明：导出基站CHRLog
        参数：WEBLMT对象、log路径
        '''
    def lmtExportCHRLog(self, lmtObj, logPath):
        res = LmtGnbModel(lmtObj).lmtExportCHRLog(logPath)
        if res != False:
            logging.warning(key_get_time() + ': weblmt export chr log success')
            return True
        else:
            logging.warning(key_get_time() + ': weblmt export chr log fail')
            return False

    '''
        说明：导出基站BlackBoxLog
        参数：WEBLMT对象、log路径
        '''
    def lmtExportBlackBoxLog(self, lmtObj, logPath):
        res = LmtGnbModel(lmtObj).lmtExportBlackBoxLog(logPath)
        if res != False:
            logging.warning(key_get_time() + ': weblmt export black box log success')
            return True
        else:
            logging.warning(key_get_time() + ': weblmt export black box log fail')
            return False

    '''
    说明：激活自测模式
    参数：WEBLMT对象
    '''
    def lmtTestModeActivated(self, lmtObj, testMode):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtTestModeActivated(testMode)
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt test mode set success')
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt test mode set fail')
            return False

    '''
    说明：打开IPV4/V6使能开关
    参数：WEBLMT对象，IP模式
    '''
    def lmtIpEnableSwitch(self, lmtObj, ipMode):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtIpEnableSwitch(ipMode)
        res = "IPV4" if ipMode==0 else "IPV6"
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt open %s enable switch success' % (res))
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt open %s enable switch fail' % (res))
            return False

    '''
    说明：获取IPV4/V6地址
    参数：WEBLMT对象，IP模式
    '''
    def lmtGetIpAddress(self, lmtObj, ipMode):
        resCode, resInfo = LmtGnbModel(lmtObj).lmtGetIpAddress(ipMode)
        res = "IPV4" if ipMode == 0 else "IPV6"
        if resCode == 200:
            logging.warning(key_get_time() + ': weblmt get %s address success' % (res))
            return resInfo
        else:
            logging.warning(key_get_time() + ': weblmt get %s address switch fail' % (res))
            return False