#coding = 'utf-8'
'''
Created on 2023年2月7日

@author: autotest

'''


import logging
import allure
from BasicService.attenuator.attenuatorService import AttenuatorService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
    说明：连接程控衰减
    参数：
    serialPort:程控衰减虚拟串口号
    serialRate:程控衰减串口速率
'''
def key_connect_attenuator(serialPort=BASIC_DATA['attenuator']['serialPort'], serialRate=BASIC_DATA['attenuator']['serialRate']):
    with allure.step(key_get_time() +":串口连接可调衰减:"+serialPort+','+str(serialRate)):
        logging.info(key_get_time()+':connect attenuator by serial:'+serialPort+','+str(serialRate))
        attenuator = AttenuatorService().connect_attenuator(serialPort, serialRate)
        return attenuator
    
'''
    说明：断开程控衰减连接
    参数：
    attenuator:程控衰减对象
'''
def key_disconnect_attenuator(attenuator):
    with allure.step(key_get_time() +":串口断开可调衰减连接"):
        logging.info(key_get_time()+':disconnect attenuator')
        AttenuatorService().disconnect_attenuator(attenuator)
    
'''
    说明：读取单通道衰减值
    参数：
    attenuator:程控衰减对象
    channel:通道号
'''
def key_read_signal_channel(attenuator, channel):
    with allure.step(key_get_time() +":读取可调衰减单通道值:"+str(channel)):
        logging.info(key_get_time()+':read signal channel value:'+str(channel))
        chaVal = AttenuatorService().read_single_channel_value(attenuator, channel)
        logging.info(key_get_time()+': attenuator signal channel value:'+chaVal)
        
'''
    说明：设置单通道衰减值
    参数：
    attenuator:程控衰减对象
    channel:通道号
    value:衰减值
'''
def key_send_signal_channel(attenuator, channel, value):
    with allure.step(key_get_time() +":设置可调衰减单通道值:"+str(channel)+'-'+str(value)):
        logging.info(key_get_time()+':set signal channel value:'+str(channel)+'-'+str(value))
        setVal = AttenuatorService().send_single_channel_value(attenuator, channel, value)
        logging.info(key_get_time()+': set result:'+setVal)

'''
    说明：读取单通道衰减值
    参数：
    attenuator:程控衰减对象
    channel:通道号
'''
def key_read_multi_channel(attenuator, channelStr):
    with allure.step(key_get_time() +":读取可调衰减多通道值:"+channelStr):
        logging.info(key_get_time()+':read multi channel value:'+channelStr)
        chaVal = AttenuatorService().read_multi_channel_value(attenuator, channelStr)
        logging.info(key_get_time()+': attenuator multi channel value:'+chaVal)
        
'''
    说明：设置单通道衰减值
    参数：
    attenuator:程控衰减对象
    channel:通道号
    value:衰减值
'''
def key_send_multi_channel(attenuator, channelStr, value):
    with allure.step(key_get_time() +":设置可调衰减单通道值:"+channelStr+'-'+value):
        logging.info(key_get_time()+':set signal channel value:'+channelStr+'-'+value)
        setVal = AttenuatorService().send_multi_channel_value(attenuator, channelStr, value)
        logging.info(key_get_time()+': set result:'+setVal)