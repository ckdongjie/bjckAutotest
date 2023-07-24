# coding = 'utf-8'
'''
Created on 2023年6月8日
@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.wifiData import WIFI_URL_DICT


class WifiModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
        
    def wifi_config_realtime_query(self, enbId):
        header = WIFI_URL_DICT['realtimeQueryWifiConfigByEnbId']['header']
        url = self.baseUrl+WIFI_URL_DICT['realtimeQueryWifiConfigByEnbId']['action']+enbId
        body = WIFI_URL_DICT['realtimeQueryWifiConfigByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# '0'--success '1'--fail
    
    def query_wifi_config_info(self, enbId):
        header = WIFI_URL_DICT['findPageWifiConfig']['header']
        url = self.baseUrl+WIFI_URL_DICT['findPageWifiConfig']['action']+enbId
        body = WIFI_URL_DICT['findPageWifiConfig']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['rows'][0]
    
    def update_ta_config(self, enbId, paraDict):
        wifiInfo = self.query_wifi_config_info(enbId)
        header = WIFI_URL_DICT['updateWifiConfig']['header']
        url = self.baseUrl+WIFI_URL_DICT['updateWifiConfig']['action']
        wifiInfo.update(paraDict)
        body = wifiInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']#{"result":"0"}  0--success