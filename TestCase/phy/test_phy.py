# coding = 'utf-8'
from distutils.core import setup
'''
Created on 2022年12月13日

@author: autotest

'''
'''
    物理层参数测试用例
'''
# @allure.feature("物理层参数测试")
# class TestPhy():

import logging
import os
import shutil

import allure
import pytest

from TestCaseData.basicConfig import BASIC_DATA
from TestCaseData.testcase import RUN_TESTCASE
from UserKeywords.basic.basic import key_get_time, key_wait
from UserKeywords.hms.CellManager import key_confirm_cell_status
from UserKeywords.hms.CsiRsManager import key_update_trs_period, \
    key_update_csi_report_quantity
from UserKeywords.hms.DLPowerControlManager import key_csi_rs_power_offset
from UserKeywords.hms.HmsManager import key_login_hms, key_get_enb_info
from UserKeywords.hms.PdcchManager import key_modify_pdcch_symbol_number, \
    key_modify_pdcch_cce_level, \
    key_modify_prach_config_index, key_modify_pdsch_dl_mcs, \
    key_modify_pdsch_ul_mcs
from UserKeywords.hms.PdschManager import key_modify_pdsch_resource_allocation_type
from UserKeywords.hms.PucchManager import key_modify_pucch_format1_rb_number, \
    key_modify_pucch_format3_rb_number
from UserKeywords.hms.PuschManager import key_modify_pusch_resource_allocation_type
from UserKeywords.hms.ULPowerControlManager import key_update_init_rx_power_and_ramp_step
from UserKeywords.pdn.pndManager import key_pdn_login
from UserKeywords.ue.CpeManager import key_cpe_login, key_cpe_attach, \
    key_start_ue_log_trace, key_stop_ue_log_trace, \
    key_pdcch_symbol_number_analyze, key_cpe_detach, key_confirm_pdu_setup_succ, \
    key_pdcch_cce_level_analyze, key_pdcch_transfer_formate_analyze, \
    key_dl_udp_nr_flow_test, key_pdsch_mcs_analyze, \
    key_prach_config_index_analyze, key_cpe_ping, \
    key_pucch_support_format_analyze, \
    key_pucch_support_format1_format3_hop_analyze, \
    key_support_dmrs_mapping_type_a, key_support_dl_dmrs_type1, \
    key_support_ul_dmrs_type1, key_ul_udp_nr_flow_test, key_support_csi_rs, \
    key_pre_rx_power_and_power_ramp_analyze, key_csi_rs_power_analyze, \
    key_pusch_resource_allocation_type_analyze, \
    key_pdsch_resource_allocation_type_analyze


@allure.story("支持每个时隙配置PDCCH符号数")
@pytest.mark.支持每个时隙配置PDCCH符号数
@pytest.mark.parametrize("symbolNumber",RUN_TESTCASE['支持每个时隙配置PDCCH符号数'] if RUN_TESTCASE.get('支持每个时隙配置PDCCH符号数') else [])
def testModifyPdcchSymbolNum(symbolNumber):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList= BASIC_DATA['gnb']['serialNumberList']
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    try:
        #修改pdcch符号数
        key_modify_pdcch_symbol_number(hmsObj, enbId, symbolNumber)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pdcch_symbol_number_analyze(ueLogFilePath, symbolNumber)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
    
@allure.story("支持PDCCH CCE聚合度配置")
@pytest.mark.支持PDCCH_CCE聚合度配置
@pytest.mark.parametrize("cceLevel",RUN_TESTCASE['支持PDCCH_CCE聚合度配置'] if RUN_TESTCASE.get('支持PDCCH_CCE聚合度配置') else [])
def testModifyPdcchCceLevel(cceLevel):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    try:
        #修改pdcch cce聚合度配置
        key_modify_pdcch_cce_level(hmsObj, enbId, cceLevel)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pdcch_cce_level_analyze(ueLogFilePath, cceLevel)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
    
