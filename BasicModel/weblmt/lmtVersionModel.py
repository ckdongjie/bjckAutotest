# coding = 'utf-8'
'''
Created on 2022年12月27日

@author: autotest
'''

from BasicModel.weblmt.requestdata.versionManagerData import LMT_VER_URL_DICT
from BasicModel.weblmt.weblmt import WebLmt


class LmtVersionModel(WebLmt):
    '''
    classdocs
    '''
    def __init__(self, lmtObj):
        '''
        Constructor
        '''
        if lmtObj:
            self.baseUrl = lmtObj.baseUrl
            self.ip = lmtObj.ip
          
    '''
                启动版本包上传
                参数：
        version:版本号
    '''
    def weblmt_start_upload(self, version):
        header = LMT_VER_URL_DICT['startUploadVersionPkg']['header']
        url = self.baseUrl+LMT_VER_URL_DICT['startUploadVersionPkg']['action']
        body = LMT_VER_URL_DICT['startUploadVersionPkg']['body']
        body.update({'fileName':version+'.zip'})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return  resCode, resInfo
            
    '''
                启动版本包上传
                参数：
        version:版本号
    '''
    def weblmt_query_upload_process(self, version):
        header = LMT_VER_URL_DICT['queryUploadProcess']['header']
        url = self.baseUrl+LMT_VER_URL_DICT['queryUploadProcess']['action']
        body = LMT_VER_URL_DICT['queryUploadProcess']['body']
        body.update({"fileName":version+'.zip'})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return  resCode, resInfo
    
    '''
                版本包激活
                参数：
        version:版本号
    '''
    def weblmt_active_version(self, version):
        header = LMT_VER_URL_DICT['activeVersion']['header']
        url = self.baseUrl+LMT_VER_URL_DICT['activeVersion']['action']
        body = LMT_VER_URL_DICT['activeVersion']['body']
        body.update({"fileName":version+'.zip'})
        response = self.post_request(url, json=body, headers = header)
        if response != None:
            resCode = response.status_code 
            resInfo = response.json()
            return  resCode, resInfo
        else:
            return None, None
    
    '''
                版本包激活
                参数：
        version:版本号
    '''
    def weblmt_query_version_info(self):
        header = LMT_VER_URL_DICT['queryVersionInfo']['header']
        url = self.baseUrl+LMT_VER_URL_DICT['queryVersionInfo']['action']
        body = LMT_VER_URL_DICT['queryVersionInfo']['body']
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return  resCode, resInfo
    
    '''
                上传版本包到weblmt
                参数：
        version:版本号
        localPath:文件路径
    '''
    def weblmt_upload_version(self, version, localPath):
        header = LMT_VER_URL_DICT['uploadVersionPkg']['header']
        url = self.baseUrl+LMT_VER_URL_DICT['uploadVersionPkg']['action']
        body = LMT_VER_URL_DICT['uploadVersionPkg']['body']
        uploadFile = localPath+'/'+version+'.zip'
        files = {'file':(version+'.zip', open(uploadFile, 'rb'), 'application/x-zip-compressed'),}
        response = self.post_request(url, data=body, headers=header, files = files)
        resCode = response.status_code 
        resInfo = response.json()
        return  resCode, resInfo
        
        