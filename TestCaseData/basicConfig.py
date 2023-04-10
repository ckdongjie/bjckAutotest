# coding = utf-8
'''
Created on 2022年9月8日

@author: dj
'''
BASIC_DATA = {
    'hms':{
            'ip':'172.16.2.220', #网管登录ip
            'port':'18088', #网管登录端口号
            'username':'root', #网管登录用户名
            'password':'hms123...', #网管登录密码
            'omcIp':'193:168:220::254',#网管OMC IP地址
            'ip2':'172.16.2.220',#网管2访问ip地址
            'omcIp2':'193:168:220::212',#网管OMC IP地址-正常ip
            'erroromcIp':'193:168:6::200',#网管OMC IP地址-异常ip
        },
    'version':{
            'verBranch':'BS5514_V1.30.20B3_JP_V2_V4', #冒烟测试监测的版本分支号BS5514_V1.30.30_d82c68.zip
            'upgradeVersion':'BS5514_V1.10.80P3B0',#升级目标版本号BS5514_V1.10.60P1B2  BS5514_V1.10.60C0  BS5514_V1.10.80P2
            'upgradeVersion2':'BS5514_V1.10.80P2',#升级目标版本号BS5514_V1.10.80
            'recoverVersion':'BS5514_V1.10.60P1B1',#回退版本号，weblmt回退时使用
            'versionSavePath':'D:\\bjckAutotest\\AutoTestMain\\enbVersion',#版本包存在路径
            'xmlSavePath':'D:\\autotestPro\\AutoTestMain\\xmlFile',#配置文件存储目录
            'isCheckData':'true',#是否对配置文件进行检查
            'isCheckCell':True,#是否检查小区状态
            'isDu2.0':False,#是否是Du2.0环境
            'isDownAgain':True,#是否下载中间过度版本
        },
    'VerDetail':{
            'isCheckVerDetail':True,#是否检查小版本信息
            'checkWifiVer':'W6AP-1000_20220929_C00_V07',#目标版本wifi版本号
            'checkFpgaPlVer':'21120707',#目标版本fpga pl版本号
            'checkFpgaPsVer':'36c9992b252c292f31cfe72a79845bcb94ceabd6',#目标版本fpga ps版本号
            'checkDPhyVer':'D-PHY-b84629',#目标版本d-phy版本号
            'checkCPhyVer':'C-PHY-V1.10.80',#目标版本c-phy版本号
            'checkCpldVer':'2210291',#目标版本cpld版本号
            'checkGpsVer':'01f93c3ada4fb2c43bac3c3e70f79409',#目标版本gps md5值
            'checkNrsysVer':'v21.04.01-292-ge38709aa2-bc5cb85',#目标版本nrsys版本号
            
            'isCheckRollVerDetail':True,#是否检查版本回退后小版本信息
            'checkRollWifiVer':'W6AP-1000_20220428_C00_V06',#目标版本wifi版本号
            'checkRollFpgaPlVer':'20211207',#目标版本fpga pl版本号
            'checkRollFpgaPsVer':'3329feda4a45a61cea49ed51d075072d44245d8e',#目标版本fpga ps版本号
            'checkRollDPhyVer':'D-PHY-7527f2',#目标版本d-phy版本号
            'checkRollCPhyVer':'C-PHY-V1.10.60P1',#目标版本c-phy版本号
            'checkRollCpldVer':'2210291',#目标版本cpld版本号
            'checkRollGpsVer':'c2296c8f696dd3ef6599c4227ffd32b2',#目标版本gps md5值
            'checkRollNrsysVer':'',#目标版本nrsys版本号
            'checkRollUbootVer':'2019.10v21.04.01-233-gc37076749',#目标版本nrsys版本号
        },
    'cpe':{
            'cpeSshIp':'192.168.1.1', #cpe ssh登录ip地址
            'cpeUsername':'root', #cpe ssh登录的用户名
            'cpePassword':'snc123...', #cpe ssh登录的密码
            'pingNrInterface':'rmnet_data0', #ping测试使用的端口  rmnet_data0--NR，ath0--Wifi
            'pingWifiInterface':'ath0',#ping测试使用的端口  rmnet_data0--NR，ath0--Wifi
            'isPing':False,#是否ping包测试
            'isAttach':False,#是否接入测试
            'isFlow':False,#是否流量测试
            'ueLogSavePath':'D:\\autotestPro\\AutoTestMain\\qxdmLog',#ue log文件保存路径
            'ueLogBackup':'D:\\autotestPro\\AutoTestMain\\qxdmLog\\backup',# ue log备份路径
        },
    'weblmt':{
            'ip':'172.16.3.151',# weblmt登录ip地址
            'port':'8090',#weblmt登录端口号
        },
    'gnb':{
            'serialNumberList':'902192700033', #基站序列号902225200003-216;902272840007-240-auto18;902181800017-252-auto17
            'cellIdList':0, #基站小区id列表
            'username':'root',#基站debug登录用户名
            'password':'Web2022@Nr5gTech',#基站debug登录密码
        },
    'pdn':{
            'pdnSshIp':'172.16.2.202', #pdn ssh登录ip地址
            'pdnUsername':'root', #pdn ssh登录的用户名
            'pdnPassword':'ck2022...', #pdn ssh登录的密码
            'pdnIp':'193.168.9.223',#pdn业务ip
        },
    'mate30':{
            'serialPort':'COM98', #mate30串口通信端口
            'serialRate':115200, #串口通信比特率
            'ueIp':'192.170.9.65',#UE ip地址，用于ping包测试
        },
    'flow':{
            'type':'TCP',#UDP/TCP
            'nrUlPort':'8989', #nr灌包端口号
            'nrDlPort':'8999', #nr灌包端口号
            'wifiUlPort':'5598',#wifi灌包端口号
            'wifiDlPort':'5599',#wifi灌包端口号
            'udpUlSize':'500m', #udp上行灌包大小
            'udpDlSize':'500m',#udp下行灌包大小
            'tcpUlSize':'1400k',#tcp上行灌包大小
            'tcpDlSize':'1400k',#tcp下行灌包大小
            'processNum':'10', #进程个数据
            'dir':'DL', #DL--下行，UL--上行，UDL--上下行
            'iperfLocalPath':'D:\iperf-3.1.3-win64',#本地iperf路径
            'scrapFileName':'autotest.pcap',#抓包文件名
            'pcNetworkCardName':'TP-Link Gigabit PCI Express Adapter',#抓包对应的网卡
            'cpePcIp':'192.168.1.200',#cpe连接pc配置的ip地址，用于本地执行iperf灌包命令
            'localPcIp':'172.16.2.138',#抓包用
            'spanTime':180,#灌包时长（单位：秒）,大于60
            'expNearDlTcpTraf':180,#下行期望流量
            'expNearUlTcpTraf':90,#上行期望流量
            'expFarDlTcpTraf':180,#下行期望流量
            'expFarUlTcpTraf':90,#上行期望流量
            'expNearDlUdpTraf':180,#下行期望流量
            'expNearUlUdpTraf':90,#上行期望流量
            'expFarDlUdpTraf':180,#下行期望流量
            'expFarUlUdpTraf':90,#上行期望流量
        },
    'cpeList':{
            'cpeInfo':'192.168.1.1,root,snc123...;192.168.2.1,root,ck123...', #数据格式：cpeIp,cpeUsername,cpePassword
            'pingInterface':'rmnet_data0', #ping包测试使用的网口
        },
    'ping':{
            'pingNum':10, #ping包次数
            'pingSize':32,#ping包大小
            'logSavePath':'D:\log',#执行log保存路径【预留】
            'loseRate':0,#ping包丢包率
            'pingAvg':15,#ping包平均时延
        },
    'attach':{
            'attachDelay':3, #接入后等待时间（s）
            'detachDelay':3,  #去接入后等待时间（s）
            'succRate':100, #接入成功率
        },
    'power':{
            'powerType':'aps7100',#程控电源类型
            'serialPort':'COM7', #程控电源串口号
            'serialRate':9600  #程控电源串口速率
        },
    'attenuator':{
            'serialPort':'COM21', #程控衰减串口号
            'serialRate':9600  #程控衰减串口速率
        },
    'alarm':{
            'activeBlackList':['gNodeB NG Fault', 'NR Cell Unavailable'],
            'activeWhiteList':[],
            'historyBlackList':['gNodeB NG Fault', 'NR Cell Unavailable'],
            'historyWhiteList':[]
        }
    }