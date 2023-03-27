# coding = utf-8 
'''
Created on 2022年9月8日

@author: dj

以下模板包括已经开发的所有用例，
用例模板说明：
        测试用例：配置参数（基础参数需要在basicConfig中配置）
'''
from TestCaseData.basicConfig import BASIC_DATA

TESTCASE_TEMPLATE = {
        '基站版本冒烟测试':[],
        #功能：版本分支升级测试，升级后校验小区状态、cpe接入、ping包、灌包等
        #参数：
        '基站版本升级回退测试':[(30)],
        #功能：基站版本升级加退压测
        #参数：testNum--用例压测执行次数
        '基站版本下载过程中再次执行版本下载':[(10)], 
        #功能：基站版本下载过程中再次执行版本下载
        #参数：testNum--用例压测执行次数
        '基站版本下载过程中执行版本激活':[(10)],
        #功能：基站版本下载过程中执行版本激活
        #参数：testNum--用例压测执行次数
        '基站版本下载过程中执行版本回退':[(10)],
        #功能：基站版本下载过程中执行版本回退
        #参数：testNum--用例压测执行次数
        '基站版本包激活过程中下载版本':[(10)],
        #功能：基站版本包激活过程中下载版本
        #参数：testNum--用例压测执行次数
        '基站版本包激活过程中激活版本':[(10)],
        #功能：基站版本包激活过程中激活版本
        #参数：testNum--用例压测执行次数
        '基站版本包激活过程中回退版本':[(1)],
        #功能：基站版本包激活过程中回退版本
        #参数：testNum--用例压测执行次数 
        '基站版本下载过程中omc复位基站':[(1)],
        #功能：基站版本下载过程中omc复位基站  [*基站可能会挂死*]
        #参数：testNum--用例压测执行次数 
        '基站版本包下载过程中基站断链x秒':[(1,1)],
        #功能：基站版本包下载过程中基站断链x秒
        #参数：testNum--用例压测执行次数 
        #    waitTime--等待时间（s）  等待5s时异常--网管给基站发消息
        '基站版本包激活过程中基站断链x秒':[(1,1)],
        #功能：基站版本包激活过程中基站断链x秒
        #参数：testNum--用例压测执行次数 
        #    waitTime--等待时间（s）
        '基站版本下载过程中修改基站参数':[(10)],
        #功能：基站版本下载过程中修改基站参数
        #参数：testNum--用例压测执行次数 
        '基站版本包激活过程中修改参数':[(10,2)],
        #功能：基站版本包激活过程中修改参数
        #参数：testNum--用例压测执行次数 
        #    waitTime--等待时间（s） 
        '基站版本包回退过程中修改参数':[(1,3)],
        #功能：基站版本包回退过程中修改参数
        #参数：testNum--用例压测执行次数 
        #    waitTime--等待时间（s） 
        '基站版本包回退过程中回退版本':[(10)],
        #功能：基站版本包回退过程中回退版本
        #参数：testNum--用例压测执行次数
        #-----------------------------------------------
        '反复闭塞解闭塞小区并ping包测试':[(500)],
        #功能：闭塞解闭塞小区状态，小区正常后ping包
        #参数：testNum--用例压测执行次数
        '复位基站正常后ping包':[(1)],
        #功能：复位基站，小区正常后ping包
        #参数：testNum--用例压测执行次数
        '闭塞小区后复位基站':[(1)],
        #功能：闭塞小区后复位基站，基站启动后查看小区状态
        #参数：testNum--用例压测执行次数
        'weblmt复位基站正常后ping包':[(10)],
        #功能：weblmt上复位基站，基站正常后ping包测试
        #参数：testNum--用例压测执行次数
        #-----------------------------------------------
        '更新omcIp地址_地址正确且基站已注册':[(1)],
        #功能：更新基站omc ip地址，目标网管上基站已经注册
        #参数：testNum--用例压测执行次数
        '更新omcIp地址_地址正确但基站未注册':[(1)],
        #功能：更新基站omc ip地址，目标网管上基站未注册
        #参数：testNum--用例压测执行次数
        '更新omcIp地址_地址错误':[(1)],
        #功能：更新基站omc ip地址，目标网管ip是错误ip地址
        #参数：testNum--用例压测执行次数
        #----------------------------------------------- 
        'CPE注册去注册后接入成功率测试':[(3)],
        #功能：小区状态正常，cep去注册注册后重新接入，测试接入成功率
        #参数：testNum--用例压测执行次数
        'CPE复位后接入成功率测试':[(3)],
        #功能：小区状态正常，cep复位后重新接入，测试接入成功率
        #参数：testNum--用例压测执行次数
        '基站复位后接入成功率测试':[(3)],
        #功能：小区状态正常，基站复位，启动正常后cep重新接入，测试接入成功率
        #参数：testNum--用例压测执行次数
        '去激活激活小区后接入成功率测试':[(3)],
        #功能：小区状态正常，小区去激活激活后cep重新接入，测试接入成功率
        #参数：testNum--用例压测执行次数
        '闭塞解闭塞小区后接入成功率测试':[(3)],
        #功能：小区状态正常，小区闭塞解闭塞后cep重新接入，测试接入成功率
        #参数：testNum--用例压测执行次数
        #-----------------------------------------------
        '配置文件导出导入测试':[(5)],
        #功能：配置文件导出导入测试
        #参数：testNum--用例压测执行次数
        '配置文件导出导入测试_SN为空':[(1)],
        #功能：配置文件导出后修改sn号为空并保存，导入测试，导入失败
        #参数：testNum--用例压测执行次数
        '配置文件导出导入测试_SN长度过短':[(1)],
        #功能：配置文件导出后修改sn号为较短的sn号并保存，导入测试，导入失败
        #参数：testNum--用例压测执行次数
        '配置文件导出导入测试_SN长度过长':[(1)],
        #功能：配置文件导出后修改sn号为较长的sn号并保存，导入测试，导入失败
        #参数：testNum--用例压测执行次数
        '配置文件导出导入测试_SN非法值':[(1)],
        #功能：配置文件导出后修改sn号为非法数值并保存，导入测试，导入失败
        #参数：testNum--用例压测执行次数
    #     '配置文件导出导入测试_Tac值异常':[(1)],error
        #功能：配置文件导出后修改tac值为非法数值并保存，导入测试，导入失败
        #参数：testNum--用例压测执行次数
        'UDP下行流量测试':[],
        #功能：UDP下行流量测试
        #参数：
        'TCP下行流量测试_动态调度':[],
        #功能：UDP下行流量测试
        #参数：
        'TCP下行流量测试_预调度':[],
        #功能：UDP下行流量测试
        #参数：
        'TCP上行流量测试':[],
        #功能：UDP下行流量测试
        #参数：
    }


