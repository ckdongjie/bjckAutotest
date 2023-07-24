# coding:utf-8
'''
Created on 2023年5月11日
@author: autotest
'''
import os
import re
import subprocess
from time import sleep

from BasicModel.basic.loadFileAndAnalyzeData import startMonitorTask, \
    startCatputer, stopCatputer, loadDataAndCalculateFlow
from BasicModel.basic.udpSocket import udpSocketModel


class PhoneModel():
    '''
        adb命令获取手机设备编号
    '''
    def get_devices_list(self):
        cmdStr = 'adb devices'
        osChanel = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE)
        queryRes = osChanel.stdout.read().decode('utf-8')
        deviceList = self.filter_device_list(queryRes)
        return deviceList
    
    '''
                正则表达式过滤提取设备编号
    '''
    def filter_device_list(self, queryRes):
        deviceList = []
        pattern = '(.*)\s*device\s'
        result = re.findall(pattern, queryRes)
        for str in result:
            deviceList.append(str.replace('\t', ''))
        return deviceList    
    
    '''
        adb命令设置手机飞行模式：
        adb shell settings put global airplane_mode_on 1
        adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
    '''
    def set_mobile_airplane_mode(self, deviceId, phoneType='xiaomi'):
        #设置飞行模式
        subprocess.Popen('adb -s '+deviceId+' shell settings put global airplane_mode_on 1', shell=False, stdout=subprocess.PIPE)
        if phoneType != 'mate30':
            #配置生效
            subprocess.Popen('adb -s '+deviceId+' shell am broadcast -a android.intent.action.AIRPLANE_MODE', shell=False, stdout=subprocess.PIPE)
        
    '''
        adb命令设置手机去飞行模式：
        adb shell settings put global airplane_mode_on 0
        adb shell am broadcast -a android.intent.action.AIRPLANE_MODE
    '''
    def set_mobile_no_airplane_mode(self, deviceId, phoneType='xiaomi'):    
        #设置去飞行模式
        subprocess.Popen('adb -s '+deviceId+' shell settings put global airplane_mode_on 0', shell=False, stdout=subprocess.PIPE)
        if phoneType != 'mate30':
            #配置生效
            subprocess.Popen('adb -s '+deviceId+' shell am broadcast -a android.intent.action.AIRPLANE_MODE', shell=False, stdout=subprocess.PIPE)
    
    '''
                    获取终端业务地址
    '''
    def get_ip_addr(self, deviceId):
        execRes = subprocess.Popen('adb -s '+deviceId+' shell ifconfig', shell=False, stdout=subprocess.PIPE)
        ipInfo = execRes.stdout.read().decode('utf-8')
        ipAddr = self.filter_inet_addr(ipInfo)
        return ipAddr
    
    '''
                正则表达式对ifconfig结果进行过滤获取ip地址
    '''
    def filter_inet_addr(self, ipInfo):
        pattern = 'rmnet_data.*\s*inet addr:(.*)  Mask:255.255'
        ipAddr = re.findall(pattern, ipInfo)
        if ipAddr != []:
            return ipAddr[0]
        else:
            return ''
    
    '''
                查询手机网络接入状态
    '''
    def query_access_status(self, deviceId):
        execRes = subprocess.Popen('adb -s '+deviceId+' shell dumpsys telephony.registry', shell=False, stdout=subprocess.PIPE)
        networkInfo = execRes.stdout.read().decode('utf-8')
        accStatus = self.filter_access_status(networkInfo)
        return accStatus # 2-正常接入   0-无数据连接
    
    '''
                网络接入状态过滤
    '''
    def filter_access_status(self, networkInfo):
        pattern = 'mDataConnectionState=(.*)\\r'
        result = re.findall(pattern, networkInfo)
        if result !=[]:
            return str(result[0])
        else:
            return ''
    '''
        adb命令启动iperf进程进行tcp上行灌包
    '''
    def ul_tcp_traffic(self, deviceId, pdnIp, packageSize='1400k', monitorPort=5555, processNum = 3, spanTime = 120):
        iperfCmd = 'adb -s '+deviceId+' shell su -c iperf -c '+pdnIp+' -i 1 -w '+packageSize+' -t '+str(spanTime+10)+' -p '+str(monitorPort)+' -P '+str(processNum)
        subprocess.Popen(iperfCmd, shell=False, stdout=subprocess.PIPE)
        
    '''
        adb命令启动iperf进程进行tcp下行灌包
    '''
    def dl_tcp_traffic(self, deviceId, monitorPort=5555):
        iperfCmd = 'adb -s '+deviceId+' shell su -c iperf -s -p '+str(monitorPort)
        subprocess.Popen(iperfCmd, shell=False, stdout=subprocess.PIPE)
    
    '''
        adb命令启动iperf进程进行udp上行灌包
    '''
    def ul_udp_traffic(self, deviceId, pdnIp, packageSize='300m', monitorPort=5555, processNum = 3, spanTime = 120):
        iperfCmd = 'adb -s '+deviceId+' shell su -c iperf -u -c '+pdnIp+' -b '+ packageSize +' -i 1 -t '+str(spanTime+10)+' -l 1300 -p '+str(monitorPort)+' -P '+str(processNum)
        subprocess.Popen(iperfCmd, shell=False, stdout=subprocess.PIPE)
        
    '''
        adb命令启动iperf进程进行udp下行灌包
    '''
    def dl_udp_traffic(self, deviceId, monitorPort=5555):
        iperfCmd = 'adb -s '+deviceId+' shell su -c iperf -s -u -p '+str(monitorPort)
        subprocess.Popen(iperfCmd, shell=False, stdout=subprocess.PIPE)
    
    '''
                    流量数据分析
    '''    
    def traffic_data_analyze(self, enbIp, pcIp, scrapFileName, trafficDir = 'DL', pcNetworkCardName ='', spanTime = 120, type='WIFI'):
        svSocket = udpSocketModel().socket_sv_basic_client(enbIp, 16677)
        startMonitorTask(svSocket)
        startCatputer(pcNetworkCardName)
        sleep(spanTime)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        capturePath = BASE_DIR+'\\AutoTestMain\\captureData'
        stopCatputer(capturePath+'\\'+scrapFileName)
        dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = loadDataAndCalculateFlow(capturePath+'\\'+scrapFileName, enbIp, pcIp, trafficDir, type)
        svSocket.close()
        return dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf
    '''
                    停止iperf进程
    '''    
    def stop_iperf_process(self, deviceId, mointorPort, testType='tcp'):
        query_proc_cmd = 'adb -s '+deviceId+' shell su -c netstat -anp|grep '+str(mointorPort)
        pro = subprocess.Popen(query_proc_cmd, shell=False, stdout=subprocess.PIPE)
        queryRes = (pro.communicate()[0]).decode('utf-8')
        processId = self.iperf_query_result_mattch(queryRes, testType, 'iperf')
        if processId != -1:
            stop_proc_cmd = 'adb -s '+deviceId+' shell su -c kill -9 '+str(processId)
            subprocess.Popen(stop_proc_cmd, shell=False, stdout=subprocess.PIPE)
    
    '''
                说明：正则匹配查找对应的iperf进程
                参数：
        resString:iperf进程信息
    '''    
    def iperf_query_result_mattch(self, resString, testType='tcp', iperfType='iperf3'):
        if testType=='udp':
            pattern = 'udp.*0.0.0.0:\*\s*(.*)/iperf'
        else:
            pattern = '.*LISTEN\s*(.*)/'+iperfType
        result = re.findall(pattern, resString)
        if len(result)!=0:
            return result[0]
        else:
            return -1
        
        
if __name__ == '__main__':
#     PhoneModel().traffic_data_analyze('172.16.2.240', '172.16.2.138', 'autotest.pcap', 'DL', 'TP-Link Gigabit PCI Express Adapter', 30, 'NR')
    str = '''
    
    '''
    PhoneModel().filter_access_status(str)