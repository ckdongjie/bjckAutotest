# coding = 'utf-8'
'''
Created on 2023年2月8日

@author: dj

'''

from datetime import datetime
import os
import re
import subprocess
from threading import Thread
import time

import paramiko


iperfPath = 'D:\iperf-3.1.3-win64'
pdnIp = '193.168.9.223'
pdnLoginIP='172.16.2.202'
logingUser='root'
loginPass='ck2022...'
cpeLoginUser='root' 
cpeLoginPass='snc123...'
cpeInfoDict={'192.168.1.1':['9996-UL-NR','9997-DL-WIFI']}
logDir='D:\iperf-3.1.3-win64'

def monitor_ping(cpeIp, cpeLoginUser, cpeLoginPass, pdnIp, testType):
    cpeChannel=login_host(cpeIp, cpeLoginUser, cpeLoginPass)
    if testType == 'NR':
        cmdStr = 'ping -I rmnet_data0 '+pdnIp
    elif testType == 'WIFI':
        cmdStr = 'ping -I ath0 '+pdnIp
    cpeChannel.send(cmdStr+'\n') 
    time.sleep(1)
    count = 0
    while(cpeChannel.recv_ready()):
        result = cpeChannel.recv(65535).decode() 
        print(result)
        PING_RUN = ping_result_mattch(result)
        if PING_RUN == True:
            if count > 10:
                print('-------------------------------------------------')
                print('--              ping recover normal            --')
                print('-------------------------------------------------')
                break
            else:
                count = count+1
        time.sleep(1)
    return PING_RUN

def query_pdu_ip(cpeIp, cpeLoginUser, cpeLoginPass):
    cpeChannel=login_host(cpeIp, cpeLoginUser, cpeLoginPass)
    mattchRes = ['','']
    for i in range (1, 50):
        cpeChannel.send('ifconfig\n')
        time.sleep(5)
        ipInfo = cpeChannel.rece_at_command()
        mattchRes = ip_info_mattch(ipInfo)
        if len(mattchRes)==2:
            break
        else:
            time.sleep(5)
    return mattchRes[0],[1]
    
    

def ip_info_mattch(ipInfo):
    pattern = '.*rmnet_data[0|1].*\n*.*inet addr:(.*)  Mask:255.255'
    result = re.findall(pattern, str)
    print('ip info mattch result is{0}'.format(result))
    return result
        
#ping包结果检查  
def ping_result_mattch(pingRes=''):
    pattern = '64 bytes from (.*)ttl=64 (.*)ms'
    result = re.findall(pattern, str(pingRes))
    if len(result)!=0:
        PING_RUN = True
    else:
        PING_RUN = False 
    return PING_RUN
    
