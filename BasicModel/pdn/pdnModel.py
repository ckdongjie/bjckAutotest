'''
Created on 2022年7月25日
'''
import logging
import re
from time import sleep

import paramiko


class PdnModel():
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
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname=pdnIp, username=username, password=password)
        self._channel = self._ssh.invoke_shell()
        logging.info('login pdn server success!') 
        return self
    
    '''
                说明：登出pdn
                参数：
    '''
    def pdn_logout(self):
        if not self._ssh:
            return
        self._ssh.close()
        self._ssh = None
    
    '''
                说明：在pdn上执行cmd命令
                参数：
        commandStr:cmd 命令
        waitTime:命令执行后的等待时间
    '''    
    def exec_cmd(self, commandStr, waitTime=1):
        self._channel.send(commandStr+'\n') 
        sleep(waitTime)
        return self.rece_cmd_result()
    
    '''
                说明：接收cmd命令执行返回结果
                参数：
    '''    
    def rece_cmd_result(self):
        try:
            result = ''
            while(self._channel.recv_ready()):
                result = result + self._channel.recv(65535).decode() 
            return result
        except:
            print('receive error!')      
    
    '''
                说明：杀死对应端口的iperf进程
                参数：
        port:iperf使用的端口号
    '''
    def kill_iperf_process(self, port):
        query_proc_cmd = 'netstat -anp|grep '+str(port)
        queryCmdRes = self.exec_cmd(query_proc_cmd)
        processId = self.iperf_query_result_mattch(queryCmdRes)
        if processId != -1:
            stop_proc_cmd = 'kill -9 '+str(processId)
            killRes = self.exec_cmd(stop_proc_cmd)
            return killRes
        
    '''
                说明：正则匹配查找对应的iperf进程
                参数：
        resString:iperf进程信息
    '''    
    def iperf_query_result_mattch(self, resString):
        pattern = '.*LISTEN\s*(.*)/iperf3'
        result = re.findall(pattern, resString)
        if len(result)!=0:
            return result[0]
        else:
            return -1    
        
if __name__ == '__main__':
    pdn = PdnModel().pdn_login('172.16.2.202')
    res = pdn.exec_cmd('nohup iperf3 -s -p 5599 &')
    print('=============1',res)