# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj
'''
URL_DICT_USER={
    'userExist':
    {
        'action':'/api/usmc/v1/userExist?userName=',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'userAdd':
    {
        'action':'/api/usmc/v1/userAdd',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userName":"auto",
            "userPasswd":"qiL+2W59DQtDMSiLBj3img==",
            "userMailbox":"",
            "userSafeAddress":"",
            "userPhone":"",
            "userDetails":""
        }
    },
        
}