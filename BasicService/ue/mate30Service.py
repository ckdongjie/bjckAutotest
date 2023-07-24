'''
Created on 2022.5.31
'''
import logging
import re
from time import sleep
import time

import serial

from BasicModel.ue.mate30 import mate30Model


class mate30Service():
    
    '''
                说明：登录mate30
                参数：
        serialPort:mate30端口号
        serialRate:mate30端口比特率
        timeout:端口连接超时时间
    '''
    def login_serial(self, serialPort='COM9', serialRate=115200, timeout = 30):
        mate30 = mate30Model().login_serial(serialPort, serialRate, timeout)
        return mate30
        
    '''
                说明：登出mate30
                参数：
    '''     
    def logout_serial(self, mate30):
        if mate30:
            mate30.logout_serial()
    
    
    '''
                说明：mate30接入小区
                参数：
    '''
    def ue_attach(self, mate30):
        cmd = 'at+cfun=1'
        result = mate30.ue_attach_detach(cmd)
        return result
    
    '''
                说明：mate30去接入小区
                参数：
    '''
    def ue_detach(self, mate30):
        cmd = 'at+cfun=0'
        result = mate30.ue_attach_detach(cmd)
        return result
    
    '''
                说明：查询mate30接入小区信息
                参数：
    '''
    def query_attach_cell_info(self, mate30):
        attachStatus, cellInfo = mate30.query_attach_info()
        return attachStatus, cellInfo
    
    '''
                说明：mate30 ping包测试
                参数：
        mate30:mate30对象
        pdn:pdn对象
        ueIp:ueIp地址，mate30需要从pdn上ping，因此需要知道ue ip地址
        pingNum:ping包测试端口
    '''
    def mate30_ping_test(self, mate30, pdn, ueIp, pingNum=20):
        pingRes = mate30.mate30_ping_test(pdn, ueIp, pingNum)
        return pingRes
        
    '''
                说明：mate30下行UDP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''    
    #PDN Send UDP Package To Ue(DL)
    def send_udp_package_DL(self, mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        flowRes = mate30.send_udp_package_DL(pdnIp, packageSize, monitorPort, processNum)
        return flowRes
    
    '''
                说明：mate30上行UDP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #Ue Send UDP Package To PDN(UL)
    def send_udp_package_UL(self, mate30, pdnIp, packageSize='300m', monitorPort='5555', processNum = '3'):
        flowRes = mate30.send_udp_package_UL(pdnIp, packageSize, monitorPort, processNum)
        return flowRes
    
    '''
                说明：mate30下行TCP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''    
    #PDN Send TCP Package To Ue(DL)
    def send_tcp_package_DL(self, mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        flowRes = mate30.send_tcp_package_DL(pdnIp, packageSize, monitorPort, processNum)
        return flowRes
    
    '''
                说明：mate30上行TCP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #Ue Send TCP Package To PDN(UL)
    def send_tcp_package_UL(self, mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        flowRes = mate30.send_tcp_package_UL(pdnIp, packageSize, monitorPort, processNum)
        return flowRes   
