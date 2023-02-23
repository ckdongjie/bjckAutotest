'''
Created on 2022年10月27日

@author: dj
'''
from BasicModel.basic.restful import HttpClient


class WebLmt(HttpClient):
    '''
    classdocs
    '''

    ip = '172.16.2.153'
    port = '8090'
    baseUrl = 'http://'+ip+':'+port
    
    def __init__(self, ip='172.16.2.153', port='8090'):
        '''
        Constructor
        '''
        self.ip = ip
        self.port = port
        self.baseUrl = 'http://'+ip+':'+port
        