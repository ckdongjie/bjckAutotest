# coding = utf-8
'''
Created on 2022年9月13日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.requestdata import URL_DICT


class CuModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        self.baseUrl = hmsObj.baseUrl
        
    def batchRealTimeQueryCuCellStatus(self, enbId):
        header = URL_DICT['batchRealTimeQueryCuCellStatus']['header']
        url = self.baseUrl+URL_DICT['batchRealTimeQueryCuCellStatus']['action']
        body = URL_DICT['batchRealTimeQueryCuCellStatus']['body']
        params = {"cuCellIdentifierList":[{"enbId":enbId,"cuCellInstanceId":1}]}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def query_cell_status(self, serialNumber):
        header = URL_DICT['queryCellStatus']['header']
        url = self.baseUrl+URL_DICT['queryCellStatus']['action']
        body = URL_DICT['queryCellStatus']['body']
        params = {'serialNumber':serialNumber}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
        
    def query_cu_cell_info(self, enbId):
        header = URL_DICT['findCuCellBasicByEnbId']['header']
        url = self.baseUrl+URL_DICT['findCuCellBasicByEnbId']['action']+str(enbId)
        body = URL_DICT['findCuCellBasicByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            infoDict = resInfo['rows'][0]
            infoDict.pop('enbInfo')
            infoDict.pop('nci')
        return infoDict
        
    def update_cu_cell_para(self, enbId, params):
        cuCellInfo = self.query_cu_cell_info(enbId)
        cuCellInfo.update(params)
        header = URL_DICT['updateCUCellBasic']['header']
        url = self.baseUrl+URL_DICT['updateCUCellBasic']['action']
        body = URL_DICT['updateCUCellBasic']['body']
        body.update(cuCellInfo) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:           
            return False   