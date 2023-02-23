# coding = 'utf-8'

'''
Created on 2022年10月17日

@author: dj
'''

from BasicModel.hms.versionModel import EnbVersionModel

class VersionService():
    '''
    classdocs
    '''
    
    '''
                说明：查询基站版本信息
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
    '''
    def query_gnb_version_info(self, hmsObj, serialNumber):
        resCode, resInfo = EnbVersionModel(hmsObj).query_gnb_version_info(serialNumber)
        return resCode, resInfo
    
    '''
                说明：查询基站版本信息
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
    '''
    def query_gnb_version_info_from_device(self, hmsObj, serialNumber):
        resCode, resInfo = EnbVersionModel(hmsObj).query_gnb_version_info_from_device(serialNumber)
        return resCode, resInfo
    
    '''
                说明：下载基站版本
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
        softVersion:版本号
    '''
    def download_gnb_version(self, hmsObj, serialNumberList, softVersion, user='root'):
        resCode, resInfo = EnbVersionModel(hmsObj).download_gnb_version(serialNumberList, softVersion, user)
        return resCode, resInfo
    
    '''
                说明：版本下载状态查询
                参数：
        hmsObj:hms对象
        enbName:基站名
    '''
    def query_download_status(self, hmsObj, enbName):
        dowStatus = EnbVersionModel(hmsObj).query_download_status(enbName)
        return dowStatus
    
    '''
                说明：版本激活
                参数：
        hmsObj:hms对象
        serialNumberList:基站sn号
    '''
    def active_gnb_version(self, hmsObj, serialNumberList):
        resCode, resInfo = EnbVersionModel(hmsObj).active_gnb_version(serialNumberList)
        return resCode, resInfo
    
    '''
                说明：版本激活状态查询
                参数：
        hmsObj:hms对象
        enbName:基站名
    '''
    def query_active_status(self, hmsObj, enbName):
        activeStatus = EnbVersionModel(hmsObj).query_active_status(enbName)
        return activeStatus 
    
    '''
                说明：版本回退
                参数：
        hmsObj:hms对象
        serialNumberList:基站sn号
    '''
    def rollback_gnb_version(self, hmsObj, serialNumberList):
        resCode, resInfo = EnbVersionModel(hmsObj).rollback_gnb_version(serialNumberList)
        return resCode, resInfo
    
    '''
                说明：版本回退状态查询
                参数：
        hmsObj:hms对象
        enbName:基站名
    '''
    def query_rollback_status(self, hmsObj, enbName):
        rollStatus = EnbVersionModel(hmsObj).query_rollback_status(enbName)
        return rollStatus
    
    '''
                说明：查询版本包是否入库
                参数：
        hmsObj:hms对象
        softVersion:版本号
    '''
    def exist_in_version_management(self, hmsObj, softVersion):
        isExist = EnbVersionModel(hmsObj).exist_in_version_management(softVersion)
        return isExist
    
    '''
                说明：上传版本包到hms
                参数：
        hmsObj:hms对象
        fileSize:版本文件大小
        version:版本号
        localPath:本地目录
    '''
    def upload_version_to_hms(self, hmsObj, fileSize, version, localPath):
        resCode, resInfo = EnbVersionModel(hmsObj).upload_version_to_hms(fileSize, version, localPath)
        return resCode, resInfo
    
    '''
                说明：从基站上载配置到hms
                参数：
        hmsObj:hms对象
        dataDir:参数字典
    '''
    def upload_xml_file_from_gnb_to_hms(self, hmsObj, dataDir):
        resInfo = EnbVersionModel(hmsObj).upload_xml_file_from_gnb_to_hms(dataDir)
        return resInfo
    
    '''
                说明：查询基站xml文件信息
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
    '''
    def query_gnb_info_xml(self, hmsObj, serialNumber):
        dataDir = EnbVersionModel(hmsObj).query_gnb_info_xml(serialNumber)
        return dataDir
    
    '''
                说明：查询基站数据文件
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''
    def query_gnb_data_file(self, hmsObj, enbId):
        resInfo = EnbVersionModel(hmsObj).query_gnb_data_file(enbId)
        return resInfo
    
    '''
                说明：下载配置文件到本地目录
                参数：
        hmsObj:hms对象
        xmlPath:hms上xml文件目录
        xmlFilename:xml文件名
        savePath:文件保存路径
    '''
    def download_xml_file_to_local(self, hmsObj, xmlPath, xmlFilename, savePath):
        fileSize = EnbVersionModel(hmsObj).download_xml_file_to_local(xmlPath, xmlFilename, savePath)
        return fileSize
    
    '''
                说明：上传本地xml文件到hms
                参数：
        hmsObj:hms对象
        localPath:本地文件目录
        filename:xml文件名
        fileSize:xml文件大小
        checkData:是否校验数据
    '''
    def upload_xml_from_local_to_hms(self, hmsObj, localPath, filename, fileSize, isCheckData='true'):
        uploadRes = EnbVersionModel(hmsObj).upload_xml_from_local_to_hms(localPath, filename, fileSize, isCheckData)
        return uploadRes
    
    '''
                说明：查询hms上xml文件的id
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
    '''
    def query_xml_data_file_info(self, hmsObj, serialNumber):
        fileId = EnbVersionModel(hmsObj).query_xml_data_file_info(serialNumber)
        return fileId
    
    '''
                说明：删除hms上的xml文件
                参数：
        hmsObj:hms对象
        idsList:xml文件id列表
    '''
    def delete_xml_file_by_ids(self, hmsObj, idsList):
        delRes = EnbVersionModel(hmsObj).delete_xml_file_by_ids(idsList)
        return delRes
    
    '''
                说明：同步数据到基站
                参数：
        hmsObj:hms对象
        dataId:xml文件id
        serialNumber:基站sn号
        fileName:文件名
    '''
    def download_xml_from_hms_to_gnb(self, hmsObj, dataId, serialNumber, fileName):
        sysRes = EnbVersionModel(hmsObj).download_xml_from_hms_to_gnb(dataId, serialNumber, fileName)
        return sysRes