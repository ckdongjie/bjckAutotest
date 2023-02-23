# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''

from BasicModel.weblmt.requestdata.cellManagerData import LMT_CELL_URL_DICT
from BasicModel.weblmt.weblmt import WebLmt


class LmtCellModel(WebLmt):
    '''
    classdocs
    '''


    def __init__(self, lmtObj):
        '''
        Constructor
        '''
        if lmtObj:
            self.baseUrl = lmtObj.baseUrl
            self.ip = lmtObj.ip
        
    def lmtQueryCellStatus(self):
        header = LMT_CELL_URL_DICT['QueryCuCellParams']['header']
        url = self.baseUrl+LMT_CELL_URL_DICT['QueryCuCellParams']['action']
        body = LMT_CELL_URL_DICT['QueryCuCellParams']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
        
    def lmtQueryDuCellParams(self):
        header = LMT_CELL_URL_DICT['QueryDuCellParams']['header']
        url = self.baseUrl+LMT_CELL_URL_DICT['QueryDuCellParams']['action']
        body = LMT_CELL_URL_DICT['QueryDuCellParams']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
        
    def lmtModifyDuCellParams(self, parsms):
        header = LMT_CELL_URL_DICT['ModifyDuCellParams']['header']
        url = self.baseUrl+LMT_CELL_URL_DICT['ModifyDuCellParams']['action']
        body = LMT_CELL_URL_DICT['ModifyDuCellParams']['body']
        body['data'] = parsms
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo