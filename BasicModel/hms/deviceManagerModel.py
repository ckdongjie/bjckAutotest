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

    #查询基站信息
    def query_device_by_serial_number(self, serialNumber):
        header = URL_DICT['queryPageEnbByCondition']['header']
        url = self.baseUrl + URL_DICT['queryPageEnbByCondition']['action']
        body = URL_DICT['queryPageEnbByCondition']['body']
        body.update({"serialNumber": serialNumber})
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            return resInfo
        else:
            return False

    #根据enbId查询Function
    def find_device_function_by_enbId(self, id):
        header = URL_DICT['findPageGNodeBFunctionByEnbId']['header']
        url = self.baseUrl + URL_DICT['findPageGNodeBFunctionByEnbId']['action'] + "?enbId=" + str(id)
        response = self.get_request(url, headers = header)
        resCode = response.status_code
        resInfo = response.json()
        if resCode == 200:
            return resInfo
        else:
            return False

    #设置自测模式
    def set_auto_test_mode(self, serialNumber, testMode):
        resInfo = self.query_device_by_serial_number(serialNumber)
        if resInfo == False:
            return resInfo
        resInfo = self.find_device_function_by_enbId(resInfo['rows'][0]['enbId'])
        if resInfo == False:
            return resInfo

        header = URL_DICT['setAutoTestMode']['header']
        url = self.baseUrl + URL_DICT['setAutoTestMode']['action']
        body = URL_DICT['setAutoTestMode']['body']
        body.update({'gNodeBFunctionId': resInfo['rows'][0]['gNodeBFunctionId'],
                     'enbId': resInfo['rows'][0]['enbId'],
                     'gNodeBFunctionInstanceId': resInfo['rows'][0]['gNodeBFunctionInstanceId'],
                     'gNBName': resInfo['rows'][0]['gNBName'],
                     'userLabel': resInfo['rows'][0]['userLabel'],
                     'gNBId': resInfo['rows'][0]['gNBId'],
                     'gNBIdLength': resInfo['rows'][0]['gNBIdLength'],
                     'selfTestSwitch': "0" if testMode==0 else "1"})
        response = self.post_request(url, json=body, headers=header)
        resCode = response.status_code
        resInfo = response.json()
        return resCode, resInfo