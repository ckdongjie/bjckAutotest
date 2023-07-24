import struct

class T_EIGeneralInfo:
    def __init__(self):
        self.u16CellID = 0
        self.u8OpticPort = 0
        self.u8IsSuperCell = 0
        self.u8FreqBandInd = 0
        self.u16CellLiveCount = 0
        self.tEICellGeneralCfg = T_EICellGeneralCfg()
        self.tEICellGeneralState = T_EICellGeneralState()
        self.tEICellULDetailState = T_EICellULDetailState()
        self.tEICellDLDetailState = T_EICellDLDetailState()
        self.tEIUEGeneralList = T_EIUEGeneralList()
    def packCell(self):
        buffer = struct.pack('<H3BHB', self.u16CellID, self.u8OpticPort, self.u8IsSuperCell, self.u8FreqBandInd, self.u16CellLiveCount, 0) \
                 + self.tEICellGeneralCfg.pack() + self.tEICellGeneralState.pack() + self.tEICellULDetailState.pack() + self.tEICellDLDetailState.pack()
        return buffer


class T_EICellGeneralCfg:
    def __init__(self):
        self.u32EnbId = 0
        self.u32CellCenterFreq = 0
        self.u16CellPCI = 0
        self.u8CellBandWidth = 0
        self.u8CellULDLConfig = 0
        self.u8CellSpecSubFramCfg = 0
        self.u8CellULAntNum = 0
        self.u8CellDLAntNum = 0
        self.au8CpEnable = bytes(3)
        self.au8CpPort = bytes(3)
        self.u8Index = 0
        self.au8Rcv = bytes(2)
    def pack(self):
        buffer = struct.pack('<2IH14B',self.u32EnbId, self.u32CellCenterFreq, self.u16CellPCI, self.u8CellBandWidth,
                             self.u8CellULDLConfig, self.u8CellSpecSubFramCfg, self.u8CellULAntNum, self.u8CellDLAntNum,
                             self.au8CpEnable[0], self.au8CpEnable[1], self.au8CpEnable[2], self.au8CpPort[0], self.au8CpPort[1],
                             self.au8CpPort[2], self.u8Index, self.au8Rcv[0], self.au8Rcv[1])
        return buffer

class T_EICellGeneralState:
    def __init__(self):
        self.u16SFN = 0
        self.u16ActiveUENum = 0
        self.s16NI = 0
        self.u8TXPower = 0
        self.u8Rcv = 0
        self.as16SubNI = [0] * 273
        self.u16Rsv = 0
    def pack(self):
        buffer = struct.pack('<2Hh2B', self.u16SFN, self.u16ActiveUENum, self.s16NI, self.u8TXPower, self.u8Rcv)
        for i in range(0,273):
            buffer = buffer + struct.pack('<h', self.as16SubNI[i])
        buffer = buffer + struct.pack('<H', self.u16Rsv)
        return buffer

class T_EICellULDetailState:
    def __init__(self):
        self.u32CellULMacThroughput = 0
        self.u32CellULRlcThrput = 0
        self.u32CellULPdcpThrput = 0
        self.u32CellULWifiThrput = 0 # add dj
        self.u8ULRbRatio = 0
        self.u8CellULSchdUeNumPerTti = 0
        self.u8CellULAvrHarqTxCnt = 0
        self.u8CellULBler = 0
        self.u16CellULHarqFailRatio = 0
        self.u16CellULHarqSelfMaintainRatio = 0
        self.au16AvrgULMcs = [0] * 4
        self.u16CellULHqRetSuccRatio1 = 0
        self.u16CellULHqRetSuccRatio2 = 0
        self.u16CellULHqRetSuccRatio3 = 0
        self.u16CellULHqRetSuccRatio4 = 0
        self.u16CellULMaxSchdTaskTime = 0
        self.u16CellULMaxPhyMgrTaskTime = 0
        self.u32MaxTotalTaskTime = 0

    def pack(self):
        buffer = struct.pack('<4I4B12HI', self.u32CellULMacThroughput, self.u32CellULRlcThrput, self.u32CellULPdcpThrput, self.u32CellULWifiThrput, self.u8ULRbRatio,
                             self.u8CellULSchdUeNumPerTti, self.u8CellULAvrHarqTxCnt, self.u8CellULBler, self.u16CellULHarqFailRatio,
                             self.u16CellULHarqSelfMaintainRatio,self.au16AvrgULMcs[0], self.au16AvrgULMcs[1], self.au16AvrgULMcs[2],
                             self.au16AvrgULMcs[3], self.u16CellULHqRetSuccRatio1, self.u16CellULHqRetSuccRatio2, self.u16CellULHqRetSuccRatio3,
                             self.u16CellULHqRetSuccRatio4, self.u16CellULMaxSchdTaskTime, self.u16CellULMaxPhyMgrTaskTime, self.u32MaxTotalTaskTime)
        return buffer

