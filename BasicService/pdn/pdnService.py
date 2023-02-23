'''
Created on 2022年7月25日
'''
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
    def start_listening_port(self, pdn, port, waitTime = 1):
        cmdStr = 'nohup iperf3 -s -p '+str(port)+' &'
        result = pdn.exec_cmd(cmdStr, waitTime)
        return result
    
    
    '''
                说明：关闭监听端口进程
                参数：
        pdn:pdn对象
        port:iperf使用的端口号
    '''
    def kill_iperf_process(self, pdn, port):
        pdn.kill_iperf_process(port)