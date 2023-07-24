# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.requestdata import URL_DICT


class DiagnosticModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    '''
                基站复位
                参数：
        serialNumber:基站序列号
    '''    
    def reboot_enb(self, enbId):
        header = URL_DICT['reboot']['header']
        url = self.baseUrl+URL_DICT['reboot']['action']+str(enbId)
        body = URL_DICT['reboot']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                基站ping诊断
                参数：
        serialNumber:基站序列号
    '''    
    def gnb_ping_diag(self, pingTimes, gnbIp):
        header = URL_DICT['pingDiagnose']['header']
        url = self.baseUrl+URL_DICT['pingDiagnose']['action']
        paraDict = {"pingTimes":str(pingTimes),"ipList":[gnbIp]}
        body = paraDict
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        return resInfo
            
    '''
                获取基站ping诊断结果
                参数：
        serialNumber:基站序列号
    '''    
    def get_ping_diag_res(self, reqId, clientId):
        header = URL_DICT['getHmsReponse']['header']
        url = self.baseUrl+URL_DICT['getHmsReponse']['action']
        body = URL_DICT['getHmsReponse']['body']
        paraDict = {"id":reqId, 'clientId':clientId}
        body[0].update(paraDict)
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                获取client id
                参数：
        serialNumber:基站序列号
    '''    
    def get_client_id(self):
        header = URL_DICT['queryClientId']['header']
        url = self.baseUrl+URL_DICT['queryClientId']['action']
        body = URL_DICT['queryClientId']['body']
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        clientId = resInfo[0]['clientId']
        return clientId
    
    '''
                绑定client id
                参数：
        serialNumber:基站序列号
    '''    
    def binding_client_id_diag(self, clientId):
        header = URL_DICT['bandClientId']['header']
        url = self.baseUrl+URL_DICT['bandClientId']['action']
        body = URL_DICT['bandClientId']['body']
        body[0].update({'clientId':clientId})
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        res = resInfo[0]['successful']
        return res
    
    '''
                跟踪路由诊断
                参数：
        serialNumber:基站序列号
    '''    
    def gnb_trace_route_diag(self, gnbIp):
        header = URL_DICT['traceRouteDiagnose']['header']
        url = self.baseUrl+URL_DICT['traceRouteDiagnose']['action']
        paraDict = {"ipList":[gnbIp]}
        body = paraDict
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        return resInfo
    
    '''
                信念跟踪任务参数修改
                参数：
        :基站序列号
    '''    
    def find_trace_me_para(self, sn):
        header = URL_DICT['findPageTraceMeEnbs']['header']
        url = self.baseUrl+URL_DICT['findPageTraceMeEnbs']['action']
        body = URL_DICT['findPageTraceMeEnbs']['body']
        body.update({'serialNumber':sn})
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        return resInfo
    
    '''
                信念跟踪任务参数修改
                参数：
        :基站序列号
    '''    
    def modify_trace_me_para(self, paraDict):
        header = URL_DICT['traceRouteDiagnose']['header']
        url = self.baseUrl+URL_DICT['traceRouteDiagnose']['action']
        body = paraDict
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json()
        return resInfo