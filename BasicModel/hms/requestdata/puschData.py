# coding = 'utf-8'
'''
Created on 2023年2月22日

@author: autotest
'''
PUSCH_URL_DICT={
    'realtimeQueryPuschByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryPuschByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPagePuschByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPagePuschByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updatePusch':
    {
        'action':'/api/hmsCfg/v1/updatePusch',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":231,
            "fapInstanceId":"1",
            "puschKeyId":"1673835841234-1442157681",
            "cellId":"0",
            "ulDmrsType":"1",
            "ulAdditionalDmrsPos":"1",
            "ulTargetIbler":"10",
            "sinrThldforWaveformSel":"32",
            "puschAllocType":"2"
        }
    },
            
}