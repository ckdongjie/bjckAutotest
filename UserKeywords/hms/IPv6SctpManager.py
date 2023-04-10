# coding = 'utf-8'
'''
Created on 2023年3月2日

@author: auto

'''


import logging
import allure
from BasicService.hms.ipv6SctpService import IPv6SctpService
from UserKeywords.basic.basic import key_get_time

'''
        功能：修改ipv6 sctp目标ip地址
'''
def key_modify_ipv6_sctp_dest_ip(hmsObj, enbId, destIp):
    
    with allure.step(key_get_time() +": 修改IPv6 sctp目标ip地址,ip:"+destIp+'\n'):
        logging.info(key_get_time()+': modify IPv6 Sctp destIP,IP:'+destIp)
        modifyRes = IPv6SctpService().update_ipv6_sctp_dest_ip(hmsObj, enbId, destIp)
        if modifyRes == True:
            with allure.step(key_get_time() +":ipv6 sctp目标ip地址修改成功。"):
                logging.info(key_get_time()+': ipv6 sctp dest ip modify success!')
        else:
            with allure.step(key_get_time() +":ipv6 sctp目标ip地址修改失败。"):
                logging.warning(key_get_time()+': ipv6 sctp dest ip modify failure!')
        assert modifyRes == True,'修改IPv6 sctp目标ip地址异常，请检查！'
        
'''
        功能：修改ipv6 sctp本地端口号
'''
def key_modify_ipv6_sctp_local_port(hmsObj, enbId, localPort):
    
    with allure.step(key_get_time() +": 修改IPv6 sctp本地端口号,端口号:"+str(localPort)+'\n'):
        logging.info(key_get_time()+': modify IPv6 Sctp Local Port,Port:'+str(localPort))
        modifyRes = IPv6SctpService().update_ipv6_sctp_local_port(hmsObj, enbId, localPort)
        if modifyRes == True:
            with allure.step(key_get_time() +":ipv6 sctp本地端口号修改成功。"):
                logging.info(key_get_time()+': ipv6 sctp local port modify success!')
        else:
            with allure.step(key_get_time() +":ipv6 sctp本地端口号修改失败。"):
                logging.warning(key_get_time()+': ipv6 sctp local port modify failure!')
        assert modifyRes == True,'修改IPv6 sctp本地端口号异常，请检查！'

'''
        功能：修改ipv6 sctp远端端口号
'''
def key_modify_ipv6_sctp_remote_port(hmsObj, enbId, remotePort):
    
    with allure.step(key_get_time() +": 修改IPv6 sctp远端端口号,端口号:"+str(remotePort)+'\n'):
        logging.info(key_get_time()+': modify IPv6 Sctp Remote Port,Port:'+str(remotePort))
        modifyRes = IPv6SctpService().update_ipv6_sctp_remote_port(hmsObj, enbId, remotePort)
        if modifyRes == True:
            with allure.step(key_get_time() +":ipv6 sctp远端端口号修改成功。"):
                logging.info(key_get_time()+': ipv6 sctp remote port modify success!')
        else:
            with allure.step(key_get_time() +":ipv6 sctp远端端口号修改失败。"):
                logging.warning(key_get_time()+': ipv6 sctp remote port modify failure!')
        assert modifyRes == True,'修改IPv6 sctp远端端口号异常，请检查！'
