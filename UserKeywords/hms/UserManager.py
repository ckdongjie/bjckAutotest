# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''
'''
        说明：hms上添加用户
        参数：
    hmsObj:hms对象
    username:用户名
    password:密码
        返回：
'''

from datetime import datetime
import logging
import os

import allure

from BasicService.hms.userService import UserService
from UserKeywords.basic.basic import key_get_time
from UserKeywords.hms.DomainManager import key_query_doamin_info
from UserKeywords.hms.RoleManager import key_query_role_info


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
                
'''
        说明：hms上查询用户信息
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_query_user_info(hmsObj, username, queryUsername='root'):
    with allure.step(key_get_time() +": 查询网管用户信息\n"):
        logging.info(key_get_time()+': query user info')
        userInfoList = UserService().query_user_info(hmsObj, queryUsername)
        if userInfoList != []:
            for userInfo in userInfoList:
                if userInfo['userName'] == username:
                    break
            with allure.step(key_get_time() +": 用户["+username+"]的信息："+str(userInfo)):
                logging.info(key_get_time()+': user ['+username+'] info:'+str(userInfo))
                return userInfo
        else:
            with allure.step(key_get_time() +": 用户信息查询失败"):
                logging.warning(key_get_time()+': query user info failure')
                return {}
            
'''
        说明：hms上查询用户信息
        参数：
    hmsObj:hms对象
    username:用户名
    updateInfoDict:用户信息字典
        返回：
'''
def key_update_user_info(hmsObj, username, updateInfoDict):
    with allure.step(key_get_time() +": 更新用户信息\n"):
        logging.info(key_get_time()+': update user info')
        userInfoList = UserService().query_user_info(hmsObj)
        if userInfoList != []:
            for userInfo in userInfoList:
                if userInfo['userName'] == username:
                    break
            with allure.step(key_get_time() +": 用户["+username+"]的原始信息："+str(userInfo)):
                logging.info(key_get_time()+': user ['+username+'] original info:'+str(userInfo))
        userInfo.upadte(updateInfoDict)
        updateRes = UserService().update_user_info(hmsObj, userInfo)
        if updateRes == True:
            with allure.step(key_get_time() +": 用户信息更新成功"):
                logging.info(key_get_time()+': update user info success')
        else:
            with allure.step(key_get_time() +": 用户信息更新失败"):
                logging.warning(key_get_time()+': update user info failure')
        assert updateRes == True, '用户信息更新失败，请检查！'
        
'''
        说明：hms上重置用户密码
        参数：
    hmsObj:hms对象
    username:用户名
    updateInfoDict:用户信息字典
        返回：
'''
def key_reset_user_pass(hmsObj, username):
    with allure.step(key_get_time() +": 重置用户密码\n"):
        logging.info(key_get_time()+': reset user password')
        resetRes = UserService().user_pass_reset(hmsObj, username)
        if resetRes == 0:
            with allure.step(key_get_time() +": 用户密码重置成功"):
                logging.info(key_get_time()+': reset user password success')
        else:
            with allure.step(key_get_time() +": 用户密码重置失败"):
                logging.warning(key_get_time()+': reset user password failure')
        assert resetRes == 0, '重置用户密码失败，请检查！'
        
'''
        说明：hms上扩展用户有效期
        参数：
    hmsObj:hms对象
    username:用户名
    userExpiryDate:扩展日期
        返回：
'''
def key_extend_user_account(hmsObj, username, userExpiryDate):
    with allure.step(key_get_time() +": 重置用户密码\n"):
        logging.info(key_get_time()+': reset user password')
        userInfoList = UserService().query_user_info(hmsObj)
        if userInfoList != []:
            for userInfo in userInfoList:
                if userInfo['userName'] == username:
                    userId = userInfo['userID']
                    break
        extendRes = UserService().extend_user_account(hmsObj, userId, userExpiryDate)
        if extendRes['result'] == 0:
            with allure.step(key_get_time() +": 用户账户有效期扩展成功"):
                logging.info(key_get_time()+': extend user date success')
        else:
            with allure.step(key_get_time() +": 用户账户有效期扩展失败，原因："+str(extendRes)):
                logging.warning(key_get_time()+': extend user date failure, reason:'+str(extendRes))
        assert extendRes['result'] == 0, '用户账户有效期扩展失败，请检查！'
        
'''
        说明：锁定用户
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_lock_user(hmsObj, username):
    with allure.step(key_get_time() +": 锁定用户\n"):
        logging.info(key_get_time()+': lock user')
        lockRes = UserService().lock_user(hmsObj, username)
        if lockRes['result'] == 0:
            with allure.step(key_get_time() +": 用户锁定成功"):
                logging.info(key_get_time()+': lock user success')
        else:
            with allure.step(key_get_time() +": 用户锁定失败，原因："+str(lockRes)):
                logging.warning(key_get_time()+': lock user failure, reason:'+str(lockRes))
        assert lockRes['result'] == 0, '用户锁定失败，请检查！'
        
