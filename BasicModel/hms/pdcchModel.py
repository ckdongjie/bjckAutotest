# coding = 'utf-8'
'''
Created on 2022年12月13日

@author: autotest
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.pdcchData import PDCCH_URL_DICT


class PdcchModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
            
    def realtime_query_pdcch_params(self, enbId, tryNum=3):
        header = PDCCH_URL_DICT['realtimeQueryPdcchByEnbId']['header']
        url = self.baseUrl+PDCCH_URL_DICT['realtimeQueryPdcchByEnbId']['action']+str(enbId)
        body = PDCCH_URL_DICT['realtimeQueryPdcchByEnbId']['body']
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
    
    def query_pdcch_params(self, enbId):
        header = PDCCH_URL_DICT['findPagePdcchByEnbId']['header']
        url = self.baseUrl+PDCCH_URL_DICT['findPagePdcchByEnbId']['action']+str(enbId)
        body = PDCCH_URL_DICT['findPagePdcchByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
        
    def update_pdcch_params(self, enbId, paraDict):
        self.realtime_query_pdcch_params(enbId)
        infoDict = self.query_pdcch_params(enbId)
        infoDict.update(paraDict)
        header = PDCCH_URL_DICT['updatePdcch']['header']
        url = self.baseUrl+PDCCH_URL_DICT['updatePdcch']['action']
        body = PDCCH_URL_DICT['updatePdcch']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo
        