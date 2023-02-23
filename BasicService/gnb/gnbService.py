# coding = 'utf-8'
'''
Created on 2022年11月17日

@author: dj
'''

import logging
from time import sleep
from BasicModel.gnb.gnbModel import gnbModel


class gnbService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
   
    def ssh_login_gnb(self, gnbDebIp, username, password):
        for i in range (1,10):
            gnbObj = gnbModel().ssh_login_gnb(gnbDebIp, username, password)
            if gnbObj != None:
                logging.info('ssh login gnb success, gnb: '+str(gnbObj))
                break
            else:
                logging.warning('ssh login gnb error')
                sleep(2)
        return gnbObj
    
    def logout_gnb(self, gnb):
        gnb.logout_gnb()
    
    '''
                登录nrapp
    '''     
    def login_nr_process(self, gnb, exptStr=''):
        gnb.login_nr_process(exptStr)
        
    '''
                基站上执行打开log打印开关
    '''    
    def open_log_switch(self, gnb, exptStr=''):
        gnb.open_log_switch(exptStr)
    
    '''
                基站上执行ping包命令
    '''    
    def ping_hms_server(self, gnb, hmsIp):
        gnb.exec_fun_command("ping "+hmsIp)
    
    '''
                基站上执行抓包命令
    '''    
    def capture_package_on_gnb(self, gnb, filePath='/'):
        gnb.capture_package_on_gnb(filePath) 
    
    '''
                基站上执行桩函数
    '''    
    def exec_command_on_gnb(self, gnb, cmdStr):
        result = gnb.exec_command_on_gnb(cmdStr) 
        return result
           
    '''
                查询基站gps文件的md5值
    '''
    def check_gps_md5(self, gnb):
        md5Val = gnb.check_gps_md5()
        logging.info('md5sum: '+md5Val)
        return md5Val
    
    '''
                    查询基站nrsys版本号
    '''
    def query_nrsys_version(self, gnb):
        ubootRes, nrsysRes = gnb.query_nrsys_version()
        logging.info('ubootRes: '+ubootRes+', nrsysRes: '+ nrsysRes)
        return ubootRes, nrsysRes
    
    '''
                    更新cpld版本号
    '''
    def upgrade_cpld_version(self, gnb, cpldVersion, cpldPath, enbType):
        upgradeRes = gnb.upgrade_cpld_version(cpldVersion, cpldPath, enbType)
        return upgradeRes
