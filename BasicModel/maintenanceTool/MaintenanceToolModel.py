#coding = 'utf-8'
'''
Created on 2023年4月19日
@author: autotest
'''

import datetime
import threading
from time import sleep

from BasicModel.basic.EIDetailConfigParse import GetActiveEIMsgList, \
    GetsvHeartBeat
from BasicModel.basic.loadFileAndAnalyzeData import startMonitorTask
from BasicModel.basic.sigTraceParse import GetSigHeartBeat
from BasicModel.basic.udpSocket import udpSocketModel
from BasicModel.maintenanceTool.CaptureNetData import CaptureNetData
from BasicModel.maintenanceTool.SvAndSigDataDeal import capture_data_analyse

class MaintenanceToolModel():
    '''
        sv工具心跳监控线程
    '''
    def svTaskTimerStart(self, svSocket):
        heartBeat = GetsvHeartBeat()
        if getattr(svSocket, '_closed') == False:
            svSocket.send(heartBeat)
            threading.Timer(10, self.svTaskTimerStart,(svSocket,)).start()
    
    '''
        sig工具心跳监控线程
    '''
    def sigTaskTimerStart(self, sigSocket):
        heartBeat = GetSigHeartBeat()
        if getattr(sigSocket, '_closed') == False:
            sigSocket.send(heartBeat)
            threading.Timer(10, self.sigTaskTimerStart,(sigSocket,)).start()
    
    '''
                    连接sv基本信息工具
    '''
    def connect_sv_basic_tool(self, debugIp, svBasicPort=16666):
        svBasicSocket = udpSocketModel().socket_sv_basic_client(debugIp, svBasicPort)
        self.svTaskTimerStart(svBasicSocket)
        return svBasicSocket
    
    '''
                    连接sv详细信息工具
    '''
    def connect_sv_detail_tool(self, debugIp, svDetailPort=16667):
        g_tEiMsgList = GetActiveEIMsgList()
        svDetailSocket = udpSocketModel().socket_sv_deatil_client(debugIp, g_tEiMsgList, svDetailPort)
        self.svTaskTimerStart(svDetailSocket)
        return svDetailSocket
    
    '''
                    连接signal工具
    '''        
    def connect_signal_tool(self, debugIp, localIp):
        sigSocket = udpSocketModel().socket_Sigclient(debugIp, localIp)
        self.sigTaskTimerStart(sigSocket)
        return sigSocket
    
    '''
                    关闭连接
    ''' 
    def disconnect_tool(self, Socket):
        if getattr(Socket, '_closed') == False:
            Socket.close()
    
        
if __name__ == '__main__':
    debugIp = '172.16.7.15'
    localIp = '172.16.7.100'
    mtool = MaintenanceToolModel()
    capture = CaptureNetData()
    try:
#         sigSocket = mtool.connect_signal_tool(debugIp, localIp)
        svBasicSocket = mtool.connect_sv_basic_tool(debugIp)
        capture.startCatputer('Realtek PCIe GbE Family Controller')
        print('--------------')
        sleep(2)
        print('-----ping-------')
        sleep(5)
        print('-----tcp-------')
        sleep(15)
        print('-----utp-------')
        capture.stopCatputer('D:/bjckAutotest/AutoTestMain/captureData/auto.pcap')
        print('-----data analyze-------')
        sleep(5)
        capture_data_analyse(debugIp, localIp, 'D:/bjckAutotest/AutoTestMain/captureData/auto.pcap', isWriteSig=False, isWriteSvBasic=False, isWriteTrace=False, isWriteSvDetail=False)
    finally:
#         print('-----stop signal-------')
#         mtool.disconnect_tool(sigSocket)
        print('-----stop sv-------')
        mtool.disconnect_tool(svBasicSocket)
    