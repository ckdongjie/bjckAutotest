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