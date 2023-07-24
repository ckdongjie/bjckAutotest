# coding = 'utf-8'
'''
Created on 2023年5月11日
@author: autotest
'''
from BasicModel.ue.phoneModel import PhoneModel
class MobilePhoneService():
    
    '''
                    获取设备列表
    '''
    def get_phone_devices(self):
        phoneDevList = PhoneModel().get_devices_list()
        return phoneDevList
    
    '''
                    多设备获取设备ip地址
    '''    
    def get_phone_ip_addr(self, deviceId):
        ipAddr = PhoneModel().get_ip_addr(deviceId)
        return ipAddr
    
    '''
                    多设备获取手机连接状态
    '''
    def query_access_status(self, deviceId):
        accStatus = PhoneModel().query_access_status(deviceId)
        return accStatus
    
    '''
                    设置手机飞行模式
    '''
    def set_airplane_mode(self, deviceId, phoneType='xiaomi'):
        PhoneModel().set_mobile_airplane_mode(deviceId, phoneType)
    
    '''
                    设置手机去飞行模式
    '''
    def set_no_airplane_mode(self, deviceId, phoneType='xiaomi'):
        PhoneModel().set_mobile_no_airplane_mode(deviceId, phoneType)
    
    '''
                    多设备获取设备ip地址
    '''    
    def get_muti_phone_ip_addr(self, phoneDevList):
        devIpDict = {}
        for deviceId in phoneDevList:
            ipAddr = PhoneModel().get_ip_addr(deviceId)
            devIpDict[deviceId] = ipAddr
        return devIpDict
    
    '''
                    多设备获取手机连接状态
    '''
    def query_muti_access_status(self, phoneDevList):
        devAccStatusInfo = {}
        for deviceId in phoneDevList:
            accStatus = PhoneModel().query_access_status(deviceId)
            devAccStatusInfo[deviceId] = accStatus
        return devAccStatusInfo
    
    '''
                    设置手机飞行模式
    '''
    def set_muti_airplane_mode(self, phoneDevList):
        for deviceId in phoneDevList:
            PhoneModel().set_mobile_airplane_mode(deviceId)
    
    '''
                    设置手机去飞行模式
    '''
    def set_muti_no_airplane_mode(self, phoneDevList):
        for deviceId in phoneDevList:
            PhoneModel().set_mobile_no_airplane_mode(deviceId)
    
    '''
                    上行tcp灌包
    '''
    def phone_ul_tcp_traffic(self, deviceId, pdnIp, packageSize='1400k', monitorPort=5555, processNum = 3, spanTime = 120):
        PhoneModel().ul_tcp_traffic(deviceId, pdnIp, packageSize, monitorPort, processNum, spanTime)
    
    '''
                    下行tcp灌包
    '''    
    def phone_dl_tcp_traffic(self, deviceId, monitorPort=5555):
        PhoneModel().dl_tcp_traffic(deviceId, monitorPort) 
    
    '''
                    停止iperf进程
    '''
    def phone_stop_iperf(self, deviceId, monitorPort, testType='tcp'):
        PhoneModel().stop_iperf_process(deviceId, monitorPort, testType)
    '''
                    上行udp灌包
    '''    
    def phone_ul_udp_traffic(self, deviceId, pdnIp, packageSize='300m', monitorPort=5555, processNum = 3, spanTime = 120):
        PhoneModel().ul_udp_traffic(deviceId, pdnIp, packageSize, monitorPort, processNum, spanTime)
    
    '''
                    下行udp灌包
    '''    
    def phone_dl_udp_traffic(self, deviceId, monitorPort=5555):
        PhoneModel().dl_udp_traffic(deviceId, monitorPort)
        
    '''
                    灌包数据分析
    '''    
    def phone_traffic_data_analyze(self, enbIp, pcIp, scrapFileName, trafficDir = 'DL', pcNetworkCardName ='', spanTime=120, type='NR'):
        dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = PhoneModel().traffic_data_analyze(enbIp, pcIp, scrapFileName, trafficDir, pcNetworkCardName, spanTime, type)
        return dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf