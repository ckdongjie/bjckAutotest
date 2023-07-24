'''
Created on 2023年6月12日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.ngInterfaceData import NG_URL_DICT


class NgInterfaceModel(HMS):
    
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
        
    def ng_config_realtime_query(self, enbId):
        header = NG_URL_DICT['realtimeQueryNgInterfaceByEnbId']['header']
        url = self.baseUrl+NG_URL_DICT['realtimeQueryNgInterfaceByEnbId']['action']+enbId
        body = NG_URL_DICT['realtimeQueryNgInterfaceByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# '0'--success '1'--fail
    
    def query_ng_config_info(self, enbId):
        header = NG_URL_DICT['findPageNGInterface']['header']
        url = self.baseUrl+NG_URL_DICT['findPageNGInterface']['action']+enbId
        body = NG_URL_DICT['findPageNGInterface']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['rows'][0]
    
    def update_ng_config(self, enbId, paraDict):
        ngInfo = self.query_ng_config_info(enbId)
        header = NG_URL_DICT['updateNGInterface']['header']
        url = self.baseUrl+NG_URL_DICT['updateNGInterface']['action']
        ngInfo.update(paraDict)
        body = ngInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']#{"result":"0"}  0--success