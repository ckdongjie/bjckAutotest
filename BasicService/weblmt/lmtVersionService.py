# coding = 'utf-8'
'''
Created on 2022年12月27日

@author: autotest

'''

import logging
from time import sleep

from BasicModel.weblmt.lmtVersionModel import LmtVersionModel
from UserKeywords.basic.basic import key_get_time


class LmtVersionService():
    '''
    classdocs
    '''

    '''
                在weblmt上传版本包到基站
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtUploadVersionPkg(self, lmtObj, version, localPath, tryNum=3):
        for i in range (1, tryNum+1):
            resCode, resInfo = LmtVersionModel(lmtObj).weblmt_start_upload(version)
            if resCode == 200 and resInfo['result']== 'success':
                break
            else:
                logging.info(key_get_time()+': upload fail, try again')
                sleep(1)
        if resCode == 200 and resInfo['result']== 'success':
            resCode, resInfo = LmtVersionModel(lmtObj).weblmt_upload_version(version, localPath)
            if resCode == 200 and resInfo['result']== "\u6587\u4ef6\"\"\u4e0a\u4f20\u6210\u529f":
                logging.info(key_get_time()+': start version upload on weblmt')
                return True
            else:
                logging.info(key_get_time()+': start version upload failure, upload result:'+str(resInfo))
                return False
        else:
            logging.info(key_get_time()+': start version upload failure, upload result:'+str(resInfo))
    
    '''
                查询 版本包上传进度
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtQueryUploadProcess(self, lmtObj, version):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_query_upload_process(version)
        return resInfo
    
    '''
                查询 版本包上传进度
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtActiveVersion(self, lmtObj, version):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_active_version(version)
        logging.info(key_get_time()+': active version result:'+str(resInfo))
        return resInfo
    
    '''
                查询版本信息
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtQueryVersionInfo(self, lmtObj):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_query_version_info()
        if resCode == 200 :
            logging.info(key_get_time()+': version info:'+str(resInfo))
            return resInfo
        
    '''
                查询版本包信息
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtQueryVersionPackageInfo(self, lmtObj):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_query_version_package_info()
        if resCode == 200 :
            logging.info(key_get_time()+': SwPkg info, run package:'+str(resInfo['data'][0]['PkgVer'])+'; back package:'+str(resInfo['data'][1]['PkgVer']))
            return resInfo['data'][0]['PkgVer'], resInfo['data'][1]['PkgVer']
            
        