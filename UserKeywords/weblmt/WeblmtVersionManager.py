# coding = 'utf-8'
'''
Created on 2022年12月27日

@author: autotest
'''
'''
        说明：weblmt上传版本
        参数：
    lmtObj:weblmt对象
    version:版本包名称
    localPath:版本包存储的本地路径
'''

import logging

import allure

from BasicService.weblmt.lmtVersionService import LmtVersionService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time


def key_weblmt_upload_version(lmtObj, version=BASIC_DATA['version']['upgradeVersion'], localPath=BASIC_DATA['version']['versionSavePath']):
    with allure.step(key_get_time() +": weblmt上传基站版本包："+version+'\n'):
        logging.info(key_get_time()+': weblmt upload gnb version package: '+version)
        uploadRes = LmtVersionService().lmtUploadVersionPkg(lmtObj, version, localPath)
        assert uploadRes == True, 'weblmt上传基站版本包操作失败，请检查！'

'''
        说明：weblmt上查询版本上传结果
        参数：
    lmtObj:weblmt对象
    version:版本包名称
'''
def key_weblmt_query_upload_result(lmtObj, version=BASIC_DATA['version']['upgradeVersion']):
    with allure.step(key_get_time() +": weblmt上查询版本包上传结果，版本："+version+'\n'):
        logging.info(key_get_time()+': weblmt query upload result, version: '+version)
        queryUploadRes = LmtVersionService().lmtQueryUploadProcess(lmtObj, version)
        assert queryUploadRes == True, 'weblmt上传版本包失败，请检查！'
        
'''
        说明：weblmt上激活版本
        参数：
    lmtObj:weblmt对象
    version:版本包名称
'''
def key_weblmt_active_version(lmtObj, version=BASIC_DATA['version']['upgradeVersion']):
    with allure.step(key_get_time() +": weblmt上激活版本包："+version+'\n'):
        logging.info(key_get_time()+': weblmt active version package: '+version)
        activeRes = LmtVersionService().lmtActiveVersion(lmtObj, version)
        assert activeRes == True, 'weblmt上激活版本包失败，请检查！'


'''
        说明：weblmt上查询版本信息
        参数：
    lmtObj:weblmt对象
'''
def key_weblmt_query_version_info(lmtObj):
    with allure.step(key_get_time() +": weblmt上查询版本信息：\n"):
        logging.info(key_get_time()+': weblmt query version info')
        verInfo = LmtVersionService().lmtQueryVersionInfo(lmtObj)
        return verInfo