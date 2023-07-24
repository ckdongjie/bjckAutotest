# coding = 'utf-8'
'''
Created on 2022年11月11日

@author: dj
'''

from BasicModel.weblmt.lmtXmlModel import LmtXmlModel


class LmtXmlService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    '''
                下载xml文件到本地目录
                参数：
        xmlFilename:xml文件名,默认是BntCfgFile
        savePath:保存xml文件的本地路径
    '''    
    def export_xml_file_to_local(self, lmt, savePath, xmlFilename='BntCfgFile'):
        fileSize = LmtXmlModel(lmt).export_xml_file_to_local(savePath, xmlFilename)
        if fileSize != 0:
            return fileSize
        else:
            return 0
    
    '''
                下载xml文件到本地目录
                参数：
        xmlFilename:xml文件名,默认是BntCfgFile
        savePath:保存xml文件的本地路径
    '''    
    def upload_xml_file_to_lmt(self, lmt, localPath, filename='BntCfgFile'):
        uploadRes = LmtXmlModel(lmt).upload_xml_file_to_lmt(localPath, filename)
        return uploadRes
    
    '''
                导入xml文件到基站
                参数：
        fileName:xml文件名,默认是BntCfgFile
        staType:xml文件针对的基站类型
    '''    
    def import_xml_file_to_gnb(self, lmt, fileName, staType='BS5514'):
        importRes = LmtXmlModel(lmt).import_xml_file_to_gnb(fileName, staType)
        return importRes