# coding = utf-8
'''
Created on 2022年9月15日

@author: dj
'''
import json
import os
import re
import time

from BasicModel.basic.restful import HttpClient


class TversionModel(HttpClient):
    '''
    classdocs
    '''
#     baseUrl = 'http://version.hlt.com/'
    baseUrl = 'http://172.16.2.246/'
    
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
        newestVer = ''
        pattern = verBranch+"_([0-9,a-z]{6}).zip"
        verParBranch = verBranch.split('_')[0]
        timeStamp = str(int(time.time()))
        url = self.baseUrl+'-/json/Tversion/'+verParBranch+'?_='+timeStamp
        res = self.get_request(url).json()
        fileList = res['files']
        #查询当前版本的时间戳
        for fileInfo in fileList:
            fileName = fileInfo['name']
            if fileName == versionNum+'.zip' :
                curVerMTime = fileInfo['mtime']
#                 print('curVerMTime is :',curVerMTime) #1660104925093
                break
        #查询是否有最新版本存在
        for fileInfo in fileList:
            newVerMTime = fileInfo['mtime']
            fileName = fileInfo['name']
            if newVerMTime > curVerMTime and re.match(pattern, fileName) != None:
                curVerMTime = newVerMTime
                newestVer = fileName
        newestVer = newestVer.split('.zip')[0]
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
        fileSize = 0
        verBranch = verNum.split('_')[0]
        url = self.baseUrl+'Tversion/'+verBranch+'/'+verNum+'.zip?download=true'
        response = self.get_request(url)
        filePath = savePath +'/'+ verNum +'.zip'
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
# if __name__ == '__main__':
#     verBranch = 'BS5514'
#     verNum = 'BS5514_V1.30.30B2_0313cc'
#     savePath = 'F:\\log'
#     tv = Tversion()
# #     tv.download_gkg_to_local(verBranch, verNum, savePath)    
#     tv.get_newest_version('BS5514_V1.30.30B2','BS5514_V1.30.30B2_337c90')
        
        