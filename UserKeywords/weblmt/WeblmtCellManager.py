# coding = 'utf-8'
'''
Created on 2022年10月27日

@author: dj

'''

import logging

import allure

from BasicService.weblmt.lmtCellService import LmtCellService
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.weblmt.WeblmtGnbManager import key_weblmt_login

'''
        说明：weblmt上查询小区状态
        参数：
    weblmt:weblmt对象
    cellId:小区id
'''  
def key_weblmt_query_cell_status(weblmt, cellId=0):
    with allure.step(key_get_time() +": weblmt上查询小区状态\n"):
        logging.info(key_get_time()+': query cell status from weblmt')
        cellStatus = LmtCellService().lmtQueryCellStatus(weblmt, cellId=cellId)
        if cellStatus == 0:
            with allure.step(key_get_time() +": 小区状态正常\n"):
                logging.info(key_get_time()+': cell status is available')
                return 'available'
        else:
            with allure.step(key_get_time() +": 小区状态异常\n"):
                logging.info(key_get_time()+': cell status is unavailable')
                return 'unavailable'

'''
        说明：weblmt上确认小区状态与预期状态一致
        参数：
    weblmt:weblmt对象
    cellId:小区id
    expectStatus:预期状态
    tryNum:最大尝试次数
'''         
def key_weblmt_confirm_cell_status(weblmt, cellId=0, expectStatus='available', tryNum=50):
    with allure.step(key_get_time() +": weblmt上查询小区状态是否与预期一致\n"):
        logging.info(key_get_time()+': confirm if cell status is same as expect, expect status: '+ expectStatus)
        for i in range (tryNum):
            cellStatus = key_weblmt_query_cell_status(weblmt, cellId)
            if cellStatus == expectStatus:
                break
            else:
                key_wait(5)
        if cellStatus == expectStatus:
            with allure.step(key_get_time()+':小区状态与预期一致'):
                logging.info(key_get_time()+': cell status is same as expect')
                return True
        else:
            with allure.step(key_get_time()+':小区状态与预期不一致'):
                logging.warning(key_get_time()+': cell status is not same as expect')
                return False
        
'''
        说明：weblmt上修改du小区参数-小区带宽
        参数：
    weblmt:weblmt对象
    bandwidth:小区带宽
'''         
def key_weblmt_modifiy_cell_bandwidth(weblmt, bandwidth):
    bandwithDict = {'100M':12, '80M':10, '60M':8, '40M':6, '20M':4}
    with allure.step(key_get_time() +": weblmt修改小区带宽\n"):
        logging.info(key_get_time()+': modify du cell bandwidth: '+ str(bandwidth))
        params={"UlBandwidth":bandwithDict[bandwidth],"DlBandwidth":bandwithDict[bandwidth]}
        modiryRes = LmtCellService().lmtModiryDuCellParams(weblmt, params)
        assert modiryRes == 'success','du参数修改失败，请检查！'
        logging.info(key_get_time()+': modiry du cell params success')
        
'''
        说明：weblmt上修改du小区参数-小区频点
        参数：
    weblmt:weblmt对象
    narfcn:小区频点
'''         
def key_weblmt_modifiy_cell_narfcn(weblmt, narfcn):
    with allure.step(key_get_time() +": weblmt修改小区频点\n"):
        logging.info(key_get_time()+': modify du cell narfcn: '+ str(narfcn))
        params={"DlNarfcn":narfcn,"UlNarfcn":narfcn}
        modiryRes = LmtCellService().lmtModiryDuCellParams(weblmt, params)
        assert modiryRes == 'success','du参数修改失败，请检查！'
        logging.info(key_get_time()+': modiry du cell params success')
        
'''
        说明：weblmt上修改du小区参数-小区帧结构
        参数：
    weblmt:weblmt对象
    slotAssignment:小区帧结构
'''         
def key_weblmt_modifiy_cell_slot_assignment(weblmt, slotAssignment):
    slotAssignmentDict = {'7:3':0, '4:1':1, '8:2':2, '2:3':3, '6:4':4}
    with allure.step(key_get_time() +": weblmt修改小区时隙配比\n"):
        logging.info(key_get_time()+': modify du cell slot assignment: '+ slotAssignment)
        params={"SlotAssignment":slotAssignmentDict[slotAssignment]}
        modiryRes = LmtCellService().lmtModiryDuCellParams(weblmt, params)
        assert modiryRes == 'success','du参数修改失败，请检查！'
        logging.info(key_get_time()+': modiry du cell params success')
        
if __name__ == '__main__':
    weblmt = key_weblmt_login(lmtIp='172.16.2.152')
    key_weblmt_modifiy_cell_bandwidth(weblmt, '80M')
    key_weblmt_modifiy_cell_narfcn(weblmt, 723326)
    key_weblmt_modifiy_cell_slot_assignment(weblmt, '7:3')
        
    