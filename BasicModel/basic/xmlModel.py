# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj
'''

import logging

import xml.etree.ElementTree as ET


class xmlModel():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def read_xml_record_value(self, filename, filePath, xmlTreePath):
        xmlFile = ET.parse(filePath+'\\'+filename)
        xmlRoot = xmlFile.getroot()
        sub = xmlRoot.find(xmlTreePath)
        logging.info('the current value:'+sub.text)
        return sub.text
        
    def modify_xml_record_value(self, filename, filePath, xmlTreePath, modifyContext):
        xmlFile = ET.parse(filePath+'\\'+filename)
        xmlRoot = xmlFile.getroot()
        sub = xmlRoot.find(xmlTreePath)
        logging.info('the old value:'+sub.text)
        sub.text = modifyContext
        xmlFile.write(filePath+'\\'+filename)
     
    def modify_xml_root_value(self, filePath, valueDir):
        xmlFile = ET.parse(filePath)
        xmlRoot = xmlFile.getroot()
        for key in valueDir.keys():
            logging.info('the old value:'+xmlRoot.attrib[key])
            xmlRoot.attrib[key] = valueDir[key]
        xmlFile.write(filePath) 
        
    def rename_xml_filename(self, newfilePath, filePath):
        xmlFile = ET.parse(filePath)
        xmlFile.write(newfilePath)
          
    def read_root_note_value(self, filePath, noteName):
        xmlFile = ET.parse(filePath)
        xmlRoot = xmlFile.getroot()
        return xmlRoot.attrib[noteName]  
    
    def read_record_value(self, filePath, xmlTreePath):
        xmlFile = ET.parse(filePath)
        xmlRoot = xmlFile.getroot()
        sub = xmlRoot.find(xmlTreePath)
        return sub.text    

if __name__ == '__main__':
    filePath = 'F:\\eclipseworkspace\\autotestPro\\AutoTestMain\\xmlFile\\Automatic-18_902272840007_20221110103414.cfg'
    valueDir = {'sn':'902272840008'}
#     xmlModel().modify_xml_root_value(filePath, valueDir)
    xmlTreePath = './/gNodeB_Function/t_gnbfunction/External_NR_Adjacent_Cell/t_nradjcell[@record="1"]/Tac'
    modifyContext = '512003'
#     xmlModel().modify_xml_record_value(filePath, xmlTreePath, modifyContext)
    version = xmlModel().read_root_note_value(filePath, 'version')
    print(version)