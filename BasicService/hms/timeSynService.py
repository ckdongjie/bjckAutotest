# coding='utf-8'
'''
Created on 2023年6月28日
@author: dj
'''
from BasicModel.hms.timeSynModel import TimeSynModel

class TimeSynService():
    
    '''
                说明：查询ntp信息
                参数：
        hmsObj:hms对象
    '''    
    def query_ntp_info(self, hmsObj): 
        ntpInfoDict = TimeSynModel(hmsObj).query_ntp_info()
        return ntpInfoDict
    
    '''
                说明：更新ntp信息
                参数：
        hmsObj:hms对象
        paraDict:参数字典
    '''    
    def update_ntp_info(self, hmsObj, paraDict): 
        ntpInfoDict = TimeSynModel(hmsObj).query_ntp_info()
        ntpInfoDict.update(paraDict)
        updateRes = TimeSynModel(hmsObj).update_ntp_info(ntpInfoDict)
        return updateRes
    
    
        