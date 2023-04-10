'''
Created on 2023年4月10日

@author: autotest
'''
from BasicModel.serial.serialModel import SerialModel


class DelixiService():

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
                启动程控电源开关
    '''    
    def power_on(self, serial):
        cmdStr = bytes.fromhex('A0 01 01 A2')
        serial.exec_command_with_hex(cmdStr)
        ponRes = serial.read_result_of_serial()
        return ponRes
    
    '''
                关闭程控电源开关
    '''    
    def power_off(self, serial):
        cmdStr = bytes.fromhex('A0 01 00 A1')
        serial.exec_command_with_hex(cmdStr)
        poffRes = serial.read_result_of_serial()
        return poffRes
        
    