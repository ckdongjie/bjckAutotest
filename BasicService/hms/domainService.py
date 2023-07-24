'''
Created on 2023年6月25日
@author: dj
'''
from BasicModel.hms.domainModel import DomainModel


class DomainService(object):
    
    def __init__(self):

        '''
        Constructor
        '''
        
    '''
                说明：查询域信息
                参数：
        hmsObj:hms对象
    '''    
    def query_domain_info(self, hmsObj):
        resCode, resInfo = DomainModel(hmsObj).query_domain_info()
        return resInfo['rows']
        