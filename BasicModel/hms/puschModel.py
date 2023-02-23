# coding = 'utf-8'
'''
Created on 2023年02月22日

@author: autotest
'''

from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.puschData import PUSCH_URL_DICT


class PuschModel(HMS):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_pusch_params(self, enbId, tryNum=3):
        header = PUSCH_URL_DICT['realtimeQueryPuschByEnbId']['header']
        url = self.baseUrl+PUSCH_URL_DICT['realtimeQueryPuschByEnbId']['action']+str(enbId)
        body = PUSCH_URL_DICT['realtimeQueryPuschByEnbId']['body']
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
            
    def find_page_pusch_by_enbId(self, enbId):
        header = PUSCH_URL_DICT['findPagePuschByEnbId']['header']
        url = self.baseUrl+PUSCH_URL_DICT['findPagePuschByEnbId']['action']+str(enbId)
        body = PUSCH_URL_DICT['findPagePuschByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict

    def update_pusch_params(self, enbId, paraDict):
        self.realtime_query_pusch_params(enbId)
        infoDict = self.find_page_pusch_by_enbId(enbId)
        infoDict.update(paraDict)
        header = PUSCH_URL_DICT['updatePusch']['header']
        url = self.baseUrl+PUSCH_URL_DICT['updatePusch']['action']
        body = PUSCH_URL_DICT['updatePusch']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo