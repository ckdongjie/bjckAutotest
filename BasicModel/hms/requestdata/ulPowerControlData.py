# coding = 'utf-8'
'''
Created on 2022年12月22日

@author: autotest
'''
POWER_CONTROL_URL_DICT={
    'realtimeQueryULPowerControlByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryULPowerControlByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageULPowerControlByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPageULPowerControlByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateULPowerControl':
    {
        'action':'/api/hmsCfg/v1/updateULPowerControl',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":5,
            "fapInstanceId":"1",
            "ulPowerControlKeyId":"1670307104616-1916500364",
            "cellId":"0",
            "poNominalPusch":"-37",
            "pathLossCoeff":"5",
            "poNominalPucch":"-50",
            "preambleInitRxTargetPwr":"-50",
            "pwrRampingStep":"1",
            "deltaPreambleMsg3":"4",
            "poNominalSrs":"-40",
            "pucchPcSwitch":"1",
            "puschPcType":"0",
            "msg3PcSwitch":"1"
        }
    },
    #-------------DL---------------
    'realtimeQueryDLPowerControlByEnbId':
    {
        'action':'/api/hmsCfg/v1/realtimeQueryDLPowerControlByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'findPageDLPowerControlByEnbId':
    {
        'action':'/api/hmsCfg/v1/findPageDLPowerControlByEnbId?enbId=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateDLPowerControl':
    {
        'action':'/api/hmsCfg/v1/updateDLPowerControl',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "enbId":231,
            "fapInstanceId":"1",
            "dlPowerControlKeyId":"16738358414431536576954",
            "cellId":"0",
            "sssPwrOffSet":"0",
            "pssPwrOffset":"0",
            "csiRsPwrOffset":"2",
            "commChPdschPwrOffset":"0",
            "commChPdcchPwrOffset":"0",
            "dlPcTestSwitch":"0",
            "uePdcchPwroffset":"0"
        }
    },        
}