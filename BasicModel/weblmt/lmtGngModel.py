'''
Created on 2022年10月27日

@author: dj
'''
from BasicModel.weblmt.requestdata.gnbManagerData import LMT_URL_DICT
from BasicModel.weblmt.weblmt import WebLmt


class LmtGnbModel(WebLmt):
    '''
    classdocs
    '''
    ip = ''
    port = '8090'
    baseUrl = 'http://'+ip+':'+port
    
    def __init__(self, lmtObj=None):
        '''
        Constructor
        '''
        if lmtObj:
            self.baseUrl = lmtObj.baseUrl
            self.ip = lmtObj.ip
    
    def lmtLogin(self, lmtIp, lmtPort='8090'):
        self.ip = lmtIp
        self.port = lmtPort
        self.baseUrl = 'http://'+lmtIp+':'+lmtPort
        return self
        
    def lmtRebootGnb(self):
        header = LMT_URL_DICT['BntReboot']['header']
        url = self.baseUrl+LMT_URL_DICT['BntReboot']['action']
        body = LMT_URL_DICT['BntReboot']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo    