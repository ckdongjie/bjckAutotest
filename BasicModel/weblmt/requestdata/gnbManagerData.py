# coding = utf-8 
'''
Created on 2022年10月27日

@author: dj
'''
LMT_URL_DICT={
    'BntReboot':
    {
        'action':'/cgi-bin/BntReboot.py',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'LoginName=admin'
        },
        'body':{
        }
    },
        
}