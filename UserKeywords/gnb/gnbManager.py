# coding= 'utf-8'
'''
Created on 2022年11月17日
@author: dj
'''
from time import sleep
import logging
import allure
from BasicService.gnb.gnbService import gnbService
from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.basic.basic import key_get_time

'''
            说明：登录gnb
            参数：
    gnbIp:基站debug ip
    username:登录用户名
    password:登录密码
''' 
def key_ssh_login_gnb(gnbIp=BASIC_DATA['weblmt']['ip'], username=BASIC_DATA['gnb']['username'], password=BASIC_DATA['gnb']['password']):
    with allure.step(key_get_time() +": ssh登录基站\n"):
        logging.info(key_get_time()+': login gnb by ssh.')
        gnb = gnbService().ssh_login_gnb(gnbIp, username, password)
        return gnb
    
'''
          登出gnb
'''
def key_logout_gnb(gnb):
    with allure.step(key_get_time() +": 登出基站ssh\n"):
        logging.info(key_get_time()+': logout gnb by ssh.')
        gnbService().logout_gnb(gnb)

'''
        说明：查询gps md5值
        参数：
    gnb:gnb对象
''' 
def key_query_gps_md5_value(gnb):
    with allure.step(key_get_time() +": 查询基站gps md5值\n"):
        logging.info(key_get_time()+': query gps md5 value.')
        md5val = gnbService().check_gps_md5(gnb)
        return md5val
        
'''
        说明：查询nrsys、uboot版本
        参数：
    gnb:gnb对象
'''
def key_query_nrsys_version(gnb):
    with allure.step(key_get_time() +": 查询基站nrsys/uboot版本信息\n"):
        logging.info(key_get_time()+': query nrsys/uboot version.')
        ubootRes, nrsysRes = gnbService().query_nrsys_version(gnb)
        return ubootRes, nrsysRes
    
'''
        说明：打开log打印开关
        参数：
    gnb:gnb对象
'''
def key_open_log_print_switch(gnb):
    with allure.step(key_get_time() +": 打开基站log打印开关\n"):
        logging.info(key_get_time()+': open gnb log print switch.')
        gnbService().open_log_switch(gnb)
        
'''
        说明：基站侧执行抓包命令
        参数：
    gnb:gnb对象
'''
def key_capture_package_on_gnb(gnb, filePath='/'):
    with allure.step(key_get_time() +": 基站侧执行抓包命令\n"):
        logging.info(key_get_time()+': capture package on gnb.')
        gnbService().capture_package_on_gnb(gnb, filePath)

'''
        说明：禁用dpdk0网卡
        参数：
    gnb:gnb对象
'''
def key_forbid_dpdk0(gnb):
    cmdStr = 'ifconfig dpdk0 down'
    with allure.step(key_get_time() +": 执行命令禁用dpdk0网卡\n"):
        logging.info(key_get_time()+': exec command forbidden dpdk0')
        gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：启用dpdk0网卡
        参数：
    gnb:gnb对象
'''
def key_unforbid_dpdk0(gnb):
    cmdStr = 'ifconfig dpdk0 up'
    with allure.step(key_get_time() +": 执行命令禁用dpdk0网卡\n"):
        logging.info(key_get_time()+': exec command start using dpdk0')
        gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：基站前台执行桩函数
        参数：
    gnb:gnb对象
'''
def key_exec_command_on_gnb(gnb, cmdStr):
    with allure.step(key_get_time() +": 基站侧执行桩函数:"+cmdStr):
        logging.info(key_get_time()+': exec command on gnb, command:'+cmdStr)
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)

'''
        说明：手工升级cpld版本
        参数：
    gnb:gnb对象
    cpldVersion:cpdl版本号
    cpldPath:cpld版本存放目录
    enbType:V2/V4
'''
def key_upgrade_cpld_version(gnb, cpldVersion, cpldPath, enbType):
    with allure.step(key_get_time() +": 手工升级cpld版本\n"):
        logging.info(key_get_time()+': upgrade cpld version')
        upgradeRes = gnbService().upgrade_cpld_version(gnb, cpldVersion, cpldPath, enbType)
        logging.info(key_get_time()+': cpld upgrade result:'+upgradeRes)

'''
        说明：使用源文件替换目标文件
        参数：
    gnb:gnb对象
    souFilePath:源文件
    desFilePath:目标文件
'''
def key_gnb_copy_file(gnb, souFilePath, desFilePath):
    with allure.step(key_get_time() +": 使用源文件替换目标文件\n"):
        logging.info(key_get_time()+': source file update target file')
        cpRes = gnbService().gnb_copy_file(gnb, souFilePath, desFilePath)
        logging.info(key_get_time()+': file update result:'+cpRes)
        
'''
        说明：使用源文件替换目标文件
        参数：
    gnb:gnb对象
    souFilePath:源文件
    desFilePath:目标文件
'''
def key_query_cpld_version_info(gnb):
    with allure.step(key_get_time() +": 查询cpld版本信息\n"):
        logging.info(key_get_time()+': query cpld version info')
        cpRes = gnbService().query_cpld_version_info(gnb)
        logging.info(key_get_time()+': file update result:'+cpRes)
        
