# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
from BasicModel.basic.restful import HttpClient
from BasicModel.hms.requestdata.requestdata import URL_DICT
from TestCaseData.basicConfig import BASIC_DATA


class HMS(HttpClient):
    '''
    classdocs
    '''
    
    hmsIp = ''
    hmsPort = ''
    baseUrl = 'http://'+hmsIp+':'+hmsPort
    
    def __init__(self, ip='172.16.2.159', port='18088'):
        '''
        Constructor
        '''
        self.hmsIp = ip
        self.hmsPort = port
        self.baseUrl = 'http://'+ip+':'+port
    
    def login_hms(self, username='root', password='hms123...'):
        header = URL_DICT['login']['header']
        url = self.baseUrl+URL_DICT['login']['action']
        data = URL_DICT['login']['body']
        params = {'username':username, 'password':password}
        data.update(params)
        response = self.post_request(url, data=header, json=data)
        return response.status_code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    
    def query_enb_info(self, serialNumber):
        header = URL_DICT['queryPageEnbByCondition']['header']
        url = self.baseUrl+URL_DICT['queryPageEnbByCondition']['action']
        body = URL_DICT['queryPageEnbByCondition']['body']
        params = {'serialNumber':serialNumber}
        body.update(params) #更新body参数
        response = self.post_request(url, json=body, headers = header)
        resCode = response.status_code 
        enbId = None
        enbName = None
        if resCode == 200:
            resInfo = response.json()
            enbId = resInfo['rows'][0]['enbId']
            enbName = resInfo['rows'][0]['enbName']
        return enbId, enbName
     
        
if __name__ == '__main__':
    hms = HMS('172.16.2.220', '18088')
#     hms.login_hms()
    resCode, resInfo = hms.query_cell_status(902230500159)
    print(resCode)
    print(resInfo)
