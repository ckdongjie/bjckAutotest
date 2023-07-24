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
    'queryPageUserInfos':
    {
        'action':'/api/usmc/v1/queryPageUserInfos',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "username":"root",
            "start":0,
            "limit":100
        }
    },
    'userUpdate':
    {
        'action':'/api/usmc/v1/userUpdate',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userID":"4950869e-d7fe-4f5c-9daf-e3cee40014eb",
            "userMailbox":"",
            "userName":"auto",
            "userSafeAddress":"",
            "userPhone":"18092586454",
            "userDetails":""
        }
    },   
    'passreset':
    {
        'action':'/api/usmc/v1/passreset',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "username":"auto",
            "newpassword":"48mBV6PTLkgiJ8oCKc1FYQ=="
        }
    }, 
    'extendUserAccount':
    {
        'action':'/api/usmc/v1/extendUserAccount',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userID":"4950869e-d7fe-4f5c-9daf-e3cee40014eb",
            "userExpiryDate":"2023-10-13"
        }
    }, 
    'clockUserName':
    {
        'action':'/api/usmc/v1/clockUserName',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userName":"auto"
        }
    },
    'unlockUserName':
    {
        'action':'/api/usmc/v1/unlockUserName',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userName":"auto"
        }
    },
    'exportUserInfo':
    {
        'action':'api/usmc/v1/exportUserInfo?fileName=',
        'method':'GET',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
        }
    },
    'userDelete':
    {
        'action':'/api/usmc/v1/userDelete',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "loginName":"root",
            "userID":"4950869e-d7fe-4f5c-9daf-e3cee40014eb",
            "userName":"auto"
        }
    },
    'designateUserRoleInfo':
    {
        'action':'/api/usmc/v1/designateUserRoleInfo',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userName":"user2",
            "roleIdList":"1",
            "creatName":"root"
        }
    },
    'designateUserDomainInfo':
    {
        'action':'/api/usmc/v1/designateUserDomainInfo',
        'method':'POST',
        'header':{
            'content-type': "application/json; charset=UTF-8",
            'Cookie':'lang=en-US; warningFlag=false; BAYEUX_BROWSER=as0hxfztixv81uxu; sessioncode=yd97jwdao3; username=root'
        },
        'body':{
            "userName":"user2",
            "domainIdList":"2,3,4",
            "creatName":"root"
        }
    },
}