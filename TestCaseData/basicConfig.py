# coding = utf-8
'''
Created on 2022年9月8日

@author: dj
'''
BASIC_DATA = {
    'hms':{
            'ip':'172.16.2.220', #网管登录ip
            'port':'18088', #网管登录端口号
            'omcIp':'193:168:220::212',#网管OMC IP地址
            'username':'root', #网管登录用户名
            'password':'hms123...', #网管登录密码
            
        },
    'url':{
            'ip2':'172.16.2.159',#网管2访问ip地址
            'omcIp2':'193:168:220::254',#网管OMC IP地址-正常ip
            'erroromcIp':'193:168:6::200',#网管OMC IP地址-异常ip
        },
    'common':{
            'isCheckCell':True,#是否检查小区状态
            'isCheckData':'true',#是否对配置文件进行检查
            'gnbType':'BS5514',#是否是Du2.0环境 BS5514/BS5120/BS5524
            'isPing':True,#是否ping包测试
            'isAttach':True,#是否接入测试
            'isTraffic':False,#是否流量测试
            'ueType':'CPE',#终端类型：CPE/mate30/xiaomi
        },
    'version':{
            'verBranch':'BS5514_V1.30.20B3_JP_V2_V4', #冒烟测试监测的版本分支号BS5514_V1.30.30_d82c68.zip
            'upgradeVersion':'BS5514_V1.20.00',#升级目标版本号BS5514_V1.10.60P1B2  BS5514_V1.10.60C0  BS5514_V1.10.80P2  BS5514_V1.20.20
            'upgradeVersion2':'BS5514_V1.20.20P1',#升级目标版本号BS5514_V1.10.80
            'recoverVersion':'BS5514_V1.20.20',#回退版本号，weblmt回退时使用
            'isDownAgain':False,#是否下载中间过度版本
            'isRollback':True,#版本升级后是否回退
        },
    'polSoft':{
            'isRoll':True,#是否执行版本回退
            'activeVersion':'BS5514_V1.20.20',#升级目标版本号BS5514_V1.10.60P1B2  BS5514_V1.10.60C0  BS5514_V1.10.80P2  BS5514_V1.20.20
            'rollVersion':'BS5514_V1.20.00P1',#回退版本号，反复升级时使用
            "policyName":"", #策略名，为空时自动生成格式：auto_time
            "policyStatus":"1", # 0-suspend  1-active
            "downloadFlag":"1",# 0-no download 1-download
            "triggerMode":"0",# 0-time 1-event
            "times":"",# download time, triggerMode是0时需要配置
            "triggerType":"",#下载触发类型 
            "startTime":"", #触发起时间,triggerMode是1时需要配置
            "endTime":"", #触发终时间,triggerMode是1时需要配置
            "activateType":"1",# 激活类型  0-不激活  1-下载后激活   2--时间激活
            "timerActivateTime":"",#激活时间,activateType是2时需要配置
            "gnbSerList":["902106900049"],#gnb序号号，用，分割
        },
    'VerDetail':{
            'isCheckVerDetail':False,#是否检查小版本信息
            'checkWifiVer':'W6AP-1000_20230627_C00_V08',#目标版本wifi版本号
            'checkFpgaPlVer':'22040905',#目标版本fpga pl版本号
            'checkFpgaPsVer':'e9f5161115c68d84fafe38b15d7f08bdcdc3c311',#目标版本fpga ps版本号
            'checkDPhyVer':'D-PHY-c084df',#目标版本d-phy版本号
            'checkCPhyVer':'C-PHY-V1.20.20',#目标版本c-phy版本号
            'checkCpldVer':'229231',#目标版本cpld版本号
            'checkGpsVer':'2c6f55b9b19f21275f6fa167002669fc',#目标版本gps md5值
            'checkNrsysVer':'v21.04.01-330-gc24ccaf96-c9ecd90',#目标版本nrsys版本号
            'checkAipVer':'',#目标版本Aip版本号
            
            'isCheckRollVerDetail':False,#是否检查版本回退后小版本信息
            'checkRollWifiVer':'W6AP-1000_20220929_C00_V07',#目标版本wifi版本号
            'checkRollFpgaPlVer':'22040904',#目标版本fpga pl版本号
            'checkRollFpgaPsVer':'53f9da6aaff41aaf6ff03838916d026ef45326b5',#目标版本fpga ps版本号
            'checkRollDPhyVer':'D-PHY-c084df',#目标版本d-phy版本号
            'checkRollCPhyVer':'C-PHY-V1.20.00',#目标版本c-phy版本号
            'checkRollCpldVer':'229231',#目标版本cpld版本号
            'checkRollGpsVer':'e369d6d035b429394b6988bc77563b5e',#目标版本gps md5值
            'checkRollNrsysVer':'v21.04.01-319-g74c49b873-8be957c',#目标版本nrsys版本号
            'checkRollUbootVer':'v21.04.01-291-ga21f3cc5b-bc5cb85',#目标版本nrsys版本号
            'checkRollAipVer':'',#目标版本Aip版本号
        },
    'cpe':{
            'cpeSshIp':'192.168.1.1', #cpe ssh登录ip地址
            'cpeUsername':'root', #cpe ssh登录的用户名
            'cpePassword':'snc123...', #cpe ssh登录的密码
            'pingNrInterface':'rmnet_data0', #ping测试使用的端口  rmnet_data0--NR，ath0--Wifi
            'pingWifiInterface':'ath0',#ping测试使用的端口  rmnet_data0--NR，ath0--Wifi
        },
    'weblmt':{
            'ip':'172.16.3.240',# weblmt登录ip地址
            'port':'8090',#weblmt登录端口号
        },
    'gnb':{
            'serialNumberList':'902181800017', #基站序列号902225200003-216;902272840007-253-auto18;902181800017-240-auto17
            'cellIdList':[1], #基站小区id列表
            'username':'root',#基站debug登录用户名
            'password':'Web2022@Nr5gTech',#基站debug登录密码
        },
    'gnbSerial':{
            '2160Port':'COM14',
            '2160PortRate':115200,
            'psPort':'COM15',
            'psPortRate':115200
        },
    'pdn':{
            'pdnSshIp':'172.16.2.202', #pdn ssh登录ip地址  172.16.2.202-root-root123...-192.168.9.223 172.16.2.157-root/ck1234...
            'pdnUsername':'root', #pdn ssh登录的用户名
            'pdnPassword':'root123...', #pdn ssh登录的密码
            'pdnIp':'193.168.9.223',#pdn业务ip
        },
    'phone':{
            'phoneType':'mate30', #手机类型
            'serialPort':'COM98', #mate30串口通信端口
            'serialRate':115200, #串口通信比特率
            'ueIp':'190.1.41.85',#mate30时需要配置
            'iperfPort':'5201',#iperf灌包使用的端口号，需要手工在手机上启动iperf监听进程
        },
    'traffic':{
            'isCheckTraffic':True,# 是否对流量进行校验
            'isLocalExec':True,# 是否在pc上执行iperf, False时在cpe上启动iperf
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
            'iperfLocalPath':'D:\\iperf-3.1.3-win64',#本地iperf路径
            'scrapFileName':'autotest.pcap',#抓包文件名
            'pcNetworkCardName':'ASIX AX88772C USB2.0 to Fast Ethernet Adapter #4',#抓包对应的网卡  TP-Link Gigabit PCI Express Adapter///Realtek PCIe GbE Family Controller
            'cpePcIp':'192.168.1.5',#cpe连接pc配置的ip地址，用于本地执行iperf灌包命令
            'localPcIp':'172.16.3.200',#抓包用
            'spanTime':60,#灌包时长（单位：秒）
            'expNearDlTcpTraf':80,#下行期望流量
            'expNearUlTcpTraf':25,#上行期望流量
            'expFarDlTcpTraf':60,#下行期望流量
            'expFarUlTcpTraf':20,#上行期望流量
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
            'isCheckPing':False,#是否对ping包结果进行校验
            'pingType':'both',# cpe/pc/both
            'pingNum':20, #ping包次数
            'pingSize':32,#ping包大小
            'logSavePath':'D:\\log',#执行log保存路径【预留】
            'loseRate':50,#ping包丢包率
            'pingAvg':300,#ping包平均时延
        },
    'attach':{
            'isCheckSuccRate':True,#是否对接入成功率进行校验
            'attachDelay':3, #接入后等待时间（s）
            'detachDelay':3,  #去接入后等待时间（s）
            'succRate':100, #接入成功率
        },
    'power':{
            'powerType':'aps7100',#aps7100;delixi
            'serialPort':'COM7', #程控电源串口号
            'serialRate':9600  #程控电源串口速率
        },
    'attenuator':{
            'serialPort':'COM21', #程控衰减串口号
            'serialRate':9600, #程控衰减串口速率
            'nearPoint':0,#近点衰减值
            'midPoint':20,#中点衰减值
            'farPoint':40,#远点衰减值
        },
    'alarm':{
            'activeBlackList':['gNodeB NG Fault', 'NR Cell Unavailable'],#当前告警黑名单
            'activeWhiteList':[],#当前告警白名单
            'historyBlackList':['gNodeB NG Fault', 'NR Cell Unavailable'],#历史告警黑名单
            'historyWhiteList':[]#历史告警白名单
        },
    'maintenanceTool':{
            'isSaveSig':True, #是否打开信令跟踪
            'isSaveTrace':True,#是否打开trace me
            'isSaveSvBasic':True, #是否保存基本ei文件
            'isSaveSvDetail':True,#是否保存ei明细
            'isSaveQxdm':True,#是否跟踪qxdm log
        }
    }