'''
Created on 2022年12月9日

@author: autotest
'''
UL_SCHEDULE_URL_DICT={
    'realtimeQueryUlScheduleInfo':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryDUULScheduleByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageUlScheduleInfo':
    {
        'action':'/api/hmsCfg/v1/findPageDUULScheduleByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateUlSchedule':
    {
        'action':'/api/hmsCfg/v1/updateDUULSchedule',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "recordKeyId":"1670307103616-1120595221",
            "cellId":"0",
            "ulPreSchdTestSwitch":"1",
            "ulPrbTestSwitch":"0",
            "maxUlPrb":"273",
            "minUlPrb":"8",
            "ulMimoTestSwitch":"1",
            "ulRank":"0",
            "ulAmcTestSwitch":"0",
            "ulMaxMcs":"28",
            "ulMinMcs":"0",
            "ulHarqTestSwitch":"1",
            "ulMaxHarqTxCnt":"4",
            "ulHarqCommbineType":"1",
            "ulMaxMsg3TxCnt":"5",
            "maxUlRlcVoiceLchSegments":"0",
            "ulPrbAllocStep":"8",
            "ulPreSchdType":"0"
        }
    },
            
}