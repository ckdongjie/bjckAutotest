# 'coding='utf-8'
'''
Created on 2023年6月28日
@author: dj
'''
TIME_SYN_URL_DICT = {
    'update':
    {
        'action':'/api/sm/v1/ntpInfo/update',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; BAYEUX_BROWSER=1myku1tiv3o1t1if; warningFlag=false'
        },
        'body':{
            "id":1,
            "ntpType":1,
            "ntpServerUrl":"pool.ntp.org",
            "ntpInterval":60,
            "ntpTime":"2023-06-28 12:07:00"
        }
    },# {"result":true}
    'query':
    {
        'action':'/api/sm/v1/ntpInfo/query',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; BAYEUX_BROWSER=1myku1tiv3o1t1if; warningFlag=false'
        },
        'body':{
        }
    },# {"result":true}
}
