# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
'''
        基站版本下载
        参数：
    serialNumberList:基站序列号列表
    softVersion:版本号
''' 

from datetime import datetime
import logging
import os
import time

import allure

from BasicService.hms.versionService import VersionService
from BasicService.tversion.tversionService import TversionService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.HmsManager import key_login_hms


def key_download_version(hmsObj, serialNumberList=BASIC_DATA['gnb']['serialNumberList'], softVersion=BASIC_DATA['version']['upgradeVersion'], user='root', tryNum=5):
    with allure.step(key_get_time()+": 执行版本下载，下载版本："+ softVersion+'\n'):
        logging.info(key_get_time()+': exec download task, version: '+softVersion)
        gnbType = BASIC_DATA['common']['gnbType']
        if gnbType == 'BS5120':
            softVersion = softVersion+'.zip'
        for i in range (1, tryNum):
            resCode, resInfo = VersionService().download_gnb_version(hmsObj, serialNumberList, softVersion, user=user)
            if resInfo['enbUpgradeFailedInfoList'] != []:
                if resInfo['enbUpgradeFailedInfoList'][0]['faultCode'] == 'DEVICE_OFFLINE':
                    logging.info(key_get_time()+': download exec abnormal, abnormal info:'+str(resInfo))
                    key_wait(5)
                else:
                    break
            else:
                break
        if resCode == 200 and resInfo['result'] == 0:
            with allure.step(key_get_time()+": 下载操作执行成功\n"):
                logging.info(key_get_time()+': download exec success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 下载操作执行失败，失败信息："+str(resInfo)):
                logging.warning(key_get_time()+': download exec fail, fail info:'+str(resInfo))
                return 'fail'    
            
            
            
'''
        查询版本包下载任务状态
        参数：
    enbName:基站别名
    tryNum:尝试次数，默认10次，间隔30s
        返回：
    downloadTaskRes:下载任务执行状态
'''        
def key_query_download_status(hmsObj, enbName, tryNum=10):
    with allure.step(key_get_time()+": 查询下载任务状态\n"):
        logging.info(key_get_time()+': query status of download task!')
        for i in range (tryNum):
            downStatus = VersionService().query_download_status(hmsObj, enbName)
            if downStatus == 2 or downStatus == 3:
                break
            key_wait(30) #任务执行中，等待30S再次查询
        #下载任务执行状态2-success 3--fail 4--downloading
        if downStatus == 2:
            with allure.step(key_get_time()+": 下载任务执行成功\n"):
                logging.info(key_get_time()+': download task exec success!')
                return 'success'
        if downStatus == 3:
            with allure.step(key_get_time()+": 下载任务执行失败\n"):
                logging.info(key_get_time()+': download task exec fail!')
                return 'fail'
        if downStatus == 4:
            with allure.step(key_get_time()+": 下载任务执行中\n"):
                logging.info(key_get_time()+': download task is execing!')
                return 'downloading'

'''
        基站版本激活
         参数：
    serialNumberList:基站序列号列表
        返回：
    activeRes:版本激活操作结果
'''        
def key_active_version(hmsObj, serialNumberList=BASIC_DATA['gnb']['serialNumberList'], tryNum=20):
    with allure.step(key_get_time()+": 版本激活\n"):
        logging.info(key_get_time()+': exec active task!')
        for i in range (1, tryNum+1):
            resCode, resInfo = VersionService().active_gnb_version(hmsObj, serialNumberList)
            if resInfo['enbUpgradeFailedInfoList'] != []:
                if resInfo['enbUpgradeFailedInfoList'][0]['faultCode'] == 'DEVICE_OFFLINE':
                    logging.warning(key_get_time()+': active exec abnormal, abnormal info:'+str(resInfo))
                    key_wait(5)
                else:
                    break
            else:
                break
        if resCode == 200 and resInfo['result'] == 0:
            with allure.step(key_get_time()+": 激活操作执行成功\n"):
                logging.info(key_get_time()+': active exec success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 版本激活执行失败，请检查！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': active exec fail, fail info:'+str(resInfo))
                return 'fail'
'''
        查询版本包激活任务状态
        参数：
    enbName:基站别名
    tryNum:尝试次数，默认10次，间隔30s
'''        
def key_query_active_status(hmsObj, enbName, tryNum=30):
    with allure.step(key_get_time()+": 查询激活任务状态\n"):
        logging.info(key_get_time()+': query status of active task')
        for i in range (tryNum):
            activeStatus = VersionService().query_active_status(hmsObj, enbName)
            if activeStatus == 2 or activeStatus == 3:
                break
            key_wait(30) #任务执行中，等待30S再次查询
        if activeStatus == 2:
            with allure.step(key_get_time()+": 激活任务执行成功\n"):
                logging.info(key_get_time()+': active task exec success!')
                return 'success'
        if activeStatus == 3:
            with allure.step(key_get_time()+": 激活任务执行失败\n"):
                logging.info(key_get_time()+': active task exec fail!')
                return 'fail'
        if activeStatus == 4:
            with allure.step(key_get_time()+": 激活任务执行中\n"):
                logging.info(key_get_time()+': active task is execing!')
                return 'activing'

'''
        基站版本回退
        参数：
    serialNumberList:基站序列号列表
        返回
    rollbackRes:版本回退操作执行结果
'''
def key_rollback_version(hmsObj, serialNumberList=BASIC_DATA['gnb']['serialNumberList'], tryNum=20):
    with allure.step(key_get_time()+": 执行版本回退\n"):
        logging.info(key_get_time()+': exec rollabck task')
        serialNumberList = serialNumberList.split(',')
        for i in range (1, tryNum):
            resCode, resInfo = VersionService().rollback_gnb_version(hmsObj, serialNumberList)
            if resInfo['enbUpgradeFailedInfoList'] != []:
                if resInfo['enbUpgradeFailedInfoList'][0]['faultCode'] == 'DEVICE_OFFLINE':
                    logging.warning(key_get_time()+': rollback exec abnormal, abnormal info:'+str(resInfo))
                    key_wait(5)
                else:
                    break
            else:
                break
        if resCode == 200 and resInfo['result'] == 0:
            with allure.step(key_get_time()+": 下载操作执行成功\n"):
                logging.info(key_get_time()+': rollback exec success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 版本回退执行失败，请检查！异常信息:"+str(resInfo)):
                logging.warning(key_get_time()+': rollback exec fail, fail info:'+str(resInfo))
                return 'fail'

'''
        查询版本包回退任务状态
        参数：
    enbName:基站别名
    tryNum:尝试次数，默认10次，间隔30s
'''        
def key_query_rollback_status(hmsObj, enbName, tryNum=10):
    with allure.step(key_get_time()+": 查询回退任务状态\n"):
        logging.info(key_get_time()+': query status of rollabck task')
        for i in range (tryNum):
            rollbackStatus = VersionService().query_rollback_status(hmsObj, enbName)
            if rollbackStatus == 2 or rollbackStatus == 3:
                break
            key_wait(30) #任务执行中，等待30S再次查询
        if rollbackStatus == 2:
            with allure.step(key_get_time()+": 回退任务执行成功\n"):
                logging.info(key_get_time()+': rollabck task exec success!')
                return 'success'
        if rollbackStatus == 3:
            with allure.step(key_get_time()+": 回退任务执行失败\n"):
                logging.info(key_get_time()+': rollback task exec fail!')
                return 'fail'
        if rollbackStatus == 4:
            with allure.step(key_get_time()+": 回退任务执行中\n"):
                logging.info(key_get_time()+': rollback task is execing!')
                return 'rollbacking'

'''
        基站版本查询
        参数：
    serialNumberList:基站序列号列表
'''
def key_query_version_info(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 版本信息查询\n"):
        logging.info(key_get_time()+': query gnb version info')
        resCode, resInfo = VersionService().query_gnb_version_info(hmsObj, serialNumber)
        if resCode != 200:
            logging.info(key_get_time()+': query gnb version info fail, fail info:'+str(resInfo))
        assert resCode == 200,'版本查询执行失败，请检查！异常信息：'+str(resInfo)
        return resInfo      
    
    
'''
        同步基站版本信息
        参数：
    serialNumberList:基站序列号列表
'''
def key_query_version_info_from_device(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList'], tryNum=20):
    with allure.step(key_get_time()+": 同步获取基站版本信息\n"):
        logging.info(key_get_time()+': get gnb version info from device')
        for i in range (1, tryNum):
            resCode, resInfo = VersionService().query_gnb_version_info_from_device(hmsObj, serialNumber)
            if resInfo['result'] == '0':
                break
            else:
                logging.info(key_get_time()+': query gnb version info from device abnormal, abnormal info:'+str(resInfo))
                key_wait(5)
        if resCode != 200:
            logging.warning(key_get_time()+': query gnb version info from device fail, fail info:'+str(resInfo))
        assert resCode == 200 and resInfo['result'] == '0','版本查询执行失败，请检查！异常信息：'+str(resInfo)
        
        
'''
        基站回退版本信息查询
        参数：
    serialNumberList:基站序列号列表
'''
def key_query_backup_version_info(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 备用版本信息查询\n"):
        logging.info(key_get_time()+': query gnb backup version info')
        resCode, resInfo = VersionService().query_gnb_backup_version_info(hmsObj, serialNumber)
        if resCode != 200:
            logging.info(key_get_time()+': query gnb version info fail, fail info:'+str(resInfo))
        assert resCode == 200,'版本查询执行失败，请检查！异常信息：'+str(resInfo)
        backupVer = resInfo['rows'][0]['versionCtrlParameter']['systemBackupVersion']
        return backupVer
    
'''
        基站下载版本信息查询
        参数：
    serialNumberList:基站序列号列表
'''
def key_query_download_version_info(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 下载版本信息查询\n"):
        logging.info(key_get_time()+': query gnb download version info')
        resCode, resInfo = VersionService().query_gnb_download_version_info(hmsObj, serialNumber)
        if resCode != 200:
            logging.info(key_get_time()+': query gnb version info fail, fail info:'+str(resInfo))
        assert resCode == 200,'版本查询执行失败，请检查！异常信息：'+str(resInfo)
        downloadVer = resInfo['rows'][0]['softwareVersionCtrlParameter']['systemBackupVersion']
#         isDownload = resInfo['rows'][0]['mu']['systemBackupVersion']
        return downloadVer
    
'''
        基站版本包是否入库查询
        参数：
    softVersion:版本号
'''
def key_query_package_exist(hmsObj, softVersion=BASIC_DATA['version']['upgradeVersion']):
    with allure.step(key_get_time()+": 版本库中查询版本包是否存在\n"):
        logging.info(key_get_time()+': query package exist in version manager or not')
        isExist = VersionService().exist_in_version_management(hmsObj, softVersion)
        if isExist == False:
            logging.info(key_get_time()+': the package is not exist in version manager! need to download!')
        else:
            logging.info(key_get_time()+': the package has existed in version manager!')
        return isExist

'''
        上传本地版本包到hms
        参数：
    softVersion:版本号
'''
def key_upload_version_to_hms(hmsObj, fileSize, version=BASIC_DATA['version']['upgradeVersion']):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    localPath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    with allure.step(key_get_time()+": 上传版本包到版本库\n"):
        logging.info(key_get_time()+': upload package to HMS')
        resCode, resInfo = VersionService().upload_version_to_hms(hmsObj, fileSize, version, localPath)
        if resCode == 200 and resInfo['result'] == True:
            with allure.step(key_get_time()+": 版本包上传成功\n"):
                logging.info(key_get_time()+': upload package to HMS success! version:'+version)
        else:
            logging.warning(key_get_time()+': upload package to HMS fail, fail info:'+str(resInfo))
        assert resCode == 200 and resInfo['result'] == True,'版本上传执行失败，请检查！异常信息: '+str(resInfo)

'''
        从版本库下载版本到地址
        参数：
    softVersion:版本号
'''
def key_download_gkg_to_local(verNum=BASIC_DATA['version']['upgradeVersion']):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    savePath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    with allure.step(key_get_time()+": 下载版本包到本地\n"):
        logging.info(key_get_time()+': the version is not exist, download package to local path!')
        fileSize = TversionService().download_gkg_to_local(verNum, savePath)
        if fileSize > 1024:
            with allure.step(key_get_time()+": 版本包下载成功"):
                logging.info(key_get_time()+': version package download success!')
        else:
            with allure.step(key_get_time()+": 版本包下载失败"):
                logging.info(key_get_time()+': version package download failure!')
        assert fileSize > 1024,'下载版本包到本地目录执行失败，请检查！'
        return fileSize

'''
    检查版本包是否存在，不存在则从版本库下载版本并上传
    参数：
    softVersion:升级版本号
    savePath:版本包保存路径
'''
def key_upload_version_to_hms_if_version_no_exit(hmsObj, softVersion=BASIC_DATA['version']['upgradeVersion']):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    savePath = BASE_DIR+'\\AutoTestMain\\enbVersion'
    with allure.step(key_get_time()+": 检查版本包是否存在，不存在则从版本库下载并上传。\n"):
        logging.info(key_get_time()+': check version package is exist in HMS.')
    isExist = key_query_package_exist(hmsObj, softVersion)
    if isExist == False:
        with allure.step(key_get_time()+": 版本包不存在，从版本库下载并上传到网管。\n"):
            fileSize = key_download_gkg_to_local(softVersion)
            key_upload_version_to_hms(hmsObj, fileSize, softVersion)
    else:
        with allure.step(key_get_time()+": 版本包已经存在，不需要下载上传。\n"):
            logging.info(key_get_time()+': the version is exist, not need to download!')

'''
    从版本库中查询最新的版本信息
    参数：
    verBranch:版本分支名
    curVersionNum:当前版本号
'''         
def key_get_newest_version(curVersionNum, verBranch=BASIC_DATA['version']['verBranch']):
    with allure.step(key_get_time()+": 查询版本库中是否有最新版本发布\n"):
        logging.info(key_get_time()+': check if has newest version in TVersion')
        newestVer = TversionService().get_newest_version(verBranch, curVersionNum)
        if newestVer == '':
            with allure.step(key_get_time()+': 版本库中无最新版本发布。'):
                logging.info(key_get_time()+': there has not newest version in TVersion.')
        else:
            with allure.step(key_get_time()+': 最新版本号: '+newestVer):
                logging.info(key_get_time()+': the newest version: '+newestVer) 
        return newestVer 
    
     
'''
    配置文件上载
    参数：
    serialNumber:基站sn号
'''
def key_upload_xml_file_from_gnb_to_hms(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 配置文件上载。\n"):
        logging.info(key_get_time()+': upload xml file from gnb to hms.')
        dataDir = VersionService().query_gnb_info_xml(hmsObj, serialNumber)
        resInfo = VersionService().upload_xml_file_from_gnb_to_hms(hmsObj, dataDir)
        if resInfo['fail'] ==0:
            with allure.step(key_get_time()+': weblmt上传配置文件成功'):
                logging.info(key_get_time()+': upload xml file from gnb to hms success.')
        else:
            with allure.step(key_get_time()+': weblmt上传配置文件失败，原因：'+str(resInfo)):
                logging.warning(key_get_time()+': upload xml file from gnb to hms failure. reason:'+str(resInfo))
        assert resInfo['fail']==0,'配置数据上载失败，请检查！'
        key_wait(10)
    
'''
    下载xml文件到本地
    参数：
    enbId:基站enbId
    savePath:xml文件存在路径
'''    
def key_download_xml_file_to_local(hmsObj, enbId, tryNum=5):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time()+": 下载配置文件到本地。\n"):
        logging.info(key_get_time()+': download xml file to local.')
        for i in range (1, tryNum):
            fileList = VersionService().query_gnb_data_file(hmsObj, enbId)
            if fileList['total'] != 0:
                break
        xmlPath = fileList['rows'][0]['path']
        xmlFilename = fileList['rows'][0]['filename']
        fileSize = VersionService().download_xml_file_to_local(hmsObj, xmlPath, xmlFilename, filePath)
        if fileSize != 0:
            with allure.step(key_get_time()+': xml文件下载成功'):
                logging.info(key_get_time()+': download xml file success!')
            return fileSize, xmlFilename
        else:
            with allure.step(key_get_time()+': xml文件下载失败'):
                logging.warning(key_get_time()+': download xml file failure!')
        assert fileSize != 0, key_get_time()+': xml文件下载失败，请检查！'
    
'''
    上传xml文件到hms
    参数：
    enbId:基站enbId
    savePath:xml文件存在路径
'''     
def key_upload_xml_from_local_to_hms(hmsObj, filename, fileSize, isCheckData=BASIC_DATA['common']['isCheckData']):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time()+": 上传配置文件到网管,文件名："+filename):
        logging.info(key_get_time()+': upload xml file to hms, file name:'+filename)    
        uploadRes = VersionService().upload_xml_from_local_to_hms(hmsObj, filePath, filename, fileSize, isCheckData)
        if uploadRes['result'] == True:
            with allure.step(key_get_time()+": 配置文件上传成功"):
                logging.info(key_get_time()+': xml upload success')
        else:
            with allure.step(key_get_time()+": 配置文件上传失败"):
                logging.info(key_get_time()+': xml upload failure')
        return uploadRes['result']

'''
    删除hms上的最后一次同步的配置文件
    参数：
    serialNumber:基站sn号
'''      
def key_delete_last_xml_file_by_ids(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 删除网管上最后一次同步的配置文件。\n"):
        logging.info(key_get_time()+': delete the last xml file on hms.')       
        dataId = VersionService().query_xml_data_file_info(hmsObj, serialNumber)
        idsList = []
        idsList.append(dataId)
        delRes = VersionService().delete_xml_file_by_ids(hmsObj, idsList)
        if delRes == '0':
            logging.info(key_get_time()+': delete xml file success!') 
        else:
            logging.warning(key_get_time()+': delete xml file failure!') 
        assert delRes == '0', key_get_time()+':xml文件删除失败，请检查！'
    
'''
    删除hms上的同步失败的配置文件
    参数：
    serialNumber:基站sn号
'''      
def key_delete_fail_xml_file(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 删除网管上执行失败的配置文件。\n"):
        logging.info(key_get_time()+': delete fail upgrade xml file on hms.')       
        dataId = VersionService().query_fail_xml_data_file_info(hmsObj, serialNumber)
        if dataId == '':
            with allure.step(key_get_time()+": 网管上不存在同步失败的xml文件"):
                logging.info(key_get_time()+': no upgrad fail xml') 
        else:
            idsList = []
            idsList.append(dataId)
            delRes = VersionService().delete_xml_file_by_ids(hmsObj, idsList)
            if delRes == '0':
                with allure.step(key_get_time()+": xml文件删除成功"):
                    logging.info(key_get_time()+': delete xml file success!') 
            else:
                with allure.step(key_get_time()+": xml文件删除失败"):
                    logging.warning(key_get_time()+': delete xml file failure!') 
            assert delRes == '0', key_get_time()+':xml文件删除失败，请检查！'
            
'''
    查询hms上的同步失败的配置文件
    参数：
    serialNumber:基站sn号
'''      
def key_query_fail_xml_file(hmsObj, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 查询hms上的同步失败的配置文件。\n"):
        logging.info(key_get_time()+': query upgrade fail xml file on hms.')       
        dataId = VersionService().query_fail_xml_data_file_info(hmsObj, serialNumber)
        if dataId == '':
            with allure.step(key_get_time()+": 网管上不存在同步失败的xml文件"):
                logging.info(key_get_time()+': not exist upgrad fail xml') 
        else:
            with allure.step(key_get_time()+": 网管存在同步失败的xml文件"):
                logging.info(key_get_time()+': exist upgrad fail xml') 
        return dataId
'''
    同步xml文件到基站
    参数：
    serialNumber:基站sn号
    fileName:xml文件名
'''    
def key_download_xml_from_hms_to_gnb(hmsObj, fileName, serialNumber=BASIC_DATA['gnb']['serialNumberList'], tryNum = 3):
    with allure.step(key_get_time()+": 同步配置文件到基站。\n"):
        logging.info(key_get_time()+': syn xml file to gnb.')  
        for i in range (1, tryNum+1):
            dataId = VersionService().query_xml_data_file_info(hmsObj, serialNumber)     
            sysRes = VersionService().download_xml_from_hms_to_gnb(hmsObj, dataId, serialNumber, fileName)
            if sysRes == 0:
                break
        if sysRes == 0:
            with allure.step(key_get_time()+': 同步xml文件成功'):
                logging.info(key_get_time()+': synchronization xml file success!')
            return True 
        else:
            with allure.step(key_get_time()+': 同步xml文件失败'):
                logging.warning(key_get_time()+': synchronization xml file failure!') 
            return False
        
'''
    同步xml文件到基站
    参数：
    serialNumber:基站sn号
    fileName:xml文件名
'''    
def key_download_xml_from_hms_to_gnb_imediate(hmsObj, fileName, serialNumber=BASIC_DATA['gnb']['serialNumberList']):
    with allure.step(key_get_time()+": 同步配置文件到基站。\n"):
        logging.info(key_get_time()+': syn xml file to gnb.')  
        dataId = VersionService().query_xml_data_file_info(hmsObj, serialNumber)     
        sysRes = VersionService().download_xml_from_hms_to_gnb(hmsObj, dataId, serialNumber, fileName)
        with allure.step(key_get_time()+": 同步完成"):
            logging.info(key_get_time()+': synchronization complatly')
            
'''
    策略升级任务参数校验
    参数：
    
'''    
def key_check_polic_upgrade_cfg(hmsObj, policyCfgId, policyName, policyStatus, downloadFlag, softVersion, triggerMode, times, triggerType, startTime, endTime, activateType, timerActivateTime):
    with allure.step(key_get_time()+": 校验策略升级任务参数"):
        logging.info(key_get_time()+': check cfg of policy upgrade task')  
        cfgDict = {
            "policyCfgId":policyCfgId, #时间戳
            "policyName":policyName, #策略名
            "policyStatus":policyStatus, # 0-suspend  1-active
            "downloadFlag":downloadFlag,# 0-no download 1-download
            "softVersion":softVersion, #版本号
            "triggerMode":triggerMode,# 0-time 1-event
            "times":times,# download time
            "triggerType":triggerType,#下载触发类型 
            "startTime":startTime, #触发起时间
            "endTime":endTime, #触发终时间
            "activateType":activateType,# 激活类型  0-不激活  1-下载后激活   2--时间激活
            "timerActivateTime":timerActivateTime,#激活时间
            }
        checkRes = VersionService().check_policy_upgrade_cfg(hmsObj, cfgDict)
        if checkRes['success'] == True:
            with allure.step(key_get_time()+": 策略任务参数校验成功"):
                logging.info(key_get_time()+': cfg check success')
        else:
            with allure.step(key_get_time()+": 策略任务参数校验失败，信息："+str(checkRes)):
                logging.info(key_get_time()+': cfg check failure, info:'+str(checkRes))
        assert checkRes['success'] == True, '策略任务参数校验失败, 请检查！'
        
'''
    创建策略升级任务
    参数：
    
'''    
def key_create_polic_upgrade_task(hmsObj, policyName=BASIC_DATA['polSoft']['policyName'], policyStatus=BASIC_DATA['polSoft']['policyStatus'], downloadFlag=BASIC_DATA['polSoft']['downloadFlag'], softVersion=BASIC_DATA['polSoft']['activeVersion'], triggerMode=BASIC_DATA['polSoft']['triggerMode'], times=BASIC_DATA['polSoft']['times'], triggerType=BASIC_DATA['polSoft']['triggerType'], startTime=BASIC_DATA['polSoft']['startTime'], endTime=BASIC_DATA['polSoft']['endTime'], activateType=BASIC_DATA['polSoft']['activateType'], timerActivateTime=BASIC_DATA['polSoft']['timerActivateTime'], gnbSerList=BASIC_DATA['polSoft']['gnbSerList']):
    with allure.step(key_get_time()+": 创建策略升级任务参数"):
        logging.info(key_get_time()+': create cfg of policy upgrade task')  
        nowtime = time.time()
        policyCfgId = str(nowtime)[:-4].replace('.','')
        if policyName == '':
            policyName = 'auto_'+policyCfgId
        if triggerMode == '0':
            if times == '':
                nowtime = datetime.now()
                nowtime.strftime('%Y-%m-%d %H:%M')
                timeStr = str(nowtime).split(':')
                if int(timeStr[1]) < 10:
                    min = '10'
                elif int(timeStr[1])>=10 and int(timeStr[1]) < 20:
                    min = '20'
                elif int(timeStr[1])>=20 and int(timeStr[1]) < 30:
                    min = '30'
                elif int(timeStr[1])>=30 and int(timeStr[1]) < 40:
                    min = '40'
                elif int(timeStr[1])>=40 and int(timeStr[1]) < 50:
                    min = '50'
                elif int(timeStr[1])>=50 and int(timeStr[1]) < 60:
                    min = '00'
                times = timeStr[0]+':'+min
            assert times != '', '策略任务下载触发模式是时间触发，需要配置触发时间！'
        elif triggerMode == '1':
            assert triggerType != '', '策略任务下载触发模式是事件触发，需要配置触发事件！'        
            assert startTime != '', '策略任务下载触发模式是事件触发，需要配置触发事件的开始时间！'   
            assert endTime != '', '策略任务下载触发模式是事件触发，需要配置触发事件的结束时间！'   
        if activateType == '2':
            assert timerActivateTime != '', '策略任务版本激活触发模式是时间触发，需要配置激活时间！'   
        cfgDict = {
            "policyCfgId":policyCfgId, #时间戳
            "policyName":policyName, #策略名
            "policyStatus":policyStatus, # 0-suspend  1-active
            "downloadFlag":downloadFlag,# 0-no download 1-download
            "softVersion":softVersion, #版本号
            "triggerMode":triggerMode,# 0-time 1-event
            "times":times,# download time
            "triggerType":triggerType,#下载触发类型 
            "startTime":startTime, #触发起时间
            "endTime":endTime, #触发终时间
            "activateType":activateType,# 激活类型  0-不激活  1-下载后激活   2--时间激活
            "timerActivateTime":timerActivateTime,#激活时间
            }
        gnbList = []
        for gnbSer in gnbSerList:
            gnbList.append({'serialNumber':gnbSer, 'triggerMode':triggerMode})
        #检查策略任务参数是否正常
        key_check_polic_upgrade_cfg(hmsObj, policyCfgId, policyName, policyStatus, downloadFlag, softVersion, triggerMode, times, triggerType, startTime, endTime, activateType, timerActivateTime)
        #执行任务创建
        addRes = VersionService().create_policy_upgrade_task(hmsObj, cfgDict, gnbList)
        if addRes['result'] == True:
            with allure.step(key_get_time()+": 策略任务创建成功"):
                logging.info(key_get_time()+': policy upgrade task create success')
        else:
            with allure.step(key_get_time()+": 策略任务创建失败，信息："+str(addRes)):
                logging.info(key_get_time()+': policy upgrade task create failure, info:'+str(addRes))
        assert addRes['result'] == True, '策略任务创建失败, 请检查！'
        return policyName
'''
    查询策略升级任务信息
    参数：
    
'''    
def key_query_polic_upgrade_task_info(hmsObj):
    with allure.step(key_get_time()+": 查询策略升级任务信息"):
        logging.info(key_get_time()+': query policy upgrade task info')  
        queryResList = VersionService().query_policy_upgrade_task_info(hmsObj)
        return queryResList
    
'''
    删除策略升级任务
    参数：
    taskName：任务名
'''    
def key_del_polic_upgrade_task(hmsObj, taskName):
    with allure.step(key_get_time()+": 删除策略任务, 任务名："+taskName):
        logging.info(key_get_time()+': delete policy upgrade task, taskName:'+taskName)  
        delRes = VersionService().delete_policy_upgrade_task(hmsObj, taskName)
        if delRes['result']==True:
            with allure.step(key_get_time()+": 策略任务删除成功"):
                logging.info(key_get_time()+': policy upgrade task delete success')
        else:
            with allure.step(key_get_time()+": 策略任务删除失败，信息："+str(delRes)):
                logging.info(key_get_time()+': policy upgrade task delete failure, info:'+str(delRes))
        assert delRes['result']==True, '策略任务删除失败，请检查！'
    
'''
    激活策略升级任务
    参数：
    taskName：任务名
'''    
def key_active_polic_upgrade_task(hmsObj, taskName):
    with allure.step(key_get_time()+": 激活策略任务, 任务名："+taskName):
        logging.info(key_get_time()+': active policy upgrade task, taskName:'+taskName)  
        activeRes = VersionService().active_policy_upgrade_task(hmsObj, taskName)
        if activeRes['result']==True:
            with allure.step(key_get_time()+": 策略任务激活成功"):
                logging.info(key_get_time()+': policy upgrade task active success')
        else:
            with allure.step(key_get_time()+": 策略任务激活失败，信息："+str(activeRes)):
                logging.info(key_get_time()+': policy upgrade task active failure, info:'+str(activeRes))
        assert activeRes['result']==True, '策略任务激活失败，请检查！'
            
if __name__ == '__main__':
    hmsObj = key_login_hms()
    key_query_fail_xml_file(hmsObj)
            
