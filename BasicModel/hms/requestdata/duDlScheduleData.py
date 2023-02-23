'''
Created on 2022年12月9日

@author: autotest
'''
DL_SCHEDULE_URL_DICT={
    'realtimeQueryDlScheduleInfo':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryDUDLScheduleByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageDlScheduleInfo':
    {
        'action':'/api/hmsCfg/v1/findPageDUDLScheduleByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateDlSchedule':
    {
        'action':'/api/hmsCfg/v1/updateDUDLSchedule',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "recordKeyId":"1670307103729-480826120",
            "cellId":"0",
            "dlPreSchdTestSwitch":"0",
            "dlPrbTestSwitch":"0",
            "maxDlPrb":"273",
            "minDlPrb":"8",
            "dlMimoTestSwitch":"0",
            "dlRank":"0",
            "dlAmcTestSwitch":"0",
            "dlMaxMcs":"28",
            "dlMinMcs":"0",
            "dlHarqTestSwitch":"1",
            "dlMaxHarqTxCnt":"4",
            "dlHarqCommbineType":"1",
            "dlPrbAllocStep":"8",
            "slotSchdSwitch":1048575
        }
    },
            
}