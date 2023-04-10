import configparser
import csv
from ctypes import *
import datetime
import struct
import threading
import time

from pip._vendor.distlib.compat import raw_input
from scapy.all import *
from scapy.layers.inet import defragment

from BasicModel.basic.EIDetailConfigParse import GetActiveEIMsgList, \
    GetsvHeartBeat
from BasicModel.basic.msgStructDefine import T_EICellTabDspStateList, \
    T_EIGeneralInfo


exec_count = 0
g_interval = 0.00
g_originalBasicInfoList = []
g_DspStateList = T_EICellTabDspStateList()
g_BasicInfoData = []
g_tEiMsgList = GetActiveEIMsgList()

tHeadSize = 8
tMsgHeadSize = 16
tTlvHeadSize = 8

cellDLRlcList = []
cellULRlcList = []
sumCellDLRlcList = []


def loadDataAndCalculateFlow(name, srcip, dstip, dir, type):
    packets = rdpcap(name)
    packets = defragment(packets)
    oldTimeStr = ''
    cellUlRlcList=[]
    cellDlRlcList=[]
    sumDlRlc = 0
    sumUlRlc = 0
    dlTrafRes = ''
    ulTrafRes = ''
    for packet in packets:
        if 'UDP' in packet:
            if packet.payload.src == srcip and packet.payload.dst == dstip:
                DlRlcRes, UlRlcRes, DlWifiRlcRes, UlWifiRlcRes = parseOriginalData(packet)
                if type == 'NR':
                    if dir =='DL':
                        if DlRlcRes!= None:
                            cellDlRlcList.append(DlRlcRes)
                    elif dir == 'UL':
                        if UlRlcRes!= None:
                            cellUlRlcList.append(UlRlcRes)
                    else:
                        if DlRlcRes!= None:
                            cellDlRlcList.append(DlRlcRes)
                        if UlRlcRes!= None:
                            cellUlRlcList.append(UlRlcRes)
                elif type == 'WIFI':
                    if dir =='DL':
                        if DlWifiRlcRes!= None:
                            cellDlRlcList.append(DlWifiRlcRes)
                    elif dir == 'UL':
                        if UlWifiRlcRes!= None:
                            cellUlRlcList.append(UlWifiRlcRes)
                    else:
                        if DlWifiRlcRes!= None:
                            cellDlRlcList.append(DlWifiRlcRes)
                        if UlWifiRlcRes!= None:
                            cellUlRlcList.append(UlWifiRlcRes)
                timeStr = TimeStamp2Time(packet.time)
                if timeStr != oldTimeStr:
                    if cellDlRlcList:
                        for rlc in cellDlRlcList:
                            sumDlRlc = sumDlRlc + rlc
                        dlTrafRes = dlTrafRes + '['+timeStr+']:'+analizeResult(sumDlRlc)+'\n'
                        sumDlRlc = 0
                        cellDlRlcList = []
                    if cellUlRlcList:
                        for rlc in cellUlRlcList:
                            sumUlRlc = sumUlRlc + rlc
                        ulTrafRes = ulTrafRes + '['+timeStr+']:'+analizeResult(sumUlRlc)+'\n'
                        sumUlRlc = 0
                        cellUlRlcList = []     
                oldTimeStr = timeStr
    return dlTrafRes,ulTrafRes

def analizeResult(rlc):
    TrafficInfo = ''
    if int(rlc) > 1000000:
        TrafficInfo = str(round(rlc/1000000,2))+' M'
    elif int(rlc) > 1000:
        TrafficInfo = str(round(rlc/1000,2))+ 'K'
    else:
        TrafficInfo = str(round(rlc,2))+ ''
    return TrafficInfo

def parseOriginalData(packet):
    data = packet["Raw"].load
    msgid, msglen, msgsn = struct.unpack('>HHI', data[:tHeadSize])
    if msgid == 3637: #SV基本信息
        DlRlc, UlRlc, DlWifiRlc, UlWifiRlc = svBasicInfomationProc(data)
        return DlRlc, UlRlc, DlWifiRlc, UlWifiRlc
    else:
        return 0, 0, 0, 0

