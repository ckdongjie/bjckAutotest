'''
Created on 2023年2月7日

@author: autotest
'''
from BasicModel.serial.serialModel import SerialModel


class AttenuatorService():

    '''
                串口连接可调衰减
    '''  
    def connect_attenuator(self, serialPort='COM8', serialRate=9600):
        serial = SerialModel().login_serial(serialPort, serialRate)
        return serial
    
    '''
                串口断开连接可调衰减
    '''  
    def disconnect_attenuator(self, serial):
        serial.logout_serial()
        
    '''
                读取单通道衰减值
    '''    
    def read_single_channel_value(self, serial, channelNum):
        cmdStr = 'RA'+str(channelNum)
        serial.exec_at_command(cmdStr)
        sigChalValue = serial.read_result_of_serial()
        return sigChalValue
    
    '''
                设置单通道衰减值
    '''    
    def send_single_channel_value(self, serial, channelNum, attValue):
        cmdStr = 'SA'+str(channelNum)+' '+str(attValue)
        serial.exec_at_command(cmdStr)
        setValue = serial.read_result_of_serial()
        return setValue
    
    '''
                读取多通道衰减值
    '''    
    def read_multi_channel_value(self, serial, channelNumStr):
        cmdStr = ''
        channelNumList = channelNumStr.split(',')
        for channelNum in channelNumList:
            cmdStr = cmdStr + 'RA'+str(channelNum)+';'
        serial.exec_at_command(cmdStr)
        sigChalValue = serial.read_result_of_serial()
        return sigChalValue
    
    '''
                设置多通道衰减值
    '''    
    def send_multi_channel_value(self, serial, channelNumStr, attValue):
        cmdStr = ''
        channelNumList = channelNumStr.split(',')
        for channelNum in channelNumList:
            cmdStr = cmdStr + 'SA'+str(channelNum)+' '+str(attValue)+';'
        serial.exec_at_command(cmdStr)
        setValue = serial.read_result_of_serial()
        return setValue
    
    
if __name__ == '__main__':
    attSer = AttenuatorService()
    attenuator = attSer.connect_attenuator('COM8', 9600)
    value = attSer.read_multi_channel_value(attenuator, '2,3')
    print(value)
    attSer.send_multi_channel_value(attenuator, '2,3', 11)
    value = attSer.read_multi_channel_value(attenuator, '2,3')
    print(value)
    attSer.disconnect_attenuator(attenuator)
#     attSer.send_single_channel_value(attenuator, 2, 13)
#     value = attSer.read_single_channel_value(attenuator, 2)
#     print(value)