# coding='utf-8'
'''
Created on 2023年6月25日
@author: dj
'''
from BasicModel.hms.roleModel import RoleModel

class RoleService():
    
    def __init__(self):

        '''
        Constructor
        '''
    '''
                说明：查询角色信息
                参数：
        hmsObj:hms对象
    '''    
    def query_role_info(self, hmsObj):
        resCode, resInfo = RoleModel(hmsObj).query_role_info()
        return resInfo['rows']
        