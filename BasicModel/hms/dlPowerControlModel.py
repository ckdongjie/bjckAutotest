'''
Created on 2023年2月22日

@author: auto
'''

from BasicModel.hms.requestdata.ulPowerControlData import POWER_CONTROL_URL_DICT
from time import sleep

class DLPowerControlModel(object):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
       Constructor
        ''' 
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_dl_power_control_params(self, enbId, tryNum=3):
        header = POWER_CONTROL_URL_DICT['realtimeQueryDLPowerControlByEnbId']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['realtimeQueryDLPowerControlByEnbId']['action']+str(enbId)
        body = POWER_CONTROL_URL_DICT['realtimeQueryDLPowerControlByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        result = False
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['result']=='0':
                result = True
                break
            else:
                sleep(3)
        return result
    
    def query_dl_power_control_params(self, enbId):
        header = POWER_CONTROL_URL_DICT['findPageDLPowerControlByEnbId']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['findPageDLPowerControlByEnbId']['action']+str(enbId)
        body = POWER_CONTROL_URL_DICT['findPageDLPowerControlByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
        
    def update_dl_power_control_params(self, enbId, paraDict):
        self.realtime_query_dl_power_control_params(enbId)
        infoDict = self.query_dl_power_control_params(enbId)
        infoDict.update(paraDict)
        header = POWER_CONTROL_URL_DICT['updateDLPowerControl']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['updateDLPowerControl']['action']
        body = POWER_CONTROL_URL_DICT['updateDLPowerControl']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo