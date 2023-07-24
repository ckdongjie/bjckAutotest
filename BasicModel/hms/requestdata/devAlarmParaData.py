# coding = 'utf-8'
'''
Created on 2023年6月27日
@author: autotest
'''
DEV_ALARM_URL_DICT={
    'findDeviceAlarmParam':
    {
        'action':'/api/hmsCfg/v1/findDeviceAlarmParam?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'realtimeQueryDeviceAlarmParam':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryDeviceAlarmParam?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateDeviceAlarmParam':
    {
        'action':'/api/hmsCfg/v1/updateDeviceAlarmParam',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "recordKeyId":"1686276267805-989718371",
            "enbId":38,
            "tempAlarmThld":"100",
            "busVolAlarmLowThld":"10",
            "busVolAlarmHighThld":"14",
            "memUsageAlarmThld":"90",
            "cpuUsageAlarmThld":"90",
            "vswrAlarmThld":"300"
        }
    },
}
