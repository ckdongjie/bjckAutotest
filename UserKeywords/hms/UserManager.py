# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''

import logging

import allure

from BasicService.hms.userService import UserService
from UserKeywords.basic.basic import key_get_time

'''
        说明：hms上添加用户
        参数：
    hmsObj:hms对象
    username:用户名
    password:密码
        返回：
'''
def key_add_user(hmsObj, username, password):
    with allure.step(key_get_time() +": 添加网管用户\n"):
        logging.info(key_get_time()+': add user')
        isExist = UserService().query_user_is_exist(hmsObj, username)
        if not isExist:
            addRes = UserService().add_user(hmsObj, username, password)
            assert addRes == 'success', '用户添加失败，请检查！'
            with allure.step(key_get_time() +": 用户添加成功！\n"):
                logging.info(key_get_time()+': add user success!')
        else:
            with allure.step(key_get_time() +": 该用户已经存在，不需要重新添加！\n"):
                logging.warning(key_get_time()+': the user is existed, not need to add')