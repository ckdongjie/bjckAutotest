# coding = 'utf-8'
'''
Created on 2023年02月22日
@author: autotest
'''
from BasicModel.hms.pdschModel import PdschModel

class PdschService(object):
    '''
                说明：修改PDSCH资源分配类型
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        pdschAllocType:pusch资源分配类型
    '''
    def update_pdsch_resource_allocation_type(self, hmsObj, enbId, pdschAllocType):
        pdschAllocTypeDict = {'Type0':'0', 'Type1':'1', 'Adaptive':'2'}
        paramsDict = {'pdschAllocType':pdschAllocTypeDict[pdschAllocType]}
        resCode,resInfo = PdschModel(hmsObj).update_pdsch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False