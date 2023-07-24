# coding = 'utf-8'
'''
Created on 2023年6月25日
@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.domainData import URL_DICT_DOMAIN

class DomainModel(HMS):

    def __init__(self, hms):
        '''
        Constructor
        '''
        if hms:
            self.baseUrl = hms.baseUrl
        
    def query_domain_info(self):
        header = URL_DICT_DOMAIN['getDomainInfobyId']['header']
        url = self.baseUrl+URL_DICT_DOMAIN['getDomainInfobyId']['action']+'domainId=1&start=0&limit=100'
        body = URL_DICT_DOMAIN['getDomainInfobyId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
        