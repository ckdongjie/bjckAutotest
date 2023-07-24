'''
Created on 2023年6月25日
@author: dj
'''


import logging

import allure

from BasicService.hms.domainService import DomainService
from UserKeywords.basic.basic import key_get_time

'''
        说明：用户域信息查询
        参数：
    hmsObj:hms对象
        返回：
'''
def key_query_doamin_info(hmsObj):
    with allure.step(key_get_time() +": 查询域信息\n"):
        logging.info(key_get_time()+': query domain info')
        domainList = DomainService().query_domain_info(hmsObj)
        with allure.step(key_get_time()+": 查询结果："+str(domainList)):
            logging.info(key_get_time()+": query result:"+str(domainList))
        return domainList