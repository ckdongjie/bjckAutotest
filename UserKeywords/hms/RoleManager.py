'''
Created on 2023年6月25日
@author: dj
'''


import logging
import allure
from BasicService.hms.roleService import RoleService
from UserKeywords.basic.basic import key_get_time

'''
        说明：用户域分配
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_query_role_info(hmsObj):
    with allure.step(key_get_time() +": 查询角色信息\n"):
        logging.info(key_get_time()+': query role info')
        roleList = RoleService().query_role_info(hmsObj)
        with allure.step(key_get_time()+": 查询结果："+str(roleList)):
            logging.info(key_get_time()+": query result:"+str(roleList))
        return roleList