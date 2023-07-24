# coding = 'utf-8'
'''
Created on 2022年11月17日

@author: dj


'''

from datetime import datetime
import logging
import re
from time import sleep

import paramiko


class gnbModel(object):
    '''
    classdocs
    '''
    _ssh = None
    _channel = None
    
    def __init__(self):
        '''
        Constructor
        '''
#         self = gnb
    
    def ssh_login_gnb(self, gnbDebugIp, username="root", password="Web2022@Nr5gTech"):
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh.connect(hostname=gnbDebugIp, username=username, password=password)
            self._channel = self._ssh.invoke_shell()
            return self
        except Exception:
            return None
        
    def logout_gnb(self):
        if not self._ssh:
            return
        self._ssh.close()
        self._ssh = None
        
    def exec_fun_command(self, cmd):
        if not self._ssh:
            self._ssh.invoke_shell()
        try:
            self._channel.send(cmd+'\r')
            sleep(1)
            result = self.rece_fun_command()
            return result
        except:
            logging.warning('exec cmd error')
            return None
    
    def rece_fun_command(self):
        try:
            return self._channel.recv(65535).decode('utf-8')
        except:
            print('rece error!')
    
    def is_exec_succ(self, str, exptStr):
        result = exptStr in str
        if result:
            return True
        else:
            return False
    
    '''
                    登录nrapp
    '''
    def login_nr_process(self, exptStr=''):
        result = self.exec_fun_command("nrapp.sh")
        runSucc = self.is_exec_succ(result, exptStr)
        if runSucc:
            logging.info('login nrapp success.')
        else:
            logging.warning('login nrapp fail.')
    
    '''
                    打开基站log输出开关
    '''        
    def open_log_switch(self, exptStr=''):
        result = self.exec_fun_command("VOS_SetPFlag 3")
        runSucc = self.is_exec_succ(result, exptStr)
        if runSucc:
            logging.info('open log print success.')
        else:
            logging.warning('open log print fail.')
            
    '''
                    基站抓包-dpdk0网卡
    '''        
    def capture_package_on_gnb(self, filePath='/'):
        nowtime = str(datetime.timestamp(datetime.now()))
        self.exec_fun_command("nohup tcpdump -ni dpdk0 -C 500 -w "+filePath+"auto_"+str(nowtime)+".pcap &")
    
    '''
                    基站前台执行桩函数
    '''        
    def exec_command_on_gnb(self, cmdStr):
        result = self.exec_fun_command(cmdStr)
        return result 
    
    '''
                    查询基站gps文件的md5值
    '''
    def check_gps_md5(self):
        self.exec_fun_command('cd /usr/local/bin')
        execRes = self.exec_fun_command('md5sum gps')
        md5Res = self.find_md5_result(execRes)
        return md5Res
    
    def find_md5_result(self, str):
        pattern = '(.*)\s\sgps.*'
        result = re.findall(pattern, str)
        print(result)
        if result:
            return result[0]
        
    '''
                    查询基站nrsys版本号
    '''
    def query_nrsys_version(self):
        execRes = self.exec_fun_command('cat /proc/cmdline')
        nrsysRes = self.find_nrsys_result(execRes)
        ubootRes = self.find_uboot_result(execRes)
        return str(ubootRes), str(nrsysRes)
    
    def find_nrsys_result(self, str):
        pattern = '.*nrsys_ver=(.*)\r.*'
        result = re.findall(pattern, str)
        print(result)
        if result:
            return result[0]
    
    def find_uboot_result(self, str):
        pattern = '.*uboot_ver=(.*)\r.*'
        result = re.findall(pattern, str)
        print(result)
        if result:
            return result[0]    
        
    def upgrade_cpld_version(self, cpldVersion, cpldPath, enbType):
        self.exec_fun_command('cd '+cpldPath)
        cmdStr = './cpld_update_'+enbType+' '+cpldVersion
        print('cmd str:'+cmdStr)
        execRes = self.exec_fun_command(cmdStr)
        return execRes
    
    def gnb_copy_file(self, souFilePath, desFilePath):
        result = self.exec_fun_command('ssh 10.50.0.2')
        print(result)
        result = self.exec_fun_command('Web2022@Nr5gTechPs')
        print(result)
        result = self.exec_fun_command('Web2022@Nr5gTechPs')
        print(result)
        result = self.exec_fun_command('pwd')
        print(result)
        cmdStr = 'cp '+souFilePath+' '+desFilePath
        print('cmd str:'+cmdStr)
        self.exec_fun_command(cmdStr)
        cmdStr = 'md5sum /etc/init.d/bootmisc.sh'
        execRes = self.exec_fun_command(cmdStr)
        print('bootmisc md5sum:'+execRes)
        return execRes
    
    def query_cpld_version_info(self):
        cmdStr = 'ptool cpld i'
        print('cmd str:'+cmdStr)
        execRes = self.exec_fun_command(cmdStr)
        return execRes
    
    '''
                查询核x cpu利用率
    '''
    def query_core_cpu_ratio(self, cmdStr, queryNum):
        resS = self.exec_fun_command('nrapp.sh')
        cpuRatioStr = ''
        try:
            for i in range(1, queryNum+1):
                execRes = self.exec_fun_command(cmdStr)
                cpuRatio = self.filter_cpu_ratio(execRes)
                cpuRatioStr = cpuRatio + ','+cpuRatioStr
                sleep(1)
        except:
            return cpuRatioStr
        return cpuRatioStr
    
    '''
                正则表达式过滤提取cpu利用率值
    '''
    def filter_cpu_ratio(self, resStr):
        pattern = '.*nrtp_get_cpu_use return=([0-100])'
        result = re.findall(pattern, resStr)
        if result!=[]:
            return result[-1]
        else:
            return '-'
        
    '''
                登录wifi板执行桩函数
    '''    
    def login_wifi_exec_cmd(self, cmdStr):
        self.exec_fun_command('ssh 10.254.254.254')
        self.exec_fun_command('snc123...')
        result = self.exec_fun_command(cmdStr)
        return result
        
    '''
                登录nrapp执行桩函数
    '''
    def login_nrapp_exec_cmd(self, cmdStr):
        self.exec_fun_command('nrapp.sh')
        result = self.exec_fun_command(cmdStr)
        return result
    
        
if __name__ == '__main__':
    str = '''
nrtp_get_cpu_use return=0[K

nrtp> nrtp_get_cpu_use 14[K

nrtp_get_cpu_use return=0[K

        '''
    gnbModel().filter_cpu_ratio(str)