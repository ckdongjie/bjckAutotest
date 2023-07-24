'''
Created on 2023年4月18日
@author: autotest
'''
import csv
from ctypes import CDLL
import ctypes
import os
import struct
import sys
import threading
import time
from scapy.all import *
from ctypes import *
from pip._vendor.distlib.compat import raw_input
from scapy.layers.inet import defragment
from scapy.utils import rdpcap

from BasicModel.basic.EIDetailConfigParse import GetActiveEIMsgList
from BasicModel.basic.msgStructDefine import T_EICellTabDspStateList, \
    T_EIGeneralInfo
from BasicModel.basic.sigTraceParse import TraceMeInit, TraceMeParse

exec_count = 0
g_interval = 0.00
g_originalBasicInfoList = []
g_DspStateList = T_EICellTabDspStateList()
g_BasicInfoData = []

tHeadSize = 8
tMsgHeadSize = 16
tTlvHeadSize = 8
EIBasicSavedRecordNum = 0
MAX_SAVE_BASIC_INFO_RECORD_NUM = 20480
SaveRecordNum = 0

SIG_TRACE_HISTORY_MAX = 10240
TraceLogAutoSaveFileName = 'TraceLog_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv'
TraceLogHeader = ['模块名称', '打印级别', '打印时间', '上报时间', '打印内容']
TRACE_LOG_HISTORY_MAX = 20480

gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
strDllPath = gen_path + "\\EI_FileProc.dll"
dll = CDLL(strDllPath)
dll = ctypes.cdll.LoadLibrary(strDllPath)
EnbMonitorNum = dll.InitEnbMonitorThreadHandle()

def loadAllData(toolLogPath, debugIp, localIp, sigPort, tracePort, name, isWriteSig=False, isWriteSvBasic=False, isWriteTrace=False, isWriteSvDetail=False):
    packets = rdpcap(name)
    packets = defragment(packets)
    for packet in packets:
        if 'UDP' in packet:
            if packet.payload.src == debugIp and packet.payload.dst == localIp:
                if str(packet.payload.dport) == sigPort and isWriteSig == True:
                    writeSigFile(toolLogPath, packet["Raw"].load)
                elif str(packet.payload.dport) == tracePort and isWriteTrace == True:
                    writeTraceFile(packet["Raw"].load)
                else:
                    parseOriginalData(toolLogPath, packet, isWriteSvBasic, isWriteSvDetail)
    
def parseOriginalData(toolLogPath, packet, isWriteSvBasic=False, isWriteSvDetail=False):
    data = packet["Raw"].load
    msgid, msglen, msgsn = struct.unpack('>HHI', data[:tHeadSize])
    if msgid == 3637 and isWriteSvBasic == True: #SV基本信息
        global g_interval
        nowTime = (float)(round(packet.time * 100)) / 100
        # 解析基本信息
        svBasicInfomationProc(data)
        if nowTime - g_interval > 1:
            g_interval = nowTime
            writeBasicFile(toolLogPath)
    elif msgid == 3638 and isWriteSvDetail == True: #SV 详细信息
        dll.WriteEIReportDataToFile(data, EnbMonitorNum)

def svBasicInfomationProc(data):
    msgid, msglen, msgsn = struct.unpack('>HHI', data[:tHeadSize])
    RemainLen = len(data) - tHeadSize
    while RemainLen > (tMsgHeadSize + tTlvHeadSize):
        u32EiMsgId, u32AirTime, u32Sn, u16TlvNum, u16MsgLen = struct.unpack('<3I2H', data[tHeadSize:(tHeadSize + tMsgHeadSize)])
        RemainLen = RemainLen - tMsgHeadSize - u16MsgLen
        EiMsgLen = 0
        if u32EiMsgId == 1:
            NRL2_General(data, u16TlvNum, EiMsgLen)
        elif u32EiMsgId == 301:
            RTL2_General(data, u16TlvNum, EiMsgLen)

