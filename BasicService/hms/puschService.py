# coding = 'utf-8'
'''
Created on 2023年02月22日
@author: autotest
'''
from BasicModel.hms.puschModel import PuschModel
class PuschService(object):
    '''
                说明：修改PUSCH资源分配类型
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        puschAllocType:pusch资源分配类型
    '''
    def update_pusch_resource_allocation_type(self, hmsObj, enbId, puschAllocType):
        puschAllocTypeDict = {'Type0':'0', 'Type1':'1', 'Adaptive':'2'}
        paramsDict = {'puschAllocType':puschAllocTypeDict[puschAllocType]}
        resCode,resInfo = PuschModel(hmsObj).update_pusch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        