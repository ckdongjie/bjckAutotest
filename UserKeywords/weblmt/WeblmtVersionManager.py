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
import os

import allure

from BasicService.weblmt.lmtVersionService import LmtVersionService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login


def key_weblmt_upload_version(lmtObj, version=BASIC_DATA['version']['upgradeVersion']):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    with allure.step(key_get_time() +": weblmt上传基站版本包："+version+'\n'):
        logging.info(key_get_time()+': weblmt upload gnb version package: '+version)
        uploadRes = LmtVersionService().lmtUploadVersionPkg(lmtObj, version, localPath)
        if uploadRes == True:
            with allure.step(key_get_time()+': weblmt执行版本包上传成功'):
                logging.info(key_get_time()+': weblmt exec upload version package success')
        else:
            with allure.step(key_get_time()+': weblmt执行版本包上传失败'):
                logging.info(key_get_time()+': weblmt exec upload version package failure')
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
        if queryUploadRes['result']== 'success':
            with allure.step(key_get_time()+': weblmt上版本包上传成功'):
                logging.info(key_get_time()+': weblmt upload version package success')
        else:
            with allure.step(key_get_time()+': weblmt上版本包上传失败'):
                logging.info(key_get_time()+': weblmt upload version package failure, info:'+str(queryUploadRes))
        assert queryUploadRes['result']== 'success', 'weblmt上传版本包失败，请检查！'
        
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
        if activeRes['result'] == 'success':
            with allure.step(key_get_time()+": 版本包激活成功"):
                logging.info(key_get_time()+": weblmt active version success")
        else:
            with allure.step(key_get_time()+": 版本包激活失败"):
                logging.info(key_get_time()+": weblmt active version failure, info:"+str(activeRes))
        return activeRes['result']

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
    
'''
        说明：weblmt上查询版本信息
        参数：
    lmtObj:weblmt对象
'''
def key_weblmt_query_version_package_info(lmtObj):
    with allure.step(key_get_time() +": weblmt上查询版本包信息：\n"):
        logging.info(key_get_time()+': weblmt query version package info')
        runPkg, backPkg = LmtVersionService().lmtQueryVersionPackageInfo(lmtObj)
        return runPkg, backPkg
    
if __name__ == '__main__':
    weblmt = key_weblmt_login()
    runPkg, backPkg = key_weblmt_query_version_package_info(weblmt)
    print(runPkg, backPkg)