def NRL2_General(data, u16TlvNum, EiMsgLen):
    index = 0
    while(index < u16TlvNum):
        u16TlvId, u16UeGidId, u16TlvLen, u16CellId = struct.unpack('<4H', data[(tHeadSize + tMsgHeadSize + EiMsgLen):(tHeadSize + tMsgHeadSize + EiMsgLen + tTlvHeadSize)])
        EiMsgLen = EiMsgLen + tTlvHeadSize
        offset = tHeadSize + tMsgHeadSize + EiMsgLen
        #  检查小区位置
        bIsFindCell, cellIndex = checkCellIsUsed(u16CellId)
        tEIGeneralInfo = None
        if bIsFindCell:
            tEIGeneralInfo = g_BasicInfoData[cellIndex]
            tEIGeneralInfo.u16CellLiveCount = 0
        else:
            tEIGeneralInfo = T_EIGeneralInfo()
            tEIGeneralInfo.u16CellLiveCount = 0
            tEIGeneralInfo.u16CellID = u16CellId
            g_BasicInfoData.append(tEIGeneralInfo)
            u8OpticPort = selectCellShowLocation(u16CellId)
            if u8OpticPort == None:
                return
            tEIGeneralInfo.u8OpticPort = u8OpticPort
        if u16TlvId == 1:#Cell RLC
            u32CellULRlcThrput, u32CellDLRlcThrput, u32CellULMacThrput, u32CellDLMacThrput = struct.unpack('<4I', data[offset:(tHeadSize + tMsgHeadSize + EiMsgLen + u16TlvLen)])
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLRlcThrput = u32CellDLRlcThrput
            tEIGeneralInfo.tEICellULDetailState.u32CellULRlcThrput = u32CellULRlcThrput
        elif u16TlvId == 3:#Cell PDCP
            if len(data[offset:(offset + u16TlvLen)])==8:
                u32CellULPdcpThrput, u32CellDLPdcpThrput = struct.unpack('<2I', data[offset:(offset + u16TlvLen)])
            else:
                u32CellULPdcpThrput, u32CellDLPdcpThrput, u32CellULWifiThrput, u32CellDLWifiThrput = struct.unpack('<4I', data[offset:(offset + u16TlvLen)])
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLPdcpThrput = u32CellDLPdcpThrput
            tEIGeneralInfo.tEICellULDetailState.u32CellULPdcpThrput = u32CellULPdcpThrput
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLWifiThrput = u32CellDLWifiThrput  #dj 
            tEIGeneralInfo.tEICellULDetailState.u32CellULWifiThrput = u32CellULWifiThrput  #dj
        elif u16TlvId == 4:#Ue PDCP 
            u32UEULPdcpThrput, u32UEDLPdcpThrput, u32AddrLen = struct.unpack('<3I', data[offset:(offset + 12)])
            u8Addr = struct.unpack('<20B', data[offset + 12:(offset + u16TlvLen)])
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8UELiveCount = 0
            if tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed == 0:
                tEIGeneralInfo.tEIUEGeneralList.u32UENum = tEIGeneralInfo.tEIUEGeneralList.u32UENum + 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed = 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32DLPdcpThrput = u32UEDLPdcpThrput
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32ULPdcpThrput = u32UEULPdcpThrput
            from Crypto.Util.number import bytes_to_long
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u64IP = bytes_to_long(bytes(u8Addr)[:4])
        elif u16TlvId == 2:#Ue RLC
            u32UEULRlcThrput, u32UEDLRlcThrput = struct.unpack('<2I', data[offset:(offset + u16TlvLen)])
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8UELiveCount = 0
            if tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed == 0:
                tEIGeneralInfo.tEIUEGeneralList.u32UENum = tEIGeneralInfo.tEIUEGeneralList.u32UENum + 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed = 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32DLRlcThrput = u32UEDLRlcThrput
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32ULRlcThrput = u32UEULRlcThrput

        EiMsgLen = EiMsgLen + u16TlvLen
        index = index + 1
        
