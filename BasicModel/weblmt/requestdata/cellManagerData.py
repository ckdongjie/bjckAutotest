# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''
LMT_CELL_URL_DICT={
    'QueryCuCellParams':
    {
        'action':'/cgi-bin/CuDuBts.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "operationType":"select",
            "tableName":"t_cellbasic",
            "pageIndex":0,
            "pageSize":"25"
        }
    },
    'QueryDuCellParams':
    {
        'action':'/cgi-bin/CuDuBts.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "operationType":"select",
            "tableName":"t_ducellbasic",
            "pageIndex":0,
            "pageSize":"25"
        }
    },
    'ModifyDuCellParams':
    {
        'action':'/cgi-bin/CuDuBts.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "operationType":"update",
            "tableName":"t_ducellbasic",
            "data":[{
                "CellId":0,
                "DuCellName":"ducell",
                "FrequencyBand":79,
                "UlBandwidth":"10",
                "DlBandwidth":"10",
                "DuplexMode":1,
                "CellRadius":500,
                "SubcarrierSpacing":1,
                "CyclicPrefixLength":0,
                "DlNarfcn":723324,
                "PhysicalCellId":152,
                "UlNarfcn":723324,
                "CelAvailableState":0,
                "SlotAssignment":2,
                "SpecialSlotStructure":44,
                "TrackingAreaId":0,
                "TaOffset":1,
                "CellAdminState":0,
                "SsbPeriod":2,
                "Sib1Period":0,
                "SsbDescMethod":1,
                "SsbFreqPos":8752,
                "SsbTimePos":128,
                "SmtcPeriod":2,
                "SmtcDuration":3,
                "RanNotificationAreaId":65535,
                "EPRE":-10,
                "PrachConfigurationIndex":147,
                "ZeroCorrelationZoneConfig":7,
                "GPSOutClkDelWaitTime":2592000
            }]

        }
    },
        
}