'''
        说明：关闭毫米波射频通道
        参数：
    gnb:gnb对象
'''
def key_close_aip_channel(gnb, trmId = 1):
    with allure.step(key_get_time() +": 关闭毫米波射频通道\n"):
        logging.info(key_get_time()+': close mmw channel.')
        if trmId == 1:
            cmdStr = 'echo -e -n "\x55\x00\x06\x00\x01\x01\x00\x00\x8B\xAA" > /dev/ttyAMA2'
        else:
            cmdStr = 'echo -e -n "\x55\x00\x06\x00\x02\x01\x00\x00\xB1\xAA" > /dev/ttyAMA2'
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)

'''
        说明：关闭毫米波射频通道
        参数：
    gnb:gnb对象
'''
def key_open_aip_channel(gnb, trmId = 1):
    with allure.step(key_get_time() +": 打开毫米波射频通道\n"):
        logging.info(key_get_time()+': open mmw channel.')
        if trmId == 1:
            cmdStr = 'echo -e -n "\x55\x00\x06\x00\x01\x02\x00\x00\x36\xAA" > /dev/ttyAMA2'
        else:
            cmdStr = 'echo -e -n "\x55\x00\x06\x00\x02\x02\x00\x00\x0C\xAA" > /dev/ttyAMA2'
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)

'''
        说明：关闭sub6g射频通道
        参数：
    gnb:gnb对象
'''
def key_close_sub6g_channel(gnb):
    with allure.step(key_get_time() +": 关闭sub6g射频通道\n"):
        logging.info(key_get_time()+': close sub6g channel.')
        cmdStr = 'devmem 0xa6003810 32 0x0'
        gnbService().exec_command_on_gnb(gnb, 'ssh 10.50.0.2')
        gnbService().exec_command_on_gnb(gnb, 'Web2022@Nr5gTechPs')
        gnbService().exec_command_on_gnb(gnb, 'Web2022@Nr5gTechPs')
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：打开sub6g射频通道
        参数：
    gnb:gnb对象
'''
def key_open_sub6g_channel(gnb):
    with allure.step(key_get_time() +": 打开sub6g射频通道\n"):
        logging.info(key_get_time()+': open sub6g channel.')
        cmdStr = 'devmem 0xa6003810 32 0xff'
        gnbService().exec_command_on_gnb(gnb, 'ssh 10.50.0.2')
        gnbService().exec_command_on_gnb(gnb, 'Web2022@Nr5gTechPs')
        gnbService().exec_command_on_gnb(gnb, 'Web2022@Nr5gTechPs')
        result = gnbService().exec_command_on_gnb(gnb, cmdStr)
        
'''
        说明：打开sub6g射频通道
        参数：
    gnb:gnb对象
'''
def key_query_gnb_cpu_ratio(coreNum=14, queryNum=1):
    gnb = key_ssh_login_gnb()
    with allure.step(key_get_time() +": 查询基站核"+str(coreNum)+" CPU利用率"):
        logging.info(key_get_time()+': query gnb core'+str(coreNum)+' cpu ratio')
        queryCpuRes = gnbService().query_cpu_ratio(gnb, coreNum, queryNum)
        with allure.step(key_get_time() +": 核"+str(coreNum)+" CPU利用率查询结果："+queryCpuRes):
            logging.info(key_get_time()+': the query result of gnb core'+str(coreNum)+' cpu ratio:'+queryCpuRes)
#         print(queryCpuRes)
        
'''
        说明：登录wifi板执行command命令
        参数：
    gnb:gnb对象
'''
def key_login_wifi_exec_command(cmdStr):
    gnb = key_ssh_login_gnb()
    with allure.step(key_get_time() +": 登录wifi板执行桩函数："+cmdStr):
        logging.info(key_get_time()+': login wifi exec command:'+cmdStr)
        execRes = gnbService().login_wifi_exec_command(gnb, cmdStr)
        with allure.step(key_get_time() +": 桩函数结果："+execRes):
            logging.info(key_get_time()+': command exec result:'+execRes)
        
'''
        说明：登录基站nrapp执行command命令
        参数：
    gnb:gnb对象
'''
def key_login_nrapp_exec_command(cmdStr):
    gnb = key_ssh_login_gnb()
    with allure.step(key_get_time() +": 登录nrapp执行桩函数："+cmdStr):
        logging.info(key_get_time()+': login nrapp exec command:'+cmdStr)
        execRes = gnbService().login_nrapp_exec_command(gnb, cmdStr)
        with allure.step(key_get_time() +": 桩函数结果："+execRes):
            logging.info(key_get_time()+': command exec result:'+execRes)       

'''
            说明：串口登录gnb
            参数：
    serialPort:2160端口号
    serialRate:端口比特率
    timeout:登录超时时间
''' 
def key_serial_login_2160(serialPort=BASIC_DATA['gnbSerial']['2160Port'], serialRate=BASIC_DATA['gnbSerial']['2160PortRate']):
    with allure.step(key_get_time() +": 串口登录2160"):
        logging.info(key_get_time()+': login 2160 by serial port')
        serial = gnbService().serial_login_2160(serialPort, serialRate)
        return serial
    
'''
          登出gnb
'''
def key_serial_logout_2160(serial):
    with allure.step(key_get_time() +": 串口登出2160"):
        logging.info(key_get_time()+': logout 2160 by serial port')
        gnbService().serial_logout_2160(serial)
        
if __name__ == '__main__':
    gnb = key_ssh_login_gnb()
#     key_query_cpld_version_info(gnb)
#     key_gnb_copy_file(gnb, '/home/bootmisc.sh', '/etc/init.d/bootmisc.sh')
    key_query_gnb_cpu_ratio(gnb, 14, 5)