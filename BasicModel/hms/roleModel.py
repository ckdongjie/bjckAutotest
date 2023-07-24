'''
Created on 2023年6月25日

@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.roleData import URL_DICT_ROLE


class RoleModel(HMS):
    '''
    classdocs
    '''

    def __init__(self, hms):
        '''
        Constructor
        '''
        if hms:
            self.baseUrl = hms.baseUrl
        
    def query_role_info(self):
        header = URL_DICT_ROLE['findPageSubRoles']['header']
        url = self.baseUrl+URL_DICT_ROLE['findPageSubRoles']['action']+'roleId=1&start=0&limit=100'
        body = URL_DICT_ROLE['findPageSubRoles']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo