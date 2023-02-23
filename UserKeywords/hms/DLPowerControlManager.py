# coding = 'utf-8'
'''
Created on 2023年2月22日
@author: auto
'''


import logging

import allure

from BasicService.hms.dlPowerControlService import DLPowerControlService
from UserKeywords.basic.basic import key_get_time

'''
        说明：支持CSI-RS发射功率可配置
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    csirsPowerOffset:CSI-RS功率值
        返回：
''' 
def key_csi_rs_power_offset(hmsObj, enbId, csirsPowerOffset):
    
    with allure.step(key_get_time() +": 修改CSI-RS功率，参数:"+str(csirsPowerOffset)+'\n'):
        logging.info(key_get_time()+': modify CSI-RS power, params:'+str(csirsPowerOffset))
        modifyCsiRsPowerRes = DLPowerControlService().update_csi_rs_power_offset(hmsObj, enbId, csirsPowerOffset)
        if modifyCsiRsPowerRes == True:
            with allure.step(key_get_time() +":CSI-RS功率参数修改成功。"):
                logging.info(key_get_time()+':CSI-RS power modify success!')
        else:
            with allure.step(key_get_time() +":CSI-RS功率参数修改失败。"):
                logging.warning(key_get_time()+':CSI-RS power modify failure!')   
        assert modifyCsiRsPowerRes == True,'修改CSI-RS功率异常，请检查！'