#iperf客户端启动
def monitor_iperf(iperfPath, pdnIp, port, logFile, dir, errFile):
    if dir == 'DL':
        cmdStr = iperfPath+'\\iperf3 -c '+pdnIp+' -p '+port+' -i 1 -w 1000k -t 86400 -P 5 --logfile '+logFile+' -R'
    elif dir == 'UL':
        cmdStr = iperfPath+'\\iperf3 -c '+pdnIp+' -p '+port+' -i 1 -w 1000k -t 86400 -P 5 --logfile '+logFile
    time.sleep(2)
    subprocess.Popen(cmdStr, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk')
    time.sleep(3)
    IPERF_RUN = read_iperf_result(port, logFile, errFile)
    return IPERF_RUN
    
#iperf执行结果校验
def read_iperf_result(port, logFile, errFile):
    IPERF_RUN = True
    while True:
        time.sleep(1)
        with open(logFile, 'r') as fp:
            file_lines = fp.readlines()[-2:]
            for lines in file_lines:
                print(lines)
                IPERF_RUN = iperf_result_mattch(lines)
                if IPERF_RUN == False:
                    break
        if IPERF_RUN == False:
            break
    return IPERF_RUN

#杀死iperf客户端进程                
def kill_iperf_client(port, logFile, errFile):
    cmdStr = 'netstat -aon | findstr '+port
    pipe = subprocess.Popen(cmdStr, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk')
    iperfProStr = pipe.stdout.readline()
    print(iperfProStr)
    processId = win_iperf_result_mattch(iperfProStr)
    if processId != -1:
        killCmdStr = 'tskill '+processId
        subprocess.Popen(killCmdStr, shell=True, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='gbk')
        print('-------------------------------------------------')
        print('--               port:',port,'                   --')
        print('--             kill iperf client               --')    
        print('-------------------------------------------------')
    with open(logFile, 'r') as fp:
        file_lines = fp.readlines()[-5:]
        if 'error' not in file_lines:
            for lines in file_lines:
                rline = key_get_time()+' '+lines
                with open(errFile,'a') as cfile:
                    cfile.write(rline)
            with open(errFile,'a') as cfile:
                cfile.write(key_get_time()+' ---------------------iperf run error------------------'+'\n')


#iperf客户端查询进程 
def win_iperf_result_mattch(iperfProStr=''):
    pattern = '.*TCP.*ESTABLISHED\s*(.*)'
    result = re.findall(pattern, str(iperfProStr))
    if len(result)!=0:
        return result[0]
    else:
        return -1 

#iperf执行结果检查 
def iperf_result_mattch(iperfRes=''):
    print(iperfRes)
    pattern = '.*sec  0.00 Bytes  0.00 bits/sec.*'
    pattern2 = 'iperf Done'
    pattern3 = 'iperf3: error.*'
    result = re.findall(pattern, str(iperfRes))
    result2 = re.findall(pattern2, str(iperfRes))
    result3 = re.findall(pattern3, str(iperfRes))
    if len(result)!=0 or len(result2)!=0 or len(result3)!=0:
        print('-------------------------------------------------')
        print('--          iperf client run error             --')
        print('-------------------------------------------------')
        IPERF_RUN = False
    else:
        IPERF_RUN = True 
    return IPERF_RUN

#重启iperf服务端
def restart_iperf_server(port, ip=''):
    pdnChannel=login_host(pdnLoginIP, logingUser, loginPass)
    kill_iperf_process(pdnChannel, port)
    time.sleep(3)
    start_iperf_server(pdnChannel, port)
    time.sleep(3)

#登录pdn/cpe    
def login_host(hostIp, logingUser, loginPass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostIp, username=logingUser, password=loginPass)
    channel = ssh.invoke_shell()
    return channel

#启动iperf服务端监听
def start_iperf_server(channel, port):
    iperf_cmd = 'nohup iperf3 -s -p '+str(port)+' &'
    queryCmdRes = exec_cmd(channel, iperf_cmd)
    print(queryCmdRes)
    print('-------------------------------------------------')
    print('--             start iperf server              --')
    print('-------------------------------------------------')
 
#杀死iperf服务端监听    
def kill_iperf_process(channel, port):
    query_proc_cmd = 'netstat -anp|grep '+str(port)
    queryCmdRes = exec_cmd(channel, query_proc_cmd)
#     print(queryCmdRes)
    processId = iperf_query_result_mattch(queryCmdRes)
    if processId != -1:
        stop_proc_cmd = 'kill -9 '+str(processId)
        print("cmd", stop_proc_cmd)
        killRes = exec_cmd(channel, stop_proc_cmd)
        return killRes

#pdn上执行shell命令    
def exec_cmd(channel, commandStr, waitTime=1):
        channel.send(commandStr+'\n') 
        time.sleep(waitTime)
        res = rece_cmd_result(channel)
        return res
    
#读取shell命令返回值 
def rece_cmd_result(channel):
    try:
        result = ''
        while(channel.recv_ready()):
            result = result + channel.recv(65535).decode() 
        return result
    except:
        print('receive error!')

#查询iperf服务端进程   
def iperf_query_result_mattch(resString):
    pattern = '.*LISTEN\s*(.*)/iperf3'
    result = re.findall(pattern, resString)
    if len(result)!=0:
        print('-------------------------------------------------')
        print('--              kill iperf server              --')
        print('-------------------------------------------------')
        return result[0]
    else:
        return -1

def key_get_time():
    nowtime = datetime.now()
    nowtime.strftime('%Y-%m-%d %H:%M:%S')
    timeStr = str(nowtime).split('.')[0]
    return timeStr

#单端口监听
def one_port_monitor(cpeIp, port, dir, testType):
    nowtime = key_get_time().replace(':','_').replace(' ','_')
    logFile = logDir+'\\'+nowtime+'_'+cpeIp+'_'+port+'_log.txt'
    errFile = logDir+'\\'+nowtime+'_'+cpeIp+'_'+port+'_error.txt'
    IPERF_RUN = monitor_iperf(iperfPath, pdnIp, port, logFile, dir, errFile)
    while IPERF_RUN == False:
        PING_RUN = monitor_ping(cpeIp, cpeLoginUser, cpeLoginPass, pdnIp, testType)
        if PING_RUN == True:
            nrIp, wifiIp = query_pdu_ip(cpeIp, cpeLoginUser, cpeLoginPass)
            kill_iperf_client(port, logFile, errFile)
            time.sleep(3)
            if testType == 'NR':   
                restart_iperf_server(port, nrIp)
            elif testType == 'WIFI':
                restart_iperf_server(port, wifiIp)
            time.sleep(3)
            IPERF_RUN = monitor_iperf(iperfPath, pdnIp, port, logFile, dir, errFile)
         
def login(cpeIp, port, dir):
    while True:
        print(cpeIp, port, dir)
        time.sleep(2)
    
def thread_it(func, *args):
    #创建线程
    t = Thread(target=func, args=args)
    #守护
    t.setDaemon(True)
    #启动
    t.start()
    return t  
               
if __name__ == '__main__':
    print('***********************************************************************')
    print('**                     Cell traffic test                             **')
    print('***********************************************************************')
    thList =[]
    for cpeInfo in cpeInfoDict.keys():
        cpeIp = cpeInfo
        portList = cpeInfoDict[cpeInfo]
        for portInfo in portList:#'9996-DL-NR'
            infoList = portInfo.split('-')
            port = infoList[0]
            dir = infoList[1]
            testType = infoList[2]
            thList.append(thread_it(one_port_monitor, cpeIp, port, dir, testType))
    for th in thList:
        th.join()
    print('*************exit************')
        
        