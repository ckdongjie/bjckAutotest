# coding = 'utf-8'
'''
Created on 2023年2月22日

@author: auto
'''

from BasicModel.hms.dlPowerControlModel import DLPowerControlModel


class DLPowerControlService():
    '''
    classdocs
    '''
    
    '''
                说明：修改CSI-RS功率
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        csirsPowerOffset:修改参数字典
    '''
    def update_csi_rs_power_offset(self, hmsObj, enbId, csirsPowerOffset):
        csiRsDict = {'DB-3':'0','DB0':'1','DB3':'2','DB6':'3'}
        paramsDict = {'csiRsPwrOffset':csiRsDict[csirsPowerOffset]}
        resCode,resInfo = DLPowerControlModel(hmsObj).update_dl_power_control_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False