@allure.story("支持PDCCH的传输格式")
@pytest.mark.支持PDCCH的传输格式
@pytest.mark.parametrize("transferFormat, cceLevel",RUN_TESTCASE['支持PDCCH的传输格式'] if RUN_TESTCASE.get('支持PDCCH的传输格式') else [])
def testConfirmPdcchSupportTransferFormate(transferFormat, cceLevel):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    try:
        with allure.step(key_get_time() +": 确认支持PDCCH的传输格式,传输格式:"+transferFormat+'\n'):
            logging.info(key_get_time()+': confirm support PDCCH transfer format,transfer format:'+transferFormat)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            transferFormateRes = key_pdcch_transfer_formate_analyze(ueLogFilePath, transferFormat)
            cceLevelRes = key_pdcch_cce_level_analyze(ueLogFilePath, cceLevel)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert transferFormateRes == True and cceLevelRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
        
@allure.story("支持PDSCH_调制解调方式配置")
@pytest.mark.支持PDSCH_调制解调方式配置
@pytest.mark.parametrize("switch, mcs",RUN_TESTCASE['支持PDSCH_调制解调方式配置'] if RUN_TESTCASE.get('支持PDSCH_调制解调方式配置') else [])
def testModifyPdschMcs(switch, mcs):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 确认支持PDSCH的调制解调方式,mcs值:"+str(mcs)+'\n'):
            logging.info(key_get_time()+': confirm support PDSCH mcs config, mcs value:'+str(mcs))
        #修改pdsch调度参数
        key_modify_pdsch_dl_mcs(hmsObj, enbId, switch, mcs)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_dl_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            mcsRes = key_pdsch_mcs_analyze(ueLogFilePath, mcs)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert mcsRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持随机接入PRACH格式")
@pytest.mark.支持随机接入PRACH格式
@pytest.mark.parametrize("configIndex",RUN_TESTCASE['支持随机接入PRACH格式'] if RUN_TESTCASE.get('支持随机接入PRACH格式') else [])
def testModifyPrachConfigurationIndex(configIndex):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 检查是否随机接入PRACH格式，配置索引:"+str(configIndex)+'\n'):
            logging.warning(key_get_time()+': confirm if support PRACH format, index value:'+str(configIndex))
        #修改prach配置索引
        key_modify_prach_config_index(hmsObj, enbId, configIndex)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            indexRes = key_prach_config_index_analyze(ueLogFilePath, configIndex)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert indexRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            

@allure.story("支持PUCCH传输格式:Format1")
@pytest.mark.支持PUCCH传输格式_Format1
@pytest.mark.parametrize("format1RbNumber",RUN_TESTCASE['支持PUCCH传输格式_Format1'] if RUN_TESTCASE.get('支持PUCCH传输格式_Format1') else [])
def testPucchSupportTransferFormat1(format1RbNumber):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 检查是否支持PUCCH传输格式Format1，RB数:"+str(format1RbNumber)+'\n'):
            logging.info(key_get_time()+': confirm if support PUCCH format1, rb number:'+str(format1RbNumber))
        #修改prach配置索引
        key_modify_pucch_format1_rb_number(hmsObj, enbId, format1RbNumber)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            indexRes = key_pucch_support_format_analyze(ueLogFilePath, 'format1')
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert indexRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持PUCCH传输格式:Format3")
@pytest.mark.支持PUCCH传输格式_Format3
@pytest.mark.parametrize("format3RbNumber",RUN_TESTCASE['支持PUCCH传输格式_Format3'] if RUN_TESTCASE.get('支持PUCCH传输格式_Format3') else [])
def testPucchSupportTransferFormat3(format3RbNumber):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 检查是否支持PUCCH传输格式Format1，RB数:"+str(format3RbNumber)+'\n'):
            logging.warning(key_get_time()+': confirm if support PUCCH format1, rb number:'+str(format3RbNumber))
        #修改prach配置索引
        key_modify_pucch_format3_rb_number(hmsObj, enbId, format3RbNumber)
#             key_modify_pucch_format1_rb_number(hmsObj, enbId, format3RbNumber)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            indexRes = key_pucch_support_format_analyze(ueLogFilePath, 'format3')
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert indexRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持PUCCH format1和format3时隙内跳频")
@pytest.mark.支持PUCCH_format1和format3时隙内跳频
def testPucchSupportFormat1HopAndFormat3Hop():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            indexRes = key_pucch_support_format1_format3_hop_analyze(ueLogFilePath)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert indexRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
    
@allure.story("支持DMRS Mapping Type A")
@pytest.mark.支持DMRS_Mapping_Type_A
def testSupportDmrsMappingTypeA():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_support_dmrs_mapping_type_a(ueLogFilePath)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)   
            
