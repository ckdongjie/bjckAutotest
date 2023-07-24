# coding = 'utf-8'
'''
Created on 2023年5月11日
@author: autotest
'''
'''
        获取手机设备列表
        参数：
'''

import logging
import threading

import allure

from BasicService.pdn.pdnService import PdnService
from BasicService.ue.mobilePhoneService import MobilePhoneService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.pdn.pndManager import key_start_listen_port, \
    key_stop_listen_port, key_pdn_login, key_start_iperf_command_tcp, \
    key_start_iperf_command_udp, key_start_iperf_command_tcp_ul, \
    key_start_iperf_command_udp_ul


def key_get_devices_list():
    with allure.step(key_get_time() +": 获取设备列表\n"):
        logging.info(key_get_time()+': get devices list')
        devicesList = MobilePhoneService().get_phone_devices()
        with allure.step(key_get_time() +": 设备列表:"+str(devicesList)):
            logging.info(key_get_time()+': device list:'+str(devicesList))
        return devicesList

'''
        获取手机ip地址
        参数：
        devicesId：设备id列表
'''    
def key_get_phone_ip(deviceId, tryNum = 3):
    with allure.step(key_get_time() +": 获取设备Ip地址\n"):
        logging.info(key_get_time()+': get device ip addr')
        for i in range(1, tryNum):
            ipAddr = MobilePhoneService().get_phone_ip_addr(deviceId)
            if ipAddr != '':
                break
        with allure.step(key_get_time() +": 设备ip地址信息:"+str(ipAddr)):
            logging.info(key_get_time()+': device ip addr info:'+str(ipAddr))
        return ipAddr

'''
        多设备获取手机ip地址
        参数：
        devicesList：设备id列表
'''    
def key_get_muti_phones_ip(devicesList):
    with allure.step(key_get_time() +": 获取多设备Ip地址\n"):
        logging.info(key_get_time()+': get devices ip addr')
        devIpDict = MobilePhoneService().get_muti_phone_ip_addr(devicesList)
        with allure.step(key_get_time() +": 多设备ip地址信息:"+str(devIpDict)):
            logging.info(key_get_time()+': muti devices ip addr info:'+str(devIpDict))
        return devIpDict

'''
        获取手机接入状态
        参数：
        deviceId：设备id列表
'''
def key_query_access_status(deviceId):
    with allure.step(key_get_time() +": 查询手机网络状态"):
        logging.info(key_get_time()+': query devices access status')
        accStatus = MobilePhoneService().query_access_status(deviceId)
        with allure.step(key_get_time() +": 设备网络接入状态[0-NoAcc,2-Acc]:"+str(accStatus)):
            logging.info(key_get_time()+': device access status[0-NoAcc,2-Acc]:'+str(accStatus))
        return str(accStatus)

'''
        多设备获取手机接入状态
        参数：
        devicesList：设备id列表
'''
def key_query_muti_phones_access_status(devicesList):
    with allure.step(key_get_time() +": 查询手机网络状态"):
        logging.info(key_get_time()+': query devices access status')
        devAccStatusInfo = MobilePhoneService().query_muti_access_status(devicesList)
        with allure.step(key_get_time() +": 多设备网络接入状信息[0-NoAcc,2-Acc]:"+str(devAccStatusInfo)):
            logging.info(key_get_time()+': muti devices access info[0-NoAcc,2-Acc]:'+str(devAccStatusInfo))
        return devAccStatusInfo

'''
        设置手机飞行模式
        参数：
        devicesList：设备id列表
'''    
def key_set_phone_airplan_model(deviceId, phoneType='xiaomi'):
    with allure.step(key_get_time() +": 设置手机进入飞行模式\n"):
        logging.info(key_get_time()+': set phone airplane model')
        MobilePhoneService().set_airplane_mode(deviceId, phoneType)

'''
        设置手机去飞行模式
        参数：
        devicesList：设备id列表
'''    
def key_set_phone_no_airplan_model(deviceId, phoneType='xiaomi'):
    with allure.step(key_get_time() +": 设置手机退出飞行模式\n"):
        logging.info(key_get_time()+': set phone no airplane model')
        MobilePhoneService().set_no_airplane_mode(deviceId, phoneType)
        
'''
        多终端设置手机飞行模式
        参数：
        devicesList：设备id列表
'''    
def key_set_muti_phones_airplan_model(devicesList):
    with allure.step(key_get_time() +": 设置手机进入飞行模式\n"):
        logging.info(key_get_time()+': set phone airplane model')
        MobilePhoneService().set_muti_airplane_mode(devicesList)

