# coding = 'utf-8'
'''
Created on 2022年10月27日
@author: dj
'''

import os

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
    
    def query_user_info(self, username='root'):
        header = URL_DICT_USER['queryPageUserInfos']['header']
        url = self.baseUrl+URL_DICT_USER['queryPageUserInfos']['action']
        body = URL_DICT_USER['queryPageUserInfos']['body']
        body.update({'userName':username})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def update_user_info(self, infoDict):
        header = URL_DICT_USER['userUpdate']['header']
        url = self.baseUrl+URL_DICT_USER['userUpdate']['action']
        body = URL_DICT_USER['userUpdate']['body']
        body.update(infoDict)
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def user_pass_reset(self, username):
        header = URL_DICT_USER['passreset']['header']
        url = self.baseUrl+URL_DICT_USER['passreset']['action']
        body = URL_DICT_USER['passreset']['body']
        body.update({'username':username})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def extend_user_account(self, userId, userExpiryDate):
        header = URL_DICT_USER['extendUserAccount']['header']
        url = self.baseUrl+URL_DICT_USER['extendUserAccount']['action']
        body = URL_DICT_USER['extendUserAccount']['body']
        body.update({'userID':userId, 'userExpiryDate':userExpiryDate})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def lock_user(self, userName):
        header = URL_DICT_USER['clockUserName']['header']
        url = self.baseUrl+URL_DICT_USER['clockUserName']['action']
        body = URL_DICT_USER['clockUserName']['body']
        body.update({'userName':userName})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo#{"result":0}
    
    def unlock_user(self, userName):
        header = URL_DICT_USER['unlockUserName']['header']
        url = self.baseUrl+URL_DICT_USER['unlockUserName']['action']
        body = URL_DICT_USER['unlockUserName']['body']
        body.update({'userName':userName})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def export_user_info(self, filepath, filename):
        header = URL_DICT_USER['exportUserInfo']['header']
        url = self.baseUrl+URL_DICT_USER['exportUserInfo']['action']+filename+'.xlsx&filePath=/var/hms/usmc/userInfo/'
        response = self.get_request(url, headers = header)
        filePath = filepath +'/'+ filename
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
    def delete_user(self, userName, userId, oprateUser='root'):
        header = URL_DICT_USER['userDelete']['header']
        url = self.baseUrl+URL_DICT_USER['userDelete']['action']
        body = URL_DICT_USER['userDelete']['body']
        body.update({'userName':userName, 'userID':userId, 'loginName':oprateUser})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def designate_user_role(self, userName, roleIdList, oprateUser='root'):
        header = URL_DICT_USER['designateUserRoleInfo']['header']
        url = self.baseUrl+URL_DICT_USER['designateUserRoleInfo']['action']
        body = URL_DICT_USER['designateUserRoleInfo']['body']
        body.update({'userName':userName, 'roleIdList':roleIdList, 'creatName':oprateUser})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    def designate_user_domain(self, userName, domainIdList, oprateUser='root'):
        header = URL_DICT_USER['designateUserDomainInfo']['header']
        url = self.baseUrl+URL_DICT_USER['designateUserDomainInfo']['action']
        body = URL_DICT_USER['designateUserDomainInfo']['body']
        body.update({'userName':userName, 'domainIdList':domainIdList, 'creatName':oprateUser})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo