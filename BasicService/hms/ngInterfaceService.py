'''
Created on 2023年6月12日
@author: dj
'''
from BasicModel.hms.ngInterfaceModel import NgInterfaceModel

class NgInterfaceService():

    '''
                说明：实时查询ng配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_ng_info(self, hmsObj, enbId): 
        realQueryRes = NgInterfaceModel(hmsObj).ng_config_realtime_query(enbId)
        return realQueryRes
    
    '''
                说明：查询ng配置信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def query_ng_config_info(self, hmsObj, enbId):
        self.realtime_query_ng_info(hmsObj, enbId)
        ngInfo = NgInterfaceModel(hmsObj).query_ng_config_info(enbId)
        return ngInfo
    
    '''
                说明：修改ng接口参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def modify_ng_info(self, hmsObj, enbId, paraDict): 
        self.realtime_query_ng_info(hmsObj, enbId)
        updateRes = NgInterfaceModel(hmsObj).update_ng_config(enbId, paraDict)
        return updateRes
    
