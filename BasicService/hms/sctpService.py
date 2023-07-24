# coding = 'utf-8'
'''
Created on 2023年1月13日
@author: autotest
'''
from BasicModel.hms.sctpModel import SctpModel

class SctpService():

    '''
                说明：实时查询ipv6 sctp信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_ipv6_sctp_info(self, hmsObj, enbId): 
        realQueryRes = SctpModel(hmsObj).ipv6_sctp_config_realtime_query(enbId)
        return realQueryRes
    
    '''
                说明：修改ipv6 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def modify_ipv6_sctp_info(self, hmsObj, enbId, paraDict): 
        self.realtime_query_ipv6_sctp_info(hmsObj, enbId)
        updateRes = SctpModel(hmsObj).update_ivp6_sctp_config(enbId, paraDict)
        return updateRes
    
    '''
                说明：新增ipv6 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def add_ipv6_sctp_info(self, hmsObj, enbId, paraDict): 
        addRes = SctpModel(hmsObj).add_ivp6_sctp_config(enbId, paraDict)
        return addRes
    
    '''
                说明：删除ipv6 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def del_ipv6_sctp_info(self, hmsObj, enbId, assID): 
        delRes = SctpModel(hmsObj).del_ivp6_sctp_config(enbId, assID)
        return delRes
    
    '''
                说明：查询ipv6 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def query_ipv6_sctp_info(self, hmsObj, enbId): 
        self.realtime_query_ipv6_sctp_info(hmsObj, enbId)
        queryRes = SctpModel(hmsObj).query_ipv6_sctp_config_info(enbId)
        return queryRes
    
    '''
                说明：实时查询ipv4 sctp信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_ipv4_sctp_info(self, hmsObj, enbId): 
        realQueryRes = SctpModel(hmsObj).ipv4_sctp_config_realtime_query(enbId)
        return realQueryRes
    
    '''
                说明：修改ipv4 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def modify_ipv4_sctp_info(self, hmsObj, enbId, paraDict): 
        self.realtime_query_ipv4_sctp_info(hmsObj, enbId)
        updateRes = SctpModel(hmsObj).update_ivp4_sctp_config(enbId, paraDict)
        return updateRes
    
    '''
                说明：查询ipv4 sctp参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        paraDict:参数字典
    '''    
    def query_ipv4_sctp_info(self, hmsObj, enbId): 
        self.realtime_query_ipv4_sctp_info(hmsObj, enbId)
        queryRes = SctpModel(hmsObj).query_ipv4_sctp_config_info(enbId)
        return queryRes