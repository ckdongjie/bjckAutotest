# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.userData import URL_DICT_USER


class UserModel(HMS):
    '''
    classdocs
    '''

    def __init__(self, hms):
        '''
        Constructor
        '''
        if hms:
            self.baseUrl = hms.baseUrl
        
    def query_user_is_exist(self, usrename):
        header = URL_DICT_USER['userExist']['header']
        url = self.baseUrl+URL_DICT_USER['userExist']['action']+usrename
        body = URL_DICT_USER['userExist']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
        
    def add_user(self, username, password):
        header = URL_DICT_USER['userAdd']['header']
        url = self.baseUrl+URL_DICT_USER['userAdd']['action']
        body = URL_DICT_USER['userAdd']['body']
        body.update({'userName':username,'userPasswd':password})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo