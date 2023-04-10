# coding = 'utf-8'
'''
Created on 2023年1月5日
@author: autotest
'''

from time import sleep

from BasicModel.serial.serialModel import SerialModel


class APS7100Service():

    '''
                串口登录程控电源
    '''  
    def login_serial(self, serialPort='COM7', serialRate=9600):
        serial = SerialModel().login_serial(serialPort, serialRate)
        return serial
    
    '''
                串口登出程控电源
    '''  
    def logout_serial(self, serial):
        serial.logout_serial()
        
    '''
                读取程控电源最大功率
    '''    
    def read_max_pow(self, serial):
        cmdStr = '?MAXPOW'
        serial.exec_at_command(cmdStr)
        maxPow = serial.read_result_of_serial()
        return maxPow
    
    '''
                读取程控电源最大电压
    '''    
    def read_max_vol(self, serial):
        cmdStr = '?MAXVOL'
        serial.exec_at_command(cmdStr)
        maxVol = serial.read_result_of_serial()
        return maxVol
    
    '''
                读取程控电源最大电流
    '''    
    def read_max_cur(self, serial):
        cmdStr = '?MAXCUR'
        serial.exec_at_command(cmdStr)
        maxCur = serial.read_result_of_serial()
        return maxCur
    
    '''
                读取程控电源最大频率
    '''    
    def read_max_fre(self, serial):
        cmdStr = '?MAXFRE'
        serial.exec_at_command(cmdStr)
        maxFre = serial.read_result_of_serial()
        return maxFre
    
    '''
                读取程控电源最小频率
    '''    
    def read_min_fre(self, serial):
        cmdStr = '?MINFRE'
        serial.exec_at_command(cmdStr)
        minFre = serial.read_result_of_serial()
        return minFre
    
    '''
                读取程控电源型号
    '''    
    def read_model(self, serial):
        cmdStr = '?MODEL'
        serial.exec_at_command(cmdStr)
        model = serial.read_result_of_serial()
        return model
    
    '''
                启动程控电源开关
    '''    
    def power_on(self, serial):
#         cmdStr = 'PON'
        cmdStr = bytes.fromhex('A0 01 01 A2')
        serial.exec_at_command(cmdStr)
        ponRes = serial.read_result_of_serial()
        return ponRes
    
    '''
                关闭程控电源开关
    '''    
    def power_off(self, serial):
#         cmdStr = 'POFF'
        cmdStr = bytes.fromhex('A0 01 00 A1')
        serial.exec_at_command(cmdStr)
        poffRes = serial.read_result_of_serial()
        return poffRes
    
    '''
                设置程控电源电压
    '''    
    def set_power_vol(self, serial, vol):
        cmdStr = 'SVOL '+str(vol)
        serial.exec_at_command(cmdStr)
        svolRes = serial.read_result_of_serial()
        return svolRes
    
    '''
                设置程控电源电流
    '''    
    def set_power_cur(self, serial, cur):
        cmdStr = 'SCUR '+str(cur)
        serial.exec_at_command(cmdStr)
        scurRes = serial.read_result_of_serial()
        return scurRes
    
    '''
                设置程控电源频率
    '''    
    def set_power_fre(self, serial, fre):
        cmdStr = 'SFRE '+str(fre)
        serial.exec_at_command(cmdStr)
        sfreRes = serial.read_result_of_serial()
        return sfreRes
    
    '''
                读取设置程控电源电压值
    '''    
    def read_set_power_vol(self, serial):
        cmdStr = '?SVOL'
        serial.exec_at_command(cmdStr)
        svolRes = serial.read_result_of_serial()
        return svolRes
    
    '''
                读取设置程控电源电流值
    '''    
    def read_set_power_cur(self, serial):
        cmdStr = '?SCUR'
        serial.exec_at_command(cmdStr)
        scurRes = serial.read_result_of_serial()
        return scurRes
    
    '''
                读取设置程控电源频率值
    '''    
    def read_set_power_fre(self, serial):
        cmdStr = '?SFRE'
        serial.exec_at_command(cmdStr)
        sfreRes = serial.read_result_of_serial()
        return sfreRes
    
    '''
                读取程控电源输出电压值
    '''    
    def read_measure_power_vol(self, serial):
        cmdStr = '?MVOL'
        serial.exec_at_command(cmdStr)
        mvolRes = serial.read_result_of_serial()
        return mvolRes
    
    '''
                读取程控电源输出电流值
    '''    
    def read_measure_power_cur(self, serial):
        cmdStr = '?MCUR'
        serial.exec_at_command(cmdStr)
        mcurRes = serial.read_result_of_serial()
        return mcurRes
    
    '''
                读取程控电源输出频率值
    '''    
    def read_measure_power_fre(self, serial):
        cmdStr = '?MFRE'
        serial.exec_at_command(cmdStr)
        mfreRes = serial.read_result_of_serial()
        return mfreRes

if __name__ == '__main__':
    apsServer = APS7100Service()
    aps = apsServer.login_serial('COM16', 9600)
#     svol = apsServer.read_set_power_vol(aps)
#     apsServer.power_off(aps)
#     print('power off')
#     sleep(10)
    ponRes = apsServer.power_on(aps)
    print('power on')
#     print(ponRes)
    
        