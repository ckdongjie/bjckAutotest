'''
Created on 2023年4月19日

@author: autotest
'''
import threading
from time import sleep

from scapy.sendrecv import sniff
from scapy.utils import wrpcap


global isStop, packetList
isStop = False
packetList = []
class CaptureNetData():
    '''
            捕获监听程序
    '''
    def isStopCaputer(self):
        global isStop
        if isStop:
            return True
        else:
            return False 
    '''
            抓包数据保存
    '''    
    def saveCaputerData(self, packet):
        global packetList
        packetList.append(packet)
        
    '''
            数据抓包
    '''    
    def scrapNetworkPackData(self, interface=''):
        global isStop
        isStop = False
        if interface == '':
            sniff(prn=(lambda x: self.saveCaputerData(x)), filter='udp', stop_filter=(lambda x: self.isStopCaputer()))
        else:
            sniff(prn=(lambda x: self.saveCaputerData(x)), iface = interface, filter='udp', stop_filter=(lambda x: self.isStopCaputer()))
    
    '''
            抓包数据写入
    '''
    def writeNetworkData(self, saveName):
        global packetList
        global isStop
        isStop = True
        wrpcap(saveName, [packetList])
        
    '''
            启动抓包线程
    '''
    def startCatputer(self, interfaceName=''):
        t = threading.Thread(target=self.scrapNetworkPackData, args=(interfaceName,))
        t.start()
    
    '''
            停止抓包线程，并把抓包数据写入文件
    ''' 
    def stopCatputer(self, packetSaveName):
        t2 = threading.Thread(target=self.writeNetworkData, args=(packetSaveName,))
        t2.start()
        sleep(5)