'''
        多终端设置手机去飞行模式
        参数：
        devicesList：设备id列表
'''    
def key_set_muti_phones_no_airplan_model(devicesList):
    with allure.step(key_get_time() +": 设置手机退出飞行模式\n"):
        logging.info(key_get_time()+': set phone no airplane model')
        MobilePhoneService().set_muti_no_airplane_mode(devicesList)
'''
        单ue ping包测试
'''
def key_phone_ping(phoneIp, pdn, pingNum=BASIC_DATA['ping']['pingNum'], pingSize=BASIC_DATA['ping']['pingSize'], exptLossRate = BASIC_DATA['ping']['loseRate'],exptPingAvg = BASIC_DATA['ping']['pingAvg'], isCheckPing=BASIC_DATA['ping']['isCheckPing'], tryNum=3):
    with allure.step(key_get_time() +": 执行ping包命令, 终端ip:"+phoneIp):
        logging.info(key_get_time()+': exec ping command, ue ip: '+phoneIp)
        for i in range (1, tryNum+1):
            min, avg, max, transmitted, received, lossrate = PdnService().ping_ue_ip(pdn, phoneIp, pingNum, pingSize)
            if avg != -1:
                break
        with allure.step(key_get_time()+': UE['+phoneIp+'] ping result[max/avg/min/transmitted/received/loss rate] = '+str(max)+"/"+str(avg)+"/"+str(min)+"/"+str(transmitted)+"/"+str(received)+"/"+str(lossrate)+"\n"):
            logging.info(key_get_time()+': UE['+phoneIp+'] ping result[max/avg/min/transmitted/received/loss rate] = '+str(max)+"/"+str(avg)+"/"+str(min)+"/"+str(transmitted)+"/"+str(received)+"/"+str(lossrate))
    if isCheckPing == True:
        assert avg != -1,'ping包测试不通过，请检查'
        lossrate = lossrate.split('%')[0]
        assert int(lossrate) <= exptLossRate, 'IP:'+phoneIp+' ping包丢包率大于预期，请检查！'
        assert float(avg) <= exptPingAvg, 'IP:'+phoneIp+' ping包平均时延大于预期，请检查！'  
           
