# coding = 'utf-8'
'''
Created on 2023年4月20日
@author: autotest


'''


import logging

import allure
from BasicService.maintenanceTool.maintenanceToolService import MaintenanceToolService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
        功能：连接sv基本信息工具
        参数：
        debugIp:基站debugIp
'''
def key_connect_sv_basic_tool(debugIp=BASIC_DATA['weblmt']['ip'], svBasicPort=16666):
    with allure.step(key_get_time() +": 连接sv基本信息工具"):
        logging.info(key_get_time()+': connect sv basic tool')
        svBasicSocket = MaintenanceToolService().connect_sv_basic_tool(debugIp, svBasicPort)
        return svBasicSocket
    
'''
        功能：连接sv详细信息工具
        参数：
        debugIp:基站debugIp
'''
def key_connect_sv_detail_tool(debugIp=BASIC_DATA['weblmt']['ip'], svDetailPort=16667):
    with allure.step(key_get_time() +": 连接sv详细信息工具"):
        logging.info(key_get_time()+': connect sv detail tool')
        svDetailSocket = MaintenanceToolService().connect_sv_detail_tool(debugIp, svDetailPort)
        return svDetailSocket
    
'''
        功能：连接signal工具
        参数：
        debugIp:基站debugIp
'''        
def key_connect_signal_tool(debugIp=BASIC_DATA['weblmt']['ip'], localIp=BASIC_DATA['traffic']['localPcIp']):
    with allure.step(key_get_time() +": 连接信令跟踪工具"):
        logging.info(key_get_time()+': connect signal tool')
        sigSocket = MaintenanceToolService().connect_signal_tool(debugIp, localIp)
        return sigSocket

'''
        功能：关闭连接
        参数：
        Socket:socket对象
''' 
def key_disconnect_tool(Socket):
    with allure.step(key_get_time() +": 关闭socket连接"):
        logging.info(key_get_time()+': disconnect socket')
        MaintenanceToolService().disconnect_tool(Socket)
    
'''
        功能：开始捕获网口数据
        参数：
        interfaceName:网卡名称，与debugIp通信的网卡
'''
def key_start_capture_data(interfaceName=BASIC_DATA['traffic']['pcNetworkCardName']):
    with allure.step(key_get_time() +": 启动网络抓包程序"):
        logging.info(key_get_time()+': start capture process')
        MaintenanceToolService().start_capture_data(interfaceName)

'''
        功能： 停止捕获网口数据并保存文件
        参数：
        packetSaveName:抓包数据存在文件名
'''    
def key_stop_capture_data(packetSaveName='autoTool.pcap', isSaveSig=BASIC_DATA['maintenanceTool']['isSaveSig'], isSaveSvBasic=BASIC_DATA['maintenanceTool']['isSaveSvBasic'], isSaveTrace=BASIC_DATA['maintenanceTool']['isSaveTrace'], isSaveSvDetail=BASIC_DATA['maintenanceTool']['isSaveSvDetail']):   
    if isSaveSig == True or isSaveSvBasic == True or isSaveTrace == True or isSaveSvDetail == True:
        with allure.step(key_get_time() +": 停止网络抓包程序"):
            logging.info(key_get_time()+': stop capture process')
            MaintenanceToolService().stop_capture_data(packetSaveName)

'''
        功能：网络数据分析
        参数：
        debugIp:基站debug Ip
        localIp:与基站debug ip通信的ip地址
        packetSaveName:抓包数据存在文件名
                
'''    
def key_network_data_analyse(debugIp=BASIC_DATA['weblmt']['ip'], localIp=BASIC_DATA['traffic']['localPcIp'], packetSaveName='autoTool.pcap', isSaveSig=BASIC_DATA['maintenanceTool']['isSaveSig'], isSaveSvBasic=BASIC_DATA['maintenanceTool']['isSaveSvBasic'], isSaveTrace=BASIC_DATA['maintenanceTool']['isSaveTrace'], isSaveSvDetail=BASIC_DATA['maintenanceTool']['isSaveSvDetail']):
    if isSaveSig == True or isSaveSvBasic == True or isSaveTrace == True or isSaveSvDetail == True:
        with allure.step(key_get_time() +": 抓包数据分析"):
            logging.info(key_get_time()+': capture data analyze')
            MaintenanceToolService().network_data_analyse(debugIp, localIp, packetSaveName, isSaveSig=isSaveSig, isSaveSvBasic=isSaveSvBasic, isSaveTrace=isSaveTrace, isSaveSvDetail=isSaveSvDetail)

'''
        功能：启动log保存
'''
def key_start_save_log(isSaveSig=BASIC_DATA['maintenanceTool']['isSaveSig'], isSaveSvBasic=BASIC_DATA['maintenanceTool']['isSaveSvBasic'], isSaveTrace=BASIC_DATA['maintenanceTool']['isSaveTrace'], isSaveSvDetail=BASIC_DATA['maintenanceTool']['isSaveSvDetail']):
    sigSocket, svBasicSocket, svDetailSocket = None, None, None
    with allure.step(key_get_time() +": 启动log保存相关程序"):
        logging.info(key_get_time()+': start log save process')
        if isSaveSig == True:
            sigSocket = key_connect_signal_tool()
        if isSaveSvBasic == True:
            svBasicSocket = key_connect_sv_basic_tool()
        if isSaveTrace == True:
            pass
        if isSaveSvDetail == True:
            svDetailSocket = key_connect_sv_detail_tool()
        if isSaveSig == True or isSaveSvBasic == True or isSaveTrace == True or isSaveSvDetail == True:
            key_start_capture_data()
        return sigSocket, svBasicSocket, svDetailSocket

'''
        功能：关闭log保存
'''    
def key_close_save_log(sigSocket, svBasicSocket, svDetailSocket):
    if sigSocket != None or svBasicSocket != None or svDetailSocket != None:
        with allure.step(key_get_time() +": 关闭log保存相关程序"):
            logging.info(key_get_time()+': close log save process')
            if sigSocket != None:
                key_disconnect_tool(sigSocket)
            if svBasicSocket != None:
                key_disconnect_tool(svBasicSocket)
            if svDetailSocket != None:
                key_disconnect_tool(svDetailSocket)
