# coding = 'utf-8'
'''
Created on 2022年12月2日

@author: dj


'''

import logging

from BasicModel.ue.qCatModel import QCatModel


class LogAnalyzeModel():
    '''
    classdocs
    '''
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_DCCH / RRCReconfiguration
                校验参数：duration、monitoringSymbolsWithinSlot
    '''
    def rrc_reconfiguration(self, qcatApp, ueLogFilePath, attrDict):
        logId =  0xB821
        subTitle = 'DL_DCCH / RRCReconfiguration'
        paraDict = {'subTitle':subTitle}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        resultDict = {}
        if 'duration' in attrDict:
            isFind1 = False
        else:
            isFind1 = True
        if 'monitoringSymbolsWithinSlot' in attrDict:
            isFind2 = False
        else:
            isFind2 = True
        if 'searchSpaceTypeUeSpecific' in attrDict:
            isFind3 = False
        else:
            isFind3  = True
        if 'resourceAllocation' in attrDict and 'rbg-Size' in attrDict and 'mcs-Table' in attrDict:
            isFind4 = False
        else:
            isFind4 = True
        if 'trsPeriod' in attrDict:
            isFind5 = False
        else:
            isFind5 = True
        isCheck = False
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'controlResourceSetToAddModList' in contextStr and isFind1 == False:
                    duration = contextList[num+5].split('duration ')[1][:-1]
                    isFind1 = True
                if 'searchSpacesToAddModList' in contextStr and isFind2 == False:
                    monitoringSymbolsWithinSlot = contextList[num+6].split('monitoringSymbolsWithinSlot ')[1][:-1]
                    isFind2 = True
                if 'searchSpaceType ue-Specific' in contextStr and isFind3 == False:
                    searchSpaceTypeUeSpecific = contextList[num+2].split('dci-Formats ')[1]
                    isFind3 = True
                if 'pdsch-Config setup' in contextStr and isFind4 == False:
                    resourceAllocation = contextList[num+2].split('resourceAllocation ')[1][:-1]
                    rbgSize = contextList[num+3].split('rbg-Size ')[1][:-1]
                    mcsTable = contextList[num+4].split('mcs-Table ')[1][:-1]
                    isFind4 = True
                if 'csi-MeasConfig setup' in contextStr:
                    trsPeriod = contextList[num+22].split('periodicityAndOffset ')[1].split(' :')[0]
                    isFind5 = True
            if isFind1 and isFind2 and isFind3 and isFind4 and isFind5:
                isCheck = True
                break
        if isCheck:
            for attrName in attrDict.keys():
                if attrName == 'duration':
                    resultDict['duration'] = True
                    if attrDict['duration'] != duration:
                        resultDict['duration'] = False
                if attrName == 'monitoringSymbolsWithinSlot':
                    resultDict['monitoringSymbolsWithinSlot'] = True
                    if attrDict['monitoringSymbolsWithinSlot'] != monitoringSymbolsWithinSlot:
                        resultDict['monitoringSymbolsWithinSlot'] = False
                if attrName == 'searchSpaceTypeUeSpecific':
                    resultDict['searchSpaceTypeUeSpecific'] = True
                    if attrDict['searchSpaceTypeUeSpecific'] != searchSpaceTypeUeSpecific:
                        resultDict['searchSpaceTypeUeSpecific'] = False
                if attrName == 'resourceAllocation':
                    resultDict['resourceAllocation'] = True
                    if attrDict['resourceAllocation'] != resourceAllocation:
                        resultDict['resourceAllocation'] = False
                if attrName == 'rbg-Size':
                    resultDict['rbg-Size'] = True
                    if attrDict['rbg-Size'] != rbgSize:
                        resultDict['rbg-Size'] = False
                if attrName == 'mcs-Table':
                    resultDict['mcs-Table'] = True
                    if attrDict['mcs-Table'] != mcsTable:
                        resultDict['mcs-Table'] = False
                if attrName == 'trsPeriod':
                    resultDict['trsPeriod'] = True
                    if attrDict['trsPeriod'] != trsPeriod:
                        resultDict['trsPeriod'] = False
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  BCCH_DL_SCH / SystemInformationBlockType1
                校验参数：offsetToCarrier、subcarrierSpacing、carrierBandwidth
    '''
    def system_information_block_type1_analyze(self, qcatApp, ueLogFilePath, attrDict):
        logId =  0xB821
        subTitle = 'BCCH_DL_SCH / SystemInformationBlockType1'
        paraDict = {'subTitle':subTitle}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        resultDict = {}
        if 'offsetToCarrier' in attrDict and 'subcarrierSpacing' in attrDict and 'nrofDownlinkSlots' in attrDict:
            isFind1 = False
        else:
            isFind1 = True
        if 'nrofDownlinkSlots' in attrDict and 'nrofDownlinkSymbols' in attrDict and 'nrofUplinkSlots' in attrDict and 'nrofUplinkSymbols' in attrDict:
            isFind2 = False
        else:
            isFind2 = True
        if 'dciFormate' in attrDict:
            isFind3 = False
        else:
            isFind3  = True
        if 'preambleReceivedTargetPower' in attrDict and 'powerRampingStep' in attrDict:
            isFind4 = False
        else:
            isFind4 = True
        if 'p0NominalPusch' in attrDict:
            isFind5 = False
        else:
            isFind5 = True
        isCheck = False
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'scs-SpecificCarrierList' in contextStr and isFind1 == False:
                    offsetToCarrier = contextList[num+3].split(' ')[-1][:-1]
                    subcarrierSpacing = contextList[num+4].split(' ')[-1][:-1]
                    carrierBandwidth = contextList[num+5].split(' ')[-1][:-1]
                    isFind1 = True
                if 'tdd-UL-DL-ConfigurationCommon' in contextStr and isFind2 == False:
                    nrofDownlinkSlots = contextList[num+6].split(' ')[-1][:-1]
                    nrofDownlinkSymbols = contextList[num+7].split(' ')[-1][:-1]
                    nrofUplinkSlots = contextList[num+8].split(' ')[-1][:-1]
                    nrofUplinkSymbols = contextList[num+9].split(' ')[-1]
                    isFind2 = True
                if 'searchSpaceType common' in contextStr and isFind3 == False:
                    dciFormate = contextList[num+2].split(' ')[-2]
                    isFind3 = True
                if 'rach-ConfigCommon setup' in contextStr and isFind4 == False:
                    preambleReceivedTargetPower = contextList[num+8].split('preambleReceivedTargetPower ')[1][:-1]
                    powerRampingStep = contextList[num+10].split('powerRampingStep ')[1][:-1]
                    isFind4 = True
                if 'p0-NominalWithGrant' in contextStr and isFind5 == False:
                    p0NominalPusch = contextList[num].split('p0-NominalWithGrant ')[1]
                    isFind5 = True
            if isFind1 and isFind2 and isFind3 and isFind4 and isFind5:
                isCheck = True
                break
        if isCheck:
            for attrName in attrDict.keys():
                if attrName == 'offsetToCarrier':
                    resultDict['offsetToCarrier'] = True
                    if attrDict['offsetToCarrier'] != offsetToCarrier:
                        resultDict['offsetToCarrier'] = False
                if attrName == 'subcarrierSpacing':
                    resultDict['subcarrierSpacing'] = True
                    if attrDict['subcarrierSpacing'] != subcarrierSpacing:
                        resultDict['subcarrierSpacing'] = False
                if attrName == 'carrierBandwidth':
                    resultDict['carrierBandwidth'] = True
                    if attrDict['carrierBandwidth'] != carrierBandwidth:
                        resultDict['carrierBandwidth'] = False
                if attrName == 'nrofDownlinkSlots':
                    resultDict['nrofDownlinkSlots'] = True
                    if attrDict['nrofDownlinkSlots'] != nrofDownlinkSlots:
                        resultDict['nrofDownlinkSlots'] = False
                if attrName == 'nrofDownlinkSymbols':
                    resultDict['nrofDownlinkSymbols'] = True
                    if attrDict['nrofDownlinkSymbols'] != nrofDownlinkSymbols:
                        resultDict['nrofDownlinkSymbols'] = False
                if attrName == 'nrofUplinkSlots':
                    resultDict['nrofUplinkSlots'] = True
                    if attrDict['nrofUplinkSlots'] != nrofUplinkSlots:
                        resultDict['nrofUplinkSlots'] = False
                if attrName == 'nrofUplinkSymbols':
                    resultDict['nrofUplinkSymbols'] = True
                    if attrDict['nrofUplinkSymbols'] != nrofUplinkSymbols:
                        resultDict['nrofUplinkSymbols'] = False
                if attrName == 'dciFormate':
                    resultDict['dciFormate'] = True
                    if attrDict['dciFormate'] != dciFormate:
                        resultDict['dciFormate'] = False
                if attrName == 'preambleReceivedTargetPower':
                    resultDict['preambleReceivedTargetPower'] = True
                    if str(attrDict['preambleReceivedTargetPower']*2) != preambleReceivedTargetPower:
                        resultDict['preambleReceivedTargetPower'] = False
                if attrName == 'powerRampingStep':
                    resultDict['powerRampingStep'] = True
                    if attrDict['powerRampingStep'] != powerRampingStep:
                        resultDict['powerRampingStep'] = False
                if attrName == 'p0NominalPusch':
                    resultDict['p0NominalPusch'] = True
                    if str(attrDict['p0NominalPusch']*2) != p0NominalPusch:
                        resultDict['p0NominalPusch'] = True
        return resultDict
        
    '''
                信令解析：0xB885  NR5G MAC DCI Info
                校验参数：
    '''
    def nr5g_mac_dci_info_analyze(self, qcatApp, ueLogFilePath, attrDict):
        logId =  0xB885
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId)
        resultDict = {}
        isFind1 = False
        resultDict['dciFormat'] = False
        resultDict['aggregationLevel'] = False
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            attrNameStrList = []
            attrValueStrList = []
            DciFormat = ''
            AggregationLevel = ''
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if '|#  |' in contextStr:
                    attrNameStrList = contextStr.split('|')
                    attrValueStrList = contextList[num+2].split('|')
                for num in range (len(attrNameStrList)):
                    attrName = attrNameStrList[num]
                    if 'DCI Format' in attrName:
                        DciFormat = attrValueStrList[num]
                        if DciFormat != '':
                            DciFormat = DciFormat.split(' ')[-1]
                    if  'Level' in attrName:
                        AggregationLevel = attrValueStrList[num]
                        if AggregationLevel != '':
                            AggregationLevel = AggregationLevel.split(' ')[-1]
                    if DciFormat != '' and AggregationLevel != '':
                        if DciFormat == attrDict['dciFormat'] and AggregationLevel == attrDict['aggregationLevel']:
                            resultDict['dciFormat'] = True
                            resultDict['aggregationLevel'] = True
                            isFind1 = True
                            break
                if isFind1:
                    break
            if isFind1:
                break        
        
        return resultDict
    
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def nr5g_mac_pdsch_status_analyze(self, qcatApp, ueLogFilePath):
        logId =  0xB887
        filterContext = 'DL_DCCH / RRCReconfiguration'
        paraDict = {'filterContext':filterContext}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        resultDict = {'MCS-Mod Type':False}
        checkList = []
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if '|#  |' in contextStr:
                    checkValuesList = self.searchAllValues(contextList, num, len(contextList))
                    checkList.append(checkValuesList)
                    break
        checkRes = self.checkMcsAndModType(checkList)
        resultDict['MCS-Mod Type'] = checkRes
        return resultDict
    
    def searchAllValues(self, contextList, begin, listLength):
        attrNameStrList = contextList[begin].split('|')
        checkList = []
        index = begin + 2
        while index < listLength:
            attrValueStrList = contextList[index].split('|')
            for num in range (len(attrNameStrList)):
                attrName = attrNameStrList[num]
                if 'MCS' in attrName:
                    MCS = attrValueStrList[num]
                    if MCS != '':
                        MCS = MCS.split(' ')[-1]
                if  'Mod Type' in attrName:
                    ModType = attrValueStrList[num]
                    if ModType != '':
                        ModType = ModType.split(' ')[-1]
                if MCS != '' and ModType != '':
                    checkList.append(MCS+';'+ModType+';'+contextList[0])
            index = index + 1
        return checkList
    
    def checkMcsAndModType(self, Mcs_ModType_List):
        checkRes = True
        for subStr in Mcs_ModType_List:
            mcs = int(subStr.split(';')[0])
            modType = subStr.split(';')[1]
            logTime = subStr.split(';')[2]
            if 0<= mcs and mcs <=4:
                if modType != 'QPSK':
                    checkRes = False
                    break
            elif 5<= mcs and mcs <=10:
                if modType != '16_QAM':
                    checkRes = False
                    break
            elif 11<= mcs and mcs <=19:
                if modType != '64_QAM':
                    checkRes = False
                    break
            elif 20<= mcs and mcs <=27:
                if modType != '256_QAM':
                    checkRes = False
                    break
        if checkRes == False:
            logging.warning('MCS:'+str(mcs)+'; Mod Type:'+modType+'; Error Time:'+logTime)
        return checkRes
       
    '''
                信令解析：0xB88A  NR5G MAC RACH Attempt
                校验参数：
    '''
    def nr5g_mac_rach_attempt_analyze(self, qcatApp, ueLogFilePath, attrCheckDict):
        logId =  0xB88A
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId)
        resultDict = {'prachConfig':True, 'preambleFormat':True}
        checkList = []
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            checkDict = {}
            prachConfig = ''
            preambleFormat = ''
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if '|#  |' in contextStr:
                    attrNameStrList = contextStr.split('|')
                    attrValueStrList = contextList[num+2].split('|')
                    for i in range (len(attrNameStrList)):
                        attrName =  attrNameStrList[i]
                        if 'Config' in attrName:
                            prachConfig = attrValueStrList[i].split(' ')[-1]
                        if 'Format' in attrName:
                            preambleFormat = attrValueStrList[i].split(' ')[-1]
                        if prachConfig != '' and preambleFormat != '':
                            checkDict.update({'prachConfig':prachConfig})
                            checkDict.update({'preambleFormat':preambleFormat})
                            break
                if checkDict != {}:
                    checkList.append(checkDict)
                    break
        for checkDir in checkList:
            if checkDir['prachConfig'] != attrCheckDict['prachConfig']:
                resultDict['prachConfig'] = False
            if checkDir['preambleFormat'] != attrCheckDict['preambleFormat']:
                resultDict['preambleFormat'] = False
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                解析参数：
            alpha
    '''
    def rrc_setup_alpha_analyze(self, qcatApp, ueLogFilePath, checkDict):
        logId =  0xB821
        subTitle = 'DL_CCCH / RRC Setup'
        paraDict = {'subTitle':subTitle}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        resultDict = {'alpha':True}
        resultList = []
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'p0-AlphaSets' in contextStr:
                    alpha = contextList[num+5].split('alpha ')[1]
                    resultList.append(alpha)
                    break
        for resultStr in resultList:
            if resultStr != checkDict['alpha']:
                resultDict['alpha'] = False
                break
        return resultDict
    
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  DL_CCCH / RRC Setup
                校验参数：
    '''
    def dl_ccch_rrc_setup_analyze(self, qcatApp, ueLogFilePath):
        logId =  0xB821
        subTitle = 'DL_CCCH / RRC Setup'
        paraDict = {'subTitle':subTitle}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        resultDict = {'format1':True, 'format3':True, 'dmrs dl type':False, 'dmrs ul type':False, 'dmrs dl type1':False, 'dmrs ul type1':False}
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            format1Begin = 0
            format3Begin = 0
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'pucch-ResourceSetId 0' in contextStr:
                    format1Begin = num + 3
                if 'pucch-ResourceSetId 1' in contextStr:
                    format3Begin = num + 3
                if 'dmrs-DownlinkForPDSCH-MappingTypeA' in contextStr:
                    resultDict['dmrs dl type'] = True
                    DL_DMRS_Type = contextList[num + 2]
                    if 'pos1' in DL_DMRS_Type:
                        resultDict['dmrs dl type1'] = True
                if 'dmrs-UplinkForPUSCH-MappingTypeA' in contextStr:
                    resultDict['dmrs ul type'] = True
                    UL_DMRS_Type = contextList[num + 2]
                    if 'pos1' in UL_DMRS_Type:
                        resultDict['dmrs ul type1'] = True
                if format1Begin != 0 and format3Begin != 0 and resultDict['dmrs dl type'] == True and resultDict['dmrs ul type'] == True:
                    break
            formate1List = self.findFormateList(format1Begin, contextList)
            formate3List = self.findFormateList(format3Begin, contextList)
            resultDict['format1'] = self.confirmPucchFormate(formate1List, contextList, 'format1')  
            resultDict['format3'] = self.confirmPucchFormate(formate3List, contextList, 'format3')    
        return resultDict
    
    def findFormateList(self, begin, contextList): 
        formateList = []
        for num in range (begin, len(contextList)):
            contextStr = contextList[num]
            if '}' in contextStr:
                break
            if ',' in contextStr:
                formateNum = contextStr.split(' ')[-1][:-1]
            else:
                formateNum = contextStr.split(' ')[-1]
            formateList.append(formateNum)
        return formateList
    
    def confirmPucchFormate(self, formateList, contextList, confirmFormate):
        formateRes = True
        for formateNum in formateList:
            for logNum in range (len(contextList)):
                contextStr = contextList[logNum] 
                print('**********',contextStr)
                print('**********',formateNum)
                if 'pucch-ResourceId '+formateNum in contextStr: 
                    formate = contextList[logNum + 4]
                    if confirmFormate not in formate:
                        formateRes = False
                    break
        return  formateRes
                
    '''
                信令解析：0xB822  NR5G RRC MIB Info
                校验参数：
    '''
    def nr5g_rrc_mib_info_analyze(self, qcatApp, ueLogFilePath, configSsb):
        logId =  0xB822
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId)
        SSB_Frequency_Dict = {'8752':'720288', '8768':'721824', '8784':'723360', '8800':'724896'}
        resultDict = {'DL Frequency':True}
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'DL Frequency' in contextStr:
                    FrequencyValue = contextStr.split('= ')
                    if FrequencyValue == SSB_Frequency_Dict[configSsb]:
                        resultDict['DL Frequency'] = False
        return resultDict
    
    '''
                信令解析：0xB883  NR5G MAC UL Physical Channel Schedule Report
                校验参数：
    '''
    def nr5g_mac_ul_physical_channel_schedule_analyze(self, qcatApp, ueLogFilePath):
        logId =  0xB883
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId)
        formatDict = {'PUCCH_FORMAT_F1':'HOP_MODE_GROUP', 'PUCCH_FORMAT_F3':'HOP_MODE_GROUP'}
        resultDict = {'Format1_Hop':True, 'Format3_Hop':True}
        formatList = []
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            isSkip = False
            pucch_Formate = ''
            freq_hopping_flag = ''
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if '|#  |' in contextStr:
                    attrNameList = contextStr.split('|')
                    attrValueList = contextList[num+2].split('|')
                    for i in range (len(attrNameList)):
                        if 'Phychan Bit Mask' in attrNameList[i]:
                            Phychan_Bit_Mask = attrValueList[i].split(' ')[-1]
                            if Phychan_Bit_Mask != 'PUCCH':
                                isSkip = True
                                break
                        if 'PUCCH Format' in attrNameList[i]:
                            pucch_Formate = attrValueList[i].split(' ')[-1]
                        if 'Freq Hopping Flag' in attrNameList[i]:
                            freq_hopping_flag = attrValueList[i].split(' ')[-1]
                    if pucch_Formate != '' and freq_hopping_flag != '':
                        formatList.append({'Format_Type':pucch_Formate, 'Format_Hop':freq_hopping_flag})
                if isSkip == True:
                    break
        for formatStr in formatList:
            checkFormatStr = formatStr['Format_Type']
            if formatDict[checkFormatStr] != formatStr['Format_Hop']:
                if checkFormatStr == 'PUCCH_FORMAT_F1':
                    resultDict['Format1_Hop'] = False
                elif checkFormatStr == 'PUCCH_FORMAT_F3':
                    resultDict['Format3_Hop'] = False
        return resultDict
    
    '''
                信令解析： 0xB821  NR5G RRC OTA Packet  --  SIB2
                校验参数：
    '''
    def sib2_smtc_analyze(self, qcatApp, ueLogFilePath, smtcPeriod):
        logId =  0xB821
        subTitle = 'SIB2'
        paraDict = {'subTitle':subTitle}
        smtcDict = {'MS5':'sf5','MS10':'sf10','MS20':'sf20','MS40':'sf40',}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        smtcList = []
        result = True
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'smtc' in contextStr:
                    smtcPeriod = contextList[num+2].split('periodicityAndOffset ')[1].split(' :')[0]
                    smtcList.append(smtcPeriod)
                    break
        for smtc in smtcList:
            if smtcDict[smtcPeriod] != smtc:
                result = False
                break
        return result
             
    '''
                信令解析：0xB821  NR5G RRC OTA Packet  --  BCCH_DL_SCH / SystemInformationBlockType1
                校验参数：offsetToCarrier、subcarrierSpacing、carrierBandwidth
    '''
    def sib1_ssb_period_analyze(self, qcatApp, ueLogFilePath, ssbPeriod):
        logId =  0xB821
        subTitle = 'BCCH_DL_SCH / SystemInformationBlockType1'
        paraDict = {'subTitle':subTitle}
        ssbPeriodDict = {'MS5':'ms5', 'MS105':'ms10','MS20':'ms20','MS540':'ms40'}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        result = True
        ssbPeriodList = []
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'ssb-PeriodicityServingCell' in contextStr:
                    ssbPeriod = contextList[num].split('ssb-PeriodicityServingCell ')[1][:-1]
                    ssbPeriodList.append(ssbPeriod)
                    break
        for period in ssbPeriodList:
            if period != ssbPeriodDict[ssbPeriod]:
                result = False
                break 
        return result  
 
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def cis_rs_power_analyze(self, qcatApp, ueLogFilePath, cisRsPower):
        logId =  0xB887
        filterContext = 'DL_DCCH / RRCReconfiguration'
        paraDict = {'filterContext':filterContext}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'nzp-CSI-RS-ResourceToAddModList' in contextStr:
                    powerControlOffsetSSStr = contextList[num+18]
                    break
        powerControlOffsetSS = powerControlOffsetSSStr.split(' ')[-1][:-1]
        if powerControlOffsetSS == cisRsPower.lower():
            return True
        else:
            return False
    
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def pusch_res_alloca_type_analyze(self, qcatApp, ueLogFilePath, puschAllocType):
        logId =  0xB821
        filterContext = 'DL_CCCH / RRC Setup'
        paraDict = {'filterContext':filterContext}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'pusch-Config setup' in contextStr:
                    findPuschAllocTypeStr = contextList[num+28]
                    break
        findPuschAllocType = findPuschAllocTypeStr.split(' ')[-1][:-1]
        if puschAllocType in findPuschAllocType:
            return True
        else:
            return False
        
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def pdsch_res_alloca_type_analyze(self, qcatApp, ueLogFilePath, pdschAllocType):
        logId =  0xB821
        filterContext = 'DL_CCCH / RRC Setup'
        paraDict = {'filterContext':filterContext}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'pdsch-Config setup' in contextStr:
                    findPdschAllocTypeStr = contextList[num+7]
                    break
        findPdschAllocType = findPdschAllocTypeStr.split(' ')[-1][:-1]
        if pdschAllocType in findPdschAllocType:
            return True
        else:
            return False
    
    
    '''
                信令解析：0xB887  NR5G MAC PDSCH Status
                校验参数：
    '''
    def pucch_channel_feedback_per_bandwith_analyze(self, qcatApp, ueLogFilePath, pdschAllocType):
        logId =  0xB821
        filterContext = 'DL_CCCH / RRC Setup'
        paraDict = {'filterContext':filterContext}
        logContextList = QCatModel().load_ue_log(qcatApp, ueLogFilePath, logId, **paraDict)
        for logNum in range (len(logContextList)):
            logContextStr = logContextList[logNum]
            contextList = logContextStr.split('\r\n')
            for num in range (len(contextList)):
                contextStr = contextList[num]
                if 'pdsch-Config setup' in contextStr:
                    findPdschAllocTypeStr = contextList[num+7]
                    break
        findPdschAllocType = findPdschAllocTypeStr.split(' ')[-1][:-1]
        if pdschAllocType in findPdschAllocType:
            return True
        else:
            return False
              