'''
        下行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_dl_udp_nr_traffic(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpDlSize'], monitorPort=BASIC_DATA['traffic']['nrDlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 下行UDP流量测试"):
        logging.info(key_get_time()+': exec DL UDP traffic test')
        with allure.step(key_get_time() +": 手机执行iperf监听"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_dl_udp_traffic(phoneId, monitorPort)
        key_start_iperf_command_udp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'DL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        MobilePhoneService().phone_stop_iperf(phoneId, monitorPort, 'udp')
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL UDP Nr test result:\n'+dlTrafRes)
        return avgDlTraf
        
'''
        上行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_ul_udp_nr_traffic(phoneId, phoneIp, pdn, pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpUlSize'], monitorPort=BASIC_DATA['traffic']['nrUlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 上行UDP流量测试"):
        logging.info(key_get_time()+': exec UL UDP traffic test')
        key_start_listen_port(pdn, monitorPort, 'iperf')
        with allure.step(key_get_time() +": 手机执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_ul_udp_traffic(phoneId, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort, 'iperf')
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] UL UDP Nr test result:\n'+ulTrafRes)
        return avgUlTraf
    
'''
        下行tcp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_dl_tcp_nr_traffic(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpDlSize'], monitorPort=BASIC_DATA['traffic']['nrDlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 下行TCP流量测试"):
        logging.info(key_get_time()+': exec DL TCP traffic test')
        with allure.step(key_get_time() +": 手机执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_dl_tcp_traffic(phoneId, monitorPort)
        key_start_iperf_command_tcp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'DL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        MobilePhoneService().phone_stop_iperf(phoneId, monitorPort)
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL TCP Nr test result:\n'+dlTrafRes)
        return avgDlTraf
    
'''
        上行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_ul_tcp_nr_traffic(phoneId, pdn, pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'], monitorPort=BASIC_DATA['traffic']['nrUlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 上行TCP流量测试"):
        logging.info(key_get_time()+': exec UL TCP traffic test')
        key_start_listen_port(pdn, monitorPort, 'iperf')
        with allure.step(key_get_time() +": 手机执行iperf命令"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_ul_tcp_traffic(phoneId, pdnIp, packageSize, monitorPort, processNum, spanTime=spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        key_stop_listen_port(pdn, monitorPort, 'iperf')
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL TCP NR test result:\n'+ulTrafRes)
        return avgUlTraf
    
'''
        上下行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_udl_udp_nr_traffic(phoneId, phoneIp, ulPdn, dlPdn, pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], ulPackageSize=BASIC_DATA['traffic']['udpUlSize'], dlPackageSize=BASIC_DATA['traffic']['udpUlSize'],ulMonitorPort=BASIC_DATA['traffic']['nrUlPort'],dlMonitorPort=BASIC_DATA['traffic']['nrDlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 上下行UDP流量测试"):
        logging.info(key_get_time()+': exec UL&DL TCP traffic test')
        with allure.step(key_get_time() +": 手机执行iperf监听命令"):
            logging.info(key_get_time()+': exec iperf moinitor')
            MobilePhoneService().phone_dl_udp_traffic(phoneId, dlMonitorPort)
        key_start_listen_port(ulPdn, ulMonitorPort, 'iperf')
        with allure.step(key_get_time() +": 手机执行iperf灌包命令"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_ul_udp_traffic(phoneId, pdnIp, ulPackageSize, ulMonitorPort, processNum, spanTime=spanTime)
            key_start_iperf_command_udp(dlPdn, phoneIp, dlPackageSize, dlMonitorPort, processNum, spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UDL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        key_stop_listen_port(dlPdn, dlMonitorPort, 'iperf')
        MobilePhoneService().phone_stop_iperf(phoneId, dlMonitorPort, 'udp')
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] UL TCP NR test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL TCP NR test result:\n'+dlTrafRes)
        return avgDlTraf, avgUlTraf 
    
'''
        上下行tcp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_udl_tcp_nr_traffic(phoneId, phoneIp, ulPdn, dlPdn, pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], ulPackageSize=BASIC_DATA['traffic']['tcpUlSize'], dlPackageSize=BASIC_DATA['traffic']['tcpUlSize'],ulMonitorPort=BASIC_DATA['traffic']['nrUlPort'],dlMonitorPort=BASIC_DATA['traffic']['nrDlPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 上下行TCP流量测试"):
        logging.info(key_get_time()+': exec UL&DL TCP traffic test')
        key_start_listen_port(ulPdn, ulMonitorPort, 'iperf')
        with allure.step(key_get_time() +": 手机执行iperf监听命令"):
            logging.info(key_get_time()+': exec iperf monitor command by mobile phone')
            MobilePhoneService().phone_dl_tcp_traffic(phoneId, dlMonitorPort)
        with allure.step(key_get_time() +": 手机执行iperf灌包命令"):
            logging.info(key_get_time()+': exec iperf command by mobile phone')
            MobilePhoneService().phone_ul_tcp_traffic(phoneId, pdnIp, ulPackageSize, ulMonitorPort, processNum, spanTime=spanTime)
        key_start_iperf_command_tcp(dlPdn, phoneIp, dlPackageSize, dlMonitorPort, processNum, spanTime)
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UDL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        key_stop_listen_port(ulPdn, ulMonitorPort, 'iperf')
        with allure.step(key_get_time() +": 停止iperf监听"):
            logging.info(key_get_time()+': stop iperf monitor')
            MobilePhoneService().phone_stop_iperf(phoneId, dlMonitorPort)
        with allure.step(key_get_time() +": 上行流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] UL TCP NR test result:\n'+ulTrafRes)
        with allure.step(key_get_time() +": 下行流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL TCP NR test result:\n'+dlTrafRes)
        return avgDlTraf, avgUlTraf

'''
            多终端ping包测试
'''
def key_muti_ue_ping(devicesList, pdn):
    start_thread(devicesList, key_phone_ping, {'pdn':pdn})

'''
            多终端上行udp流量测试
'''
def key_muti_ue_ul_udp_traffic(devicesList, pdn):
    start_thread(devicesList, key_phone_ul_udp_nr_traffic, {'pdn':pdn})

'''
            多终端下行udp流量测试
'''
def key_muti_ue_dl_udp_traffic(devicesList, pdn):
    start_thread(devicesList, key_phone_dl_udp_nr_traffic, {'pdn':pdn})

'''
            多终端上行tcp流量测试
'''
def key_muti_ue_ul_tcp_traffic(devicesList, pdn):
    start_thread(devicesList, key_phone_ul_tcp_nr_traffic, {'pdn':pdn})
            
'''
            多终端下行tcp流量测试
'''
def key_muti_ue_dl_tcp_traffic(devicesList, pdn):
    start_thread(devicesList, key_phone_dl_tcp_nr_traffic, {'pdn':pdn})    

'''
            多终端下行tcp流量测试
'''
def key_muti_ue_udl_udp_traffic(devicesList, ulpdn, dlpdn):
    start_thread(devicesList, key_phone_udl_udp_nr_traffic, {'ulPdn':ulpdn, 'dlPdn':dlpdn}) 
    
'''
            多终端下行tcp流量测试
'''
def key_muti_ue_udl_tcp_traffic(devicesList, ulpdn, dlpdn):
    start_thread(devicesList, key_phone_udl_tcp_nr_traffic, args=(ulpdn, dlpdn,)) 

'''
    ping测试线程
'''    
def start_ping_thread(deviceList, funName, kwargs={}):
    tList = []
    devIpDict = key_get_phone_ip(deviceList)
    for device in deviceList:
        ueIp = devIpDict[device]
        kwargs.update({'phoneIp':ueIp})
        t = threading.Thread(target = funName, kwargs=kwargs)
        tList.append(t)
        t.start()

'''
            灌包测试线程
'''
def start_thread(deviceList, funName, kwargs={}):
    tList = []
    devIpDict = key_get_phone_ip(deviceList)
    for device in deviceList:
        ueIp = devIpDict[device]
        kwargs.update({'phoneId':device,'phoneIp':ueIp})
        t = threading.Thread(target = funName, kwargs=kwargs)
        tList.append(t)
        t.start()

'''
        下行tcp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_dl_tcp_nr_traffic_port_banding(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpDlSize'], monitorPort=BASIC_DATA['phone']['iperfPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 手机端口绑定场景，下行TCP流量测试"):
        logging.info(key_get_time()+': exec DL TCP traffic test when iperf port is banding')
        key_start_iperf_command_tcp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf3')
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'DL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL TCP Nr test result:\n'+dlTrafRes)
        return avgDlTraf

'''
        上行tcp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_ul_tcp_nr_traffic_port_banding(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'], monitorPort=BASIC_DATA['phone']['iperfPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 手机端口绑定场景，上行TCP流量测试"):
        logging.info(key_get_time()+': exec UL TCP traffic test when iperf port is banding')
        key_start_iperf_command_tcp_ul(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf3')
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.warning(key_get_time()+': ['+phoneId+'] DL TCP NR test result:\n'+ulTrafRes)
        return avgUlTraf

'''
        下行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_dl_udp_nr_traffic_port_banding(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpDlSize'], monitorPort=BASIC_DATA['phone']['iperfPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 手机端口绑定场景，下行UDP流量测试"):
        logging.info(key_get_time()+': exec DL UDP traffic test when iperf port is banding')
        key_start_iperf_command_udp(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf3')
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'DL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        with allure.step(key_get_time() +": 流量测试结果：\n"+dlTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL UDP Nr test result:\n'+dlTrafRes)
        return avgDlTraf

'''
        上行udp nr灌包
        参数： 
    phoneId:设备编号
    pdn:pdn对象
    pdnIp:pdn业务ip地址
    enbDebugIp:基站debug地址
    pcIp:电脑ip地址，与基站debug通信的地址，用于抓包
    scrapFileName:pcIp对应网卡名称
    packageSize:包大小 
    monitorPort:使用端口
    processNum:进程个数  
    spanTime:灌包持续时间
'''            
def key_phone_ul_udp_nr_traffic_port_banding(phoneId, phoneIp, pdn, enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'], monitorPort=BASIC_DATA['phone']['iperfPort'], pcNetworkCardName=BASIC_DATA['traffic']['pcNetworkCardName'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    with allure.step(key_get_time() +": 手机端口绑定场景，上行UDP流量测试"):
        logging.info(key_get_time()+': exec UL UDP traffic test when iperf port is banding')
        key_start_iperf_command_udp_ul(pdn, phoneIp, packageSize, monitorPort, processNum, spanTime, iperfType='iperf3')
        with allure.step(key_get_time() +": 启动抓包程序，进行数据分析"):
            logging.info(key_get_time()+': start scrap process, analyze data, capture time(s):'+str(spanTime))
            dir = 'UL'
            dlTrafRes,ulTrafRes, avgDlTraf, avgUlTraf = MobilePhoneService().phone_traffic_data_analyze(enbDebugIp, pcIp, scrapFileName, dir, pcNetworkCardName, spanTime, type='NR')
        with allure.step(key_get_time() +": 流量测试结果：\n"+ulTrafRes):
            logging.info(key_get_time()+': ['+phoneId+'] DL UDP NR test result:\n'+ulTrafRes)
        return avgUlTraf
    

if __name__ == '__main__':
    ulPdn = key_pdn_login()
    dlPdn = key_pdn_login()
    devicesList = key_get_devices_list()
    phoneId = 'XPL0220428027472'
#     ueIp = key_get_phone_ip(devicesList[0])
    phoneIp = '190.1.41.85'
#     key_phone_ping(phoneIp, ulPdn)
#     key_phone_dl_tcp_nr_traffic_port_banding(phoneId, phoneIp, ulPdn)
    key_phone_ul_tcp_nr_traffic_port_banding(phoneId, phoneIp, ulPdn)