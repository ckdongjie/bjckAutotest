# coding = 'utf-8'
'''
Created on 2022年12月27日

@author: autotest
'''
LMT_VER_URL_DICT={
    'startUploadVersionPkg':
    {
        'action':'/cgi-bin/upgradeProcess.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "optType":3002,
            "cfgFlag":0,
            "fileName":"BS5514_V1.10.80P2.zip"
        }
    },
    'uploadVersionPkg':
    {
        'action':'/cgi-bin/upload.py',
        'method':'POST',
        'header':{
#             'content-type': "multipart/form-data; boundary=----WebKitFormBoundary4dwEHI4Y62sUZ5KB",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "filename":"BS5514_V1.10.80P2.zip"
        }
    },
    'queryUploadProcess':
    {
        'action':'/cgi-bin/upgradeProcess.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "optType":1101,
            "cfgFlag":0,
            "fileName":"BS5514_V1.10.80P2.zip"
        }
    }, 
    'activeVersion':
    {
        'action':'/cgi-bin/upgradeProcess.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "optType":3011,
            "cfgFlag":0,
            "fileName":"BS5514_V1.10.80P2.zip"
        }
    }, 
    'queryVersionInfo':
    {
        'action':'/cgi-bin/queryBoardStatus.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "operationType":"query",
            "tableName":"boardStatus"
        }
    },  
    'queryVersionPackageInfo':
    {
        'action':'/cgi-bin/CuDuBts.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "operationType":"select",
            "tableName":"t_swpkg",
            "pageIndex":0,
            "pageSize":"25"
        }
    }, 
}