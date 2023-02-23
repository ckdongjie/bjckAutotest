#coding=utf-8
import struct

#通过minidom解析xml文件
from xml.dom.minidom import parse
import xml.dom.minidom
import os

class EiMsgObj:
    def __init__(self):
        self.strEiMsgName = ''
        self.u32EiMsgId = 0
        self.u16DspId = 0
        self.u16CoreId = 0
        self.CellIdList = [0] * 4
        self.UeIdList = [0] * 40
        self.tEiTlvList = []
        self.tEiStrctLst = []

class EiTlvObj:
    def __init__(self):
        self.strEiTlvName = ''
        self.u32EiTlvId = 0
        self.strEiTlvStructName = ''
        self.bSelected = True
        self.eiStrctObj = EiStructObj()

class EiStructObj:
    def __init__(self):
        self.strStrctName = ''
        self.u16StrctLen = 0
        self.EiVarList = []

class EiVarObj:
    def __init__(self):
        self.strVarName = ''
        self.strVarType = ''
        self.u16Offset = 0
        self.u16Len = 0
        self.bSigned = 0

class T_VarInfo:
    def __init__(self):
        self.strVarName = ''
        self.b8Signed = 0
        self.u16Offset = 0
        self.u16Len = 0

    def pack(self):
        buffer = struct.pack('<47b', *(bytes(self.strVarName.ljust(47, '\0'), encoding="utf-8"))) + \
                 struct.pack('<B2H', self.b8Signed, self.u16Offset, self.u16Len)
        return buffer

class T_TlvInfo:
    def __init__(self):
        self.u32TlvId = 0
        self.strTlvName = ''
        self.u16VarNum = 0
        self.atVarInfo = []
        for i in range(200):
            self.atVarInfo.append(T_VarInfo())

    def pack(self):
        buffer = struct.pack('<I', self.u32TlvId) + struct.pack('<46b', *(bytes(self.strTlvName.ljust(46, '\0'), encoding="utf-8"))) + \
                 struct.pack('<H', self.u16VarNum)
        for i in range(200):
            buffer = buffer + self.atVarInfo[i].pack()
        return buffer


class T_EiMsgInfo:
    def __init__(self):
        self.u32MsgId = 0
        self.strMsgName = ''
        self.u16DspId = 0
        self.u16CoreId = 0
        self.u16CellNum = 0
        self.au16CellId = [0] * 4
        self.u16Resv = 0
        self.u16UeNum = 0
        self.au16UeId = [0] * 40
        self.u16TagNum = 0
        self.u16Resv = 0
        self.atTlvInfo = []
        for i in range(100):
            self.atTlvInfo.append(T_TlvInfo())
    def pack(self):
        buffer = struct.pack('<I', self.u32MsgId) + struct.pack('<64b', *(bytes(self.strMsgName.ljust(64, '\0'), encoding="utf-8"))) + \
                 struct.pack('<8H', self.u16DspId, self.u16CoreId, self.u16CellNum, self.au16CellId[0], self.au16CellId[1],
                             self.au16CellId[2], self.au16CellId[3], self.u16UeNum)
        for i in range(40):
            buffer = buffer + struct.pack('<H', self.au16UeId[i])
        buffer = buffer + struct.pack('<2H', self.u16TagNum, self.u16Resv)
        for i in range(100):
            buffer = buffer + self.atTlvInfo[i].pack()
        return buffer

class T_EISpecificStartItem:
    def __init__(self):
        self.u16MajorId = 0
        self.u16MinorId = 0
        self.u8Index = 0
        self.au8Resv = bytes(3)
        self.u32EiMsgId = 0
        self.u16TagNum = 0
        self.au16Tag = [0] * 100
        self.au8Resv1 = bytes(2)
        self.u16CellNum = 0
        self.au16CellId = [0] * 4
        self.u16UeNum = 0
        self.au16Gid = [0] * 40
    def pack(self):
        buffer = struct.pack('>2HB', self.u16MajorId, self.u16MinorId, self.u8Index) + self.au8Resv + \
                 struct.pack('<IH', self.u32EiMsgId, self.u16TagNum)
        for i in range(0, 100):
            buffer += struct.pack('<H', self.au16Tag[i])
        buffer = buffer + self.au8Resv1 + struct.pack('<6H', self.u16CellNum, self.au16CellId[0], self.au16CellId[1],
                                                      self.au16CellId[2], self.au16CellId[3], self.u16UeNum)
        for i in range(0, 40):
            buffer += struct.pack('<H', self.au16Gid[i])
        return buffer