if __name__ == '__main__':
    qcatApp = QCatModel().init_QCat()
    ueLogFilePath = 'D:\\autotestPro\\AutoTestMain\\qxdmLog\\29a2c86d-2a16-43d5-b722-d43d94a03976_50191_Diag_2500-ffff192_168_1_1_1.hdf'
    
#     attrDict = {
#             'offsetToCarrier':'0',
#             'subcarrierSpacing':'kHz30',
#             'carrierBandwidth':'273',
#             'nrofDownlinkSlots':'7',
#             'nrofDownlinkSymbols':'6',
#             'nrofUplinkSlots':'2',
#             'nrofUplinkSymbols':'4'
#             'dciFormate':'dci-Format0-0-AndFormat1-0',
#             }
    
#     resultDict = LogAnalyzeModel().system_information_block_type1_analyze(QCat, ueLogFilePath, attrDict)
#     attrDict = {
#             'duration':'1',
#             'monitoringSymbolsWithinSlot':'\'10000000 000000\'B',
#             'searchSpaceTypeUeSpecific':'formats0-1-And-1-1',
#             'resourceAllocation':'resourceAllocationType1',
#             'rbg-Size':'config1',
#             'mcs-Table':'qam256'
#         }
#     resultDict = LogAnalyzeModel().rrc_reconfiguration(qcatApp, ueLogFilePath, attrDict)
#     attrDict = {
#         'dciFormat':'DL_1_1',
#         'aggregationLevel':'LEVEL_4'
#         }
#     resultDict = LogAnalyzeModel().nr5g_mac_dci_info_analyze(qcatApp, ueLogFilePath, attrDict)
    
#     resultDict = LogAnalyzeModel().nr5g_mac_pdsch_status_analyze(qcatApp, ueLogFilePath)
    attrCheckDict = {
        'prachConfig':'147',
        'preambleFormat':'FORMAT_B4'
        }
    resultDict = LogAnalyzeModel().nr5g_mac_rach_attempt_analyze(qcatApp, ueLogFilePath, attrCheckDict)
#     resultDict = LogAnalyzeModel().dl_ccch_rrc_setup_analyze(qcatApp, ueLogFilePath)
    print(resultDict)
        