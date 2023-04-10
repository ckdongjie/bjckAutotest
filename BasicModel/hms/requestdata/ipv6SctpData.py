# coding = 'utf-8'
'''
Created on 2023年3月2日

@author: auto
'''
IPV6_SCTP_URL_DICT={
    'realtimeQueryIpv6SctpByEnbId':
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
            "recordKeyId":"16777457470862062165540",
            "enbId":231,
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