# coding = utf-8
'''
Created on 2022年9月14日

@author: dj
'''
from BasicModel.hms.diagnosticModel import DiagnosticModel


class DiagnosticService():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    
    '''
                基站复位
                参数：
        hmsObj:hms对象
        serialNumber:基站序列号
    '''    
    def reboot_enb(self, hmsObj, enbId):
        resCode, resInfo = DiagnosticModel(hmsObj).reboot_enb(enbId)
        return resCode, resInfo
            