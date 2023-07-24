# coding = 'utf-8'
from BasicModel.basic.xmlModel import xmlModel
'''
Created on 2022年11月10日

@author: dj
'''

class xmlService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    '''
                说明：读取xml文件中记录节点值
                参数：
        filePath:xml文件路径
        xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
    '''    
    def read_xml_record_value(self, filename, filePath, xmlTreePath):
        return xmlModel().read_xml_record_value(filename, filePath, xmlTreePath)
    
    '''
                说明：修改xml文件中记录节点值
                参数：
        filePath:xml文件路径
        xmlTreePath:修改值的层级目录，例：'.//gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'，.//--根目录
        modifyContext:修改的目标值
    '''    
    def modify_xml_record_value(self, filename, filePath, xmlTreePath, modifyContext):
        xmlModel().modify_xml_record_value(filename, filePath, xmlTreePath, modifyContext)
    
    '''
                说明：修改xml文件中根节点属性值
                参数：
        filePath:xml文件路径
        valueDir:修改属性的字典值，例：{'sn':'902272840008'}
    '''  
    def modify_xml_root_value(self, filePath, valueDir):
        xmlModel().modify_xml_root_value(filePath, valueDir)
        
    '''
        xml文件重命名
    '''    
    def rename_xml_filename(self, newfilePath, filePath):
        xmlModel().rename_xml_filename(newfilePath, filePath) 
     
    '''
                说明：读取xml文件中根节点属性值
                参数：
        filePath:xml文件路径
        noteName:属性名称
    '''  
    def read_xml_root_value(self, filePath, noteName):
        return xmlModel().read_root_note_value(filePath, noteName)
        
        