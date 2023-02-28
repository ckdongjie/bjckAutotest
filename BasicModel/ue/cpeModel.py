'''
Created on 2022.5.31
'''
import logging
import os
import re
from time import sleep
import time

import paramiko

from BasicModel.basic.loadFileAndAnalyzeData import loadDataAndCalculateFlow, \
    g_tEiMsgList, startMonitorTask, scrapNetworkPackData
from BasicModel.basic.udpSocket import udpSocketModel


class CpeModel(object):
    '''
    classdocs
    '''
    def __init__(self, ssh=None, channel=None):
        '''
        Constructor
        '''
        self.ip = None
        self._ssh = ssh
        self._channel = channel
    
    def cpe_login(self, cpeIp, username="root", password="snc123...", tryNum = 5):
        for i in range(1, tryNum):
            try:
                self._ssh = paramiko.SSHClient()
                self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh.connect(hostname=cpeIp, username=username, password=password)
                self._channel = self._ssh.invoke_shell()
                self.ip = cpeIp
                logging.info('login cpe success!')
                return self
            except:
                logging.warning('login cpe failure, wait for 5s try again!')
                sleep(5)
        
    def cpe_logout(self):
        if not self._ssh:
            return
        self._ssh.close()
        self._ssh = None
        
    def login_at_model(self):
        self._channel.send('at_cmd_task\n')
    
    def logout_at_model(self):
        self._channel.send('quit\n')
        
    def exec_at_command(self, cmd):
        if not self._ssh:
            self._ssh.invoke_shell()
        self._channel.send(cmd+'\n')
        time.sleep(2)
        logging.info('AT Command is:{0}'.format(cmd))
        result = self.rece_at_command()
#         logging.warning('AT Command Result is:{0}'.format(result))
        return self.at_result_mattch(result)
    
    def exec_at_command_and_check_cell_info(self, cmd):
        if not self._ssh:
            self._ssh.invoke_shell()
        self._channel.send(cmd+'\n')
        time.sleep(2)
        logging.info('AT Command is:{0}'.format(cmd))
        result = self.rece_at_command()
