'''
Created on 2023年6月12日
@author: dj
'''
NG_URL_DICT={
    'realtimeQueryNgInterfaceByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryNgInterfaceByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageNGInterface':
    {
        'action':'/api/hmsCfg/v1/findPageNGInterface?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateNGInterface':
    {
        'action':'/api/hmsCfg/v1/updateNGInterface',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":6,
            "ngInterfaceKeyId":"1686554534690-904789863",
            "gNodeBFunctionInstanceId":"1",
            "ngInterfaceInstanceId":"1",
            "gNBNgInterfaceId":"1",
            "operatorId":"0",
            "state":"0",
            "assId":"1"
        }
    },
}