'''
Created on 2022年10月17日

@author: dj
'''
from BasicModel.hms.hms import HMS
from TestCaseData.basicConfig import BASIC_DATA


class hmsService():
    
    hms = None
    '''
    classdocs
    '''
    def __init__(self, ip='172.16.2.159', port='18088'):
        '''
        Constructor
        '''
        self.hms = HMS(ip, port)
        
        
    '''
                说明：登录hms
                参数：
        username:用户名
        password:密码
    '''    
    def login_hms(self, username='root', password='hms123...'):
        loginRes = self.hms.login_hms(username, password)
        if loginRes == 200:
            return self.hms
    
    '''
                说明：查询基站信息
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
    '''
    def query_enb_info(self, hmsObj, serialNumber):
        if hmsObj:
            enbId, enbName = hmsObj.query_enb_info(serialNumber)
        else:
            enbId, enbName = self.hms.query_enb_info(serialNumber)
        return enbId, enbName