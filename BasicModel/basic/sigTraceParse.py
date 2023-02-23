import time
import struct

class T_SIG_HEAD:
    def __init__(self):
        self.u32SInfoSeq = 0
        self.u32FrmInf = 0
        self.u8Res = 0
        self.tTM = T_ABS_TM()
        self.au8TraceTaskID = bytes(8)
        self.tSigTrace = T_SignalTraceInfo()
    def unPackHead(self, data):
        self.u32SInfoSeq, self.u32FrmInf, self.u8Res = struct.unpack('>IIB', data[0:5])
        self.tTM.unPackTm(data[5:7])
        self.au8TraceTaskID = bytes(struct.unpack('>8B', data[12:8]))
        self.tSigTrace.unPackSigInfo(data[20:20])

class T_ABS_TM:
    def __init__(self):
        self.au8Year = bytes(2)
        self.u8Mon = 0
        self.u8Day = 0
        self.u8Hour = 0
        self.u8Min = 0
        self.u8Sec = 0
    def unPackTm(self, data):
        self.au8Year[1], self.au8Year[0], self.u8Mon, self.u8Day, self.u8Hour, self.u8Min, self.u8Sec = struct.unpack('>7B', data[0:7])

class T_SignalTraceInfo:
    def __init__(self):
        self.u16CellID = 0
        self.u16DuGID = 0
        self.u32GID = 0
        self.u32Interface = 0
        self.u8Dir = 0
        self.u8Reserved = 0
        self.u16MsgID = 0
        self.u32EnbID = 0
    def unPackSigInfo(self, data):
        self.u16CellID, self.u16DuGID, self.u32GID, self.u32Interface, self.u8Dir,\
        self.u8Reserved, self.u16MsgID, self.u32EnbID = struct.unpack('>2H2I2BHI', data[0:20])

class SignalTraceStruct:
    def __init__(self):
        self.u16CellID = 0
        self.u16DuGID = 0
        self.u32GID = 0
        self.sInterface = ''
        self.sDir = ''
        self.u16MsgID = 0
        self.u32SInfoSeq = 0
        self.u32SFN = 0
        self.sFrameInfo = ''
        self.ReportTime = ''
        self.u16MsgLen = 0
        self.PrintTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.achPrintBuff

class TraceMeStruct:
    def __init__(self):
        self.u32ModuleNameId = 0
        self.PrintTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.u32ReportTime = 0
        self.u32FramInfo = 0
        self.PrintText = ''
        self.PrintLevel = 0

class T_TraceStartInd:
    def __init__(self):
        self.au8TraceTaskID = [0] *8
        self.au8IPAdress = [0] * 20
        self.u16PortId = 0
        self.u8TraceType = 0
        self.u8TraceDepth = 0
        self.u8Interface = 0
        self.u8Rcv = 0
        self.u16CellId = 0
        self.u32UEGid = 0
        self.u8Level = 0
        self.u8SPIDNum = 0
        self.u16Rcv = 0
        self.au32SPID = [0] * 20
    def pack(self):
        buffer = bytes(0)
        for i in range(0,8):
            buffer = buffer + struct.pack('>B', self.au8TraceTaskID[i])
        for i in range(0,20):
            buffer = buffer + struct.pack('>B', self.au8IPAdress[i])
        buffer = buffer + struct.pack('>H', self.u16PortId) + \
                 struct.pack('>4B', self.u8TraceType, self.u8TraceDepth, self.u8Interface, self.u8Rcv) + \
                 struct.pack('>HI2BH', self.u16CellId, self.u32UEGid, self.u8Level, self.u8SPIDNum, self.u16Rcv)
        for i in range(0,20):
            buffer = buffer + struct.pack('>I', self.au32SPID[i])
        return buffer



