'''
Created on 2023年4月11日

@author: autotest
'''
'''
        功能：多cpe登录
        参数：
    cpeListStr：多cpe信息
'''

import logging
import threading

import allure

from BasicService.ue.cpeService import CpeService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.ue.CpeManager import key_cpe_attach, key_cpe_detach, \
    key_cpe_attach_cell_info, key_cpe_ping, key_reboot_cpe, \
    key_confirm_pdu_setup_succ, key_confirm_pdu_setup_fail, \
    key_cpe_login_at_model, key_cpe_logout_at_model, key_dl_udp_wifi_flow_test, \
    key_dl_udp_nr_flow_test, key_ul_udp_wifi_flow_test, key_ul_udp_nr_flow_test, \
    key_dl_tcp_wifi_flow_test, key_dl_tcp_nr_flow_test, \
    key_ul_tcp_wifi_flow_test, key_ul_tcp_nr_flow_test, key_udl_tcp_nr_flow_test, \
    key_udl_tcp_wifi_flow_test, key_udl_udp_wifi_flow_test, \
    key_udl_udp_nr_flow_test


def key_muti_cpe_login(cpeListStr=BASIC_DATA['cpeList']['cpeInfo']):
    cpeList = cpeListStr.split(';')
    cpeObjList = []
    for cpe in cpeList:
        cpeInfo = cpe.split(',')
        cpeIp = cpeInfo[0]
        username = cpeInfo[1]
        password = cpeInfo[2]
        print('cpe info:',cpeIp,username,password)
        with allure.step(key_get_time() +": 登录CPE前台:"+cpeIp+"\n"):
            logging.info(key_get_time()+': login cpe command model, cpe:'+cpeIp)
            cpe = CpeService().cpe_login(cpeIp, username, password)
            assert cpe != None, 'cpe登录失败，请检查！'
            cpeObjList.append(cpe)
    return cpeObjList
            
'''
        功能：SSH登出CPE
        参数：
'''    
def key_muti_cpe_logout(cpeList):
    for cpe in cpeList:
        with allure.step(key_get_time() +": 登出CPE前台\n"):
            logging.info(key_get_time()+': logout cpe command model')
            CpeService().cpe_logout(cpe)
                     
'''
         多CPE接入
        参数：    
'''
def key_muti_cpe_attach(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_cpe_attach)
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+"接入结果"+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' attach result:'+result)

'''
        多CPE去接入
        参数：    
'''
def key_muti_cpe_detach(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_cpe_detach)
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+"去接入结果"+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' detach result:'+result)
    
'''
        查询CPE接入小区信息
        参数：  cpe对象  
'''
def key_muti_cpe_resident_cell(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_cpe_attach_cell_info)
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+"驻留小区PCI"+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' resident cell pci:'+result)

'''
         多CPE ping包测试
        参数： 
    pdnIp:pdn ip地址
    pingNum:ping包测试次数
    tryNum:链路不稳定时，ping包尝试次数
    ping_interface:cpe ping包网卡
    log_save_path:ping包log记得路径 
'''
def key_muti_cpe_ping(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_cpe_ping)
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+" ping包结果："+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' ping test lossrate and avg:'+result)
            
'''
        多cpe复位
        参数：
    cpe:cpe对象 
''' 
def key_muti_reboot_cpe(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_reboot_cpe)
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+" 复位结果："+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' reboot result:'+result)
      
    
'''
    确认pdu建立成功
        参数：
    cpe:cpe对象 
''' 
def key_muti_cpe_confirm_pdu_setup_succ(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_confirm_pdu_setup_succ)
    allSucc = True
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+" pdu建立结果："+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' pdu setup result:'+result)
        if result != 'success':
            allSucc = False
            break
    return allSucc
        
  
'''
    确认pdu建立成功
        参数：
    cpe:cpe对象 
''' 
def key_muti_cpe_confirm_pdu_setup_fail(cpeList):
    mutiCpeAttachResList = start_thread(cpeList, key_confirm_pdu_setup_fail)
    allFail = True
    for resStr in mutiCpeAttachResList:
        cpeIp = resStr.split(';')[0]
        result = resStr.split(';')[1]
        with allure.step(key_get_time() +": cpe_"+cpeIp+" pdu建立结果："+result+"\n"):
            logging.info(key_get_time()+': cpe_'+cpeIp+' pdu setup result:'+result) 
        if result != 'failure':
            allFail = False
            break
    return allFail
'''
    CPE进入AT命令模式
        参数： 
'''    
def key_muti_cpe_login_at_model(cpeList):
    start_thread(cpeList, key_cpe_login_at_model)

