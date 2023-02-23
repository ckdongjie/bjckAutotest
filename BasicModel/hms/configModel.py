# coding = 'utf-8'
'''
Created on 2022年10月20日
@author: dj
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.configRequestData import URL_DICT


class ConfigModel(HMS):
    '''
    classdocs
    '''

    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
    def get_Mg_Server(self, enbId, tryNum=5):
        header = URL_DICT['getMgServer']['header']
        url = self.baseUrl+URL_DICT['getMgServer']['action']+str(enbId)
        body = URL_DICT['getMgServer']['body']
        infoDict = {}
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['result']=='0':
                infoDict = resInfo['resultObject']
                break
            else:
                sleep(15)
        return infoDict
        
    def update_Mg_Server(self, enbId, paraDict):
        infoDict = self.get_Mg_Server(enbId)
        infoDict.update(paraDict)
        header = URL_DICT['updateMgServer']['header']
        url = self.baseUrl+URL_DICT['updateMgServer']['action']
        body = URL_DICT['updateMgServer']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo
    
    def realtime_query_clock_info(self, enbId):
        header = URL_DICT['realtimeQueryClockInfo']['header']
        url = self.baseUrl+URL_DICT['realtimeQueryClockInfo']['action']+enbId
        body = URL_DICT['realtimeQueryClockInfo']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']
    
    
    def find_clock_info(self, enbId):
        header = URL_DICT['findClockInfo']['header']
        url = self.baseUrl+URL_DICT['findClockInfo']['action']+enbId
        body = URL_DICT['findClockInfo']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo
    
    def update_clock_params(self, enbId, paraDict):
        clockInfoDict = self.find_clock_info(enbId)
        header = URL_DICT['updateClockInfo']['header']
        url = self.baseUrl+URL_DICT['updateClockInfo']['action']
        clockInfoDict.update(paraDict)
        body = clockInfoDict
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo
    
#     def realtime_query_debug_switch(self, enbId):
        
    
    