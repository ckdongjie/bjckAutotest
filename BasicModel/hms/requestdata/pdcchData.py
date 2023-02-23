# coding = 'utf-8'
'''
Created on 2022年12月13日

@author: autotest
'''

PDCCH_URL_DICT={
    'realtimeQueryPdcchByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryPdcchByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPagePdcchByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPagePdcchByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updatePdcch':
    {
        'action':'/api/hmsCfg/v1/updatePdcch',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "pdcchKeyId":"16703071041822067635584",
            "cellId":"0",
            "ulMaxCcePct":"50",
            "duration":"2",
            "occupiedRbNum":"0",
            "pdcchBlerTarget":"3",
            "pdcchCceLevel":"3"
        }
    },
            
}