'''
    CPE退出AT命令模式
        参数： 
'''        
def key_muti_cpe_logout_at_model(cpeList):
    start_thread(cpeList, key_cpe_logout_at_model)

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
def key_muti_cpe_dl_udp_wifi_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpDlSize'], monitorPort=BASIC_DATA['traffic']['wifiDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_dl_udp_wifi_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))

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
def key_muti_cpe_dl_udp_nr_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpDlSize'], monitorPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_dl_udp_nr_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
             
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
def key_muti_cpe_ul_udp_wifi_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpUlSize'],monitorPort=BASIC_DATA['traffic']['wifiUlPort'], processNum =BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_ul_udp_wifi_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
 
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
def key_muti_cpe_ul_udp_nr_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['udpUlSize'],monitorPort=BASIC_DATA['traffic']['nrUlPort'], processNum =BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_ul_udp_nr_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
    
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
def key_muti_cpe_dl_tcp_wifi_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpDlSize'],monitorPort=BASIC_DATA['traffic']['wifiDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_dl_tcp_wifi_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
             
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
def key_muti_cpe_dl_tcp_nr_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpDlSize'],monitorPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_dl_tcp_nr_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
         
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
def key_muti_cpe_ul_tcp_wifi_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorPort=BASIC_DATA['traffic']['wifiUlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_ul_tcp_wifi_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
             
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
def key_muti_cpe_ul_tcp_nr_flow_test(cpeList, pdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorPort=BASIC_DATA['traffic']['nrUlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_traff_thread(cpeList, key_ul_tcp_nr_flow_test, args=(pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorPort, processNum, spanTime))
                  
'''
        上下行tcp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:第一个端口号，多cpe时会加1
    processNum:进程个数  
'''        
def key_muti_cpe_udl_tcp_nr_flow_test(ulCpeList, dlCpeList, ulPdn, dlPdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorUlPort=BASIC_DATA['traffic']['nrUlPort'], monitorDlPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_two_traff_thread(ulCpeList, dlCpeList, key_udl_tcp_nr_flow_test, args=(ulPdn, dlPdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorUlPort, monitorDlPort, processNum, spanTime))
             
'''
        上下行tcp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:第一个端口号，多cpe时会加1
    processNum:进程个数  
'''        
def key_muti_cpe_udl_tcp_wifi_flow_test(ulCpeList, dlCpeList, ulPdn, dlPdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorUlPort=BASIC_DATA['traffic']['nrUlPort'], monitorDlPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_two_traff_thread(ulCpeList, dlCpeList, key_udl_tcp_wifi_flow_test, args=(ulPdn, dlPdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorUlPort, monitorDlPort, processNum, spanTime))
                      
'''
        上下行udp nr灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:第一个端口号，多cpe时会加1
    processNum:进程个数  
'''        
def key_muti_cpe_udl_udp_nr_flow_test(ulCpeList, dlCpeList, ulPdn, dlPdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorUlPort=BASIC_DATA['traffic']['nrUlPort'], monitorDlPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_two_traff_thread(ulCpeList, dlCpeList, key_udl_udp_nr_flow_test, args=(ulPdn, dlPdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorUlPort, monitorDlPort, processNum, spanTime))
             
'''
        上下行tcp wifi灌包
        参数： 
    cpePcIp:cpe直连PC的 ip地址
    iperfPath:本地iperf安装路径，用于启动本地命令
    pdnIp:pdn ip地址
    packageSize:包大小 
    monitorPort:第一个端口号，多cpe时会加1
    processNum:进程个数  
'''        
def key_muti_cpe_udl_udp_wifi_flow_test(ulCpeList, dlCpeList, ulPdn, dlPdn, cpePcIp=BASIC_DATA['traffic']['cpePcIp'], iperfPath=BASIC_DATA['traffic']['iperfLocalPath'], pdnIp=BASIC_DATA['pdn']['pdnIp'], enbDebugIp=BASIC_DATA['weblmt']['ip'], pcIp=BASIC_DATA['traffic']['localPcIp'], scrapFileName=BASIC_DATA['traffic']['scrapFileName'], packageSize=BASIC_DATA['traffic']['tcpUlSize'],monitorUlPort=BASIC_DATA['traffic']['nrUlPort'], monitorDlPort=BASIC_DATA['traffic']['nrDlPort'], processNum=BASIC_DATA['traffic']['processNum'], spanTime=BASIC_DATA['traffic']['spanTime']):
    start_two_traff_thread(ulCpeList, dlCpeList, key_udl_udp_wifi_flow_test, args=(ulPdn, dlPdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, scrapFileName, packageSize, monitorUlPort, monitorDlPort, processNum, spanTime))
    
def start_thread(cpeList, funName, args=()):
    tList = []
    tResList = []
    for cpe in cpeList:
        if args == ():
            t = MutiCpeThread(funName, args=cpe)
        else:
            t = MutiCpeThread(funName, args=(cpe, args))
        tList.append(t)
        t.start()
    for t in tList:
        t.join()# 为线程开启同步
        tResList.append(cpe.ip+';'+str(t.get_attch_res()))
    return tResList

def start_traff_thread(cpeList, funName, args=()):
    tList = []
    for cpe in cpeList:
        t = MutiCpeThread(funName, args=(cpe, args))
        tList.append(t)
        t.start()
        argsList = list(args)
        argsList[8] = str(int(argsList[8])+1)
        args = tuple(argsList)
        
def start_two_traff_thread(cpeList1, cpeList2, funName, args=()):
    tList = []
    for i in range (len(cpeList)):
        t = MutiCpeThread(funName, args=(cpeList1[i], cpeList2[i], args))
        tList.append(t)
        t.start()
        argsList = list(args)
        argsList[9] = str(int(argsList[9])+1)
        argsList[10] = str(int(argsList[10])+1)
        args = tuple(argsList)
    
class MutiCpeThread(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, func, args = ()):
        '''
        Constructor
        '''
        super(MutiCpeThread, self).__init__()
        self.func = func
        self.args = args
        
    def run(self):
        self.execRes = self.func(self.args)
    
    def get_attch_res(self):
        try:
            return self.execRes
        except Exception:
            return None
        
if __name__ == '__main__':
#     cpeList = key_muti_cpe_login()
    cpeList = ['192.168.1.1', '192.168.2.1','192.168.3.1',]
    pdn = None
    key_muti_cpe_dl_udp_wifi_flow_test(cpeList, pdn)
    