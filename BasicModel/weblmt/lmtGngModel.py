'''
Created on 2022年10月27日

@author: dj
'''
from BasicModel.weblmt.requestdata.gnbManagerData import LMT_URL_DICT
from BasicModel.weblmt.weblmt import WebLmt
import os


class LmtGnbModel(WebLmt):
    '''
    classdocs
    '''
    ip = ''
    port = '8090'
    baseUrl = 'http://'+ip+':'+port
    
    def __init__(self, lmtObj=None):
        '''
        Constructor
        '''
        if lmtObj:
            self.baseUrl = lmtObj.baseUrl
            self.ip = lmtObj.ip
    
    def lmtLogin(self, lmtIp, lmtPort='8090'):
        self.ip = lmtIp
        self.port = lmtPort
        self.baseUrl = 'http://'+lmtIp+':'+lmtPort
        return self

    def lmtLogOut(self):
        header = LMT_URL_DICT['Logout']['header']
        url = self.baseUrl + LMT_URL_DICT['Logout']['action']
        response = self.get_request(url, headers=header)
        resCode = response.status_code
        return resCode

    def lmtRebootGnb(self):
        header = LMT_URL_DICT['BntReboot']['header']
        url = self.baseUrl+LMT_URL_DICT['BntReboot']['action']
        body = LMT_URL_DICT['BntReboot']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo

    #获取基站信息
    def lmtGetGnbInfo(self):
        header = LMT_URL_DICT['GnbInfo']['header']
        url = self.baseUrl + LMT_URL_DICT['GnbInfo']['action']
        body = LMT_URL_DICT['GnbInfo']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    #时钟源配置
    def lmtClockSrcCfg(self, clockMode):
        header = LMT_URL_DICT['ClockMode']['header']
        url = self.baseUrl + LMT_URL_DICT['ClockMode']['action']
        body = LMT_URL_DICT['ClockMode']['body']
        if clockMode == 0:
            body['data'] = [{'ClockSrcID': 0, 'ClockSrcMode': "1"}]
        elif clockMode == 1:
            body['data'] = [{'ClockSrcID': 0, 'ClockSrcMode': "1073741824"}]
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    # 获取运营商信息
    def lmtGetOperatorInfo(self):
        header = LMT_URL_DICT['OperatorInfo']['header']
        url = self.baseUrl + LMT_URL_DICT['OperatorInfo']['action']
        body = LMT_URL_DICT['OperatorInfo']['body']
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    #运营商配置
    def lmtOperatorCfg(self, mcc, mnc):
        header = LMT_URL_DICT['OperatorCfg']['header']
        url = self.baseUrl + LMT_URL_DICT['OperatorCfg']['action']
        body = LMT_URL_DICT['OperatorCfg']['body']
        body['data'][0]['Mnc'] = mnc
        body['data'][0]['Mcc'] = mcc
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    #导出WiFi log
    def lmtExportWifiLog(self, logPath):
        header = LMT_URL_DICT['WIFILog']['header']
        url = self.baseUrl + LMT_URL_DICT['WIFILog']['action']
        response = self.get_request(url, headers = header)
        if response.status_code != 200:
            return False
        fileName = logPath + "\\WifiLog.zip"
        with open(fileName, "wb+") as fp:
            fp.write(response.content)
        fileSize = os.path.getsize(fileName)
        return fileSize

    #导出Device log
    def lmtExportDeviceLog(self, logPath):
        header = LMT_URL_DICT['DeviceLog']['header']
        url = self.baseUrl + LMT_URL_DICT['DeviceLog']['action']
        response = self.get_request(url, headers = header)
        if response.status_code != 200:
            return False
        fileName = logPath + "\\DeviceLog.zip"
        with open(fileName, "wb+") as fp:
            fp.write(response.content)
        fileSize = os.path.getsize(fileName)
        return fileSize

    #导出CHR log
    def lmtExportCHRLog(self, logPath):
        header = LMT_URL_DICT['CHRLog']['header']
        url = self.baseUrl + LMT_URL_DICT['CHRLog']['action']
        response = self.get_request(url, headers = header)
        if response.status_code != 200:
            return False
        fileName = logPath + "\\CHRLog.zip"
        with open(fileName, "wb+") as fp:
            fp.write(response.content)
        fileSize = os.path.getsize(fileName)
        return fileSize

    #导出black box log
    def lmtExportBlackBoxLog(self, logPath):
        header = LMT_URL_DICT['BlackBoxLog']['header']
        url = self.baseUrl + LMT_URL_DICT['BlackBoxLog']['action']
        response = self.get_request(url, headers = header)
        if response.status_code != 200:
            return False
        fileName = logPath + "\\BlackBoxLog.zip"
        with open(fileName, "wb+") as fp:
            fp.write(response.content)
        fileSize = os.path.getsize(fileName)
        return fileSize

    #激活自测模式
    def lmtTestModeActivated(self, testMode):
        header = LMT_URL_DICT['TestModeActivated']['header']
        url = self.baseUrl + LMT_URL_DICT['TestModeActivated']['action']
        body = LMT_URL_DICT['TestModeActivated']['body']
        body['IsAutoStart'] = testMode
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    #IPV4/V6使能开关
    def lmtIpEnableSwitch(self, ipMode):
        header = LMT_URL_DICT['EnableSwitch']['header']
        url = self.baseUrl + LMT_URL_DICT['EnableSwitch']['action']
        body = LMT_URL_DICT['EnableSwitch']['body']
        if ipMode == 0:
            body['data'][0]['IPv4Enable'] = '1'
            body['data'][0]['IPv6Enable'] = '0'
        elif ipMode == 1:
            body['data'][0]['IPv4Enable'] = '0'
            body['data'][0]['IPv6Enable'] = '1'
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo

    #获取IP地址
    def lmtGetIpAddress(self, mode):
        header = LMT_URL_DICT['IPAddress']['header']
        url = self.baseUrl + LMT_URL_DICT['IPAddress']['action']
        body = LMT_URL_DICT['IPAddress']['body']
        if mode == 0:
            body['tableName'] = "t_strout"
        elif mode == 1:
            body['tableName'] = "t_ipv6"
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo