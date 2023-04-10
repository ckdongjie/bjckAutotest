# coding = utf-8 
'''
Created on 2022年9月6日

@author: dj
'''
import logging
from time import sleep

import allure

from BasicService.hms.cuService import CuService
from BasicService.hms.duService import DuService
from UserKeywords.basic.basic import key_get_time, key_wait

'''
        说明：查询小区状态
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
    status:小区状态
'''
def key_query_cell_status(hmsObj, enbId, cellId=1, tryNum = 5):
    with allure.step(key_get_time() +": 查询小区状态\n"):
        logging.info(key_get_time()+': query cell status')
        for i in range (1,tryNum):
            resCode, resInfo = CuService().real_query_cu_cell_status(hmsObj, enbId, cellId)
            if resInfo['cuCellStatusOperateResults'][0]['configOperateResult']['success'] == True:
                break
            else:
                sleep(5)
        if resInfo['cuCellStatusOperateResults'][0]['configOperateResult']['success'] == True:
            if resCode == 200 and resInfo['cuCellStatusOperateResults'][0]['configOperateResult']['resultObject']['cellAvailableState'] == 0:
                with allure.step(key_get_time() +": 小区状态:available\n"):
                    logging.info(key_get_time()+': cell_'+str(cellId)+' status:available')
                    return 'available'
            else:
                with allure.step(key_get_time() +": 小区状态:unavailable\n"):
                    logging.warning(key_get_time()+': cell_'+str(cellId)+' status:unavailable')
                    return 'unavailable'
        else:
            with allure.step(key_get_time() +": 小区状态:unavailable, Failure Info:"+str(resInfo)):
                logging.warning(key_get_time()+': cell_'+str(cellId)+' status:unavailable, query info:'+str(resInfo))
            return 'unavailable'  

'''
        说明：确认小区状态与预期状态一致
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    expectStatus:预期状态
    tryNum:最大尝试次数
        返回：
'''    
def key_confirm_cell_status(hmsObj, enbId, expectStatus='available', cellId=1, tryNum=100):
    with allure.step(key_get_time() +": 确认小区状态与预期一致,预期状态:"+expectStatus+'\n'):
        logging.info(key_get_time()+': confirm if cell status is same as expect status,expect status:'+expectStatus)
        for i in range (tryNum):
            cellStatus = key_query_cell_status(hmsObj, enbId, cellId)
            if cellStatus == expectStatus:
                break
            key_wait(5)
        with allure.step(key_get_time() +": 小区状态-"+cellStatus+',小区预期状态-'+expectStatus+'\n'):
            logging.info(key_get_time()+': cell status:'+cellStatus+', expect status:'+expectStatus)
            assert cellStatus == expectStatus,'小区状态与预期状态不符，请检查！'   

'''
        说明：闭塞小区状态
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
'''
def key_block_cell(hmsObj, enbId):
    with allure.step(key_get_time() +": 执行小区状态闭塞操作\n"):
        logging.info(key_get_time()+': block du cell')
        params = {'cellAdminState':1}
        result = DuService().update_du_cell_para(hmsObj, enbId, params)
        assert result == True, '小区闭塞操作执行失败，请检查！'
        with allure.step(key_get_time() +": 小区状态闭塞成功\n"):
            logging.info(key_get_time()+': block du cell success!')
     
'''
        说明：解闭塞小区状态
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
'''   
def key_unblock_cell(hmsObj, enbId):
    with allure.step(key_get_time() +": 执行小区状态解闭塞操作\n"):
        logging.info(key_get_time()+': unblock du cell')
        params = {'cellAdminState':0}
        result = DuService().update_du_cell_para(hmsObj, enbId, params)
        assert result == True, '小区解闭塞操作执行失败，请检查！'
        with allure.step(key_get_time() +": 小区状态解闭塞成功\n"):
            logging.info(key_get_time()+': unblock du cell success!')

'''
        说明：激活小区状态
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
'''
def key_active_cell(hmsObj, enbId):
    with allure.step(key_get_time() +": 执行小区状态激活操作\n"):
        logging.info(key_get_time()+': active cu cell')
        params = {'cellActiveState':1}
        result = CuService().update_cu_cell_para(hmsObj, enbId, params)
        assert result == True, '小区激活操作执行失败，请检查！'
        with allure.step(key_get_time() +": 小区状态激活成功\n"):
            logging.info(key_get_time()+': active cu cell success!')
 
'''
        说明：去激活小区状态
        参数：
    hmsObj:hms对象
    enbId:基站enbId
        返回：
'''        
def key_deactive_cell(hmsObj, enbId):
    with allure.step(key_get_time() +": 执行小区状态去激活操作\n"):
        logging.info(key_get_time()+': deactive cu cell')
        params = {'cellActiveState':0}
        result = CuService().update_cu_cell_para(hmsObj, enbId, params)
        assert result == True, '小区去激活操作执行失败，请检查！'
        with allure.step(key_get_time() +": 小区状态去激活成功\n"):
            logging.info(key_get_time()+': deactive cu cell success!')
        