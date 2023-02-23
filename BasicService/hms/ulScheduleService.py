# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''

from BasicModel.hms.duModel import DuModel


class ULScheduleService():
    '''
               功能：修改下行调度amc开关
                参数：
        hmsObj:hms对象
        enbId:基站ID
        switch:amc开关
    '''
    def modify_du_ul_amc_switch(self, hmsObj, enbId, switch):
        switchDict = {'open':'1', 'close':'0'}
        params = {'ulAmcTestSwitch':switchDict[switch]}
        realQuery = DuModel(hmsObj).realtime_Query_Ul_Schedule(enbId)
        if realQuery == True:
            infoDict = DuModel(hmsObj).get_Ul_Schedule_Info(enbId)
            infoDict.update(params)
            resCode,resInfo = DuModel(hmsObj).update_Ul_Schedule(enbId, params)
            if resCode == 200 and resInfo['result']=='0':
                return True
            else:
                return False
            
    '''
               功能：修改mcs值
                参数：
        hmsObj:hms对象
        enbId:基站ID
        mcs:mcs值
    '''
    def modify_du_ul_mcs(self, hmsObj, enbId, mcs):
        params = {'ulMaxMcs':str(mcs)}
        realQuery = DuModel(hmsObj).realtime_Query_Ul_Schedule(enbId)
        if realQuery == True:
            infoDict = DuModel(hmsObj).get_Ul_Schedule_Info(enbId)
            infoDict.update(params)
            resCode,resInfo = DuModel(hmsObj).update_Ul_Schedule(enbId, params)
            if resCode == 200 and resInfo['result']=='0':
                return True
            else:
                return False