class T_EICellDLDetailState:
    def __init__(self):
        self.u32CellDLMacThroughput = 0
        self.u32CellDLRlcThrput = 0
        self.u32CellDLPdcpThrput = 0
        self.u32CellDLWifiThrput = 0  # add dj
        self.u8DLRbRatio = 0
        self.u8CellDLSchdUeNumPerTti = 0
        self.u8CellDLAvrHarqTxCnt = 0
        self.u8CellDLBler = 0
        self.u16CellDLHarqFailRatio = 0
        self.u16CellDLHarqSelfMaintainRatio = 0
        self.au16AvrgDLMcs = [0] * 4
        self.u16DtxRatio = 0
        self.u8CellDLTxLayerRatio1 = 0
        self.u8CellDLTxLayerRatio2 = 0
        self.u8CellDLTxLayerRatio3 = 0
        self.u8CellDLTxLayerRatio4 = 0
        self.u16CellDLHqRetSuccRatio1 = 0
        self.u16CellDLHqRetSuccRatio2 = 0
        self.u16CellDLHqRetSuccRatio3 = 0
        self.u16CellDLHqRetSuccRatio4 = 0
        self.u16CellDLMaxSchdTaskTime = 0

    def pack(self):
        buffer = struct.pack('<4I4B7H4B5H', self.u32CellDLMacThroughput, self.u32CellDLRlcThrput, self.u32CellDLPdcpThrput, self.u32CellDLWifiThrput, self.u8DLRbRatio,
                             self.u8CellDLSchdUeNumPerTti, self.u8CellDLAvrHarqTxCnt, self.u8CellDLBler, self.u16CellDLHarqFailRatio,
                             self.u16CellDLHarqSelfMaintainRatio, self.au16AvrgDLMcs[0], self.au16AvrgDLMcs[1],self.au16AvrgDLMcs[2],self.au16AvrgDLMcs[3],
                             self.u16DtxRatio, self.u8CellDLTxLayerRatio1, self.u8CellDLTxLayerRatio2, self.u8CellDLTxLayerRatio3, self.u8CellDLTxLayerRatio4,
                             self.u16CellDLHqRetSuccRatio1, self.u16CellDLHqRetSuccRatio2, self.u16CellDLHqRetSuccRatio3, self.u16CellDLHqRetSuccRatio4, self.u16CellDLMaxSchdTaskTime)
        return buffer

class T_EIUEGeneralList:
    def __init__(self):
        self.u32UENum = 0
        self.atEIUEGeneralInfo = []
        for i in range(3600):
            self.atEIUEGeneralInfo.append(T_EIUEGeneralInfo())

class T_EIUEGeneralInfo:
    def __init__(self):
        self.u8UELiveCount = 0
        self.u8IsUsed = 0
        self.u8PL = 0
        self.u32ULPdcpThrput = 0
        self.u32ULRlcThrput = 0
        self.u32DLPdcpThrput = 0
        self.u32DLRlcThrput = 0
        self.u64IP = 0
        self.u32ULMacThrput = 0
        self.u32DLMacThrput = 0
        self.u16ULSchdCnt = 0
        self.u16DLSchdCnt = 0
        self.u16ULHarqFailRatio = 0
        self.u16DLHarqFailRatio = 0
        self.u16ULHarqExpireRatio = 0
        self.u16DLHarqExpireRatio = 0
        self.au16ULAvrgMcs = [0] * 4
        self.au16DLAvrgMcs = [0] * 4
        self.u8ULAvrgHarqTxCnt = 0
        self.u8DLAvrgHarqTxCnt = 0
        self.u16ULAvrgRbNum = 0
        self.u16DLAvrgRbNum = 0
        self.u8ULAvrgBler = 0
        self.u8DLAvrgBler = 0
        self.u16DtxRatio = 0
        self.s16Sinr = 0

    def pack(self):
        buffer = struct.pack('<4B4IQ2I14H2B2H2BHh', self.u8UELiveCount, self.u8IsUsed, self.u8PL, 0, self.u32ULPdcpThrput, self.u32ULRlcThrput,
                             self.u32DLPdcpThrput, self.u32DLRlcThrput, self.u64IP, self.u32ULMacThrput, self.u32DLMacThrput, self.u16ULSchdCnt, self.u16DLSchdCnt,
                             self.u16ULHarqFailRatio, self.u16DLHarqFailRatio, self.u16ULHarqExpireRatio, self.u16DLHarqExpireRatio, self.au16ULAvrgMcs[0],
                             self.au16ULAvrgMcs[1],self.au16ULAvrgMcs[2],self.au16ULAvrgMcs[3],self.au16DLAvrgMcs[0],self.au16DLAvrgMcs[1],self.au16DLAvrgMcs[2],
                             self.au16DLAvrgMcs[3], self.u8ULAvrgHarqTxCnt, self.u8DLAvrgHarqTxCnt, self.u16ULAvrgRbNum, self.u16DLAvrgRbNum, self.u8ULAvrgBler,
                             self.u8DLAvrgBler, self.u16DtxRatio, self.s16Sinr)
        return buffer

class T_EICellTabDspStateList:
    def __init__(self):
        self.u8ActiveCellNum = 0
        self.au16CellID = [0] * 4
        self.bIsUsedCell1 = False
        self.bIsUsedCell2 = False
        self.bIsUsedCell3 = False
        self.bIsUsedCell4 = False
