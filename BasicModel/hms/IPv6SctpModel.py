# coding = 'utf-8'
'''
Created on 2023年3月2日

@author: auto
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.ipv6SctpData import IPV6_SCTP_URL_DICT


class IPv6SctpModel(HMS):

    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_ipv6_sctp_params(self, enbId, tryNum=3):
        header = IPV6_SCTP_URL_DICT['realtimeQueryIpv6SctpByEnbId']['header']
        url = self.baseUrl+IPV6_SCTP_URL_DICT['realtimeQueryIpv6SctpByEnbId']['action']+str(enbId)
        body = IPV6_SCTP_URL_DICT['realtimeQueryIpv6SctpByEnbId']['body']
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
    
    def query_IPv6_Sctp_Assoc(self, enbId):
        header = IPV6_SCTP_URL_DICT['findPageIPv6SctpAssoc']['header']
        url = self.baseUrl+IPV6_SCTP_URL_DICT['findPageIPv6SctpAssoc']['action']+str(enbId)
        body = IPV6_SCTP_URL_DICT['findPageIPv6SctpAssoc']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
    
    def update_ipv6_sctp_params(self, enbId, paraDict):
        self.realtime_query_ipv6_sctp_params(enbId)
        infoDict = self.query_IPv6_Sctp_Assoc(enbId)
        infoDict.update(paraDict)
        header = IPV6_SCTP_URL_DICT['updateIPv6SctpAssoc']['header']
        url = self.baseUrl+IPV6_SCTP_URL_DICT['updateIPv6SctpAssoc']['action']
        body = IPV6_SCTP_URL_DICT['updateIPv6SctpAssoc']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo