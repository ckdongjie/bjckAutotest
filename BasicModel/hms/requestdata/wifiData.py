'''
Created on 2023年6月8日
@author: dj
'''
WIFI_URL_DICT={
    'realtimeQueryWifiConfigByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryWifiConfigByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageWifiConfig':
    {
        'action':'/api/hmsCfg/v1/findPageWifiConfig?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateWifiConfig':
    {
        'action':'/api/hmsCfg/v1/updateWifiConfig',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
                "enbId":44,
                "recordKeyId":"1684724892967-1468957713",
                "gNodeBFunctionInstanceId":"1",
                "instanceId":"1",
                "wifiId":"0",
                "wifiTxPower":"11",
                "wifiHBStatus":"0",
                "wifiCellStatus":"0",
                "wifiDfsStatus":"0",
                "wifiRfSwitch":"1"
            }
    },
}
