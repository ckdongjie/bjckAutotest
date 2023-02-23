# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''

from BasicModel.hms.csiRsModel import CsiRsModel


class CsiRsService(object):
    '''
    classdocs
    '''

    '''
                说明：修改csi rs的TRS Period参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        trsPeriod:trs周期
    '''
    def update_trs_period(self, hmsObj, enbId, trsPeriod):
        trsPeriodDict = {'SLOTS0':'0', 'SLOTS40':'7', 'SLOTS80':'9', 'SLOTS160':'10'}
        paramsDict = {'trsPeriod':trsPeriodDict[trsPeriod]}
        resCode,resInfo = CsiRsModel(hmsObj).update_csi_rs_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    
    '''
                说明：修改csi report quantity参数
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        csiReportQuantity:csi report quantity参数
    '''
    def update_csi_report_quantity(self, hmsObj, enbId, csiReportQuantity):
        csiReportQuantityDict = {'cri-RI-PMI-CQI':'1', 'cri-RI-CQI':'4'}
        paramsDict = {'csiReportQuantity':csiReportQuantityDict[csiReportQuantity]}
        resCode,resInfo = CsiRsModel(hmsObj).update_csi_rs_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        