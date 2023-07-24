# coding = 'utf-8'
'''
Created on 2023年6月14日
@author: dj
'''
LOG_URL_DICT={
    'findLogLevel':
    {
        'action':'/api/hmsCfg/v1/findLogLevel',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'updateLogLevel':
    {
        'action':'/api/hmsCfg/v1/upLogLevel',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "modifyLogLevelId":"1686640519674-903928037",
            "levelConfig":"ERROR",
            "levelAlarm":"ERROR",
            "levelPm":"ERROR",
            "levelNm":"ERROR",
            "levelUsmc":"ERROR",
            "levelSm":"WARN",
            "levelTr069":"ERROR"
        }
    },
    'isOneClickLogExportTaskNameExist':
    {
        'action':'/api/hmsCfg/v1/isOneClickLogExportTaskNameExist',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "taskName":"201",
            "operatorId":"65bb5097-de07-44f7-ad5d-20cb413f60de"
        }
    },
    'insertOneClickLogExportTask':
    {
        'action':'/api/hmsCfg/v1/insertOneClickLogExportTask',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "taskId":"",
            "taskName":"201",
            "taskDesc":"",
            "taskStatus":"1",
            "task2EnbInfos":[{"serialNumber":"902222640001"}],
            "creatorID":"65bb5097-de07-44f7-ad5d-20cb413f60de",
            "createTime":""
        }
    },
    'findPageOneClickLogExportTask':
    {
        'action':'/api/hmsCfg/v1/findPageOneClickLogExportTask',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "taskName":"",
            "operatorId":"65bb5097-de07-44f7-ad5d-20cb413f60de",
            "createBeginTime":"",
            "createEndTime":"",
            "taskStatus":"",
            "triggerType":"",
            "gnbName":"",
            "alarmName":"",
            "userManagedDomainList":"1",
            "rootUserFlag":True,
            "operatorUserName":"root",
            "start":0,
            "limit":100
        }
    },
    'batchDeleteOneClickLogExportTask':
    {
        'action':'/api/hmsCfg/v1/batchDeleteOneClickLogExportTask',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "deletedTaskIdList":["16867271383762070801992"]
        }
    },
    'updateOneClickLogExportTask':
    {
        'action':'/api/hmsCfg/v1/updateOneClickLogExportTask',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "taskId":"1686808555779711835364",
            "taskName":"tst",
            "taskDesc":"dfsf",
            "taskStatus":"2",
            "task2EnbInfos":[{"serialNumber":"902222640001"}],
            "creatorID":"65bb5097-de07-44f7-ad5d-20cb413f60de",
            "createTime":"2023-06-15 14:55:55"
        }
    },
    'batchUpdateOneClickLogExportTaskStatus':
    {
        'action':'/api/hmsCfg/v1/batchUpdateOneClickLogExportTaskStatus',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "taskStatus":1,
            "taskIdList":["1686808555779711835364"]
        }
    },
    'oneClickLogExport':
    {
        'action':'/api/httpfs/v1/download/oneClickLogExport/',
        'method':'GET',
        'header':{
            'Cookie':'lang=en-US; BAYEUX_BROWSER=usf05mdfqp74q6jg; sessioncode=pngljrh2rm; username=root; warningFlag=false',
        },
        'body':{
        }
    },
    'downRunLog':
    {
        'action':'/api/sm/v1/runlog/download?path=/var/hms/logs/',
        'method':'GET',
        'header':{
            'Cookie':'lang=en-US; BAYEUX_BROWSER=usf05mdfqp74q6jg; sessioncode=pngljrh2rm; username=root; warningFlag=false',
        },
        'body':{
        }
    },
    'downOperateLog':
    {
        'action':'/api/sm/v1/exportOpLog?',
        'method':'GET',
        'header':{
            'Cookie':'lang=en-US; BAYEUX_BROWSER=usf05mdfqp74q6jg; sessioncode=pngljrh2rm; username=root; warningFlag=false',
        },
        'body':{
        }
    },
    'downSecurityLog':
    {
        'action':'/api/sm/v1/safeLog/export?',
        'method':'GET',
        'header':{
            'Cookie':'lang=en-US; BAYEUX_BROWSER=usf05mdfqp74q6jg; sessioncode=pngljrh2rm; username=root; warningFlag=false',
        },
        'body':{
        }
    },
}

