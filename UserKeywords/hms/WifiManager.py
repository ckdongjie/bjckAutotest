'''
Created on 2023年6月8日

@author: dj
'''
import logging
import allure
from BasicService.hms.wifiService import WifiService
from UserKeywords.basic.basic import key_get_time

'''
        设置wifi 射频开关参数值
'''
def key_set_wifi_rf_switch(hmsObj, enbId, wifiSwitch):
    if wifiSwitch == 'on':
        wifiSwitchValue = 1
    else:
        wifiSwitchValue = 0
    paraDict = {'wifiRfSwitch':wifiSwitchValue}
    with allure.step(key_get_time()+":修改wifi调频开关，参数："+str(paraDict)):
        logging.info(key_get_time()+': modify wifi cell RF switch, params:'+str(paraDict))
        updateRes = WifiService().modify_wifi_info(hmsObj, str(enbId), paraDict)
        if updateRes == '0':
            with allure.step(key_get_time()+":wifi参数修改成功\n"):
                logging.info(key_get_time()+': wifi config modify success!')
        else:
            with allure.step(key_get_time()+":wifi参数修改失败，失败信息："+str(updateRes)):
                logging.warning(key_get_time()+': wifi config modify fail, fail info:'+str(updateRes))
        assert updateRes == '0','wifi参数修改失败，请检查！'

'''
        读取wifi 射频开关参数值
'''
def key_get_wifi_rf_switch(hmsObj, enbId):
    with allure.step(key_get_time()+":查询wifi射频开关状态"):
        logging.info(key_get_time()+': query wifi rf switch')
        wifiInfo = WifiService().query_wifi_config_info(hmsObj, str(enbId))
        if wifiInfo['wifiRfSwitch'] == 1:
            with allure.step(key_get_time()+":wifi射频开关状态:On"):
                logging.info(key_get_time()+': wifi rf switch:On')
            return 'On'
        else:
            with allure.step(key_get_time()+":wifi射频开关状态:Off"):
                logging.info(key_get_time()+': wifi rf switch:Off')
            return 'Off'
    
'''
        读取wifi小区状态
'''
def key_get_wifi_cell_status(hmsObj, enbId):
    with allure.step(key_get_time()+":查询wifi小区状态"):
        logging.info(key_get_time()+': query wifi cell status')
        wifiInfo = WifiService().query_wifi_config_info(hmsObj, str(enbId))
        if wifiInfo['wifiCellStatus'] == 0:
            with allure.step(key_get_time()+":wifi小区状态:Normal"):
                logging.info(key_get_time()+': wifi cell status:Normal')
            return 'Normal'
        else:
            with allure.step(key_get_time()+":wifi小区状态:Abnormal"):
                logging.info(key_get_time()+': wifi cell status:Abnormal')
            return 'Abnormal'
    
'''
        读取wifi DFS状态
'''
def key_get_wifi_dfs_status(hmsObj, enbId):
    with allure.step(key_get_time()+":查询wifi DFS状态"):
        logging.info(key_get_time()+': query wifi dfs status')
        wifiInfo = WifiService().query_wifi_config_info(hmsObj, str(enbId))
        if wifiInfo['wifiDfsStatus'] == 0:
            with allure.step(key_get_time()+":wifi DFS状态:No DFS Detected"):
                logging.info(key_get_time()+': wifi DFS status:No DFS Detected')
            return 'No DFS Detected'
        else:
            with allure.step(key_get_time()+":wifi DFS状态:DFS Detected"):
                logging.info(key_get_time()+': wifi DFS status:DFS Detected')
            return 'DFS Detected'
        
'''
        读取wifi心跳状态
'''
def key_get_wifi_heart_status(hmsObj, enbId):
    with allure.step(key_get_time()+":查询wifi心跳状态"):
        logging.info(key_get_time()+': query wifi heartbeat status')
        wifiInfo = WifiService().query_wifi_config_info(hmsObj, str(enbId))
        if wifiInfo['wifiHBStatus'] == 0:
            with allure.step(key_get_time()+":wifi心跳状态:Heartbeat Normal"):
                logging.info(key_get_time()+': wifi heartbeat status:Heartbeat Normal')
            return 'Heartbeat Normal'
        else:
            with allure.step(key_get_time()+":wifi心跳状态:Heartbeat Abnormal"):
                logging.info(key_get_time()+': wifi heartbeat status:Heartbeat Abnormal')
            return 'Heartbeat Abnormal'