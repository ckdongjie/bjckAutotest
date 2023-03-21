# coding = utf-8
'''
Created on 2022年9月8日

@author: dj
'''
BASIC_DATA = {
    'hms':{
            'ip':'172.16.2.159', #网管登录ip
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
            'upgradeVersion':'BS5514_V1.20.00',#升级目标版本号BS5514_V1.10.60P1B2  BS5514_V1.10.60C0  BS5514_V1.10.80P2
            'upgradeVersion2':'BS5514_V1.10.80P2',#升级目标版本号BS5514_V1.10.80
            'recoverVersion':'BS5514_V1.10.80P3(1)',#回退版本号，weblmt回退时使用
            'versionSavePath':'D:\\autotestPro\\AutoTestMain\\enbVersion',#版本包存在路径
            'xmlSavePath':'D:\\autotestPro\\AutoTestMain\\xmlFile',#配置文件存储目录
            'isCheckData':'true',#是否对配置文件进行检查
            'isCheckCell':True,#是否检查小区状态
            'isDu2.0':False,#是否是Du2.0环境
            'isDownAgain':False,#是否下载中间过度版本
        },
    'VerDetail':{
            'isCheckVerDetail':True,#是否检查小版本信息
            'checkWifiVer':'W6AP-1000_20220929_C00_V07',#目标版本wifi版本号
            'checkFpgaPlVer':'21120707',#目标版本fpga pl版本号
            'checkFpgaPsVer':'cd4d73baa4f801d9d95c3d7a306a0086da946e7f',#目标版本fpga ps版本号
            'checkDPhyVer':'D-PHY-c084df',#目标版本d-phy版本号
            'checkCPhyVer':'C-PHY-V1.10.80',#目标版本c-phy版本号
            'checkCpldVer':'2210291',#目标版本cpld版本号
            'checkGpsVer':'4bd9525882f473e5fadcf1f65639f9bc',#目标版本gps md5值
            'checkNrsysVer':'v21.04.01-306-g7f42f7235-8be957c',#目标版本nrsys版本号
            
            'isCheckRollVerDetail':True,#是否检查版本回退后小版本信息
            'checkRollWifiVer':'W6AP-1000_20220929_C00_V07',#目标版本wifi版本号
            'checkRollFpgaPlVer':'21120707',#目标版本fpga pl版本号
            'checkRollFpgaPsVer':'3a8a1f6875e4061942c082409b2c0d9ee0aebde8',#目标版本fpga ps版本号
            'checkRollDPhyVer':'D-PHY-b84629',#目标版本d-phy版本号
            'checkRollCPhyVer':'C-PHY-V1.10.80',#目标版本c-phy版本号
            'checkRollCpldVer':'2210291',#目标版本cpld版本号
            'checkRollGpsVer':'81b6aefa6fbb61e8051f05cb5b05c25c',#目标版本gps md5值
            'checkRollNrsysVer':'v21.04.01-288-gba4d0d018-2d58059',#目标版本nrsys版本号
            'checkRollUbootVer':'2019.10v21.04.01-498708312',#目标版本nrsys版本号
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
            'ip':'172.16.2.240',# weblmt登录ip地址
            'port':'8090',#weblmt登录端口号
        },
    'gnb':{
            'serialNumberList':'902272840007', #基站序列号902225200003-216;902272840007-240-auto18;902181800017-252-auto17
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
            'nrPort':'5579', #nr灌包端口号
            'wifiPort':'5599',#wifi灌包端口号
            'size':'500m', #灌包流量
            'processNum':'3', #进程个数据
            'dir':'DL', #DL--下行，UL--上行，UDL--上下行
            'iperfLocalPath':'D:\iperf-3.1.3-win64',
            'scrapFileName':'autotest.pcap',
            'pcNetworkCardName':'TP-Link Gigabit PCI Express Adapter',
            'cpePcIp':'192.168.1.16',#cpe连接pc配置的ip地址，用于本地执行iperf灌包命令
            'localPcIp':'172.16.2.138',#抓包用
            'spanTime':60,#灌包时长（单位：秒）,大于60
        },
    'cpeList':{
            'cpeInfo':'192.168.1.1,root,snc123...;192.168.2.1,root,ck123...', #数据格式：cpeIp,cpeUsername,cpePassword
            'pingInterface':'rmnet_data0', #ping包测试使用的网口
        },
    'ping':{
            'testNum':20, #ping测试次数
            'pingNum':20, #ping包次数
            'pingSize':32,#ping包大小
            'logSavePath':'D:\log',#执行log保存路径【预留】
        },
    'attach':{
            'testNum':20, #接入测试次数
            'attachDelay':3, #接入后等待时间（s）
            'detachDelay':3  #去接入后等待时间（s）
        },
    'aps7100':{
            'serialPort':'COM7', #程控电源串口号
            'serialRate':9600  #程控电源串口速率
        },
    'attenuator':{
            'serialPort':'COM8', #程控衰减串口号
            'serialRate':9600  #程控衰减串口速率
        },
    'alarm':{
            'activeBlackList':['gNodeB NG Fault'],
            'activeWhiteList':[],
            'historyBlackList':['gNodeB NG Fault'],
            'historyWhiteList':[]
        }
    }