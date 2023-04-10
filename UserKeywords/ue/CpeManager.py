'''
Created on 2022年9月23日

@author: dj
'''
'''
    SSH登录CPE
        参数：
    cpeIp:cpe ip地址
    username:cpe前台登录用户名
    passward:cpe前台登录密码
'''

import logging
import threading
from time import sleep

import allure

from BasicService.ue.cpeService import CpeService
from BasicService.ue.logAnalyzeService import LogAnalyzeService
from BasicService.ue.qutsService import QutsService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.pdn.pndManager import key_start_listen_port, \
    key_stop_listen_port, key_pdn_login


def key_cpe_login(cpeIp=BASIC_DATA['cpe']['cpeSshIp'], username=BASIC_DATA['cpe']['cpeUsername'], password=BASIC_DATA['cpe']['cpePassword']):
    with allure.step(key_get_time() +": 登录CPE前台\n"):
        logging.info(key_get_time()+': login cpe command model')
        cpe = CpeService().cpe_login(cpeIp, username, password)
        assert cpe != None, 'cpe登录失败，请检查！'
        return cpe

'''
    SSH登出CPE
        参数：
'''    
def key_cpe_logout(cpe):
    with allure.step(key_get_time() +": 登出CPE前台\n"):
        logging.info(key_get_time()+': logout cpe command model')
        CpeService().cpe_logout(cpe)
         
'''
    CPE接入
        参数：    
'''
def key_cpe_attach(cpe, tryNum=3):
    with allure.step(key_get_time() +": cpe执行attach命令\n"):
        logging.info(key_get_time()+': exec attach command')
        for i in range (1,tryNum):
            result = CpeService().cpe_attach(cpe)
            if result == 'OK':
                break
            else:
                logging.warning(key_get_time()+': exec attach command abnormal, wait for 3s try again.')
                key_wait(3)
        return result

'''
    CPE去接入
        参数：    
'''         
def key_cpe_detach(cpe):
    with allure.step(key_get_time() +": cpe执行detach命令\n"):
        logging.info(key_get_time()+': exec detach command')
        result = CpeService().cpe_detach(cpe)
        return result

'''
    查询CPE接入小区信息
    参数：  cpe对象  
'''    
def key_cpe_attach_cell_info(cpe):
    with allure.step(key_get_time() +": 查询cpe驻留状态及小区信息\n"):
        logging.info(key_get_time()+': exec c5greg command, query cpe\'s cell info')
        ueAttach, cellId = CpeService().query_cpe_access_cell_info(cpe)
        with allure.step(key_get_time()+': ['+cpe.ip+'] cpe attach status is[1:attach;2:not attach]: '+str(ueAttach)+'\n'):
            logging.info(key_get_time()+': ['+cpe.ip+'] cpe attach status is: '+str(ueAttach))
        if ueAttach == '1':
            return cellId
        else:
            return -1
        

'''
    CPE ping包测试
        参数： 
    pdnIp:pdn ip地址
    pingNum:ping包测试次数
    tryNum:链路不稳定时，ping包尝试次数
    ping_interface:cpe ping包网卡
    log_save_path:ping包log记得路径
'''      
def key_cpe_ping(cpe, pdnIp=BASIC_DATA['pdn']['pdnIp'], pingNum=BASIC_DATA['ping']['pingNum'], pingInterface = BASIC_DATA['cpe']['pingNrInterface'], log_save_path=BASIC_DATA['ping']['logSavePath'], tryNum =5, pingSize=BASIC_DATA['ping']['pingSize']):
    with allure.step(key_get_time() +": 执行ping包命令, 端口："+pingInterface):
        logging.info(key_get_time()+': exec ping command, interface: '+pingInterface)
        for i in range (1, tryNum+1):
            min, avg, max, transmitted, received, lossrate = CpeService().cpe_ping_test(cpe, pdnIp, pingNum, pingInterface, pingSize)
            if avg != -1:
                break
        with allure.step(key_get_time()+': Cpe['+cpe.ip+'_'+pingInterface+'] ping result[max/avg/min/transmitted/received/loss rate] = '+str(max)+"/"+str(avg)+"/"+str(min)+"/"+str(transmitted)+"/"+str(received)+"/"+str(lossrate)+"\n"):
            logging.info(key_get_time()+': Cpe['+cpe.ip+'_'+pingInterface+'] ping result[max/avg/min/transmitted/received/loss rate] = '+str(max)+"/"+str(avg)+"/"+str(min)+"/"+str(transmitted)+"/"+str(received)+"/"+str(lossrate))
