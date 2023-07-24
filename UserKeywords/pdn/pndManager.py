# coding = 'utf-8'
'''
Created on 2022年11月25日

@author: dj

'''
'''
    说明：登录pdn
    参数：
    pdnIp:pdn登录ip地址
    username:pdn ssh登录用户名
    password:pdn ssh登录密码
'''

import logging

import allure

from BasicService.pdn.pdnService import PdnService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time


def key_pdn_login(pdnIp=BASIC_DATA['pdn']['pdnSshIp'], username=BASIC_DATA['pdn']['pdnUsername'], password=BASIC_DATA['pdn']['pdnPassword']):
    with allure.step(key_get_time() +": 登录pdn服务器: "+pdnIp):
        logging.info(key_get_time()+': login pdn server: '+pdnIp)
        pdn = PdnService().pdn_login(pdnIp, username, password)
        return pdn

'''
            说明：登出pdn
            参数：
'''
def key_pdn_logout(pdn):
    with allure.step(key_get_time() +": 登出pdn服务器 "):
        logging.info(key_get_time()+': logout pdn server')
        PdnService().pdn_logout(pdn)

'''
    说明：启动端口监听进程
    参数：
    pdn:pdn对象
    port:监听端口
    waitTime:命令执行后的等待时间
'''     
def key_start_listen_port(pdn, port, iperfType='iperf3', waitTime=1):
    with allure.step(key_get_time() +": 启动pdn端口监听进程, 端口: "+str(port)):
        logging.info(key_get_time()+': start pdn server port listening, port: '+str(port))
        result = PdnService().start_listening_port(pdn, port, iperfType, waitTime)
        return result

'''
    说明：停止端口监听进程
    参数：
    pdn:pdn对象
    port:监听端口
''' 
def key_stop_listen_port(pdn, port, iperfType='iperf'):
    with allure.step(key_get_time() +": 停止pdn端口监听进程, 端口: "+str(port)):
        logging.info(key_get_time()+': stop pdn server port listening, port: '+str(port))
        PdnService().kill_iperf_process(pdn, port, iperfType)
        
'''
    说明：启动iperf进程-tcp
    参数：
'''     
def key_start_iperf_command_tcp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):
    with allure.step(key_get_time() +": pdn端启动iperf灌包进程[tcp] "):
        logging.info(key_get_time()+': pdn start iperf process[tcp]')
        result = PdnService().start_iperf_command_tcp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
        return result
    
'''
    说明：启动iperf进程-tcp 上行
    参数：
'''     
def key_start_iperf_command_tcp_ul(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):
    with allure.step(key_get_time() +": pdn端启动iperf灌包进程[tcp_ul] "):
        logging.info(key_get_time()+': pdn start iperf process[tcp_ul]')
        result = PdnService().start_iperf_command_tcp_ul(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType)
        return result
    
'''
    说明：启动iperf进程-udp
    参数：
'''     
def key_start_iperf_command_udp(pdn, phoneId, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):
    with allure.step(key_get_time() +": pdn端启动iperf灌包进程[udp] "):
        logging.info(key_get_time()+': pdn start iperf process[udp]')
        result = PdnService().start_iperf_command_udp(pdn, phoneId, packageSize, monitorPort, processNum, spanTime, iperfType)
        return result
    
'''
    说明：启动iperf进程-udp
    参数：
'''     
def key_start_iperf_command_udp_ul(pdn, phoneId, packageSize, monitorPort, processNum, spanTime, iperfType='iperf'):
    with allure.step(key_get_time() +": pdn端启动iperf灌包进程[udp_ul] "):
        logging.info(key_get_time()+': pdn start iperf process[udp_ul]')
        result = PdnService().start_iperf_command_udp_ul(pdn, phoneId, packageSize, monitorPort, processNum, spanTime, iperfType)
        return result