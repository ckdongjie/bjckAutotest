# coding = 'utf-8'
'''
Created on 2022年12月22日

@author: autotest

'''


import logging

import allure

from BasicService.hms.ulPowerControlService import ULPowerControlService
from UserKeywords.basic.basic import key_get_time

'''
        说明：支持运营商配置PRACH功率初始值和功率调整步长
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    preambleInitRxTargetPwr:功率初始值
    pwrRampingStep:功率调整步长
        返回：
''' 
def key_update_init_rx_power_and_ramp_step(hmsObj, enbId, preambleInitRxTargetPwr, pwrRampingStep):
    
    with allure.step(key_get_time() +": 修改PRACH功率初始值和功率调整步长，参数:"+str(preambleInitRxTargetPwr)+','+pwrRampingStep+'\n'):
        logging.info(key_get_time()+': modify PRACH init rx power and ramp step, params:'+str(preambleInitRxTargetPwr)+','+pwrRampingStep)
        modifyPowerRes = ULPowerControlService().update_initial_received_target_power(hmsObj, enbId, preambleInitRxTargetPwr)
        modifyRampRes = ULPowerControlService().update_power_ramping_step(hmsObj, enbId, pwrRampingStep)
        if modifyPowerRes == True and modifyRampRes == True:
            with allure.step(key_get_time() +":PRACH功率初始值和功率调整步长修改成功。"):
                logging.info(key_get_time()+':PRACH init rx power and ramp step modify success!')
        else:
            with allure.step(key_get_time() +":PRACH功率初始值和功率调整步长修改失败。"):
                logging.warning(key_get_time()+':PRACH init rx power and ramp step modify failure!')   
        assert modifyPowerRes == True and modifyRampRes == True,'修改PRACH功率初始值和功率调整步长异常，请检查！'

'''
        说明：配置PUSCH P0参数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    p0NominalPusch:
    pathLossCoefficient:
        返回：
''' 
def key_update_pusch_po_params(hmsObj, enbId, p0NominalPusch, pathLossCoefficient):
    
    with allure.step(key_get_time() +": 修改PUSCH P0参数值，参数:"+str(p0NominalPusch)+','+pathLossCoefficient+'\n'):
        logging.info(key_get_time()+': modify PUSCH P0 parameters, params:'+str(p0NominalPusch)+','+pathLossCoefficient)
        modifyPoPuschRes = ULPowerControlService().update_p0_nominal_pusch(hmsObj, enbId, p0NominalPusch)
        modifyPathLossCoeffRes = ULPowerControlService().update_path_loss_coefficient(hmsObj, enbId, pathLossCoefficient)
        if modifyPoPuschRes == True and modifyPathLossCoeffRes == True:
            with allure.step(key_get_time() +":PUSCH P0参数修改成功。"):
                logging.info(key_get_time()+':PUSCH P0 parameters modify success!')
        else:
            with allure.step(key_get_time() +":PUSCH P0参数修改失败。"):
                logging.warning(key_get_time()+':PUSCH P0 parameters modify failure!')   
        assert modifyPoPuschRes == True and modifyPathLossCoeffRes == True,'修改PUSCH P0参数异常，请检查！'
        
'''
        说明：配置PUCCH P0参数
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    p0NominalPucch:
        返回：
''' 
def key_update_pucch_po_params(hmsObj, enbId, p0NominalPucch):
    
    with allure.step(key_get_time() +": 修改PUCCH P0参数值，参数:"+str(p0NominalPucch)+'\n'):
        logging.info(key_get_time()+': modify PUCCH P0 parameters, params:'+str(p0NominalPucch))
        modifyPoPucchRes = ULPowerControlService().update_p0_nominal_pucch(hmsObj, enbId, p0NominalPucch)
        if modifyPoPucchRes == True:
            with allure.step(key_get_time() +":PUCCH P0参数修改成功。"):
                logging.info(key_get_time()+':PUCCH P0 parameters modify success!')
        else:
            with allure.step(key_get_time() +":PUCCH P0参数修改失败。"):
                logging.warning(key_get_time()+':PUCCH P0 parameters modify failure!')   
        assert modifyPoPucchRes == True,'修改PUCCH P0参数异常，请检查！'