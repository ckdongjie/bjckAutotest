# coding = 'utf-8'
'''
Created on 2023年1月5日
@author: autotest
'''
import logging
from time import sleep

import serial


class SerialModel():
    '''
    classdocs
    '''
    serial = None
    
    def __init__(self):
        '''
        Constructor
        '''
        self.serial = None
    
    def login_serial(self, serialPort='COM7', serialRate=9600, timeout = 30):
        self.serial = serial.Serial(serialPort, serialRate, timeout=timeout)
        if self.serial.isOpen() == False:
            self.serial.open()
        logging.info('open serial port success!')
        return self
        
    def logout_serial(self):
        if self.serial.isOpen() == True:
            self.serial.close()
        logging.info('close serial port success!')
        
    def exec_at_command(self, cmd):
        if self.serial.isOpen() == False:
            self.serial.open()
        logging.info('The Command is:{0}'.format(cmd))
        self.serial.write((cmd+'\n').encode())
        self.serial.flush()
        sleep(1)
    
    def exec_command_with_hex(self, cmd):
        if self.serial.isOpen() == False:
            self.serial.open()
        logging.info('The Command is:{0}'.format(cmd))
        self.serial.write(cmd)
        self.serial.flush()
        sleep(1)
    
    def read_result_of_serial(self):
        data = ""
        while self.serial.inWaiting()>0:
            data += self.serial.readline().decode()
#         logging.info('serial return is:{0}'.format(data))
        return data
    
if __name__ == '__main__':
    serial = SerialModel().login_serial('COM16',9600)
#     serial.login_serial()
    serial.exec_at_command(bytes.fromhex('A0 01 00 A1'))
#     result = serial.read_result_of_serial()
#     print(result)