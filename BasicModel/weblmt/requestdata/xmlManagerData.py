# coding = 'utf-8'
'''
Created on 2022年11月10日

@author: dj
'''
LMT_XML_URL_DICT={
    'BntCfgExport':
    {
        'action':'/cgi-bin/BntCfgExport.py',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
        }
    },
    'upload_BntCfgFile':
    {
        'action':'/cgi-bin/upload_BntCfgFile.py',
        'method':'POST',
        'header':{
            'Cookie':'LoginName=admin'
        },
        'body':{
        }
    },
    'BntCfgImport':
    {
        'action':'/cgi-bin/BntCfgImport.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
            "fileName":"BntCfgFile",
            "cfgFlag":0,
            "staType":"BS5514"
        }
    },    
}
