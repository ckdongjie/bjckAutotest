'''
Created on 2023年6月14日
@author: dj
'''


from datetime import datetime
import logging
import os
import allure
from BasicService.hms.logManagerService import LogManagerService
from UserKeywords.basic.basic import key_get_time
from UserKeywords.hms.HmsManager import key_login_hms

'''
        设置log level
    "levelConfig":"ERROR",
    "levelAlarm":"ERROR",
    "levelPm":"ERROR",
    "levelNm":"ERROR",
    "levelUsmc":"ERROR",
    "levelSm":"WARN",
    "levelTr069":"ERROR"
'''
def key_set_log_level(hmsObj, logLevelDict):
    with allure.step(key_get_time()+":修改log level配置参数，参数："+str(logLevelDict)):
        logging.info(key_get_time()+': modify log level, params:'+str(logLevelDict))
        updateRes = LogManagerService().update_log_level_info(hmsObj, logLevelDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":log level参数修改成功\n"):
                logging.info(key_get_time()+': log level modify success!')
        else:
            with allure.step(key_get_time()+":log level修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': log level modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','log level参数修改失败，请检查！'

'''
        读取log level配置
'''
def key_get_log_level_info(hmsObj):
    with allure.step(key_get_time()+":查询log等级配置"):
        logging.info(key_get_time()+': query log level info')
        logLevelInfo = LogManagerService().realtime_query_log_level_info(hmsObj)
        with allure.step(key_get_time()+":log level信息："+str(logLevelInfo)):
            logging.info(key_get_time()+': log level info:'+str(logLevelInfo))
        return logLevelInfo
    
'''
        查询一键式log任务状态
'''
def key_query_one_click_task_info(hmsObj, taskName):
    with allure.step(key_get_time()+":查询一键式采集log信息"):
        logging.info(key_get_time()+': query one click task info')
        taskInfoList = LogManagerService().query_one_click_log_task_info(hmsObj)
        for taskInfo in taskInfoList:
            if taskInfo['taskName']==taskName:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]的查询结果："+str(taskInfo)):
                    logging.info(key_get_time()+': one click task['+taskName+'] info:'+str(taskInfo))
                return taskInfo
            
'''
        查询一键式log任务是否存在
'''
def key_query_one_click_taskname_exist(hmsObj, taskName):
    with allure.step(key_get_time()+":检查一键式log采集任务名是否存在"):
        logging.info(key_get_time()+': check if one click taskname exist in list')
        isExist = LogManagerService().check_one_click_log_taskname_exist(hmsObj, taskName)
        if isExist == False:
            with allure.step(key_get_time()+":一键式采集任务["+taskName+"]不存在，可以创建"):
                logging.info(key_get_time()+': not exist one click task['+taskName+']')
        else:
            with allure.step(key_get_time()+":一键式采集任务["+taskName+"]存在，不可以创建"):
                logging.warning(key_get_time()+': exist one click task['+taskName+']')
        return isExist
    
'''
        创建一键式log任务信息
'''
def key_creat_one_click_taskname(hmsObj, oneClickName, sn, taskDesc='', taskStatus='1'):
    with allure.step(key_get_time()+":创建一键式log采集任务"):
        logging.info(key_get_time()+': create one click task')
        addRes = LogManagerService().add_one_click_log_task(hmsObj, oneClickName, sn, taskDesc, taskStatus)
        if addRes == True:
            with allure.step(key_get_time()+":一键式采集任务["+oneClickName+"]创建成功"):
                logging.info(key_get_time()+': one click task['+oneClickName+'] create success')
        else:
            with allure.step(key_get_time()+":一键式采集任务["+oneClickName+"]创建失败"):
                logging.warning(key_get_time()+': one click task['+oneClickName+'] create failure')
                
