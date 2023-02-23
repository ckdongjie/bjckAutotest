# coding = 'utf-8'
'''
Created on 2023年2月22日

@author: autotest
'''
PDSCH_URL_DICT={
    'realtimeQueryPdschByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryPdschByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPagePdschByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPagePdschByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updatePdsch':
    {
        'action':'/api/hmsCfg/v1/updatePdsch',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":231,
            "fapInstanceId":"1",
            "pdschKeyId":"1673835841317-711794287",
            "cellId":"0",
            "dlTargetBler":"10",
            "dlDmrsConfigType":"0",
            "dlDmrsMaxLength":"0",
            "fixedAmcStepValue":"4",
            "dlInitMcs":"4",
            "dlInitRank":"0",
            "dlAdditionalDmrsPos":"1",
            "pdschAllocType":"0",
            "pdschPmiType":"0"
        }
    },
            
}