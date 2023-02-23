# coding = 'utf-8'
'''
Created on 2022年12月27日

@author: autotest

'''
import logging
from UserKeywords.basic.basic import key_get_time
from BasicModel.weblmt.lmtVersionModel import LmtVersionModel


class LmtVersionService():
    '''
    classdocs
    '''

    '''
                在weblmt上传版本包到基站
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtUploadVersionPkg(self, lmtObj, version, localPath):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_start_upload(version)
        if resCode == 200 and resInfo['result']== 'success':
            resCode, resInfo = LmtVersionModel(lmtObj).weblmt_upload_version(version, localPath)
            if resCode == 200 and resInfo['result']== "\u6587\u4ef6\"\"\u4e0a\u4f20\u6210\u529f":
                logging.info(key_get_time()+':start version upload on weblmt')
                return True
            else:
                logging.info(key_get_time()+':start version upload failure, upload result:'+resInfo['result'])
                return False
        else:
            logging.info(key_get_time()+':start version upload failure, upload result:'+resInfo['result'])
    
    '''
                查询 版本包上传进度
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtQueryUploadProcess(self, lmtObj, version):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_query_upload_process(version)
        if resCode == 200 and resInfo['result']== 'success':
            logging.info(key_get_time()+':version upload success')
            return True
        else:
            logging.info(key_get_time()+':version upload failure')
            return False
    
    '''
                查询 版本包上传进度
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtActiveVersion(self, lmtObj, version):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_active_version(version)
        logging.info(key_get_time()+':active version result:'+str(resInfo))
        if resCode == 200 and resInfo['result']== 'success':
            logging.info(key_get_time()+':active version success')
            return True
        else:
            logging.info(key_get_time()+':active version failure')
            return False
    
    '''
                查询版本信息
                参数：
        lmtObj:weblmt对象
    '''     
    def lmtQueryVersionInfo(self, lmtObj):
        resCode, resInfo = LmtVersionModel(lmtObj).weblmt_query_version_info()
        if resCode == 200 :
            logging.info(key_get_time()+':version info:'+str(resInfo))
            return resInfo
            
        