def RTL2_General(data, u16TlvNum, EiMsgLen):
    index = 0
    
    while (index < u16TlvNum):
        u16TlvId, u16UeGidId, u16TlvLen, u16CellId = struct.unpack('<4H', data[(tHeadSize + tMsgHeadSize + EiMsgLen):(tHeadSize + tMsgHeadSize + EiMsgLen + tTlvHeadSize)])
        EiMsgLen = EiMsgLen + tTlvHeadSize
        offset = tHeadSize + tMsgHeadSize + EiMsgLen
        #  检查小区位置
        bIsFindCell, cellIndex = checkCellIsUsed(u16CellId)
        tEIGeneralInfo = None
        if bIsFindCell:
            tEIGeneralInfo = g_BasicInfoData[cellIndex]
            tEIGeneralInfo.u16CellLiveCount = 0
        else:
            tEIGeneralInfo = T_EIGeneralInfo()
            tEIGeneralInfo.u16CellLiveCount = 0
            tEIGeneralInfo.u16CellID = u16CellId
            g_BasicInfoData.append(tEIGeneralInfo)
            u8OpticPort = selectCellShowLocation(u16CellId)
            if u8OpticPort == None:
                return
            tEIGeneralInfo.u8OpticPort = u8OpticPort
        if u16TlvId == 1:
            u32CellULMacThroughput, u16CellULActUeNum, u16CellULHarqFailRatio, u16CellULHarqSelfMaintainRatio, s16NI = struct.unpack('<I3Hh', data[offset:(offset + 12)])
            tEIGeneralInfo.tEICellULDetailState.u32CellULMacThroughput = u32CellULMacThroughput
            tEIGeneralInfo.tEICellGeneralState.u16ActiveUENum = u16CellULActUeNum
            tEIGeneralInfo.tEICellULDetailState.u16CellULHarqFailRatio = u16CellULHarqFailRatio
            tEIGeneralInfo.tEICellULDetailState.u16CellULHarqSelfMaintainRatio = u16CellULHarqSelfMaintainRatio
            tEIGeneralInfo.tEICellGeneralState.s16NI = s16NI

            au16CellULMcs = struct.unpack('<4H', data[(offset + 12):(offset + 20)])
            tEIGeneralInfo.tEICellULDetailState.au16AvrgULMcs = list(au16CellULMcs)

            u8CellULRbUsedRatio, u8CellULSchdUeNumPerTti, u8CellULAvrHarqTxCnt, u8CellULBler, u16CellULHqRetSuccRatio1, u16CellULHqRetSuccRatio2, u16CellULHqRetSuccRatio3, u16CellULHqRetSuccRatio4, \
            u16CellULMaxSchdTaskTime, u16CellULMaxPhyMgrTaskTime, u32MaxTotalTaskTime = struct.unpack('<4B6HI', data[(offset + 20):(offset + 40)])
            tEIGeneralInfo.tEICellULDetailState.u8ULRbRatio = u8CellULRbUsedRatio
            tEIGeneralInfo.tEICellULDetailState.u8CellULSchdUeNumPerTti = u8CellULSchdUeNumPerTti
            tEIGeneralInfo.tEICellULDetailState.u8CellULAvrHarqTxCnt = u8CellULAvrHarqTxCnt
            tEIGeneralInfo.tEICellULDetailState.u8CellULBler = u8CellULBler
            tEIGeneralInfo.tEICellULDetailState.u16CellULHqRetSuccRatio1 = u16CellULHqRetSuccRatio1
            tEIGeneralInfo.tEICellULDetailState.u16CellULHqRetSuccRatio2 = u16CellULHqRetSuccRatio2
            tEIGeneralInfo.tEICellULDetailState.u16CellULHqRetSuccRatio3 = u16CellULHqRetSuccRatio3
            tEIGeneralInfo.tEICellULDetailState.u16CellULHqRetSuccRatio4 = u16CellULHqRetSuccRatio4
            tEIGeneralInfo.tEICellULDetailState.u16CellULMaxSchdTaskTime = u16CellULMaxSchdTaskTime
            tEIGeneralInfo.tEICellULDetailState.u16CellULMaxPhyMgrTaskTime = u16CellULMaxPhyMgrTaskTime
            tEIGeneralInfo.tEICellULDetailState.u32MaxTotalTaskTime = u32MaxTotalTaskTime

            as16SubNI = struct.unpack('<273h', data[(offset + 40):(offset + 586)])
            tEIGeneralInfo.tEICellGeneralState.as16SubNI = list(as16SubNI)

            s16Resv = struct.unpack('<h', data[(offset + 586):(offset + u16TlvLen)])
        elif u16TlvId == 2:
            u32CellDLMacThroughput, u16CellDLActUeNum, u16CellDLHarqFailRatio, u16CellDLHarqSelfMaintainRatio, u16CellDLDtxRatio = struct.unpack('<I4H', data[offset:(offset + 12)])
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLMacThroughput = u32CellDLMacThroughput
            tEIGeneralInfo.tEICellGeneralState.u16ActiveUENum = u16CellDLActUeNum
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHarqFailRatio = u16CellDLHarqFailRatio
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHarqSelfMaintainRatio = u16CellDLHarqSelfMaintainRatio
            tEIGeneralInfo.tEICellDLDetailState.u16DtxRatio = u16CellDLDtxRatio

            au16CellDLMcs = struct.unpack('<4H', data[(offset + 12):(offset + 20)])
            tEIGeneralInfo.tEICellDLDetailState.au16AvrgDLMcs = list(au16CellDLMcs)

            u8CellDLTxPwr, u8CellDLRbUsedRatio, u8CellDLSchdUeNumPerTti, u8CellDLAvrHarqTxCnt, u8CellDLBler, u8Rsvd, u8CellDLTxLayerRatio1, u8CellDLTxLayerRatio2, u8CellDLTxLayerRatio3, u8CellDLTxLayerRatio4, \
            u16CellDLHqRetSuccRatio1, u16CellDLHqRetSuccRatio2, u16CellDLHqRetSuccRatio3, u16CellDLHqRetSuccRatio4, u16CellDLMaxSchdTaskTime = struct.unpack('<10B5H', data[offset + 20:(offset + u16TlvLen)])
            tEIGeneralInfo.tEICellGeneralState.u8TXPower = u8CellDLTxPwr
            tEIGeneralInfo.tEICellDLDetailState.u8DLRbRatio = u8CellDLRbUsedRatio
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLSchdUeNumPerTti = u8CellDLSchdUeNumPerTti
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLAvrHarqTxCnt = u8CellDLAvrHarqTxCnt
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLBler = u8CellDLBler
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLTxLayerRatio1 = u8CellDLTxLayerRatio1
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLTxLayerRatio2 = u8CellDLTxLayerRatio2
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLTxLayerRatio3 = u8CellDLTxLayerRatio3
            tEIGeneralInfo.tEICellDLDetailState.u8CellDLTxLayerRatio4 = u8CellDLTxLayerRatio4
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHqRetSuccRatio1 = u16CellDLHqRetSuccRatio1
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHqRetSuccRatio2 = u16CellDLHqRetSuccRatio2
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHqRetSuccRatio3 = u16CellDLHqRetSuccRatio3
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLHqRetSuccRatio4 = u16CellDLHqRetSuccRatio4
            tEIGeneralInfo.tEICellDLDetailState.u16CellDLMaxSchdTaskTime = u16CellDLMaxSchdTaskTime
        elif u16TlvId == 3:
            u32UEULThroughput, u16UEULSchdCnt, u16UEULHarqFailRatio, u16UEULHarqSelfMaintainRatio = struct.unpack('<I3H', data[offset:(offset + 10)])
            u16UEULMcs = struct.unpack('<4H', data[offset + 10:(offset + 18)])
            u16UEULAvrRbNum, u8UEULAvrHarqTxCnt, u8UEULBler, u8UEULPL = struct.unpack('<H3b', data[offset + 18:(offset + 23)])
            u8Rsv = struct.unpack('<3b', data[offset + 23:(offset + 26)])
            s16UESinr, = struct.unpack('<h', data[offset + 26:(offset + u16TlvLen)])

            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8UELiveCount = 0
            if tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed == 0:
                tEIGeneralInfo.tEIUEGeneralList.u32UENum = tEIGeneralInfo.tEIUEGeneralList.u32UENum + 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed = 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32ULMacThrput = u32UEULThroughput
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLSchdCnt = u16UEULSchdCnt
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16ULHarqFailRatio = u16UEULHarqFailRatio
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16ULHarqExpireRatio = u16UEULHarqSelfMaintainRatio
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].au16ULAvrgMcs = list(u16UEULMcs)
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLAvrgRbNum = u16UEULAvrRbNum
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8ULAvrgHarqTxCnt = u8UEULAvrHarqTxCnt
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8ULAvrgBler = u8UEULBler
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8PL = u8UEULPL
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].s16Sinr = s16UESinr
        elif u16TlvId == 4:
            u32UEDLThroughput, u16UEDLSchdCnt, u16UEDLHarqFailRatio, u16UEDLHarqSelfMaintainRatio, u16UEDLDtxRatio = struct.unpack('<I4H', data[offset:(offset + 12)])
            u16UEDLMcs = struct.unpack('<4H', data[offset + 12:(offset + 20)])
            u16UEDLAvrRbNum, u8UEDLAvrHarqTxCnt, u8UEDLBler = struct.unpack('<H2B', data[offset + 20:(offset + 24)])
            au8UEDLTxDivRatio = struct.unpack('<4B', data[offset + 24:(offset + u16TlvLen)])

            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8UELiveCount = 0
            if tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed == 0:
                tEIGeneralInfo.tEIUEGeneralList.u32UENum = tEIGeneralInfo.tEIUEGeneralList.u32UENum + 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed = 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32DLMacThrput = u32UEDLThroughput
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLSchdCnt = u16UEDLSchdCnt
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLHarqFailRatio = u16UEDLHarqFailRatio
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLHarqExpireRatio = u16UEDLHarqSelfMaintainRatio
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DtxRatio = u16UEDLDtxRatio
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].au16DLAvrgMcs = list(u16UEDLMcs)
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u16DLAvrgRbNum = u16UEDLAvrRbNum
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8DLAvrgHarqTxCnt = u8UEDLAvrHarqTxCnt
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8DLAvrgBler = u8UEDLBler

        EiMsgLen = EiMsgLen + u16TlvLen
        index = index + 1
        
