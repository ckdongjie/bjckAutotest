# coding = utf-8
'''
Created on 2022年9月26日

@author: dj
'''
'''
        串口登录mate30
        参数：
    serialPort:串口端口号
    serialRate:串口通信比特率
    timeout:串口登录超时时间
'''

import logging

import allure

from BasicService.ue.mate30Service import mate30Service
from UserKeywords.basic.basic import key_get_time


def key_login_serial(serialPort='COM9', serialRate=115200, timeout = 30):
    with allure.step(key_get_time()+": 登录mate30串口\n"):
        logging.warning(key_get_time()+': login mate30')
        mate30 = mate30Service().login_serial(serialPort, serialRate, timeout)
        return mate30

'''
        串口登出mate30
        参数：
'''        
def key_logout_serial(mate30):
    with allure.step(key_get_time()+": 登出mate30串口\n"):
        logging.warning(key_get_time()+': logout mate30')
        mate30Service().logout_serial(mate30)

'''
    mate30执行attach
        参数：
'''        
def key_ue_attach(mate30):
    with allure.step(key_get_time()+": mate30执行attach命令\n"):
        logging.warning(key_get_time()+': exec attach on mate30')
        result = mate30Service().ue_attach(mate30)
        return result

'''
    mate30执行detach
        参数：
'''       
def key_ue_detach(mate30):
    with allure.step(key_get_time()+": mate30执行detach命令\n"):
        logging.warning(key_get_time()+': exec detach on mate30')
        result = mate30Service.ue_detach(mate30)
        return result

'''
    mate30查询驻留小区信息
        参数：
'''       
def key_query_attach_info(mate30):
    with allure.step(key_get_time()+": mate30驻留小区信息查询\n"):
        logging.warning(key_get_time()+': qury cell info on mate30')
        attachStatus, cellInfo = mate30Service().query_attach_info(mate30)
        return attachStatus, cellInfo
    

'''
    mate30执行ping包测试
        参数：
    pdn:pdn对象
    ueIp:ue ip地址，从pdn上执行ping命令
    pingNum:ping包次数
'''       
def key_mate30_ping_test(mate30, pdn, ueIp='190.1.169.96', pingNum=20):
    with allure.step(key_get_time()+": mate30执行ping包测试\n"):
        logging.warning(key_get_time()+': exec ping test on mate30')
        pingRes = mate30Service.mate30_ping_test(mate30, pdn, ueIp, pingNum)
        return pingRes

'''
    mate下行udp测试
        参数：
    pdn:pdn对象
    packageSize:包大小
    monitorPort:灌包端口
    processNum:进程个数
'''     
#PDN Send UDP Package To Ue(DL)
def key_send_udp_package_DL(mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
    with allure.step(key_get_time()+": mate30执行下行udp灌包测试\n"):
        logging.warning(key_get_time()+': exec DL udp test on mate30')
        updDlRes = mate30Service().send_udp_package_DL(mate30, pdnIp, packageSize, monitorPort, processNum)
        return updDlRes

'''
    mate上行udp测试
        参数：
    pdn:pdn对象
    packageSize:包大小
    monitorPort:灌包端口
    processNum:进程个数
'''
#Ue Send UDP Package To PDN(UL)
def key_send_udp_package_UL(mate30, pdnIp, packageSize='300m', monitorPort='5555', processNum = '3'):
    with allure.step(key_get_time()+": mate30执行上行udp灌包测试\n"):
        logging.warning(key_get_time()+': exec UL udp test on mate30')
        udpUlRes = mate30Service().send_udp_package_UL(mate30, pdnIp, packageSize, monitorPort, processNum)
        return udpUlRes
        
'''
    mate下行tcp测试
        参数：
    pdn:pdn对象
    packageSize:包大小
    monitorPort:灌包端口
    processNum:进程个数
'''        
#PDN Send TCP Package To Ue(DL)
def key_send_tcp_package_DL(mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
    with allure.step(key_get_time()+": mate30执行下行tcp灌包测试\n"):
        logging.warning(key_get_time()+': exec DL tcp test on mate30')
        tcpDlRes = mate30Service().send_tcp_package_DL(mate30, pdnIp, packageSize, monitorPort, processNum)
        return tcpDlRes

'''
    mate上行tcp测试
        参数：
    pdn:pdn对象
    packageSize:包大小
    monitorPort:灌包端口
    processNum:进程个数
'''    
#Ue Send TCP Package To PDN(UL)
def key_send_tcp_package_UL(mate30, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
    with allure.step(key_get_time()+": mate30执行上行tcp灌包测试\n"):
        logging.warning(key_get_time()+': exec UL tcp test on mate30')
        tcpUlRes = mate30Service().send_tcp_package_UL(mate30, pdnIp, packageSize, monitorPort, processNum)
        return tcpUlRes