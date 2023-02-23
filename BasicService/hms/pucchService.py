# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''

from BasicModel.hms.pucchModel import PucchModel


class PucchService(object):
    '''
    classdocs
    '''


    '''
                说明：修改PUCCH format1 RB数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        rbNumber:rb数
    '''
    def update_pucch_format1_rb_number(self, hmsObj, enbId, rbNumber):
        paramsDict = {'format1RbNum':str(rbNumber)}
        resCode,resInfo = PucchModel(hmsObj).update_pucch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改PUCCH format3 RB数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        rbNumber:rb数
    '''
    def update_pucch_format3_rb_number(self, hmsObj, enbId, rbNumber):
        paramsDict = {'format3RbNum':str(rbNumber)}
        resCode,resInfo = PucchModel(hmsObj).update_pucch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改PUCCH format0 RB数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        rbNumber:rb数
    '''
    def update_pucch_format0_rb_number(self, hmsObj, enbId, rbNumber):
        paramsDict = {'format0RbNum':str(rbNumber)}
        resCode,resInfo = PucchModel(hmsObj).update_pucch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改PUCCH format2 RB数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        rbNumber:rb数
    '''
    def update_pucch_format2_rb_number(self, hmsObj, enbId, rbNumber):
        paramsDict = {'format2RbNum':str(rbNumber)}
        resCode,resInfo = PucchModel(hmsObj).update_pucch_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        