def checkCellIsUsed(u16CellID):
    for i, val in enumerate(g_BasicInfoData):
        if val.u16CellID == u16CellID:
            return True,i
    return False,None

def selectCellShowLocation(u16CellID):
    if not g_DspStateList.bIsUsedCell1:
        g_DspStateList.bIsUsedCell1 = True
        g_DspStateList.au16CellID[0] = u16CellID
        return 0
    elif not g_DspStateList.bIsUsedCell2:
        g_DspStateList.bIsUsedCell2 = True
        g_DspStateList.au16CellID[1] = u16CellID
        return 1
    elif not g_DspStateList.bIsUsedCell3:
        g_DspStateList.bIsUsedCell3 = True
        g_DspStateList.au16CellID[2] = u16CellID
        return 2
    elif not g_DspStateList.bIsUsedCell4:
        g_DspStateList.bIsUsedCell4 = True
        g_DspStateList.au16CellID[3] = u16CellID
        return 3
    else:
        return None

def writeBasicFile(toolLogPath):
    global EIBasicSavedRecordNum, file_basic, EIAutoSaveFileName
    if EIBasicSavedRecordNum >= MAX_SAVE_BASIC_INFO_RECORD_NUM:
        file_basic.close()
        EIAutoSaveFileName = 'ei_basic_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.bei'
        file_basic = open(toolLogPath+'/EI_Report/EI_Basic/'+EIAutoSaveFileName, mode='wb+')
        eiFileHeader = struct.pack('<3I', 0xDEDEDEDE, 12, 0)
        file_basic.seek(0)
        file_basic.write(eiFileHeader)
        EIBasicSavedRecordNum = 0
    file_basic.seek(0, 2)
    RecordPosition = file_basic.tell()
    import datetime
    dTime = (datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds()
    
    recordHead = struct.pack('<2HId', 0xBCBC, 0, 0, dTime)
    file_basic.write(recordHead)
    EIBasicSavedRecordNum = EIBasicSavedRecordNum + 1

    u32RecoadTotalLen = 0
    for tEIGeneral in g_BasicInfoData:
        CellInfoStream = tEIGeneral.packCell()
        file_basic.write(CellInfoStream)
        u32RecoadTotalLen =  u32RecoadTotalLen + len(CellInfoStream)

        byUENum = struct.pack('<I', tEIGeneral.tEIUEGeneralList.u32UENum)
        file_basic.write(byUENum)
        u32RecoadTotalLen =  u32RecoadTotalLen + 4

        for UeLoop in range(0, 3600):
            if tEIGeneral.tEIUEGeneralList.atEIUEGeneralInfo[UeLoop].u8IsUsed != 0:
                byUEGid = struct.pack('<I', UeLoop)
                file_basic.write(byUEGid)
                u32RecoadTotalLen = u32RecoadTotalLen + 4

                UEInfoStream = tEIGeneral.tEIUEGeneralList.atEIUEGeneralInfo[UeLoop].pack()
                file_basic.write(UEInfoStream)
                u32RecoadTotalLen = u32RecoadTotalLen + len(UEInfoStream)
    rcdHeaderStream = struct.pack('<2HI', 0xBCBC, len(g_BasicInfoData), u32RecoadTotalLen)
    file_basic.seek(RecordPosition)
    file_basic.write(rcdHeaderStream)

    file_basic.seek(0, 2)
    fileLen = file_basic.tell()
    file_basic.seek(0)
    fileHeaderStream = struct.pack('<3I', 0xDEDEDEDE, fileLen, EIBasicSavedRecordNum)
    file_basic.write(fileHeaderStream)

def writeSigFile(toolLogPath, data):
    global SaveRecordNum, SigAutoSaveFileName, file_sig
    if SaveRecordNum >= SIG_TRACE_HISTORY_MAX:
        file_sig.close()
        SigAutoSaveFileName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xst'
        file_sig = open(toolLogPath+'/signal/'+SigAutoSaveFileName, mode='wb+')
        buffer = struct.pack('<I', 0xDEDEDEDE) + struct.pack('<4b', *(bytes(('.xst').ljust(4, '\0'), encoding="utf-8"))) + struct.pack('<2I', 0, 16)
        file_sig.seek(0)
        file_sig.write(buffer)
        SaveRecordNum = 0

    buffer = struct.pack('<2H', 0xBCBC, len(data))
    file_sig.seek(0, 2)
    fileLen = file_sig.tell()
    file_sig.seek(fileLen)
    file_sig.write(buffer)

    file_sig.write(data)
    fileLen = file_sig.tell()
    SaveRecordNum += 1

    buffer = struct.pack('<I', 0xDEDEDEDE) + struct.pack('<4b', *(bytes(('.xst').ljust(4, '\0'), encoding="utf-8")))\
             + struct.pack('<2I', SaveRecordNum, fileLen)
    file_sig.seek(0)
    file_sig.write(buffer)

def writeTraceFile(log_writer, data):
    g_traceLogInfoDic= TraceMeInit()
    traceLogMsg = TraceMeParse(data)
    strText = []
    strText.append(g_traceLogInfoDic[traceLogMsg.u32ModuleNameId])
    strText.append(traceLogMsg.PrintLevel)
    strText.append(traceLogMsg.PrintTime)
    strText.append(traceLogMsg.u32ReportTime)
    strText.append(traceLogMsg.PrintText.replace('\n', ''))
    log_writer.writerow(strText)

'''
                    捕获数据分析
    '''        
def capture_data_analyse(debugIp, localIp, offlineFilename, isSaveSig=False, isSaveSvBasic=False, isSaveTrace=False, isSaveSvDetail=False ,tracePort='6060', sigPort='6080'):
    global file_basic, file_sig, file_tracelog
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    toolPath = BASE_DIR+'\\AutoTestMain\\maintenanceTool\\'+debugIp
    
    if isSaveSvBasic == True:  
        if not os.path.exists(toolPath+'/EI_Report'):
            os.makedirs(toolPath+'/EI_Report')
            
        if not os.path.exists(toolPath+'/EI_Report/EI_Basic'):
            os.makedirs(toolPath+'/EI_Report/EI_Basic')
        EIAutoSaveFileName = 'ei_basic_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.bei'
        file_basic = open(toolPath+'/EI_Report/EI_Basic/'+EIAutoSaveFileName, mode='wb+')
        eiFileHeader = struct.pack('>3I', 0xDEDEDEDE, 12, 0)
        file_basic.seek(0)
        file_basic.write(eiFileHeader)
        
    if isSaveSvDetail == True:    
        g_tEiMsgList = GetActiveEIMsgList()
        strTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if not os.path.exists(toolPath+'/EI_Report/EI_Detail'):
            os.makedirs(toolPath+'/EI_Report/EI_Detail')
        os.makedirs(toolPath+'/EI_Report/EI_Detail/' + strTime)
        strPath =toolPath+'/EI_Report/EI_Detail/' + strTime
        ipPath = create_string_buffer(bytes(strPath, encoding='utf8'))
        ipTime = create_string_buffer(bytes(strTime, encoding='utf8'))
        for tEiMsgInfo in g_tEiMsgList:
            TlvPtr = create_string_buffer(tEiMsgInfo.pack())
            dll.CreateEIBinarySubFiles(TlvPtr, ipPath, ipTime, EnbMonitorNum)
        
    if isSaveSig == True:  
        if not os.path.exists(toolPath+'/signal'):
            os.makedirs(toolPath+'/signal')
        SigAutoSaveFileName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.xst'
        file_sig = open(toolPath+'/signal/'+SigAutoSaveFileName, mode='wb+')
        sigFileHeader = struct.pack('<I', 0xDEDEDEDE) + struct.pack('<4b', *(bytes(('.xst').ljust(4, '\0'), encoding="utf-8"))) + \
                        struct.pack('<2I', 0, 16)
        file_sig.seek(0)
        file_sig.write(sigFileHeader)
    
    if isSaveTrace == True: 
        if not os.path.exists(toolPath+'/trace'):
            os.makedirs(toolPath+'/trace')
        file_tracelog = open(toolPath+'/trace/'+TraceLogAutoSaveFileName, 'w')
        log_writer = csv.writer(file_tracelog)
        log_writer.writerow(TraceLogHeader)
  
    loadAllData(toolPath, debugIp, localIp, sigPort, tracePort, offlineFilename, isSaveSig, isSaveSvBasic, isSaveTrace, isSaveSvDetail)
    if isSaveSig == True:
        file_sig.close()
    if isSaveSvBasic == True:
        file_basic.close()
    if isSaveTrace == True:
        file_tracelog.close()
