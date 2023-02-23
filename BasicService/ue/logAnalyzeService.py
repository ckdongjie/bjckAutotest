# coding = 'utf-8'
'''
Created on 2022年12月15日

@author: autotest
'''

from BasicModel.ue.logAnalyzeModel import LogAnalyzeModel
from BasicModel.ue.qCatModel import QCatModel


class LogAnalyzeService():
    '''
    classdocs
    '''
        
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_DCCH / RRCReconfiguration
                校验参数：duration、monitoringSymbolsWithinSlot
    '''
    def rrc_reconfiguration(self, ueLogFilePath, attrDict):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().rrc_reconfiguration(qcatApp, ueLogFilePath, attrDict)
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  BCCH_DL_SCH / SystemInformationBlockType1
                校验参数：offsetToCarrier、subcarrierSpacing、carrierBandwidth
    '''
    def system_information_block_type1_analyze(self, ueLogFilePath, attrDict):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().system_information_block_type1_analyze(qcatApp, ueLogFilePath, attrDict)
        return resultDict
        
    '''
                信令解析：0xB885  NR5G MAC DCI Info
                校验参数：
    '''
    def nr5g_mac_dci_info_analyze(self, ueLogFilePath, attrDict):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().nr5g_mac_dci_info_analyze(qcatApp, ueLogFilePath, attrDict)
        return resultDict
    
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def nr5g_mac_pdsch_status_analyze(self, ueLogFilePath):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().nr5g_mac_pdsch_status_analyze(qcatApp, ueLogFilePath)
        return resultDict
    
    
    '''
                信令解析：0xB88A  NR5G MAC RACH Attempt
                校验参数：
    '''
    def nr5g_mac_rach_attempt_analyze(self, ueLogFilePath, attrCheckDict):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().nr5g_mac_rach_attempt_analyze(qcatApp, ueLogFilePath, attrCheckDict)
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                解析参数：
            alpha
    '''
    def rrc_setup_alpha_analyze(self, ueLogFilePath, checkDict):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().rrc_setup_alpha_analyze(qcatApp, ueLogFilePath, checkDict)
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                校验参数：
    '''
    def dl_ccch_rrc_setup_analyze(self, ueLogFilePath):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().dl_ccch_rrc_setup_analyze(qcatApp, ueLogFilePath)
        return resultDict
    
    '''
                信令解析：0xB822  NR5G RRC MIB Info
                校验参数：
    '''
    def nr5g_rrc_mib_info_analyze(self, ueLogFilePath, configSsb):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().nr5g_rrc_mib_info_analyze(qcatApp, ueLogFilePath, configSsb)
        return resultDict
    
    '''
                信令解析：0xB883  NR5G MAC UL Physical Channel Schedule Report
                校验参数：
    '''
    def nr5g_mac_ul_physical_channel_schedule_analyze(self, ueLogFilePath):
        qcatApp = QCatModel().init_QCat()
        resultDict = LogAnalyzeModel().nr5g_mac_ul_physical_channel_schedule_analyze(qcatApp, ueLogFilePath)
        return resultDict
    
    '''
                信令解析： 0xB821  NR5G RRC OTA Packet  --  SIB2
                校验参数：
    '''
    def sib2_smtc_analyze(self, ueLogFilePath, smtcPeriod):
        qcatApp = QCatModel().init_QCat()
        result = LogAnalyzeModel().sib2_smtc_analyze(qcatApp, ueLogFilePath, smtcPeriod)
        return result
             
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  BCCH_DL_SCH / SystemInformationBlockType1
                校验参数：offsetToCarrier、subcarrierSpacing、carrierBandwidth
    '''
    def sib1_ssb_period_analyze(self, ueLogFilePath, ssbPeriod):
        qcatApp = QCatModel().init_QCat()
        result = LogAnalyzeModel().sib1_ssb_period_analyze(qcatApp, ueLogFilePath, ssbPeriod)
        return result 
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  BCCH_DL_SCH / SystemInformationBlockType1
                校验参数：csiRsPower
    '''
    def csi_rs_power_analyze(self, ueLogFilePath, csiRsPower):
        qcatApp = QCatModel().init_QCat()
        result = LogAnalyzeModel().cis_rs_power_analyze(qcatApp, ueLogFilePath, csiRsPower)
        return result 
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                校验参数：puschAllocType
    '''
    def pusch_res_allocation_type_analyze(self, ueLogFilePath, puschAllocType):
        qcatApp = QCatModel().init_QCat()
        result = LogAnalyzeModel().pusch_res_alloca_type_analyze(qcatApp, ueLogFilePath, puschAllocType)
        return result   
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                校验参数：puschAllocType
    '''
    def pdsch_res_allocation_type_analyze(self, ueLogFilePath, pdschAllocType):
        qcatApp = QCatModel().init_QCat()
        result = LogAnalyzeModel().pdsch_res_alloca_type_analyze(qcatApp, ueLogFilePath, pdschAllocType)
        return result