'''
        说明：解锁定用户
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_unlock_user(hmsObj, username):
    with allure.step(key_get_time() +": 解锁定用户\n"):
        logging.info(key_get_time()+': unlock user')
        unlockRes = UserService().unlock_user(hmsObj, username)
        if unlockRes['result'] == 0:
            with allure.step(key_get_time() +": 用户锁定成功"):
                logging.info(key_get_time()+': lock user success')
        else:
            with allure.step(key_get_time() +": 用户解锁定失败，原因："+str(unlockRes)):
                logging.warning(key_get_time()+': unlock user failure, reason:'+str(unlockRes))
        assert unlockRes['result'] == 0, '用户解锁定失败，请检查！'
        
'''
        说明：解锁定用户
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_export_user_info(hmsObj):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    filepath = BASE_DIR+'\\AutoTestMain\\hmsLog\\UserInfo'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    nowtime = datetime.now()
    filename = 'userInfo_'+nowtime.strftime('%Y%m%d%H%M%S')
    with allure.step(key_get_time() +": 导出用户信息\n"):
        logging.info(key_get_time()+': export user info')
        fileSize = UserService().export_user_info(hmsObj, filepath,filename)
        if fileSize != 0:
            with allure.step(key_get_time() +": 用户信息导出成功"):
                logging.info(key_get_time()+': export user info success')
        else:
            with allure.step(key_get_time() +": 用户信息导出失败"):
                logging.warning(key_get_time()+': export user info failure')
        assert fileSize != 0, '用户信息导出失败，请检查！'
        
'''
        说明：删除用户
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_delete_user(hmsObj, username):
    with allure.step(key_get_time() +": 删除用户\n"):
        logging.info(key_get_time()+': delete user')
        userInfoList = UserService().query_user_info(hmsObj)
        if userInfoList != []:
            for userInfo in userInfoList:
                if userInfo['userName'] == username:
                    userId = userInfo['userID']
                    break
        delRes = UserService().del_user(hmsObj, username, userId)
        if delRes['result'] == 0:
            with allure.step(key_get_time() +": 用户删除成功"):
                logging.info(key_get_time()+': delete user success')
        else:
            with allure.step(key_get_time() +": 用户删除失败，原因："+str(delRes)):
                logging.warning(key_get_time()+': delete user failure, reason:'+str(delRes))
        assert delRes['result'] == 0, '用户删除失败，请检查！'
        
'''
        说明：用户角色分配
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_designate_user_role(hmsObj, username, roleList):
    with allure.step(key_get_time() +": 分配用户角色\n"):
        logging.info(key_get_time()+': designate user role')
        roleIdList = ''
        queryRoleList = key_query_role_info(hmsObj)
        for roleInfo in queryRoleList:
            roleName = roleInfo['roleName']
            if roleName in roleList:
                roleIdList = roleIdList + roleName['id']+','
        desRes = UserService().designate_user_role(hmsObj, username, roleIdList)
        if desRes['result'] == True:
            with allure.step(key_get_time() +": 用户角色分配成功"):
                logging.info(key_get_time()+': designate user role success')
        else:
            with allure.step(key_get_time() +": 用户角色分配失败，原因："+str(desRes)):
                logging.warning(key_get_time()+': designate user role failure, reason:'+str(desRes))
        assert desRes['result'] == True, '用户角色分配失败，请检查！'
        
'''
        说明：用户域分配
        参数：
    hmsObj:hms对象
    username:用户名
        返回：
'''
def key_designate_user_domain(hmsObj, username, domainList):
    with allure.step(key_get_time() +": 分配用户域\n"):
        logging.info(key_get_time()+': designate user domain')
        domainIdList = ''
        queryDomainList = key_query_doamin_info(hmsObj)
        for domainInfo in queryDomainList:
            domainName = domainInfo['domainName']
            if domainName in domainList:
                domainIdList = domainIdList + domainInfo['id']+','
        desRes = UserService().designate_user_domain(hmsObj, username, domainIdList)
        if desRes['result'] == True:
            with allure.step(key_get_time() +": 用户域分配成功"):
                logging.info(key_get_time()+': designate user domain success')
        else:
            with allure.step(key_get_time() +": 用户域分配失败，原因："+str(desRes)):
                logging.warning(key_get_time()+': designate user domain failure, reason:'+str(desRes))
        assert desRes['result'] == True, '用户域分配失败，请检查！'
        
