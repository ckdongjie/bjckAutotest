# coding = 'utf-8'
'''
Created on 2022年12月22日

@author: autotest
'''

from BasicModel.hms.ulPowerControlModel import ULPowerControlModel


class ULPowerControlService():
    '''
    classdocs
    '''


    '''
                说明：修改PDCCH符号数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_initial_received_target_power(self, hmsObj, enbId, preambleInitRxTargetPwr):
        paramsDict = {'preambleInitRxTargetPwr':preambleInitRxTargetPwr}
        resCode,resInfo = ULPowerControlModel(hmsObj).update_ul_power_control_params(enbId, paramsDict)
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
    def update_power_ramping_step(self, hmsObj, enbId, pwrRampingStep):
        pwrRampingStepDict = {'DB0':'0', 'DB2':'1', 'DB4':'2', 'DB6':'3'}
        paramsDict = {'pwrRampingStep':pwrRampingStepDict[pwrRampingStep]}
        resCode,resInfo = ULPowerControlModel(hmsObj).update_ul_power_control_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    
    '''
                说明：修改PUSCH P0 Nominal参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_p0_nominal_pusch(self, hmsObj, enbId, p0NominalPusch):
        paramsDict = {'poNominalPusch':p0NominalPusch}
        resCode,resInfo = ULPowerControlModel(hmsObj).update_ul_power_control_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改path loss coefficient参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_path_loss_coefficient(self, hmsObj, enbId, pathLossCoefficient):
        pathLossCoefficientDict = {'ALPHA0':'0', 'ALPHA04':'1', 'ALPHA05':'2', 'ALPHA06':'3','ALPHA07':'4','ALPHA08':'5','ALPHA09':'6','ALPHA1':'7'}
        paramsDict = {'pathLossCoeff':pathLossCoefficientDict[pathLossCoefficient]}
        resCode,resInfo = ULPowerControlModel(hmsObj).update_ul_power_control_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改PUCCH P0 Nominal参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        params:修改参数字典
    '''
    def update_p0_nominal_pucch(self, hmsObj, enbId, p0NominalPucch):
        paramsDict = {'poNominalPucch':p0NominalPucch}
        resCode,resInfo = ULPowerControlModel(hmsObj).update_ul_power_control_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        