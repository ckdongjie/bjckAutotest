# coding = 'utf-8'
'''
Created on 2022年10月20日
@author: dj
'''

from BasicModel.hms.hms import HMS
from BasicModel.hms.requestdata.deviceManagerData import URL_DICT


class DeviceManagerModel(HMS):
    '''
    classdocs
    '''

    def __init__(self, hms=None):
        '''
        Constructor
        '''
        if hms:
            self.baseUrl = hms.baseUrl
        
    def query_device_online_status(self, serialNumber):
        header = URL_DICT['queryPageEnbByCondition']['header']
        url = self.baseUrl+URL_DICT['queryPageEnbByCondition']['action']
        body = URL_DICT['queryPageEnbByCondition']['body']
        body.update({"serialNumber":serialNumber})
        response = self.post_request(url, json = body, headers = header)
        resCode = response.status_code 
        enbStatus = 1
        if resCode == 200:
            resInfo = response.json()
            enbStatus = resInfo['rows'][0]['enbStatus']
        return enbStatus
        
    