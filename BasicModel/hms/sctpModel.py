# coding = 'utf-8'
'''
Created on 2023年1月13日

@author: autotest
'''

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.sctpData import SCTP_URL_DICT


class SctpModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
        
    def ipv6_sctp_config_realtime_query(self, enbId):
        header = SCTP_URL_DICT['ipv6SctpAssocRealTimeQuery']['header']
        url = self.baseUrl+SCTP_URL_DICT['ipv6SctpAssocRealTimeQuery']['action']+enbId
        body = SCTP_URL_DICT['ipv6SctpAssocRealTimeQuery']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']
    
    def query_ipv6_sctp_config_info(self, enbId):
        header = SCTP_URL_DICT['findPageIPv6SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['findPageIPv6SctpAssoc']['action']+enbId
        body = SCTP_URL_DICT['findPageIPv6SctpAssoc']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['rows']
    
    def update_ivp6_sctp_config(self, enbId, paraDict):
        ipv6SctpInfo = self.query_ipv6_sctp_config_info(enbId)[0]
        header = SCTP_URL_DICT['updateIPv6SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['updateIPv6SctpAssoc']['action']
        ipv6SctpInfo.update(paraDict)
        body = ipv6SctpInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']
        
    def add_ivp6_sctp_config(self, enbId, paraDict):
        ipv6SctpInfo = self.query_ipv6_sctp_config_info(enbId)[0]
        header = SCTP_URL_DICT['insertIPv6SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['insertIPv6SctpAssoc']['action']
        ipv6SctpInfo.update(paraDict)
        body = ipv6SctpInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']#'0'--success
        
    def del_ivp6_sctp_config(self, enbId, assID):
        ipv6SctpInfoList = self.query_ipv6_sctp_config_info(enbId)
        for ipv6SctpInfo in ipv6SctpInfoList:
            if ipv6SctpInfo['assID'] == assID:
                break
        header = SCTP_URL_DICT['deleteIPv6SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['deleteIPv6SctpAssoc']['action']
        body = ipv6SctpInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']#'0'--success
        
    def ipv4_sctp_config_realtime_query(self, enbId):
        header = SCTP_URL_DICT['ipv4SctpAssocRealTimeQuery']['header']
        url = self.baseUrl+SCTP_URL_DICT['ipv4SctpAssocRealTimeQuery']['action']+enbId
        body = SCTP_URL_DICT['ipv4SctpAssocRealTimeQuery']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']
    
    def query_ipv4_sctp_config_info(self, enbId):
        header = SCTP_URL_DICT['findPageIPv4SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['findPageIPv4SctpAssoc']['action']+enbId
        body = SCTP_URL_DICT['findPageIPv4SctpAssoc']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['rows'][0]
    
    def update_ivp4_sctp_config(self, enbId, paraDict):
        ipv6SctpInfo = self.query_ipv4_sctp_config_info(enbId)
        header = SCTP_URL_DICT['updateIPv4SctpAssoc']['header']
        url = self.baseUrl+SCTP_URL_DICT['updateIPv4SctpAssoc']['action']
        ipv6SctpInfo.update(paraDict)
        body = ipv6SctpInfo
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']
        