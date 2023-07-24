# coding='utf-8'
'''
Created on 2023年6月28日
@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.timeSynData import TIME_SYN_URL_DICT


class TimeSynModel(HMS):
    
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def query_ntp_info(self):
        header = TIME_SYN_URL_DICT['query']['header']
        url = self.baseUrl+TIME_SYN_URL_DICT['query']['action']
        body = TIME_SYN_URL_DICT['query']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo# info dict
            
        
    def update_ntp_info(self, paraDict):
        header = TIME_SYN_URL_DICT['update']['header']
        url = self.baseUrl+TIME_SYN_URL_DICT['update']['action']
        body = TIME_SYN_URL_DICT['update']['body']
        body.update(paraDict)
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# '0'--success '1'--fail