# coding = 'utf-8'
'''
Created on 2023年1月13日

@author: autotest
'''
SCTP_URL_DICT={
    'ipv6SctpAssocRealTimeQuery':
    {
        'action':'/api/hmsCfg/v1/ipv6SctpAssocRealTimeQuery?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageIPv6SctpAssoc':
    {
        'action':'/api/hmsCfg/v1/findPageIPv6SctpAssoc?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateIPv6SctpAssoc':
    {
        'action':'/api/hmsCfg/v1/updateIPv6SctpAssoc',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "recordKeyId":"16735746801521786365898",
            "enbId":4,
            "instanceId":"1",
            "assID":"2",
            "ipId":"1",
            "primaryPeerAddress":"193:168:6::14",
            "localPort":"38412",
            "remotePort":"38412",
            "linkType":"0",
            "status":"1"
        }
    },
    'insertIPv6SctpAssoc':
    {
        'action':'/api/hmsCfg/v1/insertIPv6SctpAssoc',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "recordKeyId":"",
            "enbId":6,
            "instanceId":"",
            "assID":"2",
            "ipId":"1",
            "primaryPeerAddress":"193:168:6::145",
            "localPort":"38422",
            "remotePort":"38412",
            "linkType":"0",
            "status":"1"
        }
    },
    'deleteIPv6SctpAssoc':
    {
        'action':'/api/hmsCfg/v1/deleteIPv6SctpAssoc',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "recordKeyId":"1689663226856-1991782157",
            "enbId":55,
            "instanceId":2,
            "assID":2,
            "ipId":1,
            "primaryPeerAddress":"193:168:6::145",
            "localPort":38412,
            "remotePort":38412,
            "linkType":0,
            "status":1,
            "displayIpIdText":"1(195:168:16:0:200:100:0:1)"
        }
    },
    'ipv4SctpAssocRealTimeQuery':
    {
        'action':'/api/hmsCfg/v1/ipv4SctpAssocRealTimeQuery?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateIPv4SctpAssoc':
    {
        'action':'/api/hmsCfg/v1/updateIPv4SctpAssoc',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "recordKeyId":"16735746801521786365898",
            "enbId":4,
            "instanceId":"1",
            "assID":"2",
            "ipId":"1",
            "primaryPeerAddress":"193:168:6::14",
            "localPort":"38412",
            "remotePort":"38412",
            "linkType":"0",
            "status":"1"
        }
    },       
}