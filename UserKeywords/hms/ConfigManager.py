# coding = 'utf-8'
'''
Created on 2022年10月20日
@author: dj

'''



import logging
import allure

from BasicService.hms.configService import configService
from UserKeywords.basic.basic import key_get_time

'''
        修改网管OMC IP地址
        参数：
    serialNumber:基站序列号
    omcIp:OMC IP地址
        返回：
    modifyRes:修改结果
'''
def key_modify_omc_url(hmsObj, enbId, omcIp):
    with allure.step(key_get_time()+": 修改网管建链地址\n"):
        logging.info(key_get_time()+': modify omc ip, ip:'+omcIp)
        resCode,resInfo = configService().modify_omc_url_ip(hmsObj, enbId, omcIp)
        if resCode == 200 and resInfo['result']=='0':
            with allure.step(key_get_time()+": 网管建链地址修改成功\n"):
                logging.info(key_get_time()+': modify success!')
                return 'success'
        else:
            with allure.step(key_get_time()+": 网管建链地址修改失败，失败信息："+str(resInfo)):
                logging.warning(key_get_time()+': modify fail, fail info:'+str(resInfo))
                return 'fail'
