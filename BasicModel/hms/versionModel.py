# coding = utf-8
'''
Created on 2022年9月13日

@author: dj
'''
import os
import time

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.requestdata import URL_DICT
from Tools.scripts.eptags import treat_file


class EnbVersionModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
    '''
                基站版本信息查询
                参数：
        serialNumber:基站序列号
    '''    
    def query_gnb_version_info(self, serialNumber):
        header = URL_DICT['queryVersionInfo']['header']
        url = self.baseUrl+URL_DICT['queryVersionInfo']['action']
        body = URL_DICT['queryVersionInfo']['body']
        params = {'serialNumber':serialNumber}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                基站版本信息查询
                参数：
        serialNumber:基站序列号
    '''    
    def query_gnb_version_info_from_device(self, serialNumber):
        header = URL_DICT['queryEnbSoftwareVersionFromDeviceBySns']['header']
        url = self.baseUrl+URL_DICT['queryEnbSoftwareVersionFromDeviceBySns']['action']
        body = URL_DICT['queryEnbSoftwareVersionFromDeviceBySns']['body']
        params = {"enbSns":[serialNumber]}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                基站版本下载
                参数：
        serialNumberList:基站序列号列表
        softVersion:版本号
    '''
#     @staticmethod
    def download_gnb_version(self, serialNumberList, softVersion, user='root'):
        header = URL_DICT['downloadVersion']['header']
        url = self.baseUrl+URL_DICT['downloadVersion']['action']
        body = URL_DICT['downloadVersion']['body']
        params = {'snList':serialNumberList, 'softVersion':softVersion}
        body.update(params) #更新body参数
        if user != 'root':
            newCook = 'lang=en-US; BAYEUX_BROWSER=1gscea1y4r6fqw93; warningFlag=false; sessioncode=c9y0ixx7zs; username='+user
            header.update({'Cookie':newCook})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                下载任务状态查询
                参数：
        enbName:基站别名
    '''
    def query_download_status(self, enbName):
        header = URL_DICT['findPageDownloadTask']['header']
        url = self.baseUrl+URL_DICT['findPageDownloadTask']['action']
        body = URL_DICT['findPageDownloadTask']['body']
        params = {'enbName':enbName}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['rows'][0]['opStatus']
    
    '''
                基站版本激活
                参数：
        serialNumberList:基站序列号列表
    '''
    def active_gnb_version(self, serialNumberList):
        header = URL_DICT['activeVersion']['header']
        url = self.baseUrl+URL_DICT['activeVersion']['action']
        body = URL_DICT['activeVersion']['body']
        params = {'snList':serialNumberList}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo
    
    '''
                激活任务状态查询
                参数：
        enbName:基站别名
    '''
    def query_active_status(self, enbName):
        header = URL_DICT['findPageActivateTask']['header']
        url = self.baseUrl+URL_DICT['findPageActivateTask']['action']
        body = URL_DICT['findPageActivateTask']['body']
        params = {'enbName':enbName}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['rows'][0]['opStatus']
    
    '''
                基站版本回退
                参数：
        serialNumberList:基站序列号列表
    '''
    def rollback_gnb_version(self, serialNumberList):
        header = URL_DICT['rollbackVersion']['header']
        url = self.baseUrl+URL_DICT['rollbackVersion']['action']
        body = URL_DICT['rollbackVersion']['body']
        params = {'snList':serialNumberList}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        return resCode, resInfo  
    
    '''
                回退任务状态查询
                参数：
        enbName:基站别名
    '''
    def query_rollback_status(self, enbName):
        header = URL_DICT['findPageRollbackTask']['header']
        url = self.baseUrl+URL_DICT['findPageRollbackTask']['action']
        body = URL_DICT['findPageRollbackTask']['body']
        params = {'enbName':enbName}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['rows'][0]['opStatus']
    
    '''
                版本包是否入库
                参数：
        softVersion:版本号
    '''
    def exist_in_version_management(self, softVersion):
        header = URL_DICT['findPageSoftWareInfo']['header']
        timeStamp = str(int(time.time()))
        url = self.baseUrl+URL_DICT['findPageSoftWareInfo']['action']+softVersion+'&start=0&limit=15&_time_stamp_='+timeStamp
        body = URL_DICT['findPageSoftWareInfo']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        findVer = False
        if resCode == 200 and resInfo['total'] != 0:
            for queryVersion in resInfo['rows']:
                if queryVersion['softVersion'] == softVersion:
                    findVer = True
                    break
            if findVer == True:
                return True
            else:
                return False
        else:
            return False  
        
    '''
                上传版本包到网管版本库
                参数：
        softVersion:版本号
    '''
    def upload_version_to_hms(self, fileSize, version, localPath):
        header = URL_DICT['uploadSoft']['header']
        url = self.baseUrl+URL_DICT['uploadSoft']['action']+str(fileSize)
        body = URL_DICT['uploadSoft']['body']
        uploadFile = localPath+'/'+version+'.zip'
        files = {'file':(version+'.zip', open(uploadFile, 'rb'), 'application/x-zip-compressed'),}
        params = {'softVersion':version}
        body.update(params)
        response = self.post_request(url, data=body, headers=header, files = files)
        resCode = response.status_code 
        resInfo = response.json()
        return  resCode, resInfo
    
    '''
                从基站上载xml数据到hms
                参数：
        dataDir:参数字典
    '''
    def upload_xml_file_from_gnb_to_hms(self, dataDir):
        header = URL_DICT['uploadDataFileXml']['header']
        url = self.baseUrl+URL_DICT['uploadDataFileXml']['action']
        body = URL_DICT['uploadDataFileXml']['body']
        body[0] = dataDir #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo
    
    '''
                查询上载xml文件需要的参数字典
                参数：
        serialNumber:基站sn号
    '''
    def query_gnb_info_xml(self, serialNumber):
        header = URL_DICT['queryPageEnbWithDataFileSyncStatusByCondition']['header']
        url = self.baseUrl+URL_DICT['queryPageEnbWithDataFileSyncStatusByCondition']['action']
        body = URL_DICT['queryPageEnbWithDataFileSyncStatusByCondition']['body']
        params = {'serialNumber':serialNumber}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['rows'][0]['enbInfo']
        
    '''
                查询hms上xml文件路径及文件名
                参数：
        enbId:基站enbId
    '''
    def query_gnb_data_file(self, enbId):
        header = URL_DICT['findEnbDataFile']['header']
        url = self.baseUrl+URL_DICT['findEnbDataFile']['action']+str(enbId)+'&start=0&limit=100000000'
        body = URL_DICT['findEnbDataFile']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo  
    
    '''
                下载xml文件到本地目录
                参数：
        xmlPath:hms上xml文件目录
        xmlFilename:hms上xml文件名
        savePath:保存xml文件的本地路径
    '''    
    def download_xml_file_to_local(self, xmlPath, xmlFilename, savePath):
        fileInfo = 'filepath='+xmlPath+'&filename='+xmlFilename
        url = self.baseUrl+URL_DICT['downloadXmlFileToLocal']['action']+fileInfo
        response = self.get_request(url)
        filePath = savePath +'/'+ xmlFilename
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    '''
                上载本地xml文件到hms
                参数：
        fileSize:xml文件大小
        checkData:是否进行文件校验
        confirm:确认导入
    '''
    def upload_xml_from_local_to_hms(self, localPath, filename, fileSize, isCheckData='true', confirm='false'):
        cmdStr = 'fileSize='+str(fileSize)+'&checkData='+isCheckData+'&confirm='+confirm
        header = URL_DICT['uploadXmlDataFile']['header']
        url = self.baseUrl+URL_DICT['uploadXmlDataFile']['action']+cmdStr
        body = URL_DICT['uploadXmlDataFile']['body']
        uploadFile = localPath+'/'+filename
        files = {'file':(filename, open(uploadFile, 'rb'), 'application/x-zip-compressed'),}
        response = self.post_request(url, data=body, headers=header, files = files)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            return  resInfo['result']
    
    '''
                查询xml文件信息
                参数：
        serialNumber:基站sn号
    '''
    def query_xml_data_file_info(self, serialNumber):
        header = URL_DICT['queryPageDataFile']['header']
        url = self.baseUrl+URL_DICT['queryPageDataFile']['action']
        body = URL_DICT['queryPageDataFile']['body']
        params = {'serialNumber':serialNumber}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            return resInfo['rows'][-1]['dataId']
    
    '''
                删除hms上xml文件信息
                参数：
        idsList:xml文件id列表
    '''
    def delete_xml_file_by_ids(self, idsList):
        header = URL_DICT['deleteDataFileByIds']['header']
        url = self.baseUrl+URL_DICT['deleteDataFileByIds']['action']
        body = idsList #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['result']  #0--成功， 1--失败
        
    '''
                同步xml文件到基站
                参数：
        dataId:xml文件id
        serialNumber:基站sn号
        fileName:xml文件名
    '''
    def download_xml_from_hms_to_gnb(self, dataId, serialNumber, fileName):
        header = URL_DICT['downloadDataFileToGnb']['header']
        url = self.baseUrl+URL_DICT['downloadDataFileToGnb']['action']
        body = URL_DICT['downloadDataFileToGnb']['body']
        params = {'dataId':dataId,'serialNumber':serialNumber,'fileName':fileName}
        body[0]=params #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        resInfo = response.json()
        if resCode == 200:
            return resInfo['result']    #0--成功  1--失败
    
if __name__ == '__main__':
    hms = EnbVersionModel(HMS('172.16.2.159'))
#     dataDir = hms.query_gnb_info_xml('902272840007')
#     print(dataDir)
#     result = hms.upload_xml_file_from_gnb_to_hms(dataDir)
#     print(result)
#     fileList = hms.query_gnb_data_file(33)
#     
#     xmlPath = fileList['rows'][-1]['path']
#     xmlFilename = fileList['rows'][-1]['filename']
#     print(xmlPath,xmlFilename)
#     fileSize = hms.download_xml_file_to_local(xmlPath, xmlFilename, 'F:\\eclipseworkspace\\autotestPro\\AutoTestMain\\xmlFile')
#     result = hms.upload_xml_from_local_to_hms('F:\\eclipseworkspace\\autotestPro\\AutoTestMain\\xmlFile', xmlFilename, fileSize)
#     print('upload res',result)
#     dataId = hms.query_xml_data_file_info('902272840007')
#     print('dataId=',dataId)
#     idsList = []
#     idsList.append(dataId)
#     result =  hms.delete_xml_file_by_ids(idsList)
#     print('del res:', result)