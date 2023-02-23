# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''

import logging

from BasicModel.weblmt.lmtCellModel import LmtCellModel
from BasicModel.weblmt.lmtGngModel import LmtGnbModel


class LmtCellService():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    '''
                在weblmt上查询小区状态
                参数：
        lmtObj:weblmt对象
        cellId:小区id
    '''    
    def lmtQueryCellStatus(self, lmtObj, cellId):
        resCode, resInfo = LmtCellModel(lmtObj).lmtQueryCellStatus()
        cellStatus = ''
        if resCode == 200:
            for data in resInfo['data']:
                if data['NrCellId'] == cellId:
                    cellStatus = data['CellAvailableState']
                    break
        return cellStatus
    
    '''
                在weblmt上查询du小区信息
                参数：
        lmtObj:weblmt对象
    '''    
    def lmtQueryDuCellParams(self, lmtObj, tryNum=5):
        for i in range (1, tryNum):
            resCode, resInfo = LmtCellModel(lmtObj).lmtQueryDuCellParams()
            if resCode == 200 and resInfo['errorMessage']=='success':
                return resInfo['data']
            else:
                logging.warning('query du cell params failure, try again')
        return []
        
    '''
                在weblmt上修改du小区信息
                参数：
        lmtObj:weblmt对象
        paramsDict:小区修改参数值字典
    '''    
    def lmtModiryDuCellParams(self, lmtObj, paramsDict, tryNum=5):
        duPara = self.lmtQueryDuCellParams(lmtObj)
        duPara[0].update(paramsDict)
        for i in range (1, tryNum):
            resCode, resInfo = LmtCellModel(lmtObj).lmtModifyDuCellParams(duPara)
            if resCode == 200 and resInfo['result']==0:
                updatedInfo = self.lmtQueryDuCellParams(lmtObj)
                for duParaKey in paramsDict.keys():
                    if updatedInfo[0][duParaKey] != paramsDict[duParaKey]:
                        return 'fail'
                return 'success'
            else:
                logging.warning('modify du cell params failure, try again')
        return 'fail'
    
    

if __name__ == '__main__':
    weblmt = LmtGnbModel().lmtLogin('172.16.2.152')
    paramsDict = {"UlBandwidth":10,"DlBandwidth":10}
#     paramsDict = {"DlNarfcn":723325,"UlNarfcn":723325}
    modifyRes = LmtCellService().lmtModiryDuCellParams(weblmt, paramsDict)
    print('==========',modifyRes)
        
        