@allure.story("支持DL DMRS Type 1")
@pytest.mark.支持DL_DMRS_Type1
def testSupportDLDmrsType1():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_support_dl_dmrs_type1(ueLogFilePath)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)

@allure.story("支持UL DMRS Type 1")
@pytest.mark.支持UL_DMRS_Type1
def testSupportULDmrsType1():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    pingNrInterface = BASIC_DATA['cpe']['pingNrInterface']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    ueLogFilePath = ''
    try:
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_cpe_ping(cpe, pdnIp, cpeIp = cpeIp, username=cpeUser, password=cpePass, pingInterface = pingNrInterface)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_support_ul_dmrs_type1(ueLogFilePath)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup) 
            
@allure.story("支持PDSCH_上行调制解调方式配置")
@pytest.mark.支持PDSCH_上行调制解调方式配置
@pytest.mark.parametrize("switch, mcs",RUN_TESTCASE['支持PDSCH_上行调制解调方式配置'] if RUN_TESTCASE.get('支持PDSCH_上行调制解调方式配置') else [])
def testModifyPdschUlMcs(switch, mcs):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 确认支持PDSCH的上行调制解调方式,mcs值:"+str(mcs)+'\n'):
            logging.warning(key_get_time()+': confirm support PDSCH UL mcs config, mcs value:'+str(mcs))
        #修改pdsch调度参数
        key_modify_pdsch_ul_mcs(hmsObj, enbId, switch, mcs)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            mcsRes = key_pdsch_mcs_analyze(ueLogFilePath, mcs)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert mcsRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持单端口CS_IRS配置用于时频同步")
@pytest.mark.支持单端口CSI_RS配置用于时频同步
@pytest.mark.parametrize("trsPeriod, csiReportQuantiry",RUN_TESTCASE['支持单端口CSI_RS配置用于时频同步'] if RUN_TESTCASE.get('支持单端口CSI_RS配置用于时频同步') else [])
def testSupportCsiRsConfig(trsPeriod, csiReportQuantiry):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        with allure.step(key_get_time() +": 支持单端口CSI-RS配置用于时频同步'\n"):
            logging.warning(key_get_time()+': confirm support CSI RS config')
        #修改pdsch调度参数
        key_update_trs_period(hmsObj, enbId, trsPeriod)
        key_update_csi_report_quantity(hmsObj, enbId, csiReportQuantiry)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_support_csi_rs(ueLogFilePath, trsPeriod)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持配置PRACH功率初始值和功率调整步长")
@pytest.mark.支持配置PRACH功率初始值和功率调整步长
@pytest.mark.parametrize("preambleInitRxTargetPwr, pwrRampingStep",RUN_TESTCASE['支持配置PRACH功率初始值和功率调整步长'] if RUN_TESTCASE.get('支持配置PRACH功率初始值和功率调整步长') else [])
def testConfigPreambleInitRxTargetPwrAndPwrRampingStep(preambleInitRxTargetPwr, pwrRampingStep):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        #修改pdsch调度参数
        key_update_init_rx_power_and_ramp_step(hmsObj, enbId, preambleInitRxTargetPwr, pwrRampingStep)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pre_rx_power_and_power_ramp_analyze(ueLogFilePath, preambleInitRxTargetPwr, pwrRampingStep)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持CSI-RS发射功率可配置")
@pytest.mark.支持CSI_RS发射功率可配置
@pytest.mark.parametrize("powerOffset",RUN_TESTCASE['支持CSI_RS发射功率可配置'] if RUN_TESTCASE.get('支持CSI_RS发射功率可配置') else [])
def testConfigCSIRSPowerOffset(powerOffset):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        #修改CSI-RS发射功率参数
        key_csi_rs_power_offset(hmsObj, enbId, powerOffset)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_csi_rs_power_analyze(ueLogFilePath, powerOffset)
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert checkRes == True, '参数校验失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
            
@allure.story("支持PUSCH资源分配方式type1")
@pytest.mark.支持PUSCH资源分配方式type1
@pytest.mark.parametrize("puschAllocType",RUN_TESTCASE['支持PUSCH资源分配方式type1'] if RUN_TESTCASE.get('支持PUSCH资源分配方式type1') else [])
def testPuschResourceAllocationType(puschAllocType):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        #修改PUSCH资源分配类型参数
        key_modify_pusch_resource_allocation_type(hmsObj, enbId, puschAllocType)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pusch_resource_allocation_type_analyze(ueLogFilePath, puschAllocType)
            assert checkRes == True, '参数校验失败，请检查！'
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert setupRes == True, '终端PDU建立失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)
setup

