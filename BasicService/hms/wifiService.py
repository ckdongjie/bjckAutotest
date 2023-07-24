# coding = 'utf-8'
'''
Created on 2023年6月8日
@author: dj
'''
from BasicModel.hms.wifiModel import WifiModel


class WifiService():

    '''
                说明：实时查询wifi配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_wifi_info(self, hmsObj, enbId): 
        realQueryRes = WifiModel(hmsObj).wifi_config_realtime_query(enbId)
        return realQueryRes
    
    '''
                说明：查询wifi配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def query_wifi_config_info(self, hmsObj, enbId):
        self.realtime_query_wifi_info(hmsObj, enbId)
        wifiInfo = WifiModel(hmsObj).query_wifi_config_info(enbId)
        return wifiInfo
    
    '''
                说明：修改wifi参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def modify_wifi_info(self, hmsObj, enbId, paraDict): 
        self.realtime_query_wifi_info(hmsObj, enbId)
        updateRes = WifiModel(hmsObj).update_ta_config(enbId, paraDict)
        return updateRes
    