def svBasicInfomationProc(data):
    msgid, msglen, msgsn = struct.unpack('>HHI', data[:tHeadSize])
    RemainLen = len(data) - tHeadSize
    DlRlc, UlRlc, DlWifiRlc, UlWifiRlc = 0, 0, 0, 0
    while RemainLen > (tMsgHeadSize + tTlvHeadSize):
        u32EiMsgId, u32AirTime, u32Sn, u16TlvNum, u16MsgLen = struct.unpack('<3I2H', data[tHeadSize:(tHeadSize + tMsgHeadSize)])
        RemainLen = RemainLen - tMsgHeadSize - u16MsgLen
        EiMsgLen = 0
        if u32EiMsgId == 1:
            DlRlc, UlRlc, DlWifiRlc, UlWifiRlc = NRL2_General(data, u16TlvNum, EiMsgLen)
        elif u32EiMsgId == 301:
            RTL2_General(data, u16TlvNum, EiMsgLen)
    return DlRlc, UlRlc, DlWifiRlc, UlWifiRlc

def NRL2_General(data, u16TlvNum, EiMsgLen):
    index = 0
    DlRlc, UlRlc, DlWifiRlc, UlWifiRlc, = 0, 0, 0, 0
    while(index < u16TlvNum):
#         ULWifiThrput, DLWifiThrput = 0, 0
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
            u32CellULRlcThrput, u32CellDLRlcThrput, u32CellULMacThrput, u32CellDLMacThrput = struct.unpack('<4I', data[offset:(tHeadSize + tMsgHeadSize + EiMsgLen + u16TlvLen)])
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLRlcThrput = u32CellDLRlcThrput
            tEIGeneralInfo.tEICellULDetailState.u32CellULRlcThrput = u32CellULRlcThrput
            DlRlc = DlRlc + u32CellDLRlcThrput
            UlRlc = UlRlc + u32CellULRlcThrput
        elif u16TlvId == 3:
            u32CellULPdcpThrput, u32CellDLPdcpThrput,u32CellULWifiThrput, u32CellDLWifiThrput = struct.unpack('<4I', data[offset:(offset + u16TlvLen)])
            tEIGeneralInfo.tEICellDLDetailState.u32CellDLPdcpThrput = u32CellDLPdcpThrput
            tEIGeneralInfo.tEICellULDetailState.u32CellULPdcpThrput = u32CellULPdcpThrput
            DlWifiRlc = DlWifiRlc + u32CellDLWifiThrput
            UlWifiRlc = UlWifiRlc + u32CellULWifiThrput
        elif u16TlvId == 4:
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
        elif u16TlvId == 2:
            u32UEULRlcThrput, u32UEDLRlcThrput = struct.unpack('<2I', data[offset:(offset + u16TlvLen)])
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8UELiveCount = 0
            if tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed == 0:
                tEIGeneralInfo.tEIUEGeneralList.u32UENum = tEIGeneralInfo.tEIUEGeneralList.u32UENum + 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u8IsUsed = 1
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32DLRlcThrput = u32UEDLRlcThrput
            tEIGeneralInfo.tEIUEGeneralList.atEIUEGeneralInfo[u16UeGidId].u32ULRlcThrput = u32UEULRlcThrput

        EiMsgLen = EiMsgLen + u16TlvLen
        index = index + 1
    cellDLRlcList.append(g_BasicInfoData[0].tEICellDLDetailState.u32CellDLRlcThrput)
    cellULRlcList.append(g_BasicInfoData[0].tEICellULDetailState.u32CellULRlcThrput)
    return DlRlc, UlRlc, DlWifiRlc, UlWifiRlc

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

'''
       监控线程
'''
def taskTimerStart(svSocket):
    heartBeat = GetsvHeartBeat()
    svSocket.send(heartBeat)
'''
        启动监控线程
'''            
def startMonitorTask(svSocket):
    threadList = []
    runNum = 0
    while(runNum < 3):
        tt = threading.Timer(10, taskTimerStart,(svSocket,))# 60
        tt.start()
        threadList.append(tt)
        runNum += 1
    for tt in threadList:
        tt.join()
    
'''
        网络抓包
'''
def scrapNetworkPackData(packageFileName, pcNetworkCardName, timeout=120):
    logging.info('begin capture data package, capture time: '+str(timeout)+'s......')
    packet = sniff(iface = pcNetworkCardName, timeout=timeout)
    wrpcap(packageFileName, [packet])

def TimeStamp2Time(timeStamp):
    timeTmp = time.localtime(timeStamp)
    myTime = time.strftime("%Y-%m-%d %H:%M:%S", timeTmp)
    return myTime