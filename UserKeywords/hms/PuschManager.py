# coding = 'utf-8'
'''
Created on 2023年2月22日
@author: auto
'''
import allure
from UserKeywords.basic.basic import key_get_time
import logging
from BasicService.hms.puschService import PuschService

'''
        说明：修改PUSCH资源分配类型
        参数：
    hmsObj:hms对象
    enbId:基站enbId
    puschAllocType:pusch资源分配类型
        返回：
'''
def key_modify_pusch_resource_allocation_type(hmsObj, enbId, puschAllocType):
    with allure.step(key_get_time() +": 修改PUSCH资源分配类型，类型:"+puschAllocType+'\n'):
        logging.info(key_get_time()+': modify PUSCH resource allocation type, type:'+puschAllocType)
        modifyRes = PuschService().update_pusch_resource_allocation_type(hmsObj, enbId, puschAllocType)
        if modifyRes == True:
            with allure.step(key_get_time() +":PUSCH资源分配类型修改成功。"):
                logging.info(key_get_time()+': PUSCH resource allocation type modify success!')
        else:
            with allure.step(key_get_time() +":PUSCH资源分配类型修改失败。"):
                logging.warning(key_get_time()+': PUCCH resource allocation type modify failure!')
        assert modifyRes == True,'修改PUSCH资源分配类型异常，请检查！'