# coding = 'utf-8'
'''
Created on 2022年10月20日

@author: dj
'''

from BasicModel.hms.configModel import ConfigModel


class configService():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
    def is_ipv6(self, ip):
        if ':' in ip:
            return True
        else:
            return False    
    
    '''
                说明：修改omc ip地址
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        omcIp:目标omcIp地址
    '''    
    def modify_omc_url_ip(self, hmsObj, enbId, omcIp): 
        isIpv6 = self.is_ipv6(omcIp)
        if isIpv6:
            paraDict = {'url':"http://["+omcIp+"]:18088/acs"}  
        else:
            paraDict = {'url':"http://"+omcIp+":18088/acs"}
        resCode,resInfo = ConfigModel(hmsObj).update_Mg_Server(enbId, paraDict)  
        return resCode,resInfo
    
    '''
                说明：修改时钟源
                参数：
        hmsObj:hms对象
        clockType:时钟源类型
    '''
    def modify_clock_source(self, hmsObj, enbId, clockType):
        ConfigModel(hmsObj).realtime_query_clock_info(str(enbId))
        clockTypeDict = {'GPS':'1', 'LOCAL_CLOCK':'1073741824'}
        resCode,resInfo = ConfigModel(hmsObj).update_clock_params(str(enbId), {'clockSrc':clockTypeDict[clockType]})
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False