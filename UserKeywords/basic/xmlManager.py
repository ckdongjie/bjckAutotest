# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj

'''
import logging
import os
import allure

from BasicService.basic.xmlService import xmlService
from UserKeywords.basic.basic import key_get_time

'''
            说明：修改xml文件中记录节点值
            参数：
    filePath:xml文件路径
    xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
    modifyContext:修改的目标值
'''
def key_modify_xml_record_value(xmlTreePath, modifyContext, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time() +": 修改xml文件的记录值，修改值："+str(modifyContext)):
        logging.info(key_get_time()+': modify xml file record value, valure:'+str(modifyContext))
        xmlService().modify_xml_record_value(filename, filePath, xmlTreePath, modifyContext)
    
'''
            说明：修改xml文件中根节点属性值
            参数：
    filePath:xml文件路径
    valueDir:修改属性的字典值，例：{'sn':'902272840008'}
'''
def key_modify_xml_root_value(valueDict, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time() +": 修改xml文件的根节点属性值，修改值："+str(valueDict)):
        logging.info(key_get_time()+': modify xml file root note value, value:'+str(valueDict))
        xmlService().modify_xml_root_value(filePath+'\\'+filename, valueDict)

'''
        重命名xml文件
'''
def key_rename_xml_file(newfilename, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    with allure.step(key_get_time() +": 修改xml文件名"):
        logging.info(key_get_time()+': modify xml file name')
        xmlService().rename_xml_filename(filePath+'\\'+newfilename, filePath+'\\'+filename)
'''
            说明：读取xml文件中记录节点值
            参数：
    filePath:xml文件路径
    xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
'''    
def key_read_xml_record_value(xmlTreePath, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    return xmlService().read_xml_record_value(filename, filePath, xmlTreePath)
 
'''
            说明：读取xml文件中根节点属性值
            参数：
    filePath:xml文件路径
    noteName:属性名称
'''  
def key_read_xml_root_value(noteName, filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #d:/bjckAutotest
    filePath = BASE_DIR+'\\AutoTestMain\\xmlFile'
    return xmlService().read_xml_root_value(filePath+'\\'+filename, noteName)   