'''
    说明：
            以下是实际要执行的用例配置，格式：用例名称：参数列表
            可以从上面模板中拷贝，修改对应的参数即可。
'''
RUN_TESTCASE = {
#     '基站版本冒烟测试':[],
#     '当前告警查询':[()],
#     '复位基站正常后ping包':[(1)],
#     '基站复位后接入成功率测试':[(1)],
#     '去激活激活小区后接入成功率测试':[(1)],
#     '闭塞解闭塞小区后接入成功率测试':[(1)],
#------------------------------------------------    
#     '基站版本升级回退测试':[(100)],
#     '基站cpld版本升级回退测试':[(15)],
#     '基站版本升级回退_配置导出导入测试':[(50)],
#     '基站版本下载过程中再次执行版本下载':[(10)],
#     '基站版本下载过程中执行版本激活':[(10)],
#     '基站版本下载过程中执行版本回退':[(10)],
#     '基站版本包激活过程中下载版本':[(10)],
#     '基站版本包激活过程中激活版本':[(10)],
#     '基站版本包激活过程中回退版本':[(10)],
#     '基站版本下载过程中修改基站参数':[(1)],
#     '基站版本包激活过程中修改参数':[(1,2),(1,3)],
#     '基站版本包回退过程中修改参数':[(1,2),(1,3)],
#     '基站版本包回退过程中回退版本':[(1)],
#     '基站版本包下载过程中基站断链x秒':[(1,1)],
#     '基站版本包激活过程中基站断链x秒':[(1,1)],
#-------------------------------------------------    
#     '复位基站正常后ping包':[(200)]
#-------------------------------------------------
#     '配置文件导出导入测试':[(200)],
#     '配置文件导出导入测试_SN为空':[(1)],
#     '配置文件导出导入测试_SN长度过短':[(1)],
#     '配置文件导出导入测试_SN长度过长':[(1)],
#     '配置文件导出导入测试_SN非法值':[(1)],
#     '配置文件导出导入测试_Tac值异常':[(1)]
#-------------------------------------------------
#     'CPE注册去注册后接入成功率测试':[(1)],
#     'CPE复位后接入成功率测试':[(1)],
#     '基站复位后接入成功率测试':[(100)],
#     '去激活激活小区后接入成功率测试':[(2)],
#     '闭塞解闭塞小区后接入成功率测试':[(200)],
#     '反复闭塞解闭塞小区并ping包测试':[(200)],
#     'TCP下行流量测试_预调度':[],
#     'UDP下行流量测试':[],
#     'TCP下行流量测试_动态调度':[],
#     'TCP上行流量测试':[]
#-------------------------------------------------
#     'TCP下行流量测试_动态调度':[],
#-------------------------------------------------
#     '支持每个时隙配置PDCCH符号数':[('1 Symbol')],
#     '支持PDCCH_CCE聚合度配置':[('CCE_4')],##abnormal
#     '支持PDCCH的传输格式':[('Format0_0','CCE_4')], abnormal
#     '支持PDSCH_调制解调方式配置':[('close',25)],
#     '支持随机接入PRACH格式':[(147)],#pass
#     '支持PUCCH传输格式_Format1':[('2')],#abnormal
#     '支持PUCCH传输格式_Format3':[('4')],#abnormal
#     '支持PUCCH_format1和format3时隙内跳频':[()],
#     '支持DMRS_Mapping_Type_A':[],
#     '支持DL_DMRS_Type1':[],
#     '支持UL_DMRS_Type1':[],
#     '支持PDSCH_上行调制解调方式配置':[('open',28)],
#     '支持单端口CSI_RS配置用于时频同步':[('SLOTS160', 'cri-RI-PMI-CQI')],
#-------------------------------------------------
#     'weblmt版本升级回退':[(1)],
#     'weblmt复位基站正常后ping包':[(1)],
#     'welmt配置文件导出导入测试':[(1)],
#     'welmt配置文件导出导入异常测试_SN号为空':[],#异常，weblmt不做防护
#     'welmt配置文件导出导入异常测试_SN号过短':[],#异常，weblmt不做防护
#     'welmt配置文件导出导入异常测试_SN号过长':[],#异常，weblmt不做防护
#     'welmt配置文件导出导入异常测试_SN号为非法值':[],#异常，weblmt不做防护
#     'welmt配置文件导出导入异常测试_Tac为非法值':[],#80P2未合入
#     'weblmt基站信息查看':[],
#     'weblmt获取运营商信息':[],
#     'weblmt时钟源配置':[(0)],
#     'weblmt运营商配置':[('001', '01')],
#     'weblmt导出基站log':[('E:\\autotestpath\\')],
#     'weblmt自测模式':['902271500014'],
#     'weblmt查看IP地址信息':[0],
#     'weblmt登出':[]
#-------------------------------------------------
#     '更新omcIp地址_地址正确且基站已注册':[(1)],
#     '更新omcIp地址_地址正确但基站未注册':[(1)],
#     '更新omcIp地址_地址错误':[(1)]
#     'SCTP目标端口号修改':[],
#     '本地时钟和GPS切换测试':[],
#     'SSB发射功率修改':[-5],
#-------------------------------------------------
#     '基站上下电测试':[(100)],
#     '基站随机上下电压测':[(2)],
#     'CPE上下电测试':[(1)],
#     '整机上下电本地时钟测试':[],
#     '整机复位本地时钟测试':[],
#-------------------------------------------------
#     '当前告警查询':[()],
#     '历史告警查询':[('2023-01-29 14:31:00', '2023-01-30 14:31:00')],
    }