# coding = 'utf-8'
'''
Created on 2022年10月27日
@author: dj
'''

import logging
from BasicModel.hms.userModel import UserModel
from UserKeywords.basic.basic import key_get_time


class UserService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    '''
                说明：查询用户是否已经创建
                参数：
        hmsObj:hms对象
        username:用户名
    '''    
    def query_user_is_exist(self, hmsObj, username):
        resCode, resInfo = UserModel(hmsObj).query_user_is_exist(username)
        if resCode == 200 and resInfo['result']=='false':
            return False
        else:
            return True
    
    '''
                说明：新增用户
                参数：
        hmsObj:hms对象
        username:用户名
        password:密码
    '''
    def add_user(self, hmsObj, username, password):
        resCode, resInfo = UserModel(hmsObj).add_user(username, password)
        if resCode == 200 and resInfo['result']=='true':
            return 'success'
        else:
            logging.warning(key_get_time()+':add user fail, fail info:'+str(resInfo))
            print(key_get_time()+':add user fail, fail info:'+str(resInfo))
            return 'fail'
        
    '''
                说明：查询用户信息
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def query_user_info(self, hmsObj, username='root'):
        resCode, resInfo = UserModel(hmsObj).query_user_info(username)
        if resCode == 200:
            return resInfo['rows']
        else:
            return []
        
    '''
                说明：更新用户信息
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def update_user_info(self, hmsObj, updateInfoDict):
        resCode, resInfo = UserModel(hmsObj).update_user_info(updateInfoDict)
        if resCode == 200:
            return resInfo['result']
        else:
            return False
        
    '''
                说明：更新用户信息
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def user_pass_reset(self, hmsObj, username):
        resCode, resInfo = UserModel(hmsObj).user_pass_reset(username)
        if resCode == 200:
            return resInfo['result']#0--success  1--fail
        else:
            return 1  
        
    '''
                说明：扩展用户账户有效期
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def extend_user_account(self, hmsObj, userId, userExpiryDate):
        resCode, resInfo = UserModel(hmsObj).extend_user_account(userId, userExpiryDate)
        if resCode == 200:
            return resInfo#0--success  1--fail
        else:
            return {}  
        
    '''
                说明：锁定用户
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def lock_user(self, hmsObj, username):
        resCode, resInfo = UserModel(hmsObj).lock_user(username)
        if resCode == 200:
            return resInfo#0--success  1--fail
        else:
            return {}  
    
    '''
                说明：解锁定用户
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def unlock_user(self, hmsObj, username):
        resCode, resInfo = UserModel(hmsObj).unlock_user(username)
        if resCode == 200:
            return resInfo#0--success  1--fail
        else:
            return {}  
        
    '''
                说明：用户信息导出
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def export_user_info(self, hmsObj, filepath, filename):
        fileSize = UserModel(hmsObj).export_user_info(filepath, filename)
        return fileSize  
    
    '''
                说明：删除用户
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def del_user(self, hmsObj, username, userid, operateuser='root'):
        resCode, resInfo = UserModel(hmsObj).delete_user(username, userid, operateuser)
        if resCode == 200:
            return resInfo#0--success  1--fail
        else:
            return {} 
        
    '''
                说明：用户角色分配
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def designate_user_role(self, hmsObj, username, roleIdList, operateuser='root'):
        resCode, resInfo = UserModel(hmsObj).designate_user_role(username, roleIdList, operateuser)
        if resCode == 200:
            return resInfo#true--success  false--fail
        else:
            return {} 
        
    '''
                说明：删除用户
                参数：
        hmsObj:hms对象
        username:用户名
    '''
    def designate_user_domain(self, hmsObj, username, domainIdList, operateuser):
        resCode, resInfo = UserModel(hmsObj).designate_user_domain(username, domainIdList, operateuser)
        if resCode == 200:
            return resInfo#true--success  false--fail
        else:
            return {} 
