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
    
        
}