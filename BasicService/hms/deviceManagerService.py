# coding = 'utf-8'
'''
Created on 2022年10月20日

@author: dj

'''

import logging
from time import sleep

from BasicModel.hms.deviceManagerModel import DeviceManagerModel
from UserKeywords.basic.basic import key_get_time


class deviceManagerService():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''   
    '''
                说明：确认基站状态为online
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
        tryNum:最大尝试次数
    '''    
    def query_device_online(self, hmsObj, serialNumber, tryNum=200): 
        enbStatus = 'offline'
        for i in range (tryNum):
            isOnline = DeviceManagerModel(hmsObj).query_device_online_status(serialNumber)
            if isOnline == 0:
                logging.info(key_get_time()+': device is online!')
                enbStatus = 'online'
                break
            else:
                logging.warning(key_get_time()+': device is offline, wait 5s try again!')
                sleep(5) 
        return enbStatus 
    
    '''
                说明：确认基站状态与预期一致
                参数：
        hmsObj:hms对象
        serialNumber:基站sn号
        expectStatus:预期状态
        tryNum:最大尝试次数
    '''
    def query_device_status_same_as_expect(self, hmsObj, serialNumber, expectStatus='online', tryNum=20): 
        if expectStatus == 'online':
            status = 0
        else:
            status = 1
        for i in range (tryNum):
            isOnline = DeviceManagerModel(hmsObj).query_device_online_status(serialNumber)
            if isOnline != status:
                logging.warning(key_get_time()+': device status is not same as expect, wait 5s try again!')
                sleep(5) 
        if isOnline == status:
            return True
        else:
            return False 
