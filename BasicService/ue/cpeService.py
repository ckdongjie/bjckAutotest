# coding = 'utf-8'
'''
Created on 2022年11月1日

@author: dj
'''

import re
import subprocess
from time import sleep

from BasicModel.ue.cpeModel import CpeModel


class CpeService():
    '''
    classdocs
    '''
    
    '''
                说明：登录cpe
                参数：
        cpeIp:cpe ssh登录ip地址
        username:cpe ssh登录用户名
        password:cpe ssh登录密码
    '''
    def cpe_login(self, cpeIp, username="root", password="snc123..."):
        cpe = CpeModel().cpe_login(cpeIp, username, password)
        return cpe
    
    '''
                说明：登出cpe
                参数：
    '''    
    def cpe_logout(self, cpe):
        if cpe:
            cpe.cpe_logout()
    
    '''
                说明：进入cpe at命令模式
                参数：
    '''    
    def login_at_model(self, cpe):
        if cpe:
            cpe.login_at_model()
    
    '''
                说明：退出cpe at命令模式
                参数：
    ''' 
    def logout_at_model(self, cpe):
        if cpe:
            cpe.logout_at_model()
    
    '''
                说明：cpe 接入小区
                参数：
    '''         
    def cpe_attach(self, cpe):
        if cpe:
            cmd = 'at+cfun=1'
            cpe.login_at_model()
            sleep(1)
            attachRes = cpe.exec_at_command(cmd)
            sleep(1)
            cpe.logout_at_model()
            return attachRes
    
    '''
                说明：cpe去接入小区
                参数：
    '''    
    def cpe_detach(self, cpe):
        if cpe:
            cmd = 'at+cfun=0'
            cpe.login_at_model()
            sleep(1)
            cpe.exec_at_command(cmd)
            sleep(1)
            cpe.logout_at_model()
    
    '''
                说明：cpe去接入小区
                参数：
    '''    
    def confirm_pdu_setup(self, cpe, tryNum = 10):
        if cpe:
            setupRes = cpe.query_pdu_setup_status()
            return setupRes
            
    '''
                说明：查询cpe接入小区信息
                参数：
    '''
    def query_cpe_access_cell_info(self, cpe):
        if cpe:
            cpe.login_at_model()
            sleep(1)
            cpe.exec_at_command("at+c5greg=2")
            sleep(2)
            ueAttach, cellId = cpe.exec_at_command_and_check_cell_info("at+c5greg?")
            sleep(1)
            cpe.logout_at_model()
            return ueAttach, cellId
        
    '''
                说明：查询cpe接入小区信息
                参数：
    '''
    def query_resident_cell_pci(self, cpe):
        if cpe:
            cpe.login_at_model()
            sleep(1)
            cellPci = cpe.query_resident_cell_info("at+sgcellinfoex?")
            sleep(1)
            cpe.logout_at_model()
            return cellPci
    
    '''
                说明：cpe ping包测试
                参数：
        cpePcIp:cpe连接pc配置的ip地址，例：192.168.1.16
        pdnIp:pdn业务ip地址
        pingNum:ping测试包数
        pingInterface:ping包测试端口
        tryNum:ping失败尝试次数
    '''        
    def cpe_ping_test(self, cpe, pdnIp='193.168.9.239', pingNum=20, pingInterface = 'rmnet_data0', pingSize=32):
        min, avg, max, transmitted, received, lossrate = cpe.ping_test(pdnIp, pingNum, pingInterface, pingSize)
        return min, avg, max, transmitted, received, lossrate
    
    '''
            本地pc执行ping
    '''
    def local_pc_ping(self, pdnIp='193.168.9.239', count=10, pingSize=32):
        command = 'ping -n '+str(count)+' -l '+str(pingSize)+' '+pdnIp
        p = subprocess.Popen(command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
        out = p.stdout.read().decode('gbk')
        min,max,avg,transmitted,received,lossrate = self.filter_ping_result(out)
        if avg == -1:
            min,max,avg,transmitted,received,lossrate = self.filter_ping_result_english(out)
        return min,max,avg,transmitted,received,lossrate
        
    def filter_ping_result(self, pingResStr=''):
        pattern = r'最短 = (.*)ms，最长 = (.*)ms，平均 = (.*)ms'
        transmitted,received,lossrate = 0,0,100
        result = re.findall(pattern, str(pingResStr))
        if result !=[]:
            min = list(result[0])[0]
            max = list(result[0])[1]
            avg = list(result[0])[2]
        else:
            min = -1
            max = -1
            avg = -1
        pattern2 = r'数据包: 已发送 = (.*)，已接收 = (.*)，丢失 = (.*) ((.*) 丢失)'
        result2 = re.findall(pattern2, str(pingResStr))
        if result2 !=[]:
            pingRes2 = list(result2[0])
            transmitted = pingRes2[0]
            received = pingRes2[1]
            lossrate = int((int(transmitted)-int(received)) /int(transmitted)*100)
        return min,max,avg,transmitted,received,lossrate
    
    def filter_ping_result_english(self, pingResStr=''):
        pattern = r'Minimum = (.*)ms, Maximum = (.*)ms, Average = (.*)ms'
        transmitted,received,lossrate = 0,0,100
        result = re.findall(pattern, str(pingResStr))
        if result !=[]:
            min = list(result[0])[0]
            max = list(result[0])[1]
            avg = list(result[0])[2]
        else:
            min = -1
            max = -1
            avg = -1
        pattern2 = r'Packets: Sent = (.*), Received = (.*), Lost = (.*) ((.*) loss)'
        result2 = re.findall(pattern2, str(pingResStr))
        if result2 !=[]:
            pingRes2 = list(result2[0])
            transmitted = pingRes2[0]
            received = pingRes2[1]
            lossrate = int((int(transmitted)-int(received)) /int(transmitted)*100)
        return min,max,avg,transmitted,received,lossrate
    '''
                说明：复位cpe
                参数：
        cpe:cpe对象
    '''    
    def reboot_cpe(self, cpe):
        rebootRes = cpe.reboot_cpe() 
        return rebootRes
        
    '''
                说明：查询pdu是否建立
                参数：
    '''    
    def query_pdu_setup_status(self, cpe):
        setupStatus = cpe.query_pdu_setup_status() 
        return setupStatus   
    
    '''
                说明：cpe下行UDP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #PDN Send UDP Package To Ue(DL)
    def cpe_udp_flow_DL(self, cpe, cpePcIp, iperfPath, pdnIp, packageSize='500m', monitorPort=5555, processNum = 3, spanTime = 120, isLocalExec=True):
        flowRes = cpe.send_udp_package_DL(cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime, isLocalExec)
        return flowRes
    
    '''
                说明：cpe上行UDP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #Ue Send UDP Package To PDN(UL)
    def cpe_udp_flow_UL(self, cpe, cpePcIp, iperfPath, pdnIp, packageSize='300m', monitorPort=5555, processNum=3, spanTime=120, isLocalExec=True):
        flowRes = cpe.send_udp_package_UL(cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime, isLocalExec)
        return flowRes
    
    '''
                说明：cpe下行TCP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #PDN Send TCP Package To Ue(DL)
    def cpe_tcp_flow_DL(self, cpe, cpePcIp, iperfPath, pdnIp, packageSize='1400k', monitorPort=5555, processNum=3, spanTime=120, isLocalExec=True):
        flowRes = cpe.send_tcp_package_DL(cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime, isLocalExec)
        return flowRes
    
    '''
                说明：cpe上行TCP流量测试
                参数：
        iperfPath:本地iperf工具安装路径
        pdnIp:pdn业务ip地址
        packageSize:灌包大小
        monitorPort:灌包使用的端口
        processNum:灌包进程数
    '''
    #Ue Send TCP Package To PDN(UL)
    def cpe_tcp_flow_UL(self, cpe, cpePcIp, iperfPath, pdnIp, packageSize='1400k', monitorPort=5555, processNum=3, spanTime=120, isLocalExec=True):
        flowRes = cpe.send_tcp_package_UL(cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime, isLocalExec)
        return flowRes
    
    '''
                说明：小区流量分析
    '''
    def cell_flow_analyze(self, cpe, enbIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='', spanTime=120, type='WIFI', gnbType='BS5514', isLocalExec=True):
        dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = cpe.cell_flow_analyze(enbIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type, gnbType, isLocalExec)
        return dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf
    
    '''
                说明：新增端口绑定规则
                    1）先删除对应端口的规则 
                    2）增加端口规则
    '''                                
    def binding_port_and_network(self, cpe, port, networkType='WIFI', flowType='udp', ipType='ipv4'):
        bindRes = cpe.binding_port_and_network(port, networkType, flowType, ipType)
        return bindRes
    
if __name__ == '__main__':
    CpeService().local_pc_ping('193.168.9.223')
#     CpeService().filter_ping_result()