#         assert avg != -1,'ping包测试不通过，请检查'
        return lossrate, avg

'''
    复位cpe
        参数：
    cpe:cpe对象 
''' 
def key_reboot_cpe(cpe):
    with allure.step(key_get_time()+': 复位cpe\n'):
        logging.info(key_get_time()+': reboot cpe')
        rebootRes = CpeService().reboot_cpe(cpe)
        assert rebootRes=='success','cpe复位执行异常，请检查！'
      
    
'''
    确认pdu建立成功
        参数：
    cpe:cpe对象 
''' 
def key_confirm_pdu_setup_succ(cpe, tryNum = 50):
    with allure.step(key_get_time()+': 确认pdu创建成功\n'):
        logging.info(key_get_time()+': confirm if pdu setup success')
        for i in range (1, tryNum):
            setupRes = CpeService().confirm_pdu_setup(cpe)
            if setupRes == 'success':
                break
            else:
                logging.warning('pdu setup failure, wait for 5s try again!')
                key_wait(5)
        return setupRes
  
'''
    确认pdu建立成功
        参数：
    cpe:cpe对象 
''' 
def key_confirm_pdu_setup_fail(cpe, tryNum = 80):
    with allure.step(key_get_time()+': 确认pdu创建失败\n'):
        logging.info(key_get_time()+': confirm if pdu setup failure')
        for i in range (1, tryNum):
            setupRes = CpeService().confirm_pdu_setup(cpe)
            if setupRes == 'failure':
                break
            else:
                logging.warning('pdu setup success, wait for 5s try again!')
                key_wait(5)
        return setupRes  
  
'''
    CPE进入AT命令模式
        参数： 
'''    
def key_cpe_login_at_model(cpe):
    with allure.step(key_get_time() +": 登录cpe AT模式\n"):
        logging.info(key_get_time()+': login cpe AT model')
        CpeService().login_at_model(cpe)

'''
    CPE退出AT命令模式
        参数： 
'''        
def key_cpe_logout_at_model(cpe):
    with allure.step(key_get_time() +": 登出cpe AT模式\n"):
        logging.info(key_get_time()+': logout cep AT model')
        CpeService().logout_at_model(cpe)

'''
        下行udp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''            
def key_dl_udp_wifi_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['udpDlSize'], monitorPort=BASIC_DATA['flow']['wifiDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 下行UDP流量测试"):
        logging.info(key_get_time()+': exec DL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'udp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'udp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_DL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='WIFI')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL UDP Wifi test result:\n'+dlTrafRes)
            
'''
        下行udp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''            
def key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['udpDlSize'], monitorPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 下行UDP流量测试"):
        logging.info(key_get_time()+': exec DL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'udp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'udp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_DL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL UDP NR test result:\n'+dlTrafRes)
            
'''
        上行udp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''       
def key_ul_udp_wifi_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['udpUlSize'],monitorPort=BASIC_DATA['flow']['wifiUlPort'], processNum =BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上行UDP流量测试"):
        logging.info(key_get_time()+': exec UL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'udp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'udp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_UL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'UL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='WIFI')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL UDP Wifi test result:\n'+ulTrafRes)

'''
        上行udp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''       
