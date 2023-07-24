'''
Created on 2023年6月6日

@author: dj
'''
from BasicModel.hms.taModel import TaModel


class TaService():

    '''
                说明：实时查询ta配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_ta_info(self, hmsObj, enbId): 
        realQueryRes = TaModel(hmsObj).ta_config_realtime_query(enbId)
        return realQueryRes
    
    '''
                说明：查询ta配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def query_ta_config_info(self, hmsObj, enbId):
        self.realtime_query_ta_info(hmsObj, enbId)
        taInfo = TaModel(hmsObj).query_ta_config_info(enbId)
        return taInfo
    
    '''
                说明：修改ipv6 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def modify_ta_info(self, hmsObj, enbId, paraDict): 
        self.realtime_query_ta_info(hmsObj, enbId)
        updateRes = TaModel(hmsObj).update_ta_config(enbId, paraDict)
        return updateRes
    
