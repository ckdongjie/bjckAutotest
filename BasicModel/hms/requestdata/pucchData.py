# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''
PUCCH_URL_DICT={
    'realtimeQueryPucchByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryPucchByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPagePucchByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPagePucchByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updatePucch':
    {
        'action':'/api/hmsCfg/v1/updatePucch',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "pucchKeyId":"1670307103981541805888",
            "cellId":"0",
            "format3RbNum":"4",
            "format1RbNum":"2",
            "srPeriod":"10",
            "format2RbNum":"7",
            "format0RbNum":"7"
        }
    },
            
}