class T_EiMsgInfoSaveHead:
    def __init__(self):
        self.u32MsgId = 0
        self.strMsgName = ''
        self.u16DspId = 0
        self.u16CoreId = 0
        self.u16CellNum = 0
        self.au8CellId = bytes(3)
        self.u8Resv = 0
        self.u16UeNum = 0
        self.au16UeId = [0] * 40
        self.u16TagNum = 0
        self.u16Resv = 0

class T_TlvInfoHead:
    def __init__(self):
        self.u32TlvId = 0
        self.strTlvName = ''
        self.u16VarNum = 0


def LoadStructList(message, eiMsgObj):
    structs = message.getElementsByTagName("Struct")
    for st in structs:
        eiStrctObj = EiStructObj()
        eiStrctObj.strStrctName = st.getAttribute("name").strip()
        eiStrctObj.u16StrctLen = LoadVarList(st, eiStrctObj)
        eiMsgObj.tEiStrctLst.append(eiStrctObj)

def LoadVarList(st, eiStrctObj):
    Vars = st.getElementsByTagName("Variable")
    u16Len = 0
    for var in Vars:
        tEiVarObj = EiVarObj()
        tEiVarObj.strVarName = var.getAttribute("name").strip()
        tEiVarObj.strVarType = var.getAttribute("type").strip()
        tEiVarObj.u16Offset = u16Len
        tEiVarObj.u16Len = GetTypeLen(tEiVarObj.strVarType)
        u16Len += tEiVarObj.u16Len
        tEiVarObj.bSigned = IsTypeSigned(tEiVarObj.strVarType)

        eiStrctObj.EiVarList.append(tEiVarObj)
    return u16Len

def GetTypeLen(strTypeName):
    if strTypeName == 'B8' or strTypeName == 'S8' or strTypeName == 'U8':
        return 1
    elif strTypeName == 'S16' or strTypeName == 'U16':
        return 2
    elif strTypeName == 'S32' or strTypeName == 'U32':
        return 4
    else:
        return 0

def IsTypeSigned(strTypeName):
    if strTypeName == 'B8' or strTypeName == 'U8' or strTypeName == 'U16' or strTypeName == 'U32':
        return 0
    elif strTypeName == 'S8' or strTypeName == 'S16' or strTypeName == 'S32':
        return 1
    else:
        return 0

def LoadTlvList(message, eiMsgObj):
    Tlvs = message.getElementsByTagName("TLV")
    for tlv in Tlvs:
        eiTlvObj = EiTlvObj()
        eiTlvObj.strEiTlvName = tlv.getAttribute("name").strip()
        eiTlvObj.u32EiTlvId = int(tlv.getAttribute("id"))
        eiTlvObj.strEiTlvStructName = tlv.getAttribute("struct").strip()
        eiTlvObj.eiStrctObj = GetEiStrctObjFromName(eiMsgObj, eiTlvObj.strEiTlvStructName)

        if None == eiTlvObj.eiStrctObj:
            print("加载Struct" + eiTlvObj.strEiTlvStructName + "失败，请检查配置文件")
            return
        eiMsgObj.tEiTlvList.append(eiTlvObj)

def GetEiStrctObjFromName(eiMsgObj, strStrctName):
    for tEiStrctObj in eiMsgObj.tEiStrctLst:
        if tEiStrctObj.strStrctName == strStrctName:
            return tEiStrctObj
    return None

def loadXmlMsgStruct():
    File_DIR = os.path.dirname(os.path.abspath(__file__))
    # 得到文档对象
    DOMTree = xml.dom.minidom.parse(File_DIR+"\\pcapconfig.xml")
    collection = DOMTree.documentElement
    messages = collection.getElementsByTagName("message")
    originalEiMsgObjList = []

    for message in messages:
        msgid = int(message.getAttribute("MsgId"))
        if msgid == 1 or msgid == 301 or msgid == 502:
            continue
        eiMsgObj = EiMsgObj()
        eiMsgObj.strEiMsgName = message.getAttribute("msgname").strip()
        eiMsgObj.u32EiMsgId = int(message.getAttribute("MsgId"))
        eiMsgObj.u16DspId = int(message.getAttribute("DspId"))
        eiMsgObj.u16CoreId = int(message.getAttribute("CoreId"))
        LoadStructList(message, eiMsgObj)
        LoadTlvList(message, eiMsgObj)
        originalEiMsgObjList.append(eiMsgObj)
    return originalEiMsgObjList

