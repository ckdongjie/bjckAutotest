# coding = 'utf-8'
'''
Created on 2023年02月22日

@author: autotest
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.pdschData import PDSCH_URL_DICT


class PdschModel(HMS):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_pdsch_params(self, enbId, tryNum=3):
        header = PDSCH_URL_DICT['realtimeQueryPdschByEnbId']['header']
        url = self.baseUrl+PDSCH_URL_DICT['realtimeQueryPdschByEnbId']['action']+str(enbId)
        body = PDSCH_URL_DICT['realtimeQueryPdschByEnbId']['body']
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
            
    def find_page_pdsch_by_enbId(self, enbId):
        header = PDSCH_URL_DICT['findPagePdschByEnbId']['header']
        url = self.baseUrl+PDSCH_URL_DICT['findPagePdschByEnbId']['action']+str(enbId)
        body = PDSCH_URL_DICT['findPagePdschByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict

    def update_pdsch_params(self, enbId, paraDict):
        self.realtime_query_pdsch_params(enbId)
        infoDict = self.find_page_pdsch_by_enbId(enbId)
        infoDict.update(paraDict)
        header = PDSCH_URL_DICT['updatePdsch']['header']
        url = self.baseUrl+PDSCH_URL_DICT['updatePdsch']['action']
        body = PDSCH_URL_DICT['updatePdsch']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo