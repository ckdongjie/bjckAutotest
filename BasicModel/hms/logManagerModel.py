'''
Created on 2023年6月14日
@author: dj
'''
import os

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.logManagerData import LOG_URL_DICT


class LogManagerModel(HMS):
    
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
    def find_log_level_info(self):
        header = LOG_URL_DICT['findLogLevel']['header']
        url = self.baseUrl+LOG_URL_DICT['findLogLevel']['action']
        body = LOG_URL_DICT['findLogLevel']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo
        
    def set_log_level(self, paraDict):
        logLevelInfo = self.find_log_level_info()
        header = LOG_URL_DICT['updateLogLevel']['header']
        url = self.baseUrl+LOG_URL_DICT['updateLogLevel']['action']
        logLevelInfo.update(paraDict)
        print(url, logLevelInfo)
        response = self.post_request(url, json=logLevelInfo, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# '0'--success '1'--fail{"result":"0"}
        
    def check_one_click_taskname_exist(self, oneClickName):
        header = LOG_URL_DICT['isOneClickLogExportTaskNameExist']['header']
        url = self.baseUrl+LOG_URL_DICT['isOneClickLogExportTaskNameExist']['action']
        body = LOG_URL_DICT['isOneClickLogExportTaskNameExist']['body']
        body.update({'taskName':oneClickName})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo['result']# {"result":false}--不存在
        
    def insert_one_click_task(self, oneClickName, sn, taskDesc='', taskStatus='1'):
        header = LOG_URL_DICT['insertOneClickLogExportTask']['header']
        url = self.baseUrl+LOG_URL_DICT['insertOneClickLogExportTask']['action']
        body = LOG_URL_DICT['insertOneClickLogExportTask']['body']
        body.update({'taskName':oneClickName, 'task2EnbInfos':[{'serialNumber':sn}], 'taskDesc':taskDesc, taskStatus:taskStatus})
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json() 
        return resInfo
    
    def query_one_click_task(self):
        header = LOG_URL_DICT['findPageOneClickLogExportTask']['header']
        url = self.baseUrl+LOG_URL_DICT['findPageOneClickLogExportTask']['action']
        body = LOG_URL_DICT['findPageOneClickLogExportTask']['body']
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json() 
        return resInfo
    
    def delete_one_click_task(self, taskId):
        header = LOG_URL_DICT['batchDeleteOneClickLogExportTask']['header']
        url = self.baseUrl+LOG_URL_DICT['batchDeleteOneClickLogExportTask']['action']
        body = LOG_URL_DICT['batchDeleteOneClickLogExportTask']['body']
        body.update({'deletedTaskIdList':[taskId]})
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json() 
        return resInfo
    
    def update_one_click_task(self, paraDict):
        header = LOG_URL_DICT['updateOneClickLogExportTask']['header']
        url = self.baseUrl+LOG_URL_DICT['updateOneClickLogExportTask']['action']
        body = LOG_URL_DICT['updateOneClickLogExportTask']['body']
        body.update(paraDict)
        print(url,body)
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json() 
        return resInfo
    
    def update_one_click_task_status(self, taskId, status):
        header = LOG_URL_DICT['batchUpdateOneClickLogExportTaskStatus']['header']
        url = self.baseUrl+LOG_URL_DICT['batchUpdateOneClickLogExportTaskStatus']['action']
        body = LOG_URL_DICT['batchUpdateOneClickLogExportTaskStatus']['body']
        body.update({"taskStatus":status,"taskIdList":[taskId]})
        print(url,body)
        response = self.post_request(url, json=body, headers = header)
        resInfo = response.json() 
        return resInfo
    
    def download_one_click_log(self, taskId, filepath, filename):
        url = self.baseUrl+LOG_URL_DICT['oneClickLogExport']['action']+taskId+'/'+filename+'307.zip'
        header = LOG_URL_DICT['oneClickLogExport']['header']
        print(url)
        response = self.get_request(url, headers = header)
#         response = self.get_request(url)
        filePath = filepath +'/'+ filename+'.zip'
        print(response.content)
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
    def download_running_log(self, filepath, filename):
        url = self.baseUrl+LOG_URL_DICT['downRunLog']['action']+filename+'&ss=0.7995795692562799'
        header = LOG_URL_DICT['oneClickLogExport']['header']
        response = self.get_request(url, headers = header)
        filePath = filepath +'/'+ filename
        print(response.content)
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
    def download_operate_log(self, filepath, filename, operator='', operateResult='', operateName='', operateContent='', exportType='1'):
        url = self.baseUrl+LOG_URL_DICT['downOperateLog']['action']+'operator='+operator+'&operateResult='+operateResult+'&operateName='+operateName+'&operateContent='+operateContent+'&exportType='+exportType
        header = LOG_URL_DICT['oneClickLogExport']['header']
        response = self.get_request(url, headers = header)
        filePath = filepath +'/'+ filename+'.zip'
        print(response.content)
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    
    def download_security_log(self, filepath, filename, operator='', operateResult='', operateName='', operateContent='', exportType='1'):
        url = self.baseUrl+LOG_URL_DICT['downSecurityLog']['action']+'operator='+operator+'&operateResult='+operateResult+'&operateName='+operateName+'&operateContent='+operateContent+'&exportType='+exportType
        header = LOG_URL_DICT['downSecurityLog']['header']
        response = self.get_request(url, headers = header)
        filePath = filepath +'/'+ filename+'.zip'
        print(response.content)
        with open(filePath, 'wb') as vFile:
            vFile.write(response.content)
        fileSize = os.path.getsize(filePath)
        return fileSize
    