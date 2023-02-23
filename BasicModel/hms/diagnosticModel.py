# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.requestdata import URL_DICT


class DiagnosticModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    '''
                基站复位
                参数：
        serialNumber:基站序列号
    '''    
    def reboot_enb(self, enbId):
        header = URL_DICT['reboot']['header']
        url = self.baseUrl+URL_DICT['reboot']['action']+str(enbId)
        body = URL_DICT['reboot']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
            