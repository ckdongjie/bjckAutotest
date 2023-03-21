# coding= 'utf-8'
'''
Created on 2022年11月17日

@author: dj

'''


import logging
import allure

from BasicService.gnb.gnbService import gnbService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
            说明：登录gnb
            参数：
    gnbIp:基站debug ip
    username:登录用户名
    password:登录密码
''' 
def key_ssh_login_gnb(gnbIp=BASIC_DATA['weblmt']['ip'], username=BASIC_DATA['gnb']['username'], password=BASIC_DATA['gnb']['password']):
    with allure.step(key_get_time() +": ssh登录基站\n"):
        logging.info(key_get_time()+': login gnb by ssh.')
        gnb = gnbService().ssh_login_gnb(gnbIp, username, password)
        return gnb

'''
        说明：查询gps md5值
        参数：
    gnb:gnb对象
''' 
def key_query_gps_md5_value(gnb):
    with allure.step(key_get_time() +": 查询基站gps md5值\n"):
        logging.info(key_get_time()+': query gps md5 value.')
        md5val = gnbService().check_gps_md5(gnb)
        return md5val
        
'''
        说明：查询nrsys、uboot版本
        参数：
    gnb:gnb对象
'''
def key_query_nrsys_version(gnb):
    with allure.step(key_get_time() +": 查询基站nrsys/uboot版本信息\n"):
        logging.info(key_get_time()+': query nrsys/uboot version.')
        ubootRes, nrsysRes = gnbService().query_nrsys_version(gnb)
        return ubootRes, nrsysRes
    
'''
        说明：打开log打印开关
        参数：
    gnb:gnb对象
'''
def key_open_log_print_switch(gnb):
    with allure.step(key_get_time() +": 打开基站log打印开关\n"):
        logging.info(key_get_time()+': open gnb log print switch.')
        gnbService().open_log_switch(gnb)
        
'''
        说明：基站侧执行抓包命令
        参数：
    gnb:gnb对象
'''
def key_capture_package_on_gnb(gnb, filePath='/'):
    with allure.step(key_get_time() +": 基站侧执行抓包命令\n"):
        logging.info(key_get_time()+': capture package on gnb.')
        gnbService().capture_package_on_gnb(gnb, filePath)

'''
        说明：禁用dpdk0网卡
        参数：
    gnb:gnb对象
'''
def key_forbid_dpdk0(gnb):
    cmdStr = 'ifconfig dpdk0 down'
    with allure.step(key_get_time() +": 执行命令禁用dpdk0网卡\n"):
        logging.info(key_get_time()+': exec command forbidden dpdk0')
        gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：启用dpdk0网卡
        参数：
    gnb:gnb对象
'''
def key_unforbid_dpdk0(gnb):
    cmdStr = 'ifconfig dpdk0 up'
    with allure.step(key_get_time() +": 执行命令禁用dpdk0网卡\n"):
        logging.info(key_get_time()+': exec command start using dpdk0')
        gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：基站前台执行桩函数
        参数：
    gnb:gnb对象
'''
def key_exec_command_on_gnb(gnb, cmdStr):
    with allure.step(key_get_time() +": 基站侧执行桩函数\n"):
        logging.info(key_get_time()+': exec command on gnb.')
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)

'''
        说明：手工升级cpld版本
        参数：
    gnb:gnb对象
    cpldVersion:cpdl版本号
    cpldPath:cpld版本存放目录
    enbType:V2/V4
'''
def key_upgrade_cpld_version(gnb, cpldVersion, cpldPath, enbType):
    with allure.step(key_get_time() +": 手工升级cpld版本\n"):
        logging.info(key_get_time()+': upgrade cpld version')
        upgradeRes = gnbService().upgrade_cpld_version(gnb, cpldVersion, cpldPath, enbType)
        logging.info(key_get_time()+': cpld upgrade result:'+upgradeRes)

if __name__ == '__main__':
    gnb = key_ssh_login_gnb('172.16.2.214', 'root', 'Web2022@Nr5gTech')
    key_query_nrsys_version(gnb)