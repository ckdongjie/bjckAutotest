# coding = utf-8 
'''
Created on 2022年9月8日

@author: dj

以下模板包括已经开发的所有用例，
用例模板说明：
        测试用例：配置参数（基础参数需要在basicConfig中配置）
'''
TESTCASE_SAMPLE = {
    #------------alarm-----------------
    '当前告警查询':[],#查询当前告警是否符合预期
    '历史告警查询':[('time1', 'time2')],#查询指定时间段的告警是否符合预期
    'wifi小区退服告警上报及恢复':[],#wifi小区退服告警触发及恢复
    'wifi小区退服告警及DFS告警上报及恢复':[],#wifi小区退服及DFS告警上报及恢复
    'wifi板复位':[],#wifi板复位告警触发及恢复
    'omc复位基站检查wifi状态':[],#omc复位基站检查wifi状态及告警
    'SCTP异常告警上报及恢复':[],#sctp异常告警触发及恢复
    'DU小区闭塞告警上报及恢复':[],#du小区闭塞告警触发及恢复
    '基站退服告警上报及恢复':[],#基站退服告警上报及恢复
    '小区退服告警上报及恢复':[],#小区退服告警上报及恢复
    'Ng故障告警上报及恢复':[],#ng故障告警上报及恢复
    'SSH登录告警上报及恢复':[],#ssh登录基站告警上报及恢复
    '串口登录基站告警上报及恢复':[],#串口登录基站告警上报及恢复
    '基站过温告警上报及恢复':[],#基站过温告警上报及恢复，修改参数触发
    '基站低压告警上报及恢复':[],#基站低压告警上报及恢复，修改参数触发
    '基站过压告警上报及恢复':[],#基站过压告警上报及恢复，修改参数触发
    '基站内存使用率过高告警上报及恢复':[],#基站内存使用率过高告警上报及恢复，修改参数触发
    '基站CPU使用率过高告警上报及恢复':[],#基站cpu使用率过高告警上报及恢复，修改参数触发
    #---------------omc config------------------
    '更新omcIp地址_地址正确且基站已注册':[(1)],#修改基站url配置地址切换网管，目标网管上基站已经注册
    '更新omcIp地址_地址正确但基站未注册':[(1)],#修改基站url配置地址切换网管，目标网管上基站未注册
    '更新omcIp地址_地址错误':[(1)],#修改基站url配置地址切换网管，url地址异常
    'SSB发射功率修改':[(-10)],#修改基站rsrp参数
    '本地时钟和GPS切换测试':[],#基站本地时钟和gps参数切换测试
    'SCTP目标端口号修改':[],#修改sctp参数
    #------------gnb reboot-----------------
    '复位基站正常后ping包':[(100)],#omc上复位基站，基站启动小区正常后cpe接入ping包测试
    '闭塞小区后复位基站':[(100)],#omc上闭塞小区，复位基站，基站启动后解闭塞小区，小区正常后cpe接入ping包测试
    #--------------cell ping--------------------
    '反复闭塞解闭塞小区并ping包测试':[(20)],#闭塞解闭塞小区，小区正常后cpe接入ping包测试
    '反复去激活激活小区并ping包测试':[(20)],#去激活激活小区，小区正常后cpe接入ping包测试
    #------------omc diga-----------------
    '基站ping包诊断测试':[],#基站ping包诊断
    '基站跟踪路由诊断测试':[],#基站跟踪路由诊断
    #------------gnb 5524-----------------
    '复位基站正常后ping包_5524':[(100)],#5524基站复位启动正常后ping包测试
    #------------gnb power-----------------
    '基站下电上电后CEP接入成功率测试':[(100)],#基站上下电后cpe接入成功率测试
    '基站随机上下电压测':[(100)],#基站随机上下电压测
    '整机上下电本地时钟测试':[],#基站上下电本地时钟测试
    '整机复位本地时钟测试':[],#基站复位本地时钟测试
    '基站掉电复位基站检查wifi状态':[],#基站下电上电后检查wifi状态
    '基站下电告警上报及恢复':[],#基站下电上电后检查下电告警上报及恢复
    #------------cpe power-----------------
    'CPE下电上电后接入成功率测试':[(100)],#cpe上下电后接入成功率测试
    #------------单cpe-----------------
    'CPE注册去注册后接入成功率测试':[(20)],#cpe接入去接入操作接入成功率测试
    'CPE复位后接入成功率测试':[(20)],#cpe复位cpe接入成功率测试
    '基站复位后CPE接入成功率测试':[(20)],#基站复位cpe接入成功率测试
    '去激活激活小区后CPE接入成功率测试':[(20)],#小区去激活激活后cpe接入成功率测试
    '闭塞解闭塞小区后接入成功率测试':[(20)],#小区闭塞解闭塞后cpe接入成功率测试
    'ping包测试_CPE':[],#cpe ping包测试
    'NR上行TCP流量测试_CPE':[],#cpe上行nr tcp流量测试
    'WIFI上行TCP流量测试_CPE':[],#cpe上行wifi tcp流量测试
    'NR下行TCP流量测试_CPE':[],#cpe下行nr tcp流量测试
    'WIFI下行TCP流量测试_CPE':[],#cpe下行wifi tcp流量测试
    'NR上下行TCP流量测试_CPE':[],#cpe上下行nr tcp流量测试
    'WIFI上下行TCP流量测试_CPE':[],#cpe上下行wifi tcp流量测试
    'NR上行UDP流量测试_CPE':[],#cpe上行nr udp流量测试
    'WIFI上行UDP流量测试_CPE':[],#cpe上行wifi udp流量测试
    'NR下行UDP流量测试_CPE':[],#cpe下行nr udp流量测试
    'WIFI下行UDP流量测试_CPE':[],#cpe下行wifi udp流量测试
    'NR上下行UDP流量测试_CPE':[],#cpe上下行nr udp流量测试
    'WIFI上下行UDP流量测试_CPE':[],#cpe上下行wifi udp流量测试
    '关闭打开通道射频后CPE接入ping测试':[(1)],#关闭打开射频通道后cpe接入ping包测试
    '关闭2s后打开通道射频CPE接入ping测试':[1],#关闭射频通道2s后打开射频通道，cpe接入ping包测试
    '设置程控衰减极值恢复后接入ping测试':[(1)],#使用程控衰减，设置衰减值到极值后再恢复，恢复后cpe接入ping包测试
    '设置程控衰减极值等待2秒恢复后接入ping测试':[(1)],#使用程控衰减，设置衰减值到极值后等待2s再恢复，恢复后cpe接入ping包测试
    '程控衰减近点ping包测试':[(1)],#使用程控衰减打点到-70点位进行ping包测试
    '程控衰减远点ping包测试':[(1)],#使用程控衰减打点到-100点位进行ping包测试
    '程控衰减近点tcp上行流量测试':[],#使用程控衰减打点到-70点位进行tcp上行流量测试
    '程控衰减近点tcp下行流量测试':[],#使用程控衰减打点到-70点位进行tcp下行流量测试
    '程控衰减近点tcp上下行流量测试':[],#使用程控衰减打点到-70点位进行tcp上下行流量测试
    '程控衰减远点tcp上行流量测试':[],#使用程控衰减打点到-100点位进行tcp上行流量测试
    '程控衰减远点tcp下行流量测试':[],#使用程控衰减打点到-100点位进行tcp下行流量测试
    '程控衰减远点tcp上下行流量测试':[],#使用程控衰减打点到-100点位进行tcp上下行流量测试
    '程控衰减tcp上下行流量打点测试':[],#使用程控衰减循环打点进行tcp上下行流量测试
    #----------mate30--------------
    'Mate30注册去注册后接入成功率测试':[(1)],#mate30手机注册去注册后接入成功率测试
    '去激活激活小区后mate30接入成功率测试':[(1)],#小区激活去激活后mate30接入成功率测试
    '闭塞解闭塞小区后Mate30接入成功率测试':[(1)],#小区闭塞解闭塞后mate30接入成功率测试
    #-----------多CPE-------------------
    '多CPE注册去注册后接入成功率测试':[(1)],#多cpe场景，注册去注册后接入成功率测试
    '多CPE复位后接入成功率测试':[(1)],#多cpe场景，cpe复位后接入成功率测试
    '基站复位后多CPE接入成功率测试':[(1)],#多cpe场景，基站复位后接入成功率测试
    '去激活激活小区后多CPE接入成功率测试':[(1)],#多cpe场景，小区去激活激活后接入成功率测试
    '闭塞解闭塞小区后多CPE接入成功率测试':[(1)],#多cpe场景，小区闭塞解闭塞后接入成功率测试
    '关闭打开通道射频后多CPE接入ping测试':[(1)],#多cpe场景，关闭打开射频通道后接入成功率测试
    '关闭2s后打开通道射频多CPE接入ping测试':[(1)],#多cpe场景，关闭射频通道2s后打开射频通道，cpe接入成功率测试
    '设置程控衰减极值恢复后多CPE接入ping测试':[(1)],#多cpe场景，使用程控衰减设置衰减到极值后再恢复，cpe接入成功率测试
    '设置程控衰减极值等待2秒恢复后多CPE接入ping测试':[(1)],#多cpe场景，使用程控衰减设置衰减到极值后等待2s后再恢复，cpe接入成功率测试
    '多CPE下行UDP流量测试':[],#多cpe场景，下行UDP流量测试
    '多CPE上行TCP流量测试':[],#多cpe场景，上行TCP流量测试
    '多CPE近点ping包测试':[],#多cpe场景，近点（-70）ping测试
    '多CPE远点ping包测试':[],#多cpe场景，近点（-100）ping测试
    '多CPE近点tcp上行流量测试':[],#多cpe场景，近点（-70）tcp上行流量测试
    '多CPE近点tcp下行流量测试':[],#多cpe场景，近点（-70）tcp下行流量测试
    #--------------手机----------------
    '手机飞行去飞行后接入成功率测试':[(1)],#手机飞行去飞行后接入成功率测试
    '基站复位后接入成功率测试_手机终端':[(1)],#基站复位后手机终端接入成功率测试
    '去激活激活小区后接入成功率测试_手机终端':[(1)],#小区去激活激活后手机终端接入成功率测试
    '闭塞解闭塞小区后接入成功率测试_手机终端':[(1)],#小区闭塞解闭塞后手机终端接入成功率测试
    '关闭打开通道射频后接入ping测试_手机终端':[(1)],#关闭打开射频通道后手机终端接入成功率测试
    '关闭2s后打开通道射频接入ping测试_手机终端':[(1)],#关闭射频通道2s后打开射频通道，手机终端接入成功率测试
    '程控衰减近点ping包测试_手机终端':[(1)],#使用程控衰减打点到-70点位手机终端进行ping包测试
    '程控衰减远点ping包测试_手机终端':[(1)],#使用程控衰减打点到-100点位手机终端进行ping包测试
    '程控衰减近点tcp上行流量测试_手机终端':[],#使用程控衰减打点到-70点位手机终端进行tcp上行流量测试
    '程控衰减近点tcp下行流量测试_手机终端':[],#使用程控衰减打点到-70点位手机终端进行tcp下行流量测试
    '程控衰减近点tcp上下行流量测试_手机终端':[],#使用程控衰减打点到-70点位手机终端进行tcp上下行流量测试
    '程控衰减远点tcp上行流量测试_手机终端':[],#使用程控衰减打点到-100点位手机终端进行tcp上行流量测试
    '程控衰减远点tcp下行流量测试_手机终端':[],#使用程控衰减打点到-100点位手机终端进行tcp下行流量测试
    '程控衰减远点tcp上下行流量测试_手机终端':[],#使用程控衰减打点到-100点位手机终端进行tcp上下行流量测试
    '程控衰减tcp上下行流量打点测试_手机终端':[],#使用程控衰减循环打点，手机终端进行tcp上下行流量测试
    '近点ping包测试_手机终端':[(1)],#近点（-70）手机终端ping测试
    '远点ping包测试_手机终端':[(1)],#远点（-100）手机终端ping测试
    '近点tcp上行流量测试_手机终端':[],#近点（-70）手机终端tcp上行流量测试
    '近点tcp下行流量测试_手机终端':[],#近点（-70）手机终端tcp下行流量测试
    '近点tcp上下行流量测试_手机终端':[],#近点（-70）手机终端tcp上下行流量测试
    '远点tcp上行流量测试_手机终端':[],#远点（-100）手机终端tcp上行流量测试
    '远点tcp下行流量测试_手机终端':[],#远点（-100）手机终端tcp下行流量测试
    '远点tcp上下行流量测试_手机终端':[],#远点（-100）手机终端tcp上下行流量测试
    'iperf端口绑定场景ping包测试_手机终端':[(10)],#手机卡ip固定场景，手机终端ping测试
    'iperf端口绑定场景tcp上行流量测试_手机终端':[],#手机卡ip固定，手机iperf应用手工启动场景，tcp上行流量测试
    'iperf端口绑定场景tcp下行流量测试_手机终端':[],#手机卡ip固定，手机iperf应用手工启动场景，tcp下行流量测试
    #--------------omc version----------------
    '基站版本冒烟测试_OMC升级最新版本':[],#omc上执行版本升级，升级到指定分支的最新版本
    '基站版本升级回退测试':[(50)],#基站升级回退压测
    '基站cpld版本升级回退测试':[(10)],#基站升级回退压测，回退后更新cpld版本
    '基站cpld版本升级回退测试且更新Bootmisc':[(15)],#基站升级回退压测，回退后更新cpld版本和bootmisc文件
    'V4基站cpld版本升级回退测试且更新Bootmisc':[(15)],#v4基站升级回退压测，回退后更新cpld版本和bootmisc文件
    '基站版本升级回退_配置导出导入测试':[(50)],#基站版本升级后导出导入xml，再回退版本
    '基站版本包下载过程中查询CPU利用率':[(10)],#基站版本包下载过程中查询基站14核cpu利用率
    '基站版本包下载过程中基站断链x秒':[(1,1)],#测试现象不一致，暂不使用
    '基站版本下载过程中复位基站':[(10)],#测试现象不一致，暂不使用
    '基站版本下载过程中掉电复位基站':[(10)],#测试现象不一致，暂不使用
    '基站版本下载过程中再次执行版本下载':[(10)],#基站版本下载过程中再次执行版本下载
    '基站版本下载过程中执行版本激活':[(10)],#基站版本下载过程中执行版本激活
    '基站版本下载过程中执行版本回退':[(10)],#基站版本下载过程中执行版本回退
    '基站版本下载过程中omc复位基站':[(10)],#基站版本下载过程中执行omc复位基站
    '基站版本包激活过程中基站断链x秒':[(1,1)],#基站版本包激活过程中让基站断链x秒
    '基站版本包激活过程中下载版本':[(10)],#基站版本包激活过程中执行版本下载操作
    '基站版本包激活过程中激活版本':[(10)],#基站版本包激活过程中执行版本激活操作
    '基站版本包激活过程中回退版本':[(10)],#基站版本包激活过程中执行版本回退操作
    '基站版本包回退过程中下载版本':[(10)],#基站版本包回退过程中执行版本下载操作
    '基站版本包回退过程中回退版本':[(10)],#基站版本包回退过程中执行版本回退操作
    '基站版本下载过程中修改基站参数':[(1)],#基站版本下载过程中修改基站参数
    '基站版本包激活过程中修改参数':[(1,0),(1,2),(1,3)],#基站版本包激活过程中等待x秒后修改参数
    '基站版本包回退过程中修改参数':[(1,0),(1,2),(1,3)],#基站版本包回退过程中等待x秒后修改参数
    #--------------omc version&&xml----------------
    '基站版本包激活过程中omc导入xml':[(10)],#基站版本包激活过程中omc执行xml导入操作
    'omc导入xml过程中激活基站版本':[(10)],#omc导入xml过程中执行版本激活操作
    '基站版本包激活过程中weblmt导入xml':[(10)],#基站版本包激活过程中weblmt执行导入xml操作
    '基站版本包激活过程中weblmt导入xml':[(10)],#基站版本包激活过程中weblmt执行导入xml操作
    '基站版本包回退过程中omc导入xml':[(10)],#基站版本包回退过程中omc执行导入xml操作
    'omc导入xml过程中执行版本回退':[(10)],#omc导入xml过程中执行版本回退操作
    '基站版本包回退过程中weblmt导入xml':[(10)],#基站版本包回退过程中weblmt执行导入xml操作
    'weblmt导入xml时omc激活版本':[(10)],#weblmt导入xml过程中omc执行版本激活操作
    'weblmt导入xml时omc回退版本':[(10)],#weblmt导入xml过程中omc执行版本回退操作
    '基站版本包升级前后omc导出导入xml':[(10)],#基站版本包升级前后omc执行导出导入xml操作
    '基站版本包激活过程中omc导入xml':[(10)],#基站版本包激活过程中omc执行导入xml操作
    '基站版本包升级后omc导出导入升级前xml':[(10)],#基站版本包升级后omc导入升级前xml
    '基站策略升级压测':[(10)],#基站策略升级压测
    #--------------weblmt version----------------
    'weblmt版本升级回退':[(2)],#weblmt执行版本升级回退压测
    'weblmt最新分支版本升级':[],#weblmt升级指定版本分支的最新版本
    'weblmt导入xml时weblmt激活版本':[(10)],#weblmt导入xml时，weblmt执行版本激活操作
    'weblmt版本下载过程中查询cpu利用率':[(10)],#weblmt下载版本过程中查询cpu利用率
    'weblmt激活时weblmt导入xml':[(10)],#weblmt激活版本时，weblmt执行xml导入
    #--------------omc xml----------------
    '配置文件导出导入测试':[(100)],#配置文件导出导入压测
    '配置文件导出导入测试_SN为空':[],#SN为空时执行xml导入
    '配置文件导出导入测试_SN长度过短':[],#sn长度过短时执行xml导入
    '配置文件导出导入测试_SN长度过长':[],#sn长度过长时执行xml导入
    '配置文件导出导入测试_SN非法值':[],#sn设置成非法值时执行xml导入
    '配置文件导出导入测试_Tac值异常':[],#tac配置成非法值时执行xml导入
    '配置文件导出导入测试_版本号异常':[],#版本号异常时执行xml导入
    '配置文件导出导入测试_Tac值超界':[(-1),(16777216)],#tac值配置超边界时执行xml导入
    '配置文件导出导入测试_Tac值修改':[(0),(512001),(16777215)],#tac值配置边界值执行xml导入
    'omc导入welmt导出的xml':[(10)],#omc导入weblmt导出的xml文件
    'welmt导入omc导出的xml':[(10)],#weblmt导入omc导出的xml文件
    'weblmt激活版本时omc导入xml':[(10)],#weblmt激活版本时，omc导入xml文件
    'omc导入xml时weblmt激活版本':[(10)],#omc导入xml时weblmt激活版本
    '配置文件导入查询cpu利用率':[(10)],#omc导出导入xml时查询cpu利用率
    #--------------weblmt xml----------------
    'welmt配置文件导出导入测试':[(100)],#weblmt导出导入xml压测
    'welmt配置文件导入时查询cpu利用率':[(10)],#weblmt导入xml时查询cpu利用率
    'welmt配置文件导出导入异常测试_SN号为空':[],#weblmt不校验
    'welmt配置文件导出导入异常测试_SN号过短':[],#weblmt不校验
    'welmt配置文件导出导入异常测试_SN号过长':[],#weblmt不校验
    'welmt配置文件导出导入异常测试_SN号为非法值':[],#weblmt不校验
    'welmt配置文件导出导入异常测试_Tac为非法值':[],#tac配置成非法值时weblmt执行xml导入
    'welmt升级前后执行配置文件导出导入测试':[],#welmt升级前后执行配置文件导出导入测试
    'welmt配置文件导出导入异常测试_版本号异常':[],#版本号异常时在welmt上执行配置文件导出导入测试
    'welmt配置文件导出导入异常测试_Tac值越界':[(-1),(16777216)],#tac配置超界参数时weblmt上执行xml文件导入测试
    'welmt配置文件导出导入异常测试_Tac值修改':[(0),(512001),(16777215)],#tac值配置边界值weblmt执行xml导入油荒
    'welmt配置文件导出导入异常测试_wifi发射功率修改':[(-3)],#wifi发射功率参数修改，weblmt执行xml导入
    #---------------weblmt gnb----------------
    'weblmt复位基站正常后ping包':[(10)],#weblmt复位基站，基站正常后ping包测试
    'weblmt基站信息查看':[],#weblmt上查看基站信息
    'weblmt时钟源配置':[()],#weblmt上查看时钟源配置
    'weblmt获取运营商信息':[],#weblmt上获取运营商信息
    'weblmt运营商配置':[('001','01')],#weblmt配置运营商信息
    'weblmt导出基站log':[('#logPath')],#weblmt导出基站log
    'weblmt自测模式':[],#基站自测模式测试
    'weblmt查看IP地址信息':[('IPV6')],#weblmt查看ip地址信息
    }

'''
    说明：
            以下是实际要执行的用例配置，格式：用例名称：参数列表
            可以从上面模板中拷贝，修改对应的参数即可。
'''
RUN_TESTCASE = {
    'CPE注册去注册后接入成功率测试':[(1)],#cpe接入去接入操作接入成功率测试
    'CPE复位后接入成功率测试':[(1)],#cpe复位cpe接入成功率测试
    '基站复位后CPE接入成功率测试':[(1)],#基站复位cpe接入成功率测试
    '去激活激活小区后CPE接入成功率测试':[(1)],#小区去激活激活后cpe接入成功率测试
    '闭塞解闭塞小区后接入成功率测试':[(1)],#小区闭塞解闭塞后cpe接入成功率测试
    }