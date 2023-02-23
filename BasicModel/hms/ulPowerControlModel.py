# coding = 'utf-8'
'''
Created on 2022年12月22日

@author: autotest

'''

from BasicModel.hms.requestdata.ulPowerControlData import POWER_CONTROL_URL_DICT
from time import sleep

class ULPowerControlModel(object):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
       Constructor
        ''' 
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
            
    def realtime_query_ul_power_control_params(self, enbId, tryNum=3):
        header = POWER_CONTROL_URL_DICT['realtimeQueryULPowerControlByEnbId']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['realtimeQueryULPowerControlByEnbId']['action']+str(enbId)
        body = POWER_CONTROL_URL_DICT['realtimeQueryULPowerControlByEnbId']['body']
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
    
    def query_ul_power_control_params(self, enbId):
        header = POWER_CONTROL_URL_DICT['findPageULPowerControlByEnbId']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['findPageULPowerControlByEnbId']['action']+str(enbId)
        body = POWER_CONTROL_URL_DICT['findPageULPowerControlByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
        
    def update_ul_power_control_params(self, enbId, paraDict):
        self.realtime_query_ul_power_control_params(enbId)
        infoDict = self.query_ul_power_control_params(enbId)
        infoDict.update(paraDict)
        header = POWER_CONTROL_URL_DICT['updateULPowerControl']['header']
        url = self.baseUrl+POWER_CONTROL_URL_DICT['updateULPowerControl']['action']
        body = POWER_CONTROL_URL_DICT['updateULPowerControl']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo
        