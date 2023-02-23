# coding = utf-8
'''
Created on 2022年9月13日

@author: dj
'''
from time import sleep

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.duDlScheduleData import DL_SCHEDULE_URL_DICT
from BasicModel.hms.requestdata.duUlScheduleData import UL_SCHEDULE_URL_DICT
from BasicModel.hms.requestdata.requestdata import URL_DICT


class DuModel(HMS):
    '''
    classdocs
    '''
    def __init__(self, hmsObj=None):
        '''
        Constructor
        '''
        if hmsObj:
            self.baseUrl = hmsObj.baseUrl
    
    def realtime_query_du_cell_info(self, enbId, tryNum=3):
        header = URL_DICT['realtimeQueryDuCellBasicByEnbId']['header']
        url = self.baseUrl+URL_DICT['realtimeQueryDuCellBasicByEnbId']['action']+str(enbId)
        body = URL_DICT['realtimeQueryDuCellBasicByEnbId']['body']
        result = False
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['result']=='0':
                result = True
                break
            else:
                sleep(3)
        return result
            
    def query_du_cell_info(self, enbId):
        header = URL_DICT['findDuCellBasicByEnbId']['header']
        url = self.baseUrl+URL_DICT['findDuCellBasicByEnbId']['action']+str(enbId)
        body = URL_DICT['findDuCellBasicByEnbId']['body']
        response = self.get_request(url, json=body, headers = header)
        resCode = response.status_code 
        infoDict = {}
        if resCode == 200:
            resInfo = response.json()
            if resInfo['rows']!=[]:
                infoDict = resInfo['rows'][0]
        return infoDict
        
    def update_du_cell_para(self, enbId, params, tryNum=5):
        if self.realtime_query_du_cell_info(enbId):
            duCellInfo = self.query_du_cell_info(enbId)
            duCellInfo.update(params)
            header = URL_DICT['updateDUCellBasic']['header']
            url = self.baseUrl+URL_DICT['updateDUCellBasic']['action']
            body = URL_DICT['updateDUCellBasic']['body']
            body.update(duCellInfo) #更新body参数
            for i in range (tryNum):
                response = self.post_request(url, json=body, headers = header)
                resCode = response.status_code
                resInfo = response.json() 
                if resInfo.get('socketTimeout'):
                    continue
                if resCode == 200 and resInfo['result']=='0':
                    return True
                else:           
                    return False
        else:
            return False
    
    def realtime_Query_Dl_Schedule(self, enbId, tryNum=3):
        header = DL_SCHEDULE_URL_DICT['realtimeQueryDlScheduleInfo']['header']
        url = self.baseUrl+DL_SCHEDULE_URL_DICT['realtimeQueryDlScheduleInfo']['action']+str(enbId)
        body = DL_SCHEDULE_URL_DICT['realtimeQueryDlScheduleInfo']['body']
        result = False
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['result']=='0':
                result = True
                break
            else:
                sleep(3)
        return result
    
    def get_Dl_Schedule_Info(self, enbId, tryNum=3):
        header = DL_SCHEDULE_URL_DICT['findPageDlScheduleInfo']['header']
        url = self.baseUrl+DL_SCHEDULE_URL_DICT['findPageDlScheduleInfo']['action']+str(enbId)
        body = DL_SCHEDULE_URL_DICT['findPageDlScheduleInfo']['body']
        infoDict = {}
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['total']=='1':
                infoDict = resInfo['rows'][0]
                break
            else:
                sleep(5)
        return infoDict
    
    def update_Dl_Schedule(self, enbId, paraDict):
        self.realtime_Query_Dl_Schedule(enbId)
        infoDict = self.get_Dl_Schedule_Info(enbId)
        infoDict.update(paraDict)
        header = DL_SCHEDULE_URL_DICT['updateDlSchedule']['header']
        url = self.baseUrl+DL_SCHEDULE_URL_DICT['updateDlSchedule']['action']
        body = DL_SCHEDULE_URL_DICT['updateDlSchedule']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo

    def realtime_Query_Ul_Schedule(self, enbId, tryNum=3):
        header = UL_SCHEDULE_URL_DICT['realtimeQueryUlScheduleInfo']['header']
        url = self.baseUrl+UL_SCHEDULE_URL_DICT['realtimeQueryUlScheduleInfo']['action']+str(enbId)
        body = UL_SCHEDULE_URL_DICT['realtimeQueryUlScheduleInfo']['body']
        result = False
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['result']=='0':
                result = True
                break
            else:
                sleep(3)
        return result
    
    def get_Ul_Schedule_Info(self, enbId, tryNum=3):
        header = UL_SCHEDULE_URL_DICT['findPageUlScheduleInfo']['header']
        url = self.baseUrl+UL_SCHEDULE_URL_DICT['findPageUlScheduleInfo']['action']+str(enbId)
        body = UL_SCHEDULE_URL_DICT['findPageUlScheduleInfo']['body']
        infoDict = {}
        for i in range (tryNum):
            response = self.get_request(url, json=body, headers = header)
            resCode = response.status_code
            resInfo = response.json()
            if resCode == 200 and resInfo['total']=='1':
                infoDict = resInfo['rows'][0]
                break
            else:
                sleep(5)
        return infoDict
    
    def update_Ul_Schedule(self, enbId, paraDict):
        self.realtime_Query_Ul_Schedule(enbId)
        infoDict = self.get_Ul_Schedule_Info(enbId)
        infoDict.update(paraDict)
        header = UL_SCHEDULE_URL_DICT['updateUlSchedule']['header']
        url = self.baseUrl+UL_SCHEDULE_URL_DICT['updateUlSchedule']['action']
        body = UL_SCHEDULE_URL_DICT['updateUlSchedule']['body']
        body.update(infoDict) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code
        resInfo = response.json() 
        return resCode,resInfo