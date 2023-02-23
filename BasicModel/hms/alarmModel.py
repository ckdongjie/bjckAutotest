# coding = 'utf-8'
'''
Created on 2023年1月10日
@author: dj
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.alarmData import ALARM_URL_DICT


class AlarmModel(HMS):

    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def query_active_alarm(self, sn):
        header = ALARM_URL_DICT['queryPageActiveAlarm']['header']
        url = self.baseUrl+ALARM_URL_DICT['queryPageActiveAlarm']['action']
        body = ALARM_URL_DICT['queryPageActiveAlarm']['body']
        body.update({'sn':sn})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        alarmList = []
        if resCode == 200:
            alarmList = resInfo['rows']
        return alarmList  
    
    def query_history_alarm(self, sn, alarmRaisedStartTime='', alarmRaisedEndTime=''):
        header = ALARM_URL_DICT['queryPageHistoryAlarm']['header']
        url = self.baseUrl+ALARM_URL_DICT['queryPageHistoryAlarm']['action']
        body = ALARM_URL_DICT['queryPageHistoryAlarm']['body']
        body.update({'sn':sn, 'alarmRaisedStartTime':alarmRaisedStartTime, 'alarmRaisedEndTime':alarmRaisedEndTime})
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        alarmList = []
        if resCode == 200:
            alarmList = resInfo['rows']
        return alarmList 
    
    def sync_alarm(self, sn):
        header = ALARM_URL_DICT['alarmSync']['header']
        url = self.baseUrl+ALARM_URL_DICT['alarmSync']['action']
        body = str(sn).split(',')
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            syncRes = resInfo[0]['syncResult']
        return syncRes  