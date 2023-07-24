'''
Created on 2023年6月6日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.taData import TA_URL_DICT


class TaModel(HMS):
    
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
        
    def ta_config_realtime_query(self, enbId):
        header = TA_URL_DICT['realtimeQueryTaByEnbId']['header']
        url = self.baseUrl+TA_URL_DICT['realtimeQueryTaByEnbId']['action']+enbId
        body = TA_URL_DICT['realtimeQueryTaByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# '0'--success '1'--fail
    
    def query_ta_config_info(self, enbId):
        header = TA_URL_DICT['findPageTaByEnbId']['header']
        url = self.baseUrl+TA_URL_DICT['findPageTaByEnbId']['action']+enbId
        body = TA_URL_DICT['findPageTaByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['rows'][0]
    
    def update_ta_config(self, enbId, paraDict):
        taInfo = self.query_ta_config_info(enbId)
        header = TA_URL_DICT['updateTa']['header']
        url = self.baseUrl+TA_URL_DICT['updateTa']['action']
        taInfo.update(paraDict)
        body = taInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']#{"result":"0"}  0--success