'''
Created on 2022年7月25日
'''
import re

from BasicModel.pdn.pdnModel import PdnModel


class PdnService():
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
    '''
                说明：登录pdn
                参数：
        pdnIp:pdn登录ip地址
        username:pdn ssh登录用户名
        password:pdn ssh登录密码
    '''
    def pdn_login(self, pdnIp, username="root", password="ck2022..."):
        pdn = PdnModel().pdn_login(pdnIp, username, password)
        return pdn
    
    '''
                说明：登出pdn
                参数：
    '''
    def pdn_logout(self, pdn):
        if pdn:
            pdn.pdn_logout()
    
    '''
                说明：启动端口监听进程
                参数：
        pdn:pdn对象
        port:监听端口
        waitTime:命令执行后的等待时间
    '''      
    def start_listening_port(self, pdn, port, iperfType='iperf3', waitTime = 1):
        cmdStr = 'nohup '+iperfType+' -s -p '+str(port)+' &'
        result = pdn.exec_cmd(cmdStr, waitTime)
        return result
    
    
    '''
                说明：关闭监听端口进程
                参数：
        pdn:pdn对象
        port:iperf使用的端口号
    '''
    def kill_iperf_process(self, pdn, port, iperfType='iperf3'):
        pdn.kill_iperf_process(port, iperfType)
        
    '''
                    启动iperf tcp灌包命令
    '''    
    def start_iperf_command_tcp(self, pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):    
        pdn.start_iperf_command_tcp(phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
        
    '''
                    启动iperf tcp灌包命令 上行
    '''    
    def start_iperf_command_tcp_ul(self, pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):    
        pdn.start_iperf_command_tcp_ul(phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
    
    '''
                    启动iperf udp灌包命令
    '''    
    def start_iperf_command_udp(self, pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):    
        pdn.start_iperf_command_udp(phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
    
    '''
                    启动iperf udp灌包命令
    '''    
    def start_iperf_command_udp_ul(self, pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):    
        pdn.start_iperf_command_udp_ul(phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
        
    '''
                说明：pdn ping终端地址
                参数：
        pdn:pdn对象
        ueIp:终端ip地址
        pingTimes:ping包次数
        waitTime:命令执行后的等待时间
    '''      
    def ping_ue_ip(self, pdn, ueIp, pingTimes, pingSize=32):
        cmdStr = 'ping -c '+str(pingTimes)+' '+ueIp+' -s '+str(pingSize)
        print(cmdStr)
        pingRes = pdn.exec_cmd(cmdStr, int(pingTimes))
        print(pingRes)
        min, avg, max = self.ping_result_mattch(pingRes)
        transmitted = self.ping_result_mattch_transmitted(pingRes)
        received = self.ping_result_mattch_received(pingRes)
        lossrate = self.ping_result_mattch_loss_rate(pingRes)
        return min, avg, max, transmitted, received, lossrate
    
    def ping_result_mattch(self, str):
        pattern = '.*min/avg/max/mdev = (.*) ms'
        result = re.findall(pattern, str)
        if result:
            pingResList = result[0].split('/')
            min,avg,max = pingResList[0],pingResList[1],pingResList[2]
            return min, avg, max
        return -1, -1, -1    
    
    def ping_result_mattch_transmitted(self, str):
        pattern = r'.*\s*(.*) packets transmitted'
        result = re.findall(pattern, str)
#         logging.info('packets transmitted:{0}'.format(result))
        if result:
            tranPackage = result[-1]
            return tranPackage
        return -1
    
    def ping_result_mattch_received(self, str):
        pattern = 'packets transmitted, (.*) received'
        result = re.findall(pattern, str)
        if result:
            recePackage = result[-1]
            return recePackage
        return 0
    
    def ping_result_mattch_loss_rate(self, str):
        pattern = 'received, (.*) packet loss,'
        result = re.findall(pattern, str)
#         logging.info('packet loss:{0}'.format(result))
        if result:
            lossRate = result[-1]
            return lossRate
        return '100%'