# coding = 'utf-8'
'''
Created on 2022年12月20日

@author: autotest
'''
CSIRS_URL_DICT={
    'realtimeQueryCsiRsByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryCsiRsByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findCsiRsByEnbId':
    {
        'action':'/api/hmsCfg/v1/findCsiRsByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateCsiRs':
    {
        'action':'/api/hmsCfg/v1/updateCsiRs',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "csiRsKeyId":"16703071038061512087976",
            "cellId":"0",
            "trsPeriod":"7",
            "csiPeriod":"9",
            "cqiSubbandSize":"0",
            "cqiFormatIndicator":"0",
            "csiReportQuantity":"1",
            "csiReportType":"1",
            "csiTxPeriod":"10"
        }
    },
            
}
