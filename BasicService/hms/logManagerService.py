# coding = 'utf-8'
'''
Created on 2023年6月14日
@author: dj
'''

from BasicModel.hms.logManagerModel import LogManagerModel

class LogManagerService():
    '''
                说明：查询log level信息
                参数：
        hmsObj:hms对象
    '''    
    def realtime_query_log_level_info(self, hmsObj): 
        realQueryRes = LogManagerModel(hmsObj).find_log_level_info()
        return realQueryRes
    
    '''
                说明：设置log level信息
                参数：
        hmsObj:hms对象
        paraDict:类型及等级键值对
    '''    
    def update_log_level_info(self, hmsObj, paraDict):
        updateRes = LogManagerModel(hmsObj).set_log_level(paraDict)
        return updateRes
    
    '''
                说明：新增一键式采集log任务
                参数：
        hmsObj:hms对象
        paraDict:类型及等级键值对
    '''    
    def add_one_click_log_task(self, hmsObj, oneClickName, sn, taskDesc='', taskStatus='1'):
        addRes = LogManagerModel(hmsObj).insert_one_click_task(oneClickName, sn, taskDesc, taskStatus)
        return addRes
    
    '''
                说明：检查一键式采集log任务名是否存在
                参数：
        hmsObj:hms对象
        oneClickName:任务名
    '''    
    def check_one_click_log_taskname_exist(self, hmsObj, oneClickName):
        isExist = LogManagerModel(hmsObj).check_one_click_taskname_exist(oneClickName)
        return isExist
    
    '''
                说明：查询一键式采集log任务信息
                参数：
        hmsObj:hms对象
    '''    
    def query_one_click_log_task_info(self, hmsObj):
        queryInfo = LogManagerModel(hmsObj).query_one_click_task()
        return queryInfo['rows']
    
    '''
                说明：删除一键式采集log任务
                参数：
        hmsObj:hms对象
    '''    
    def del_one_click_log_task(self, hmsObj, taskId):
        delRes = LogManagerModel(hmsObj).delete_one_click_task(taskId)
        return delRes
    
    '''
                说明：删除一键式采集log任务
                参数：
        hmsObj:hms对象
    '''    
    def update_one_click_log_task(self, hmsObj, paraDict):
        updateRes = LogManagerModel(hmsObj).update_one_click_task(paraDict)
        return updateRes
    
    '''
                说明：删除一键式采集log任务
                参数：
        hmsObj:hms对象
    '''    
    def update_one_click_log_task_status(self, hmsObj, taskId, status):
        updateRes = LogManagerModel(hmsObj).update_one_click_task_status(taskId, status)
        return updateRes
    
    '''
                说明：下载一键式采集log
                参数：
        hmsObj:hms对象
    '''    
    def download_one_click_log(self, hmsObj, taskId, filepath, filename):
        print(taskId, filepath, filename)
        fileSize = LogManagerModel(hmsObj).download_one_click_log(taskId, filepath, filename)
        return fileSize
    
    '''
                说明：下载运行log
                参数：
        hmsObj:hms对象
    '''    
    def download_running_log(self, hmsObj, filepath, logname):
        print(filepath, logname)
        fileSize = LogManagerModel(hmsObj).download_running_log(filepath, logname)
        return fileSize
    
    '''
                说明：下载操作log
                参数：
        hmsObj:hms对象
    '''    
    def download_operate_log(self, hmsObj, filepath, logname, operator='', operateResult='', operateName='', operateContent='', exportType='1'):
        print(filepath, logname)
        fileSize = LogManagerModel(hmsObj).download_operate_log(filepath, logname, operator, operateResult, operateName, operateContent, exportType)
        return fileSize
    
    '''
                说明：下载安全log
                参数：
        hmsObj:hms对象
    '''    
    def download_security_log(self, hmsObj, filepath, logname, operator='', operateResult='', operateName='', operateContent='', exportType='1'):
        print(filepath, logname)
        fileSize = LogManagerModel(hmsObj).download_security_log(filepath, logname, operator, operateResult, operateName, operateContent, exportType)
        return fileSize
    