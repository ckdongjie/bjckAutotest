# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj

'''

import logging

import allure

from BasicService.basic.xmlService import xmlService
from UserKeywords.basic.basic import key_get_time
from TestCaseData.basicConfig import BASIC_DATA
'''
            说明：修改xml文件中记录节点值
            参数：
    filePath:xml文件路径
    xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
    modifyContext:修改的目标值
'''
def key_modify_xml_record_value(xmlTreePath, modifyContext, filePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time() +": 修改xml文件的记录值\n"):
        logging.info(key_get_time()+': modify xml file record value.')
        xmlService().modify_xml_record_value(filePath, xmlTreePath, modifyContext)
        
'''
            说明：修改xml文件中根节点属性值
            参数：
    filePath:xml文件路径
    valueDir:修改属性的字典值，例：{'sn':'902272840008'}
'''
def key_modify_xml_root_value(valueDict, filePath=BASIC_DATA['version']['xmlSavePath']):
    with allure.step(key_get_time() +": 修改xml文件的根节点属性值\n"):
        logging.info(key_get_time()+': modify xml file root note value.')
        xmlService().modify_xml_root_value(filePath, valueDict)
        
        
'''
            说明：读取xml文件中记录节点值
            参数：
    filePath:xml文件路径
    xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
'''    
def key_read_xml_record_value(xmlTreePath, filePath=BASIC_DATA['version']['xmlSavePath']):
    return xmlService().read_xml_record_value(filePath, xmlTreePath)
 
'''
            说明：读取xml文件中根节点属性值
            参数：
    filePath:xml文件路径
    noteName:属性名称
'''  
def key_read_xml_root_value(noteName, filePath=BASIC_DATA['version']['xmlSavePath']):
    return xmlService().read_xml_root_value(filePath, noteName)   