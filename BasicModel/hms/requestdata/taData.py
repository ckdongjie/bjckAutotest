# coding = 'utf-8'
'''
Created on 2023年6月6日
@author: autotest
'''
TA_URL_DICT={
    'realtimeQueryTaByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryTaByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageTaByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPageTaByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateTa':
    {
        'action':'/api/hmsCfg/v1/updateTa',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
                "enbId":44,
                "taKeyId":"16859672096811824135636",
                "gNodeBFunctionInstanceId":"1",
                "taInstanceId":"1",
                "trackingAreaId":"0",
                "tac":"512000"
            }
    },
}