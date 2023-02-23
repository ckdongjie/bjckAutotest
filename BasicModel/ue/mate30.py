'''
Created on 2022.5.31
'''
import logging
import re
from time import sleep
import time

import serial


class mate30Model(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.serial = None
    
    def login_serial(self, serialPort='COM9', serialRate=115200, timeout = 30):
        self.serial = serial.Serial(serialPort, serialRate, timeout=timeout)
        if self.serial.isOpen() == False:
            self.serial.open()
        logging.warn('open serial port success!')
        return self
        
    def logout_serial(self):
        if self.serial.isOpen() == True:
            self.serial.close()
        logging.warn('close serial port success!')
        
    def exec_at_command(self, cmd):
        if self.serial.isOpen() == False:
            self.serial.open()
        logging.warn('The Command is:{0}'.format(cmd))
        self.serial.write((cmd+'\r\n').encode())
        self.serial.flush()
        sleep(2)
    
    def read_result_of_serial(self):
        data = ""
        while self.serial.inWaiting()>0:
            data += self.serial.readline().decode()
        logging.warn('serial return is:{0}'.format(data))
        return data
    
    def ue_attach_detach(self, cmd):
        self.exec_at_command(cmd)
        cmdRes = self.read_result_of_serial()
        return self.exec_result(cmdRes)
    
    def query_attach_info(self):
        self.exec_at_command('at+c5greg=2')
        self.exec_at_command('at+c5greg?')
        cmdRes = self.read_result_of_serial()
        attachStatus, cellInfo = self.at_cell_info_mattch(cmdRes)
        return attachStatus, cellInfo
    
    def at_result_mattch(self, str):
        pattern = '.*\s*(.*)\r\r*\n*\s*'
        result = re.findall(pattern, str)
#         logging.warn('matched result is:{0}'.format(result))
        if len(result)==1:
            return result[0]
        if len(result)==2:
            return result[1]
    
    def exec_result(self, str):
        if 'OK' in str:
            return 'OK'
        else:
            return 'FAIL'
        
    def at_cell_info_mattch(self, str):
        pattern = '.*\s*\+C5GREG:\s*(.*)\r\r*\n*\s*(.*)\r\r*\s*'
        result = re.findall(pattern, str)
        logging.warn('attach cell info matched result is:{0}'.format(result))
        if 'OK' in str:
            cellInfo = result[0][0]
            cellInfoList = cellInfo.split(',')
            if len(cellInfoList) > 4:
                return cellInfoList[1], cellInfoList[3]
        return -1,-1
    
    def mate30_ping_test(self, pdn, ueIp='190.1.169.96', pingNum=20):
        pingCmd = 'ping -c '+str(pingNum)+' '+ueIp+'\n'
        pingRes = pdn.exec_cmd(pingCmd, pingNum+2)
        return self.ping_result_mattch(pingRes)
        
    def ping_result_mattch(self, str):
        pattern = '.*\s*min/avg/max/mdev = (.*) ms'
        result = re.findall(pattern, str)
        logging.warning('ping result matched is:{0}'.format(result))
        if result:
            pingResList = result[0].split('/')
            min,avg,max = pingResList[0],pingResList[1],pingResList[2]
            return min, avg, max
        return -1, -1, -1   
    
    #PDN Send UDP Package To Ue(DL)
    def send_udp_package_DL(self, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        logging.warning('command is: iperf3 -u -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 300 -l 1300 -p '+ monitorPort +' -P '+ processNum +' -R')
        self._channel.send('iperf3 -u -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 300 -l 1300 -p '+ monitorPort +' -P '+ processNum +' -R\n')
        time.sleep(10)
        trafficRes = self.rece_at_command()
        print('trafficRes:',trafficRes)
    
    #Ue Send UDP Package To PDN(UL)
    def send_udp_package_UL(self, pdnIp, packageSize='300m', monitorPort='5555', processNum = '3'):
        logging.warning('command is: iperf3 -u -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 300 -l 1300 -p '+ monitorPort +' -P '+ processNum)
        self._channel.send('iperf3 -u -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 300 -l 1300 -p '+ monitorPort +' -P '+ processNum +'\n')
        time.sleep(10) 
        trafficRes = self.rece_at_command()
        print('trafficRes:',trafficRes)
        
    #PDN Send TCP Package To Ue(DL)
    def send_tcp_package_DL(self, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        self._channel.send('iperf3 -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 180 -l 1300 -p '+ monitorPort +' -P '+ processNum +' -R\n')
        time.sleep(3)
    
    #Ue Send TCP Package To PDN(UL)
    def send_tcp_package_UL(self, pdnIp, packageSize='500m', monitorPort='5555', processNum = '3'):
        self._channel.send('iperf3 -c '+ pdnIp +' -b '+ packageSize +' -i 1 -t 180 -l 1300 -p '+ monitorPort +' -P '+ processNum +'\n')
        time.sleep(3)   