'''
        删除一键式log任务信息
'''
def key_delete_one_click_taskname(hmsObj, taskName):
    with allure.step(key_get_time()+":删除一键式log采集任务:"+taskName):
        logging.info(key_get_time()+': delete one click task:'+taskName)
        taskInfo = key_query_one_click_task_info(hmsObj, taskName)
        taskId = taskInfo['taskId']
        delRes = LogManagerService().del_one_click_log_task(hmsObj, taskId)
        if delRes == True:
            with allure.step(key_get_time()+":一键式采集任务["+taskName+"]删除成功"):
                logging.info(key_get_time()+': one click task['+taskName+'] delete success')
        else:
            with allure.step(key_get_time()+":一键式采集任务["+taskName+"]删除失败"):
                logging.warning(key_get_time()+': one click task['+taskName+'] delete failure')
                
'''
        修改一键式log任务信息
'''
def key_update_one_click_taskname(hmsObj, taskName, updateParaDict):
    taskInfo = key_query_one_click_task_info(hmsObj, taskName)
    if taskInfo['taskStatus'] != 2:
        with allure.step(key_get_time()+":一键式log采集任务["+taskName+"]不允许修改！"):
            logging.info(key_get_time()+': one click task['+taskName+'] not allow update!')
    else:
        with allure.step(key_get_time()+":修改一键式log采集任务:"+taskName):
            logging.info(key_get_time()+': update one click task:'+taskName)
            taskInfo.update(updateParaDict)
            updateRes= LogManagerService().update_one_click_log_task(hmsObj, taskInfo)
            print(updateRes)
            if updateRes == True:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]修改成功"):
                    logging.info(key_get_time()+': one click task['+taskName+'] update success')
            else:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]修改失败"):
                    logging.warning(key_get_time()+': one click task['+taskName+'] update failure')
                    
'''
        激活一键式log任务信息
'''
def key_active_one_click_taskname(hmsObj, taskName, updateParaDict):
    taskInfo = key_query_one_click_task_info(hmsObj, taskName)
    if taskInfo['taskStatus'] != 2:
        with allure.step(key_get_time()+":一键式log采集任务["+taskName+"]不允许激活！"):
            logging.info(key_get_time()+': one click task['+taskName+'] not allow active!')
    else:
        with allure.step(key_get_time()+":激活一键式log采集任务:"+taskName):
            logging.info(key_get_time()+': active one click task:'+taskName)
            updateRes= LogManagerService().update_one_click_log_task_status(hmsObj, taskInfo['taskId'], 1)
            print(updateRes)
            if updateRes == True:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]激活成功"):
                    logging.info(key_get_time()+': one click task['+taskName+'] active success')
            else:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]修改失败"):
                    logging.warning(key_get_time()+': one click task['+taskName+'] update failure')

'''
        挂起一键式log任务信息
    status:2--挂起   3--执行中  1--激活  4--完成   5--失败
'''
def key_suspend_one_click_taskname(hmsObj, taskName):
    taskInfo = key_query_one_click_task_info(hmsObj, taskName)
    if taskInfo['taskStatus'] != 1:
        with allure.step(key_get_time()+":一键式log采集任务["+taskName+"]不允许挂起！"):
            logging.info(key_get_time()+': one click task['+taskName+'] not allow suspend!')
    else:
        with allure.step(key_get_time()+":挂起一键式log采集任务:"+taskName):
            logging.info(key_get_time()+': suspend one click task:'+taskName)
            updateRes= LogManagerService().update_one_click_log_task_status(hmsObj, taskInfo['taskId'], 2)
            print(updateRes)
            if updateRes == True:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]挂起成功"):
                    logging.info(key_get_time()+': one click task['+taskName+'] suspend success')
            else:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]挂起失败"):
                    logging.warning(key_get_time()+': one click task['+taskName+'] suspend failure')
                    