teardown

@allure.story("支持PDSCH资源分配方式type1")
@pytest.mark.支持PDSCH资源分配方式type1
@pytest.mark.parametrize("pdschAllocType",RUN_TESTCASE['支持PDSCH资源分配方式type1'] if RUN_TESTCASE.get('支持PDSCH资源分配方式type1') else [])
def testPdschResourceAllocationType(pdschAllocType):
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
#     cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    cpe = key_cpe_login()
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        #修改PDSCH资源分配类型参数
        key_modify_pdsch_resource_allocation_type(hmsObj, enbId, pdschAllocType)
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pdsch_resource_allocation_type_analyze(ueLogFilePath, pdschAllocType)
            assert checkRes == True, '参数校验失败，请检查！'
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert setupRes == True, '终端PDU建立失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)                
    
@allure.story("支持在PUCCH信道反馈周期性宽带CQI/PMI/RI")
@pytest.mark.支持在PUCCH信道反馈周期性宽带
def testPucchChannelFeedbackPerBandwith():
    cpeIp = BASIC_DATA['cpe']['cpeSshIp']
    cpeUser = BASIC_DATA['cpe']['cpeUsername']
    cpePass = BASIC_DATA['cpe']['cpePassword']
    serialNumberList=BASIC_DATA['gnb']['serialNumberList']
    hmsObj = key_login_hms(BASIC_DATA['hms']['ip'])
    logSavePath = BASIC_DATA['cpe']['ueLogSavePath']
    ueLogBackup = BASIC_DATA['cpe']['ueLogBackup']
    pdnSshIp = BASIC_DATA['pdn']['pdnSshIp']
    pdnSshUser = BASIC_DATA['pdn']['pdnUsername']
    pdnSshPass = BASIC_DATA['pdn']['pdnPassword']
    nrPort = BASIC_DATA['flow']['nrPort']
    spanTime = BASIC_DATA['flow']['spanTime']
    cpePcIp = BASIC_DATA['flow']['cpePcIp']
    iperfPath = BASIC_DATA['flow']['iperfLocalPath']
    pdnIp = BASIC_DATA['pdn']['pdnIp']
    enbDebugIp = BASIC_DATA['weblmt']['ip']
    pcIp = BASIC_DATA['flow']['localPcIp']
    enbId, enbName = key_get_enb_info(hmsObj, serialNumberList)
    cpe = key_cpe_login(cpeIp,cpeUser,cpePass)
    pdn = key_pdn_login(pdnSshIp,pdnSshUser,pdnSshPass)
    ueLogFilePath = ''
    try:
        #确认小区状态正常
        key_confirm_cell_status(hmsObj, enbId, 'available')
        dev_manager, qxdm_window, diagService = key_start_ue_log_trace()
        #cpe接入小区，确认pdu建立成功
        key_cpe_attach(cpe)
        setupRes = key_confirm_pdu_setup_succ(cpe)
        if setupRes == 'success':
            key_wait(10)
            key_ul_udp_nr_flow_test(cpe, pdn, cpePcIp, iperfPath, pdnIp, enbDebugIp, pcIp, monitorPort=nrPort, spanTime=spanTime)
            ueLogFilePath = key_stop_ue_log_trace(dev_manager, qxdm_window, diagService, logSavePath)
            checkRes = key_pdsch_resource_allocation_type_analyze(ueLogFilePath, pdschAllocType)
            assert checkRes == True, '参数校验失败，请检查！'
        else:
            logging.info(key_get_time()+': ue attach failure, please check!')
        assert setupRes == True, '终端PDU建立失败，请检查！'
    finally:
        #cpe去接入小区
        key_cpe_detach(cpe)
        logging.info(key_get_time()+': move the log file to backup folder')
        fileName = ueLogFilePath.split('\\')[-1]
        if os.path.exists(ueLogBackup+'\\'+fileName):
            os.remove(ueLogFilePath)
        else:
            shutil.move(ueLogFilePath, ueLogBackup)     