def GetActiveEIMsgList():
    tEiMsgList = []
    m_EiMsgObjList = loadXmlMsgStruct()
    for tEiMsgObj in m_EiMsgObjList:
        tEiMsgInfo = T_EiMsgInfo()
        tEiMsgInfo.u32MsgId = tEiMsgObj.u32EiMsgId
        tEiMsgInfo.strMsgName = tEiMsgObj.strEiMsgName
        tEiMsgInfo.u16DspId = tEiMsgObj.u16DspId
        tEiMsgInfo.u16CoreId = tEiMsgObj.u16CoreId
        tEiMsgInfo.u16CellNum = len(tEiMsgObj.CellIdList)
        tEiMsgInfo.au16CellId = tEiMsgObj.CellIdList
        tEiMsgInfo.u16UeNum = len(tEiMsgObj.UeIdList)
        tEiMsgInfo.au16UeId = tEiMsgObj.UeIdList
        tEiMsgInfo.u16TagNum = 0
        for tEiTlvObj in tEiMsgObj.tEiTlvList:
            if tEiTlvObj.bSelected:
                tTlvInfo = T_TlvInfo()
                tTlvInfo.u32TlvId = tEiTlvObj.u32EiTlvId
                tTlvInfo.strTlvName = tEiTlvObj.strEiTlvName
                for tEiVarObj in tEiTlvObj.eiStrctObj.EiVarList:
                    if tTlvInfo.u16VarNum >= 200:
                        break
                    tTlvInfo.atVarInfo[tTlvInfo.u16VarNum].strVarName = tEiVarObj.strVarName
                    tTlvInfo.atVarInfo[tTlvInfo.u16VarNum].u16Len = tEiVarObj.u16Len
                    tTlvInfo.atVarInfo[tTlvInfo.u16VarNum].u16Offset = tEiVarObj.u16Offset
                    tTlvInfo.atVarInfo[tTlvInfo.u16VarNum].b8Signed = tEiVarObj.bSigned
                    tTlvInfo.u16VarNum = tTlvInfo.u16VarNum + 1
                if tEiMsgInfo.u16TagNum >= 100:
                    break
                tEiMsgInfo.atTlvInfo[tEiMsgInfo.u16TagNum] = tTlvInfo
                tEiMsgInfo.u16TagNum =  tEiMsgInfo.u16TagNum + 1
        if tEiMsgInfo.u16TagNum > 0:
            tEiMsgList.append(tEiMsgInfo)

    return tEiMsgList

def GetsvLinkMsg():
    buffer = struct.pack('<2HI', 8974, 0, 0)
    return buffer

def GetsvBasicMsg():
    buffer = struct.pack('<2HI', 12558, 0, 0)
    return buffer

def GetsvSpecificMsg(m_tEiMsgList):
    tHead = struct.pack('<2HI', 12814, 0x700E, 0)
    buffer = tHead
    for tEiMsgInfo in m_tEiMsgList:
        eiSpecificStart = T_EISpecificStartItem()
        eiSpecificStart.u16MajorId = tEiMsgInfo.u16DspId
        eiSpecificStart.u16MinorId = tEiMsgInfo.u16CoreId
        eiSpecificStart.u8Index = 0
        eiSpecificStart.u32EiMsgId = tEiMsgInfo.u32MsgId
        eiSpecificStart.u16TagNum = tEiMsgInfo.u16TagNum
        for i in range(0, 100):
            eiSpecificStart.au16Tag[i] = tEiMsgInfo.atTlvInfo[i].u32TlvId
        eiSpecificStart.u16CellNum = tEiMsgInfo.u16CellNum
        for i in range(0, 4):
            eiSpecificStart.au16CellId[i] = tEiMsgInfo.au16CellId[i]
        eiSpecificStart.u16UeNum = tEiMsgInfo.u16UeNum
        for i in range(0, 40):
            eiSpecificStart.au16Gid[i] = tEiMsgInfo.au16UeId[i]
        buffer = buffer + eiSpecificStart.pack()
    return buffer

def GetsvHeartBeat():
    buffer = struct.pack('<2HI', 5134, 0, 0)
    return buffer