'''
        下载一键式log任务信息
'''
def key_download_one_click_log(hmsObj, taskName):
    taskInfo = key_query_one_click_task_info(hmsObj, taskName)
    if taskInfo['taskStatus'] != 4:
        with allure.step(key_get_time()+":一键式log采集任务["+taskName+"]未执行成功，不允许下载！"):
            logging.info(key_get_time()+': one click task['+taskName+'] not allow download!')
    else:
        with allure.step(key_get_time()+":下载一键式log,采集任务:"+taskName):
            logging.info(key_get_time()+': download one click log, task:'+taskName)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            logPath = BASE_DIR+'\\AutoTestMain\\hmsLog\\OneClickLog'
            if not os.path.exists(logPath):
                os.makedirs(logPath)
            nowtime = datetime.now()
            filename = 'LogData_'+nowtime.strftime('%Y%m%d%H%M%S')
            fileSize= LogManagerService().download_one_click_log(hmsObj, taskInfo['taskId'], logPath, filename)
            print(fileSize)
            if fileSize != 0:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]下载成功"):
                    logging.info(key_get_time()+': one click task['+taskName+'] download success')
            else:
                with allure.step(key_get_time()+":一键式采集任务["+taskName+"]下载失败"):
                    logging.warning(key_get_time()+': one click task['+taskName+'] download failure')
                    
'''
        下载运行log
'''
def key_download_running_log(hmsObj, logName):
    with allure.step(key_get_time()+":下载运行log,log名:"+logName):
        logging.info(key_get_time()+': download running log, name:'+logName)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logPath = BASE_DIR+'\\AutoTestMain\\hmsLog\\RunLog'
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        fileSize= LogManagerService().download_running_log(hmsObj, logPath, logName)
        if fileSize != 0:
            with allure.step(key_get_time()+":运行log ["+logName+"]下载成功"):
                logging.info(key_get_time()+': running log ['+logName+'] download success')
        else:
            with allure.step(key_get_time()+":运行log ["+logName+"]下载失败"):
                logging.warning(key_get_time()+': running log ['+logName+'] download failure')
                
'''
        下载运行log
'''
def key_download_operate_log(hmsObj, operator='', operateResult='', operateName='', operateContent='', exportType='CSV'):
    fileType = {'CSV':'1','EXCEL':'2','TXT':'3'}
    with allure.step(key_get_time()+":下载操作log"):
        logging.info(key_get_time()+': download operate log')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logPath = BASE_DIR+'\\AutoTestMain\\hmsLog\\OperateLog'
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        nowtime = datetime.now()
        logName = 'OperateLog_'+nowtime.strftime('%Y%m%d%H%M%S') 
        fileSize= LogManagerService().download_operate_log(hmsObj, logPath, logName,operator, operateResult, operateName, operateContent, fileType[exportType])
        print(fileSize)
        if fileSize != 0:
            with allure.step(key_get_time()+":运行log ["+logName+"]下载成功"):
                logging.info(key_get_time()+': running log ['+logName+'] download success')
        else:
            with allure.step(key_get_time()+":运行log ["+logName+"]下载失败"):
                logging.warning(key_get_time()+': running log ['+logName+'] download failure')
                
'''
        下载安全log
'''
def key_download_security_log(hmsObj, operator='', operateResult='', operateName='', operateContent='', exportType='CSV'):
    fileType = {'CSV':'1','EXCEL':'2','TXT':'3'}
    with allure.step(key_get_time()+":下载安全log"):
        logging.info(key_get_time()+': download security log')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logPath = BASE_DIR+'\\AutoTestMain\\hmsLog\\SecurityLog'
        if not os.path.exists(logPath):
            os.makedirs(logPath)
        nowtime = datetime.now()
        logName = 'SecLog_'+nowtime.strftime('%Y%m%d%H%M%S') 
        fileSize= LogManagerService().download_operate_log(hmsObj, logPath, logName,operator, operateResult, operateName, operateContent, fileType[exportType])
        print(fileSize)
        if fileSize != 0:
            with allure.step(key_get_time()+":安全log ["+logName+"]下载成功"):
                logging.info(key_get_time()+': security log ['+logName+'] download success')
        else:
            with allure.step(key_get_time()+":安全log ["+logName+"]下载失败"):
                logging.warning(key_get_time()+': security log ['+logName+'] download failure')
    
if __name__ == '__main__':
    hmsObj = key_login_hms()
#     key_creat_one_click_taskname(hmsObj, 'auto_0614', '902222640001')
    key_download_security_log(hmsObj)
    