def TraceMeInit():
    TraceLogInfoDic = {}
    TraceLogInfoDic[79] = 'L3_CRM'
    TraceLogInfoDic[81] = 'L3_CUDAM'
    TraceLogInfoDic[80] = 'L3_DCRM'
    TraceLogInfoDic[87] = 'L3_DU_F1AP'
    TraceLogInfoDic[82] = 'L3_DUDAM'
    TraceLogInfoDic[78] = 'L3_DUEC'
    TraceLogInfoDic[86] = 'L3_F1AP'
    TraceLogInfoDic[88] = 'L3_E1AP'
    TraceLogInfoDic[89] = 'L3_XNAP'
    TraceLogInfoDic[85] = 'L3_NGAP'
    TraceLogInfoDic[83] = 'L3_PDCPCP'
    TraceLogInfoDic[84] = 'L3_PDCPUP'
    TraceLogInfoDic[77] = 'L3_UEC'
    TraceLogInfoDic[76] = 'L3_UECM'
    TraceLogInfoDic[90] = 'L3_COMMON'
    TraceLogInfoDic[152] = 'UP_PRINT'
    TraceLogInfoDic[151] = 'UP_RECE'
    TraceLogInfoDic[153] = 'UP_SV'
    TraceLogInfoDic[176] = 'CFGMGR'
    TraceLogInfoDic[186] = 'DLSCHD_MSG'
    TraceLogInfoDic[190] = 'DLSCHD_SCHD'
    TraceLogInfoDic[177] = 'PHYMGR_ISR'
    TraceLogInfoDic[178] = 'PHYMGR_MSG'
    TraceLogInfoDic[182] = 'PHYMGR_SCHD'
    TraceLogInfoDic[194] = 'ULSCHD_MSG'
    TraceLogInfoDic[198] = 'ULSCHD_SCHD'
    TraceLogInfoDic[0] = 'OS'
    TraceLogInfoDic[1] = 'PF_RRU'
    TraceLogInfoDic[2] = 'PF_VM'
    TraceLogInfoDic[3] = 'OAM_TRC'
    TraceLogInfoDic[4] = 'OAM_OCM'
    TraceLogInfoDic[5] = 'OAM_ACM'
    TraceLogInfoDic[6] = 'OAM_STM'
    TraceLogInfoDic[7] = 'AM_MNG'
    TraceLogInfoDic[8] = 'AM_DET'
    TraceLogInfoDic[9] = 'OAM_CMM'
    TraceLogInfoDic[10] = 'OAM_PM'
    TraceLogInfoDic[11] = 'OAM_TRC_SIG'
    TraceLogInfoDic[17] = 'OAM_LOG'
    TraceLogInfoDic[14] = 'PM_ADAPT'
    TraceLogInfoDic[16] = 'OAM_CF'
    TraceLogInfoDic[12] = 'OAM_TRC_ME'
    TraceLogInfoDic[15] = 'OAM_RM'
    TraceLogInfoDic[18] = 'OAM_HSM'
    TraceLogInfoDic[19] = 'NCM'
    TraceLogInfoDic[20] = 'NCM_UDP_SRV'
    TraceLogInfoDic[21] = 'DBS_ITF'
    TraceLogInfoDic[23] = 'DBS_TEST'
    TraceLogInfoDic[22] = 'DBS_DBM'
    TraceLogInfoDic[13] = 'OAM_MONITOR_ROUTE'

    return TraceLogInfoDic



def GetInterface(itf):
    if itf == 0:
        return 'NG'
    elif itf == 1:
        return 'XN'
    elif itf == 2:
        return 'UU'
    elif itf == 3:
        return 'CU_INNER'
    elif itf == 4:
        return 'DU_INNER'
    elif itf == 5:
        return 'OUT'
    elif itf == 6:
        return 'SYNC'
    elif itf == 7:
        return 'F1'
    else:
        return 'error'

