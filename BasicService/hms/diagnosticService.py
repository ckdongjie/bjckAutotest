# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
import json
import random
from time import sleep

from BasicModel.hms.diagnosticModel import DiagnosticModel


class DiagnosticService():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    '''
                基站复位
                参数：
        hmsObj:hms对象
        serialNumber:基站序列号
    '''    
    def reboot_enb(self, hmsObj, enbId):
        resCode, resInfo = DiagnosticModel(hmsObj).reboot_enb(enbId)
        return resCode, resInfo
            
            
    '''
                基站ping诊断
                参数：
        hmsObj:hms对象
        serialNumber:基站序列号
    '''    
    def gnb_ping_diag(self, hmsObj, pingTimes, gnbIp):
        clientId = DiagnosticModel(hmsObj).get_client_id()
        DiagnosticModel(hmsObj).binding_client_id_diag(clientId)
        resInfo = DiagnosticModel(hmsObj).gnb_ping_diag(pingTimes, gnbIp)
        return clientId, resInfo
    
    '''
                获取基站ping诊断
                参数：
        hmsObj:hms对象
        serialNumber:基站序列号
    '''    
    def get_gnb_ping_diag_res(self, hmsObj, pingTimes, clientId):
        reqId = 1
        isFinish = False
        for i in range (1, pingTimes+1):
            resCode, resInfo = DiagnosticModel(hmsObj).get_ping_diag_res(str(reqId),clientId)
            reqId = reqId+1
            pingRes = ''
            for info in resInfo:
                if info['channel'] == "/enb/diagnose":
                    pingInfo = json.loads(json.loads(info['data']))
                    pingRes = pingRes+pingInfo['content']+'\r\n'
                    if pingInfo['finish']==True:
                        isFinish = True
            if isFinish == True:
                break
            sleep(1)
        return pingRes
    
    '''
                基站跟踪路由诊断
                参数：
        hmsObj:hms对象
        serialNumber:基站序列号
    '''    
    def gnb_trace_route_diag(self, hmsObj, gnbIp):
        clientId = DiagnosticModel(hmsObj).get_client_id()
        DiagnosticModel(hmsObj).binding_client_id_diag(clientId)
        resInfo = DiagnosticModel(hmsObj).gnb_trace_route_diag(gnbIp)
        return clientId, resInfo
    
    '''
                获取基站跟踪路由诊断结果
                参数：
        hmsObj:hms对象
        clientId:客户端id
    '''    
    def get_gnb_trace_route_diag_res(self, hmsObj, clientId, tryNum=30):
        reqId = 1
        isFinish = False
        for i in range (1, tryNum+1):
            resCode, resInfo = DiagnosticModel(hmsObj).get_ping_diag_res(str(reqId),clientId)
            reqId = reqId+1
            traceRouteRes = ''
            for info in resInfo:
                if info['channel'] == "/enb/diagnose":
                    traceInfo = json.loads(json.loads(info['data']))
                    print(traceInfo['content'])
                    traceRouteRes = traceRouteRes+traceInfo['content']+'\r\n'
                    if traceInfo['finish']==True:
                        isFinish = True
            if isFinish == True:
                break
            sleep(1)
        return traceRouteRes
    
    '''
                获取基站信令跟踪参数
                参数：
        hmsObj:hms对象
        sn:基站sn号
    '''    
    def get_gnb_trace_me_para(self, hmsObj, sn):
        paraDict = DiagnosticModel(hmsObj).find_trace_me_para(sn)
        return paraDict
    
    '''
                更新基站信令跟踪参数
                参数：
        hmsObj:hms对象
        paraDict:修改参数字典
    '''    
    def update_gnb_trace_me_para(self, hmsObj, sn, paraDict):
        updateParaDict = {}
        souParaDict = self.get_gnb_trace_me_para(hmsObj, sn)
        updateParaDict.update({'serialNumber':souParaDict['souParaDict'], 'enbId':souParaDict['enbId'], 'enbName':souParaDict['enbName']})
        updateParaDict.update(paraDict)
        updateRes = DiagnosticModel(hmsObj).modify_trace_me_para(updateParaDict)
        return updateRes