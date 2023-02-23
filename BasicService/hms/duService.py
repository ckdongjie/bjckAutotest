# coding = 'utf-8'
from pip._vendor.distro.distro import InfoDict
'''
Created on 2022年10月17日

@author: dj

'''
from BasicModel.hms.duModel import DuModel


class DuService():
    '''
    classdocs
    '''
    
    '''
                说明：查询Du小区信息
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''
    def query_du_cell_info(self, hmsObj, enbId):
        InfoDict = DuModel(hmsObj).query_du_cell_info(enbId)
        return InfoDict
    
    '''
                说明：修改du基本参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_du_cell_para(self, hmsObj, enbId, params):
        updateRes = DuModel(hmsObj).update_du_cell_para(enbId, params)
        return updateRes
    
    '''
                说明：修改du下行调度参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_du_dl_schedule_para(self, hmsObj, enbId, params):
        resCode,resInfo = DuModel(hmsObj).update_Dl_Schedule(enbId, params)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    
    '''
                说明：修改du上行调度参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_du_ul_schedule_para(self, hmsObj, enbId, params):
        resCode,resInfo = DuModel(hmsObj).update_Ul_Schedule(enbId, params)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    