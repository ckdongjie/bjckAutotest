# coding = 'utf-8'
'''
Created on 2022年12月20日
@author: autotest

'''

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.csiRsData import CSIRS_URL_DICT
from time import sleep

class CsiRsModel(HMS):
    '''
    classdocs
    '''


    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        self.baseUrl = hmsObj.baseUrl
        
    def realtime_csi_rs_params(self, enbId, tryNum=3):
        header = CSIRS_URL_DICT['realtimeQueryCsiRsByEnbId']['header']
        url = self.baseUrl+CSIRS_URL_DICT['realtimeQueryCsiRsByEnbId']['action']+str(enbId)
        body = CSIRS_URL_DICT['realtimeQueryCsiRsByEnbId']['body']
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
    
    def query_csi_rs_params(self, enbId):
        header = CSIRS_URL_DICT['findCsiRsByEnbId']['header']
        url = self.baseUrl+CSIRS_URL_DICT['findCsiRsByEnbId']['action']+str(enbId)
        body = CSIRS_URL_DICT['findCsiRsByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
        
    def update_csi_rs_params(self, enbId, paraDict):
        self.realtime_csi_rs_params(enbId)
        infoDict = self.query_csi_rs_params(enbId)
        infoDict.update(paraDict)
        header = CSIRS_URL_DICT['updateCsiRs']['header']
        url = self.baseUrl+CSIRS_URL_DICT['updateCsiRs']['action']
        body = CSIRS_URL_DICT['updateCsiRs']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo    
        