#         logging.warning('AT Command Result is:{0}'.format(result))
        return self.at_cell_info_mattch(result)
        
    def rece_at_command(self):
        try:
            return self._channel.recv(65535).decode()
        except:
            logging.warning('rece error!')
    
    def at_result_mattch(self, str):
        pattern = r'.*\s*(.*)\r\s*.*AT:'
        result = re.findall(pattern, str)
        logging.info('mattch result is:{0}'.format(result))
        if len(result)==1:
            return result[0]
        if len(result)==2:
            return result[1]
        
    def at_cell_info_mattch(self, str):
        pattern = r'.*\s*\+C5GREG:\s*(.*)\r\r\s*(.*)\r\s*AT:'
        result = re.findall(pattern, str)
        logging.info('cell info mattch result is:{0}'.format(result))
        if result != []:
            if result[0][1]=='OK':
                cellInfo = result[0][0]
                cellInfoList = cellInfo.split(',')
                if len(cellInfoList) > 4:
                    return cellInfoList[1], cellInfoList[3]
        return -1,-1
    
    def ping_test(self, pdnIp='193.168.9.239', pingNum=20, pingInterface = 'rmnet_data0', pingSize=32):
        self._channel.send('ping -I '+pingInterface+' -c '+str(pingNum)+' '+pdnIp+' -s '+str(pingSize)+'\n')
        time.sleep(int(pingNum)+5)
        pingRes = self.rece_at_command()
        min, avg, max = self.ping_result_mattch(pingRes)
        transmitted = self.ping_result_mattch_transmitted(pingRes)
        received = self.ping_result_mattch_received(pingRes)
        lossrate = self.ping_result_mattch_loss_rate(pingRes)
        return min, avg, max,transmitted,received,lossrate
        
    def reboot_cpe(self):
        self._channel.send('reboot\n')
        time.sleep(5)
        resetInfo = self.rece_at_command()
        return 'success'
    
    def query_pdu_setup_status(self):
        self._channel.send('ifconfig\n')
        time.sleep(5)
        ipInfo = self.rece_at_command()
        mattchRes = self.ip_info_mattch(ipInfo)
        if len(mattchRes)<2:
            return 'failure'
        else:
            return 'success'
        
    def ip_info_mattch(self, str):
        pattern = '.*rmnet_data[0|1].*\n*.*inet addr:(.*)  Mask:255.255'
        result = re.findall(pattern, str)
        logging.info('ip info mattch result is{0}'.format(result))
        return result    
        
    def is_add_dmz_route(self, cpePcIp):
        self._channel.send('iptables -t nat -nvL\n')
        time.sleep(3)
        cmdRes = self.rece_at_command()
        if cpePcIp in cmdRes:
            return False
        else:
            return True
        
    def ping_result_mattch(self, str):
        pattern = '.*min/avg/max = (.*) ms'
        result = re.findall(pattern, str)
        logging.info('ping result mattched is:{0}'.format(result))
        if result:
            pingResList = result[0].split('/')
            min,avg,max = pingResList[0],pingResList[1],pingResList[2]
            return min, avg, max
        return -1, -1, -1    
    
    def ping_result_mattch_transmitted(self, str):
        pattern = r'.*\s*(.*) packets transmitted'
        result = re.findall(pattern, str)
        logging.info('packets transmitted:{0}'.format(result))
        if result:
            tranPackage = result[0]
            return tranPackage
        return -1
    
    def ping_result_mattch_received(self, str):
        pattern = 'packets transmitted, (.*) packets received'
        result = re.findall(pattern, str)
        logging.info('packets received:{0}'.format(result))
        if result:
            recePackage = result[0]
            return recePackage
        return 0
    
    def ping_result_mattch_loss_rate(self, str):
        pattern = 'packets received, (.*) packet loss'
        result = re.findall(pattern, str)
        logging.info('packet loss:{0}'.format(result))
        if result:
            lossRate = result[0]
            return lossRate
        return '100%'
    
    #PDN Send UDP Package To Ue(DL)
    def send_udp_package_DL(self, cpePcIp, iperfPath, pdnIp, packageSize='500m', monitorPort=5555, processNum = 3, spanTime = 120):
        if self.is_add_dmz_route(cpePcIp):
            self._channel.send('iptables -t nat -A PREROUTING -i rmnet_data0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
            self._channel.send('iptables -t nat -A PREROUTING -i ath0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
        cmd_str = iperfPath+'\\iperf3 -u -c '+pdnIp+' -b '+ packageSize +' -i 1 -t '+str(spanTime)+' -l 1300 -p '+str(monitorPort)+' -P '+str(processNum)+' -R'
        logging.info('iperf command[udp-dl]: '+cmd_str)
        os.popen(cmd_str)
    
    #Ue Send UDP Package To PDN(UL)
    def send_udp_package_UL(self, cpePcIp, iperfPath, pdnIp, packageSize='300m', monitorPort=5555, processNum = 3, spanTime = 120):
        if self.is_add_dmz_route(cpePcIp):
            self._channel.send('iptables -t nat -A PREROUTING -i rmnet_data0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
            self._channel.send('iptables -t nat -A PREROUTING -i ath0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
        cmd_str = iperfPath+'\\iperf3 -u -c '+pdnIp+' -b '+ packageSize +' -i 1 -t '+str(spanTime)+' -l 1300 -p '+str(monitorPort)+' -P '+str(processNum)
        logging.info('iperf command[udp-ul]: '+cmd_str)
        os.popen(cmd_str)
        
    #PDN Send TCP Package To Ue(DL)
    def send_tcp_package_DL(self, cpePcIp, iperfPath, pdnIp, packageSize='500m', monitorPort=5555, processNum = 3, spanTime = 120):
        if self.is_add_dmz_route(cpePcIp):
            self._channel.send('iptables -t nat -A PREROUTING -i rmnet_data0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
            self._channel.send('iptables -t nat -A PREROUTING -i ath0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
        cmd_str = iperfPath+'\\iperf3 -c '+pdnIp+' -b '+ packageSize +' -i 1 -t '+str(spanTime)+' -l 1300 -p '+str(monitorPort)+' -P '+str(processNum)+' -R'
        logging.info('iperf command[tcp-dl]: '+cmd_str)
        os.popen(cmd_str)
    
    #Ue Send TCP Package To PDN(UL)
    def send_tcp_package_UL(self, cpePcIp, iperfPath, pdnIp, packageSize='500m', monitorPort=5555, processNum = 3, spanTime = 120):
        if self.is_add_dmz_route(cpePcIp):
            self._channel.send('iptables -t nat -A PREROUTING -i rmnet_data0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
            self._channel.send('iptables -t nat -A PREROUTING -i ath0 -j DNAT --to-destination '+cpePcIp+'\n')
            time.sleep(1)
        cmd_str = iperfPath+'\\iperf3 -c '+pdnIp+' -b '+ packageSize +' -i 1 -t '+str(spanTime)+' -l 1300 -p '+str(monitorPort)+' -P '+str(processNum)
        logging.info('iperf command[tcp-ul]: '+cmd_str)
        os.popen(cmd_str)
        
    #flow analyze
    def cell_flow_analyze(self, enbIp, pcIp, scrapFileName, dir = 'DL', pcNetworkCardName ='', spanTime = 120, type='WIFI'):
        svSocket = udpSocketModel().socket_SVclient(g_tEiMsgList, enbIp)
        startMonitorTask(svSocket)
        sleep(3)
        scrapNetworkPackData(scrapFileName, pcNetworkCardName, (spanTime-30))
        flowRes = loadDataAndCalculateFlow(scrapFileName, enbIp, pcIp, dir, type)
        svSocket.close()
        return flowRes
    
    def binding_port_and_network(self, port, networkType, flowType='udp', ipType='ipv4'):
        addRes = False
        #删除端口规则 
        delRes = self.modify_port_rule('del', port, networkType, flowType, ipType)
        sleep(3)
        #增加端口规则
        if delRes == True:
            addRes = self.modify_port_rule('add', port, networkType, flowType, ipType)
        return addRes
        
    def modify_port_rule(self, operateType, port, networkType, flowType='udp', ipType='ipv4'):
        self._channel.send('cd /usr/bin\r')
        time.sleep(2)
        if networkType == 'NR':
            cmdStr = './set_multiwan_rule.sh -a '+operateType+' -n test'+networkType+' -f '+ipType+' -p '+flowType+' -t dports -o '+str(port)+' -w modem\r'
        elif networkType == 'WIFI':
            cmdStr = './set_multiwan_rule.sh -a '+operateType+' -n test'+networkType+' -f '+ipType+' -p '+flowType+' -t dports -o '+str(port)+' -w wifi_sta_wan\r'
        self._channel.send(cmdStr)
        time.sleep(2)
        cmdRes = self.rece_at_command()
        if operateType+' test'+networkType+' rule success' in cmdRes or 'rule:test'+networkType+' not exist' in cmdRes:
            return True
        else:
            return False
