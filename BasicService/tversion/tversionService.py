# coding = utf-8
'''
Created on 2022年9月15日

@author: dj
'''
import json
import os
import re
import time

from BasicService.basic.restful import HttpClient
from BasicModel.tversion.tversionModel import TversionModel


class TversionService(HttpClient):
    '''
    classdocs
    '''
    baseUrl = 'http://version.hlt.com/'
    
    def __init__(self):
        '''
        Constructor
        '''
    '''
               获取 分支版本的最新版本包
               参数：
        versionNum:版本号
        verBranch:版本分支，例：BS5514_V1.30.30
              返回值：
        newestVer:最新版本号
    '''    
    def get_newest_version(self, verBranch, versionNum):
        newestVer = TversionModel().get_newest_version(verBranch, versionNum)
        return newestVer
    
    '''
               下载版本包到本地路径
               参数：
        verNum:版本号
        savePath:文件保存路径
              返回值：
        fileSize:文件大小
    '''    
    def download_gkg_to_local(self, verNum, savePath):
        fileSize = TversionModel().download_gkg_to_local(verNum, savePath)
        return fileSize
    
# if __name__ == '__main__':
#     verBranch = 'BS5514'
#     verNum = 'BS5514_V1.30.30B2_0313cc'
#     savePath = 'F:\\log'
#     tv = TversionService()
# #     tv.download_gkg_to_local(verBranch, verNum, savePath)    
#     tv.get_newest_version('BS5514_V1.30.30B2','BS5514_V1.30.30B2_337c90')
        
        