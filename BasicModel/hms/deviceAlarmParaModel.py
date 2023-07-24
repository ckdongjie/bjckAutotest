# coding = 'utf-8'
'''
Created on 2023年6月27日
@author: autotest
'''
from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.devAlarmParaData import DEV_ALARM_URL_DICT


class DevAlarmParaModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
        
    def query_dev_alarm_para(self, enbId):
        header = DEV_ALARM_URL_DICT['findDeviceAlarmParam']['header']
        url = self.baseUrl+DEV_ALARM_URL_DICT['findDeviceAlarmParam']['action']+enbId
        body = DEV_ALARM_URL_DICT['findDeviceAlarmParam']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo
        
    def realtime_query_dev_alarm_para(self, enbId):
        header = DEV_ALARM_URL_DICT['realtimeQueryDeviceAlarmParam']['header']
        url = self.baseUrl+DEV_ALARM_URL_DICT['realtimeQueryDeviceAlarmParam']['action']+enbId
        body = DEV_ALARM_URL_DICT['realtimeQueryDeviceAlarmParam']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo #"result": "0"
        
    def update_dev_alarm_para(self, paraDict):
        header = DEV_ALARM_URL_DICT['updateDeviceAlarmParam']['header']
        url = self.baseUrl+DEV_ALARM_URL_DICT['updateDeviceAlarmParam']['action']
        body = DEV_ALARM_URL_DICT['updateDeviceAlarmParam']['body']
        body.update(paraDict)
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        if resCode == 200:
            return resInfo  #{"result":"0"}