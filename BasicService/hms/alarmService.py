# coding = 'utf-8'
'''
Created on 2023年1月10日
@author: dj
'''
from BasicModel.hms.alarmModel import AlarmModel

class AlarmService():
    '''
    classdocs
    '''
    '''
                    当前告警查询
    '''
    def query_active_alarm(self, hmsObj, sn):
        alarmList = AlarmModel(hmsObj).query_active_alarm(sn)
        return alarmList
    
    '''
                    历史告警查询
    '''
    def query_history_alarm(self, hmsObj, sn, alarmRaisedStartTime='', alarmRaisedEndTime=''):
        alarmList = AlarmModel(hmsObj).query_history_alarm(sn, alarmRaisedStartTime, alarmRaisedEndTime)
        return alarmList
    
    '''
                    告警同步
    '''
    def sync_alarm(self, hmsObj, sn):
        syncRes = AlarmModel(hmsObj).sync_alarm(sn)
        return syncRes