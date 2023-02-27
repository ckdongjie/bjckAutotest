# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
URL_DICT={
    'queryPageEnbByCondition':
    {
        'action':'/api/hmsCfg/v1/queryPageEnbByCondition',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "domainList":"1,3,7,9,11,13",
            "enbName":"","enbIp":"",
            "softVersion":"",
            "serialNumber":"902251700001",
            "enbStatus":"",
            "region":"",
            "delAccount":2,
            "start":0,
            "limit":15
        }
    },

    'findPageGNodeBFunctionByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPageGNodeBFunctionByEnbId',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
    },

    'setAutoTestMode':
    {
        'action':'/api/hmsCfg/v1/updateGNodeBFunction',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            'enbId': 30,
            'gNBId': "23450",
            'gNBIdLength': "32",
            'gNBName': "lh-test-3.5",
            'gNodeBFunctionId': "1672734484998-2134776560",
            'gNodeBFunctionInstanceId': "1",
            'selfTestSwitch': "0",
            'userLabel': "hlt"
        }
    },
        
}