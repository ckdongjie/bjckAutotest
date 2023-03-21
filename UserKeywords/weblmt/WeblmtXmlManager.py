# coding = 'utf-8'
'''
Created on 2022年11月11日

@author: dj
'''


import logging

import allure

from BasicService.weblmt.lmtXmlService import LmtXmlService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
            说明：下载xml文件到本地目录
            参数：
    xmlFilename:xml文件名,默认是BntCfgFile
    savePath:保存xml文件的本地路径
'''   
def key_export_xml_file(weblmt, savePath=BASIC_DATA['version']['xmlSavePath'], xmlFilename='BntCfgFile'):
    with allure.step(key_get_time() +": 从weblmt上导出配置数据。\n"):
        logging.info(key_get_time()+': export xml file from weblmt.')
        exportRes = LmtXmlService().export_xml_file_to_local(weblmt, savePath, xmlFilename)
        if exportRes == 'success':
            with allure.step(key_get_time()+':数据导出成功！'):
                logging.info(key_get_time()+': export xml file success!')
        else:
            with allure.step(key_get_time()+':数据导出失败！'):
                logging.warning(key_get_time()+': export xml file fail!')
        return exportRes
'''
            说明：上传xml文件到weblmt
            参数：
    filename:xml文件名,默认是BntCfgFile
    localPath:保存xml文件的本地路径
'''         
def key_upload_xml_to_weblmt(weblmt, localPath=BASIC_DATA['version']['xmlSavePath'], filename='BntCfgFile'):
    with allure.step(key_get_time() +": 上传配置文件到weblmt。\n"):
        logging.info(key_get_time()+': upload xml file to weblmt.')
        uploadRes = LmtXmlService().upload_xml_file_to_lmt(weblmt, localPath, filename)
        if uploadRes == 'yes':
            with allure.step(key_get_time()+':数据上传成功！'):
                logging.info(key_get_time()+': upload xml file success!')
        else:
            with allure.step(key_get_time()+':数据上传失败！'):
                logging.warning(key_get_time()+': upload xml file fail!')
        return uploadRes

'''
            说明：导入xml文件到基站
            参数：
    fileName:xml文件名,默认是BntCfgFile
    staType:xml文件针对的基站类型
'''         
def key_import_xml_to_gnb(weblmt, fileName='BntCfgFile', staType='BS5514'):
    with allure.step(key_get_time() +": 导入配置数据到基站。\n"):
        logging.info(key_get_time()+': import xml file to gnb.')
        importRes = LmtXmlService().import_xml_file_to_gnb(weblmt, fileName, staType)
        if importRes == 'success':
            with allure.step(key_get_time()+':数据导入成功！'):
                logging.info(key_get_time()+': import xml file success!')
        else:
            with allure.step(key_get_time()+':数据导入失败！'):
                logging.warning(key_get_time()+': import xml file fail!')
        return importRes