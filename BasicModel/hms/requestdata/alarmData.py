# coding = 'utf-8'
'''
Created on 2023年1月10日

@author: dj
'''
ALARM_URL_DICT={
    'queryPageActiveAlarm':
    {             
        'action':'/api/hmsAlarm/v1/queryPageActiveAlarm',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "domainList":"1,2,3,7,9,11,13",
            "enbSnList":["902222640001"],
            "perceivedSeverity":"",
            "eventType":"",
            "alarmRaisedStartTime":"",
            "alarmRaisedEndTime":"",
            "alarmState":"",
            "alarmCode":"",
            "alarmName":"",
            "start":0,
            "limit":100
        }
    },
    'queryPageHistoryAlarm':
    {
        'action':'/api/hmsAlarm/v1/queryPageHistoryAlarm',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "domainList":"1,2,3,7,9,11,13",
            "enbName":"",
            "enbSnList":["902222640001"],
            "perceivedSeverity":"",
            "eventType":"",
            "alarmRaisedStartTime":"",
            "alarmRaisedEndTime":"",
            "enbIp":"",
            "region":"",
            "alarmState":"",
            "alarmCode":"",
            "alarmName":"",
            "delAccount":"",
            "start":0,
            "limit":100
        }
    },
    'alarmSync':
    {
        'action':'/api/hmsAlarm/v1/alarmSync',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':
            ["902133100001"]
    }
            
}