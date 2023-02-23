# coding = 'utf-8'
'''
Created on 2023年2月22日

@author: auto
'''
import logging
import allure
from BasicService.hms.pdschService import PdschService
from UserKeywords.basic.basic import key_get_time

'''
        说明：修改PUSCH资源分配类型
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    puschAllocType:pusch资源分配类型
        返回：
'''
def key_modify_pdsch_resource_allocation_type(hmsObj, enbId, pdschAllocType):
    with allure.step(key_get_time() +": 修改PDSCH资源分配类型，类型:"+pdschAllocType+'\n'):
        logging.info(key_get_time()+': modify PDSCH resource allocation type, type:'+pdschAllocType)
        modifyRes = PdschService().update_pdsch_resource_allocation_type(hmsObj, enbId, pdschAllocType)
        if modifyRes == True:
            with allure.step(key_get_time() +":PDSCH资源分配类型修改成功。"):
                logging.info(key_get_time()+': PDSCH resource allocation type modify success!')
        else:
            with allure.step(key_get_time() +":PDSCH资源分配类型修改失败。"):
                logging.warning(key_get_time()+': PDCCH resource allocation type modify failure!')
        assert modifyRes == True,'修改PDSCH资源分配类型异常，请检查！'