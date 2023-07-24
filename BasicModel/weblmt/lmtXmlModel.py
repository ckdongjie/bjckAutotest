# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj

'''

import os
from BasicModel.weblmt.requestdata.xmlManagerData import LMT_XML_URL_DICT
from BasicModel.weblmt.weblmt import WebLmt


class LmtXmlModel(WebLmt):
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
                下载xml文件到本地目录
                参数：
        xmlFilename:xml文件名,默认是BntCfgFile
        savePath:保存xml文件的本地路径
    '''    
    def export_xml_file_to_local(self, savePath, xmlFilename='BntCfgFile'):
        url = self.baseUrl+LMT_XML_URL_DICT['BntCfgExport']['action']
        response = self.get_request(url)
        filePath = savePath +'/'+ xmlFilename
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
    '''
                上传xml文件到weblmt
                参数：
        localPath:保存xml文件的本地路径
        filename:xml文件名,默认是BntCfgFile
    '''    
    def upload_xml_file_to_lmt(self, localPath, filename='BntCfgFile'):
        url = self.baseUrl+LMT_XML_URL_DICT['upload_BntCfgFile']['action']
        header = LMT_XML_URL_DICT['upload_BntCfgFile']['header']
        body = LMT_XML_URL_DICT['upload_BntCfgFile']['body']
        uploadFile = localPath+'/'+filename
        files = {'file':(filename, open(uploadFile, 'rb'), 'application/octet-stream'),}
        response = self.post_request(url, data=body, headers=header, files = files)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            return  resInfo  # {"result": "yes", "filename": "BntCfgFile"}
    
    '''
                同步xml文件到基站
                参数：
        fileName:xml文件名,默认是BntCfgFile
        staType:数据类型
    '''    
    def import_xml_file_to_gnb(self, fileName, staType='BS5514'):
        url = self.baseUrl+LMT_XML_URL_DICT['BntCfgImport']['action']
        header = LMT_XML_URL_DICT['BntCfgImport']['header']
        body = LMT_XML_URL_DICT['BntCfgImport']['body']
        params = {'fileName':fileName, 'staType':staType}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()  #{"staType": "BS5514", "script": "yes", "result": "success", "checkFlag": 0, "fileName": "/tmp/BntCfgFile"}
        if resCode == 200:
            return resInfo
    
    
if __name__ == '__main__':
    lmt = LmtXmlModel(WebLmt('172.16.2.152'))
    fileSize = lmt.export_xml_file_to_local('F:\\eclipseworkspace\\autotestPro\\AutoTestMain\\xmlFile')
    print(fileSize)