'''
Created on 2023年6月27日
@author: autotest
'''
from BasicModel.hms.deviceAlarmParaModel import DevAlarmParaModel


class DevAlarmParaService():

    '''
                说明：实时查询设备告警参数信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def realtime_query_dev_alarm_para(self, hmsObj, enbId): 
        realQueryRes = DevAlarmParaModel(hmsObj).realtime_query_dev_alarm_para(enbId)
        return realQueryRes
    
    '''
                说明：查询设备告警参数信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''    
    def query_dev_alarm_para(self, hmsObj, enbId): 
        self.realtime_query_dev_alarm_para(hmsObj, enbId)
        devAlarmPara = DevAlarmParaModel(hmsObj).query_dev_alarm_para(enbId)
        return devAlarmPara
    
    '''
                说明：更新设备告警参数信息
                参数：
        hmsObj:hms对象
        paraDict:参数字典
    '''    
    def update_dev_alarm_para(self, hmsObj, enbId, paraDict): 
        devAlarmPara = self.query_dev_alarm_para(hmsObj, enbId)
        devAlarmPara.update(paraDict)
        updateRes = DevAlarmParaModel(hmsObj).update_dev_alarm_para(devAlarmPara)
        return updateRes
        