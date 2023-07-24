import socket
import sys
import time

from BasicModel.basic.EIDetailConfigParse import GetsvLinkMsg, GetsvBasicMsg, \
    GetsvSpecificMsg, GetsvHeartBeat
from BasicModel.basic.sigTraceParse import GetLinkMsg, GetSigStartMsg, \
    GetSigHeartBeat
from reprlib import repr

class udpSocketModel:
    def socket_Sigclient(self, srcip, localIp, sigMointerPort=6080):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bindAddr = ('', sigMointerPort)
            s.bind(bindAddr)
            s.connect((srcip, 49152))
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        # 建链消息
        linkMsg = GetLinkMsg()
        s.send(linkMsg)
        time.sleep(0.5)
        # 启动信令跟踪任务
        sigTaskMsg = GetSigStartMsg(localIp)
        s.send(sigTaskMsg)
        time.sleep(0.5)
        #心跳消息
        heartBeat = GetSigHeartBeat()
        s.send(heartBeat)
        return s
    
    def socket_sv_basic_client(self, srcip, svMointerPort=16666):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bindAddr = ('', svMointerPort)
            s.bind(bindAddr)
            s.connect((srcip, 49152))
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        #链接请求
        svLinkMsg = GetsvLinkMsg()
        s.send(svLinkMsg)
        time.sleep(0.5)
        # 启动基本信息跟踪任务
        svBasicTaskMsg = GetsvBasicMsg()
        s.send(svBasicTaskMsg)
        time.sleep(0.5)
        
        #心跳消息
        heartBeat = GetsvHeartBeat()
        s.send(heartBeat)
        return s
    
    def socket_sv_deatil_client(self, srcip, tEiMsgList, svMointerPort=16667):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            bindAddr = ('', svMointerPort)
            s.bind(bindAddr)
            s.connect((srcip, 49152))
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        #链接请求
        svLinkMsg = GetsvLinkMsg()
        s.send(svLinkMsg)
        
        # 启动详细信息任务
        svSpecificTaskMsg = GetsvSpecificMsg(tEiMsgList)
        s.send(svSpecificTaskMsg)
        time.sleep(0.5)
        
        #心跳消息
        heartBeat = GetsvHeartBeat()
        s.send(heartBeat)
        return s