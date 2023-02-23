# coding = 'utf-8'
'''
Created on 2022年12月13日

@author: autotest
'''

from BasicModel.hms.pdcchModel import PdcchModel


class PdcchService(object):

    '''
                说明：修改PDCCH符号数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_pdcch_symbol_number(self, hmsObj, enbId, symbolNumber):
        paramsDict = {'duration':symbolNumber}
        resCode,resInfo = PdcchModel(hmsObj).update_pdcch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改PDCCH聚合度
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_pdcch_cce_level(self, hmsObj, enbId, cceLevel):
        paramsDict = {'pdcchCceLevel':cceLevel}
        resCode,resInfo = PdcchModel(hmsObj).update_pdcch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        