def key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['udpUlSize'],monitorPort=BASIC_DATA['flow']['nrUlPort'], processNum =BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上行UDP流量测试"):
        logging.info(key_get_time()+': exec UL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'udp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'udp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_UL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'UL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL UDP NR test result:\n'+ulTrafRes)
            
'''
        下行tcp wifi灌包
        参数：
    cpePcIp:cpe直连PC的 ip地址 
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''       
def key_dl_tcp_wifi_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpDlSize'],monitorPort=BASIC_DATA['flow']['wifiDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 下行TCP流量测试"):
        logging.info(key_get_time()+': exec DL WIFI TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'tcp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.warning(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_DL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='WIFI')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP Wifi test result:\n'+dlTrafRes)
            
'''
        下行tcp nr灌包
        参数：
    cpePcIp:cpe直连PC的 ip地址 
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''       
def key_dl_tcp_nr_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpDlSize'],monitorPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 下行TCP流量测试"):
        logging.info(key_get_time()+': exec DL NR TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'tcp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_DL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter', spanTime=spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP NR test result:\n'+dlTrafRes)
    
'''
        上行tcp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_ul_tcp_wifi_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorPort=BASIC_DATA['flow']['wifiUlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上行TCP流量测试"):
        logging.info(key_get_time()+': exec UL TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'WIFI', 'tcp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_UL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'UL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='WIFI')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP Wifi test result:\n'+ulTrafRes)
            
'''
        上行tcp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_ul_tcp_nr_flow_test(cpe, pdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorPort=BASIC_DATA['flow']['nrUlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上行TCP流量测试"):
        logging.info(key_get_time()+': exec UL TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(cpe, monitorPort, 'NR', 'tcp', 'ipv4')
            if bindRes == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_UL(cpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(cpe, enbDebugIp, pcIp, scrapFileName, dir = 'UL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP NR test result:\n'+ulTrafRes)
        
'''
        上下行tcp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_udl_tcp_nr_flow_test(ulCpe, dlCpe, ulPdn, dlPdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorUlPort=BASIC_DATA['flow']['nrUlPort'], monitorDlPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上下行TCP流量测试"):
        logging.info(key_get_time()+': exec UDL TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'NR', 'tcp', 'ipv6')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'NR', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'NR', 'tcp', 'ipv4')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'NR', 'tcp', 'ipv4')
            if bindRes == True and bindRes2 == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(ulPdn, monitorUlPort)
        key_start_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_UL(ulCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorUlPort, processNum, spanTime=spanTime)
            CpeService().cpe_tcp_flow_DL(dlCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorDlPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(ulCpe, enbDebugIp, pcIp, scrapFileName, dir = 'UDL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='NR')
        key_stop_listen_port(ulPdn, monitorUlPort)
        key_stop_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP NR test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP NR test result:\n'+dlTrafRes)

'''
        上下行tcp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_udl_tcp_wifi_flow_test(ulCpe, dlCpe, ulPdn, dlPdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorUlPort=BASIC_DATA['flow']['nrUlPort'], monitorDlPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上下行TCP流量测试"):
        logging.info(key_get_time()+': exec UDL TCP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'WIFI', 'tcp', 'ipv6')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'WIFI', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'WIFI', 'tcp', 'ipv4')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'WIFI', 'tcp', 'ipv4')
            if bindRes == True and bindRes2 == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(ulPdn, monitorUlPort)
        key_start_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_tcp_flow_UL(ulCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorUlPort, processNum, spanTime=spanTime)
            CpeService().cpe_tcp_flow_DL(dlCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorDlPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(ulCpe, enbDebugIp, pcIp, scrapFileName, dir = 'UDL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='WIFI')
        key_stop_listen_port(ulPdn, monitorUlPort)
        key_stop_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP WIFI test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP WIFI test result:\n'+dlTrafRes)
            
'''
        上下行udp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_udl_udp_nr_flow_test(ulCpe, dlCpe, ulPdn, dlPdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorUlPort=BASIC_DATA['flow']['nrUlPort'], monitorDlPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上下行UDP流量测试"):
        logging.info(key_get_time()+': exec UDL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'NR', 'tcp', 'ipv6')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'NR', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'NR', 'tcp', 'ipv4')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'NR', 'tcp', 'ipv4')
            if bindRes == True and bindRes2 == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(ulPdn, monitorUlPort)
        key_start_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_UL(ulCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorUlPort, processNum, spanTime=spanTime)
            CpeService().cpe_udp_flow_DL(dlCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorDlPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(ulCpe, enbDebugIp, pcIp, scrapFileName, dir = 'UDL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='NR')
        key_stop_listen_port(ulPdn, monitorUlPort)
        key_stop_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP NR test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP NR test result:\n'+dlTrafRes)

'''
        上下行tcp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
'''        
def key_udl_udp_wifi_flow_test(ulCpe, dlCpe, ulPdn, dlPdn, cpePcIp=BASIC_DATA['flow']['cpePcIp'], iperfPath=BASIC_DATA['flow']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['flow']['localPcIp'], scrapFileName=BASIC_DATA['flow']['scrapFileName'], packageSize=BASIC_DATA['flow']['tcpUlSize'],monitorUlPort=BASIC_DATA['flow']['nrUlPort'], monitorDlPort=BASIC_DATA['flow']['nrDlPort'], processNum=BASIC_DATA['flow']['processNum'], spanTime=BASIC_DATA['flow']['spanTime']):
    with allure.step(key_get_time() +": 上下行UDP流量测试"):
        logging.info(key_get_time()+': exec UDL UDP traffic test')
        with allure.step(key_get_time() +": 添加端口过滤规则"):
            logging.info(key_get_time()+': add port rule')
            if ':' in pdnIp:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'WIFI', 'tcp', 'ipv6')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'WIFI', 'tcp', 'ipv6')
            else:
                bindRes = CpeService().binding_port_and_network(ulCpe, monitorUlPort, 'WIFI', 'tcp', 'ipv4')
                bindRes2 = CpeService().binding_port_and_network(ulCpe, monitorDlPort, 'WIFI', 'tcp', 'ipv4')
            if bindRes == True and bindRes2 == True:
                logging.info(key_get_time()+': binding port rule success!')
            else:
                logging.info(key_get_time()+': binding port rule failure!')
        key_start_listen_port(ulPdn, monitorUlPort)
        key_start_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command')
            CpeService().cpe_udp_flow_UL(ulCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorUlPort, processNum, spanTime=spanTime)
            CpeService().cpe_udp_flow_DL(dlCpe, cpePcIp, iperfPath, pdnIp, packageSize, monitorDlPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data')
            dlTrafRes,ulTrafRes = CpeService().cell_flow_analyze(ulCpe, enbDebugIp, pcIp, scrapFileName, dir = 'UDL', pcNetworkCardName ='TP-Link Gigabit PCI Express Adapter',spanTime=spanTime, type='WIFI')
        key_stop_listen_port(ulPdn, monitorUlPort)
        key_stop_listen_port(dlPdn, monitorDlPort)
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': UL TCP WIFI test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': DL TCP WIFI test result:\n'+dlTrafRes)

'''
           功能：启动ue log跟踪
'''
def key_start_ue_log_trace():
    with allure.step(key_get_time()+': 启动ue log跟踪'):
        logging.info(key_get_time()+': start ue log trace')
        dev_manager, qxdm_window, diagService = QutsService().startUeLogTrace()
        return dev_manager, qxdm_window, diagService

'''
           功能：停止ue log跟踪
           参数：
'''
def key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 停止ue log跟踪'):
        logging.info(key_get_time()+': stop ue log trace')
        logFilePath = QutsService().stopUeLogTrace(dev_manager, qxdm_window, diagService, logSavePath)
        return logFilePath

'''
           功能：pdcch时隙配置参数校验
           参数：
        logFilePath：ue log文件路径
        symbolNumber：时隙配置参数
'''    
def key_pdcch_symbol_number_analyze(symbolNumber='Adaptive', ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PDCCH时隙配置参数校验'):
        logging.info(key_get_time()+': PDCCH symbol number params analyze')
        attrDict = {
            'duration':'1',
            'monitoringSymbolsWithinSlot':'\'10000000 000000\'B'
        }
        resultDict = LogAnalyzeService().rrc_reconfiguration(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['duration'] == True and resultDict['monitoringSymbolsWithinSlot'] == True:
            return True
        else:
            return False

'''
           功能：pdcch cce聚合等级
           参数：
        logFilePath：ue log文件路径
        cceLevel：cce聚合等级
'''     
def key_pdcch_cce_level_analyze(cceLevel, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PDCCH CCE等级参数检验'):
        logging.info(key_get_time()+': PDCCH CCE level params analyze')
        typeDict = {'CCE_4':'LEVEL_4', 'CCE_8':'LEVEL_8', 'CCE_16':'LEVEL_16'}
        attrDLDict = {
            'dciFormat':'DL_1_1',
            'aggregationLevel':typeDict[cceLevel]
        }
        attrULDict = {
            'dciFormat':'UL_0_1',
            'aggregationLevel':typeDict[cceLevel]
        }
        resultDLDict = LogAnalyzeService().nr5g_mac_dci_info_analyze(ueLogFilePath, attrDLDict)
        resultULDict = LogAnalyzeService().nr5g_mac_dci_info_analyze(ueLogFilePath, attrULDict)
        logging.info(key_get_time()+': check DL result is:'+str(resultDLDict))
        logging.info(key_get_time()+': check UL result is:'+str(resultULDict))
        if resultDLDict == {} or resultULDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDLDict['dciFormat'] == True and resultDLDict['aggregationLevel'] == True and resultULDict['dciFormat'] == True and resultULDict['aggregationLevel'] == True:
            return True
        else:
            return False
        
'''
           功能：pdcch cce聚合等级
           参数：
        logFilePath：ue log文件路径
        transferFormat：传输格式
'''     
def key_pdcch_transfer_formate_analyze(transferFormat, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PDCCH传输格式参数检验'):
        logging.info(key_get_time()+': PDCCH transfer format params analyze')
        transferFormatDict = {'Format0_0':'dci-Format0-0-AndFormat1-0',
                              'Format0_1':'dci-Format0-1-AndFormat1-1',
                              'Format1_0':'dci-Format0-0-AndFormat1-0',
                              'Format1_1':'dci-Format0-1-AndFormat1-1'}
        attrDict = {
            'dciFormate':transferFormatDict[transferFormat],
        }
        checkRes = LogAnalyzeService().system_information_block_type1_analyze(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(checkRes))
        if checkRes == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if checkRes['dciFormate'] == True:
            return True
        else:
            return False
        
'''
           功能：pdsch调度参数
           参数：
        logFilePath：ue log文件路径
        mcs：mcs值
'''     
def key_pdsch_mcs_analyze(mcs, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PDSCH调度参数校验，参数值：'+str(mcs)):
        logging.info(key_get_time()+': PDSCH mcs params analyze')
        if mcs>=0 and mcs <5:
            mcsTable='qpsk'
        elif mcs >=5 and mcs <11:
            mcsTable='qam16'
        elif mcs >=11 and mcs <20:
            mcsTable='qam64'
        elif mcs >=20 and mcs <= 28:
            mcsTable='qam256'
        attrDict = {
            'resourceAllocation':'resourceAllocationType1',
            'rbg-Size':'config1',
            'mcs-Table':mcsTable
        }
        checkRes = LogAnalyzeService().rrc_reconfiguration(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(checkRes))
        if checkRes == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if checkRes['mcs-Table'] == True:
            return True
        else:
            return False
        
'''
           功能：prach配置索引参数
           参数：
        logFilePath：ue log文件路径
        index：索引值
'''     
def key_prach_config_index_analyze(index, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PRACH配置索引参数校验，参数值：'+str(index)):
        logging.info(key_get_time()+': PRACH config index params analyze, index:'+str(index))
        if index >= 145 and index <= 167 :
            preambleFormat='FORMAT_B4'
        elif index >= 189 and index <= 210:
            preambleFormat='FORMAT_C2'
        attrDict = {
            'prachConfig':str(index),
            'preambleFormat':preambleFormat
        }
        checkRes = LogAnalyzeService().nr5g_mac_rach_attempt_analyze(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(checkRes))
        if checkRes == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if checkRes['prachConfig'] == True and checkRes['preambleFormat'] == True:
            return True
        else:
            return False
        
'''
           功能：pucch支持format1格式
           参数：
        logFilePath：ue log文件路径
        formatType：format类型--format1/format3
'''     
def key_pucch_support_format_analyze(formatType, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': PUCCH支持格式校验，格式值：'+formatType):
        logging.info(key_get_time()+': PUCCH support format, format:'+formatType)
        
        resultDict = LogAnalyzeService().dl_ccch_rrc_setup_analyze(ueLogFilePath)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict[formatType] == True:
            return True
        else:
            return False
        
'''
           功能：支持PUCCH format1和format3时隙内跳频
           参数：
        logFilePath：ue log文件路径
'''     
def key_pucch_support_format1_format3_hop_analyze(ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持PUCCH format1和format3时隙内跳频'):
        logging.info(key_get_time()+': support PUCCH format1 hop and format3 hop')
        resultDict = LogAnalyzeService().nr5g_mac_ul_physical_channel_schedule_analyze(ueLogFilePath)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['Format1_Hop'] == True and resultDict['Format3_Hop'] == True:
            return True
        else:
            return False

'''
           功能：支持DMRS Mapping Type A
           参数：
        logFilePath：ue log文件路径
'''     
def key_support_dmrs_mapping_type_a(ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持DMRS Mapping Type A'):
        logging.info(key_get_time()+': support DMRS mapping type A')
        resultDict = LogAnalyzeService().dl_ccch_rrc_setup_analyze(ueLogFilePath)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['dmrs dl type'] == True and resultDict['dmrs ul type'] == True:
            return True
        else:
            return False 
        
'''
           功能：支持DL DMRS Type 1
           参数：
        logFilePath：ue log文件路径
'''     
def key_support_dl_dmrs_type1(ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持DL DMRS Type1'):
        logging.info(key_get_time()+': support DL DMRS type1')
        resultDict = LogAnalyzeService().dl_ccch_rrc_setup_analyze(ueLogFilePath)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['dmrs dl type1'] == True:
            return True
        else:
            return False

'''
           功能：支持UL DMRS Type 1
           参数：
        logFilePath：ue log文件路径
'''     
def key_support_ul_dmrs_type1(ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持UL DMRS Type1'):
        logging.info(key_get_time()+': support UL DMRS type1')
        resultDict = LogAnalyzeService().dl_ccch_rrc_setup_analyze(ueLogFilePath)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['dmrs ul type1'] == True:
            return True
        else:
            return False       
        
'''
           功能：支持单端口CSI-RS配置用于时频同步
           参数：
        logFilePath：ue log文件路径
'''     
def key_support_csi_rs(trsPeriod, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持单端口CSI-RS配置用于时频同步'):
        logging.info(key_get_time()+': support CSI-RS config')
        attrDict = {
            'trsPeriod':trsPeriod.lower(),
        }
        resultDict = LogAnalyzeService().rrc_reconfiguration(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['trsPeriod'] == True:
            return True
        else:
            return False
        
'''
           功能：校验smtc周期配置
           参数：
        logFilePath：ue log文件路径
'''     
def key_sib2_smtc_analyze(smtcPeriod, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持smtc周期配置'):
        logging.info(key_get_time()+': support smtc period config')
        analyRes = LogAnalyzeService().sib2_smtc_analyze(ueLogFilePath, smtcPeriod)
        logging.info(key_get_time()+': check result is:'+str(analyRes))
        return analyRes
    
'''
           功能：校验ssb周期配置
           参数：
        logFilePath：ue log文件路径
'''     
def key_sib1_ssb_period_analyze(ssbPeriod, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+': 支持ssb周期配置'):
        logging.info(key_get_time()+': support ssb period config')
        analyRes = LogAnalyzeService().sib1_ssb_period_analyze(ueLogFilePath, ssbPeriod)
        logging.info(key_get_time()+': check result is:'+str(analyRes))
        return analyRes
               
'''
           功能：校验ssb频率配置
           参数：
        logFilePath：ue log文件路径
'''     
def key_ssb_frequenty_position_analyze(ssbFreqPos, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验ssb频率位置配置'):
        logging.info(key_get_time()+':check ssb frequency position config')
        resultDict = LogAnalyzeService().nr5g_rrc_mib_info_analyze(ueLogFilePath, ssbFreqPos)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['DL Frequency'] == True:
            return True
        else:
            return False


'''
           功能：校验prach功率初始值和功率调整步长 
           参数：
        logFilePath：ue log文件路径
        preambleReceivedTargetPower：功率初始值
        powerRampingStep：功率调整步长
'''     
def key_pre_rx_power_and_power_ramp_analyze(preambleReceivedTargetPower, powerRampingStep, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验功率初始值和功率调整步长参数是否生效'):
        logging.info(key_get_time()+':check pre rx power and power ramp')
        attrDict = {'preambleReceivedTargetPower':preambleReceivedTargetPower, 'powerRampingStep':powerRampingStep}
        resultDict = LogAnalyzeService().system_information_block_type1_analyze(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['preambleReceivedTargetPower'] == True and resultDict['powerRampingStep'] == True:
            return True
        else:
            return False
                
'''
           功能：校验P0 Nominal 
           参数：
        logFilePath：ue log文件路径
'''     
def key_po_nominal_pusch_analyze(poNominal, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验p0 nominal配置参数'):
        logging.info(key_get_time()+':check po nominal config')
        attrDict = {'p0NominalPusch':poNominal}
        resultDict = LogAnalyzeService().system_information_block_type1_analyze(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['p0NominalPusch'] == True:
            return True
        else:
            return False

'''
           功能：校验Path Loss Coefficient 
           参数：
        logFilePath：ue log文件路径
'''     
def key_path_loss_coefficient_analyze(alpha, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验Path Loss Coefficient参数'):
        logging.info(key_get_time()+':check path loss coefficient config')
        checkDict = {'alpha':alpha}
        resultDict = LogAnalyzeService().rrc_setup_alpha_analyze(ueLogFilePath, checkDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['alpha'] == True:
            return True
        else:
            return False      

'''
           功能：校验prach功率初始值和功率调整步长 
           参数：
        logFilePath：ue log文件路径
        preambleReceivedTargetPower：功率初始值
        powerRampingStep：功率调整步长
'''     
def key_system_info_parameter_analyze(subcarrierSpacing, nrofDownlinkSlots, nrofDownlinkSymbols, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验功率初始值和功率调整步长参数是否生效'):
        logging.info(key_get_time()+':check pre rx power and power ramp')
        attrDict = {
            'subcarrierSpacing':subcarrierSpacing,
            'nrofDownlinkSlots':nrofDownlinkSlots,
            'nrofDownlinkSymbols':nrofDownlinkSymbols
            }
        resultDict = LogAnalyzeService().system_information_block_type1_analyze(ueLogFilePath, attrDict)
        logging.info(key_get_time()+': check result is:'+str(resultDict))
        if resultDict == {}:
            logging.info(key_get_time()+': ue log not contain the params!')
            return False
        if resultDict['subcarrierSpacing'] == True and resultDict['nrofDownlinkSlots'] == True and resultDict['nrofDownlinkSymbols'] == True:
            return True
        else:
            return False

'''
           功能：校验csi-rs功率
           参数：
        logFilePath：ue log文件路径
        csiRsPowerOffset：功率初始值
'''     
def key_csi_rs_power_analyze(csiRsPowerOffset, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验CSI-RS功率配置参数是否生效'):
        logging.info(key_get_time()+':check csi-rs power')
        result = LogAnalyzeService().csi_rs_power_analyze(ueLogFilePath, csiRsPowerOffset)
        return result
    
'''
           功能：校验pusch资源分配类型 
           参数：
        logFilePath：ue log文件路径
        puschAllocType：pusch资源分配类型
'''     
def key_pusch_resource_allocation_type_analyze(puschAllocType, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验pusch资源分配类型参数是否生效'):
        logging.info(key_get_time()+':check pusch resource allocation type')
        result = LogAnalyzeService().pusch_res_allocation_type_analyze(ueLogFilePath, puschAllocType)
        return result
    
'''
           功能：校验pdsch资源分配类型 
           参数：
        logFilePath：ue log文件路径
        pdschAllocType：pdsch资源分配类型
'''     
def key_pdsch_resource_allocation_type_analyze(pdschAllocType, ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验pdsch资源分配类型参数是否生效'):
        logging.info(key_get_time()+':check pdsch resource allocation type')
        result = LogAnalyzeService().pdsch_res_alloca_type_analyze(ueLogFilePath, pdschAllocType)
        return result
    
'''
           功能：校验pdsch资源分配类型 
           参数：
        logFilePath：ue log文件路径
        pdschAllocType：pdsch资源分配类型
'''     
def key_pucch_channel_feedback_per_bandwith_analyze(ueLogFilePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time()+':校验pdsch资源分配类型参数是否生效'):
        logging.info(key_get_time()+':check pdsch resource allocation type')
        result = LogAnalyzeService().pucch_channel_feedback_per_bandwith_analyze(ueLogFilePath)
        return result
    
if __name__ == '__main__':
    dlCpe = key_cpe_login()
    ulCpe = key_cpe_login()
    dlPdn = key_pdn_login()
    ulPdn = key_pdn_login()
#     key_dl_tcp_nr_flow_test(cpe, pdn)
    key_udl_tcp_nr_flow_test(ulCpe, dlCpe, ulPdn, dlPdn)
#     start_cell_traffic_test(cpe, 'UDL', 'NR')
#     sleep(240)