def GetDir(dir):
    if dir == 0:
        return 'CU_SEND'
    elif dir == 1:
        return 'CU_RECEIVE'
    elif dir == 2:
        return 'DU_SEND'
    elif dir == 3:
        return 'DU_RECEIVE'
    else:
        return 'error'

def SigTraceParse(data):
    tSigHead = T_SIG_HEAD()
    tSigHead.unPackHead(data)
    achPrintBuff = data[20:len(data)]
    tSigTraceStruct = SignalTraceStruct()
    tSigTraceStruct.u16CellID = tSigHead.tSigTrace.u16CellID
    tSigTraceStruct.u16DuGID = tSigHead.tSigTrace.u16DuGID
    tSigTraceStruct.u32GID = tSigHead.tSigTrace.u32GID
    tSigTraceStruct.u16MsgID = tSigHead.tSigTrace.u16MsgID
    tSigTraceStruct.u32SInfoSeq = tSigHead.u32SInfoSeq
    tSigTraceStruct.achPrintBuff = achPrintBuff
    tSigTraceStruct.u16MsgLen = len(achPrintBuff)

    tSigTraceStruct.sInterface = GetInterface(tSigHead.tSigTrace.u32Interface)
    tSigTraceStruct.sDir = GetDir(tSigHead.tSigTrace.u8Dir)

    tSigTraceStruct.u32SFN = tSigHead.u32FrmInf

    u32FrameNo = ((tSigHead.u32FrmInf >> 4)) % 1024
    u32SubFrameNo = (tSigHead.u32FrmInf & 0x0000000F)
    tSigTraceStruct.sFrameInfo = str(u32FrameNo) + ":" + str(u32SubFrameNo)

    u16Year = struct.unpack('<H', tSigHead.tTM.au8Year) + 1900
    tSigTraceStruct.ReportTime = str(u16Year) + "-" + str(tSigHead.tTM.u8Mon + 1) + "-" + \
                                 str(tSigHead.tTM.u8Day) + "  " + str(tSigHead.tTM.u8Hour) + \
                                 ":" + str(tSigHead.tTM.u8Min) + ":" + str(tSigHead.tTM.u8Sec)

def TraceMeParse(data):
    TracemeMsg = TraceMeStruct()
    u32ModuleID, u32PrnLevel, u32ReportTime, u32FramInfo = struct.unpack('<4I', data[0:16])
    achPrintBuff = data[16:len(data)]
    TracemeMsg.u32ModuleNameId = u32ModuleID
    TracemeMsg.PrintLevel = u32PrnLevel
    TracemeMsg.u32ReportTime = u32ReportTime
    TracemeMsg.u32FramInfo = u32FramInfo
    TracemeMsg.PrintText = str(achPrintBuff, encoding='utf-8')

    return TracemeMsg

def GetLinkMsg():
    buffer = struct.pack('<2HI', 0x200E, 0, 0)
    return buffer

def GetSigStartMsg():
    tTraceStartInd = T_TraceStartInd()
    tHead = struct.pack('<2HI', 4366, 0x7C00, 0)
    strIpAddress = '172.16.2.39'
    arryAddres = strIpAddress.split('.')
    tTraceStartInd.au8IPAdress[0] = int(arryAddres[0])
    tTraceStartInd.au8IPAdress[1] = int(arryAddres[1])
    tTraceStartInd.au8IPAdress[2] = int(arryAddres[2])
    tTraceStartInd.au8IPAdress[3] = int(arryAddres[3])

    tTraceStartInd.au8TraceTaskID[0] = 2
    tTraceStartInd.u16PortId = 6080
    tTraceStartInd.u8TraceType = 1
    tTraceStartInd.u8Interface = 0
    tTraceStartInd.u16CellId = 0xFFFF
    tTraceStartInd.u32UEGid = 0xFFFFFFFF

    buffer = tHead + tTraceStartInd.pack()

    return buffer

def GetSigHeartBeat():
    buffer = struct.pack('<2HI', 5134, 0, 0)
    return buffer
