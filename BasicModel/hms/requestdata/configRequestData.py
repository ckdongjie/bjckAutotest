# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
URL_DICT={
    'updateMgServer':
    {
        'action':'/api/hmsCfg/v1/updateMgServer',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "mgServerId":"1663139166681-621682232",
            "enbId":173,
            "url":"http://[193:168:6::255]:18088/acs",
            "lastConnectedURL":"http://[193:168:6::254]:18088/acs",
            "username":"",
            "password":"",
            "periodicInformEnable":"1",
            "periodicInformTime":"2022-04-12 14:35:40",
            "periodicInformInterval":"30",
            "parameterKey":"",
            "connectionRequestURL":"http://[193:168:6:0:100:600:0:1]:30005/",
            "connectionRequestUsername":"",
            "connectionRequestPassword":"",
            "udpConnectionRequestAddress":"",
            "stunEnable":"0",
            "stunServerAddress":"",
            "stunServerPort":"20000",
            "stunUsername":"",
            "stunPassword":"",
            "stunMaximumKeepAlivePeriod":"30",
            "stunMinimumKeepAlivePeriod":"0",
            "natDetected":"0"
        }
    },
    'getMgServer':
    {
        'action':'/api/hmsCfg/v1/getMgServer?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'realtimeQueryDeviceManageParam':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryDeviceManageParam?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },    
    'realtimeQueryClockInfo':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryClockInfo?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findClockInfo':
    {
        'action':'/api/hmsCfg/v1/findClockInfo?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },   
    'updateClockInfo':
    {
        'action':'/api/hmsCfg/v1/updateClockInfo',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":4,
            "clockRecordId":"1669173163050-1138603653",
            "clockSrc":"1",
            "clockStatus":"0"
        }
    },    
    
}