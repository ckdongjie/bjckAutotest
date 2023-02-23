# coding = 'utf-8'

'''
Created on 2022年10月17日

@author: dj
'''

from BasicModel.hms.cuModel import CuModel

class CuService():
    
    '''
                说明：修改Cu参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_cu_cell_para(self, hmsObj, enbId, params):
        updateRes = CuModel(hmsObj).update_cu_cell_para(enbId, params)
        return updateRes
    
    '''
                说明：查询cu小区状态
                参数：
        hmsObj:hms对象
        enbId:基站enbId
    '''
    def real_query_cu_cell_status(self, hmsObj, enbId):
        resCode, resInfo = CuModel(hmsObj).batchRealTimeQueryCuCellStatus(enbId)
        return resCode, resInfo