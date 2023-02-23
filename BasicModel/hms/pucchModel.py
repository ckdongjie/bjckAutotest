# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.pucchData import PUCCH_URL_DICT


class PucchModel(HMS):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_pucch_params(self, enbId, tryNum=3):
        header = PUCCH_URL_DICT['realtimeQueryPucchByEnbId']['header']
        url = self.baseUrl+PUCCH_URL_DICT['realtimeQueryPucchByEnbId']['action']+str(enbId)
        body = PUCCH_URL_DICT['realtimeQueryPucchByEnbId']['body']
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
            
    def findPagePucchByEnbId(self, enbId):
        header = PUCCH_URL_DICT['findPagePucchByEnbId']['header']
        url = self.baseUrl+PUCCH_URL_DICT['findPagePucchByEnbId']['action']+str(enbId)
        body = PUCCH_URL_DICT['findPagePucchByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict

    def update_pucch_params(self, enbId, paraDict):
        self.realtime_query_pucch_params(enbId)
        infoDict = self.findPagePucchByEnbId(enbId)
        infoDict.update(paraDict)
        header = PUCCH_URL_DICT['updatePucch']['header']
        url = self.baseUrl+PUCCH_URL_DICT['updatePucch']['action']
        body = PUCCH_URL_DICT['updatePucch']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo