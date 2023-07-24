'''
Created on 2023年4月20日

@author: autotest
'''
import os

from BasicModel.maintenanceTool.CaptureNetData import CaptureNetData
from BasicModel.maintenanceTool.MaintenanceToolModel import MaintenanceToolModel
from BasicModel.maintenanceTool.SvAndSigDataDeal import capture_data_analyse


class MaintenanceToolService():
    
    '''
                    连接sv基本文件工具
    '''
    def connect_sv_basic_tool(self, debugIp, svBasicPort=16666):
        svBasicSocket = MaintenanceToolModel().connect_sv_basic_tool(debugIp, svBasicPort)
        return svBasicSocket
    
    '''
                    连接sv详细文件工具
    '''
    def connect_sv_detail_tool(self, debugIp, svDetailPort=16667):
        svDetailSocket = MaintenanceToolModel().connect_sv_detail_tool(debugIp, svDetailPort)
        return svDetailSocket
    
    '''
                    连接signal工具
    '''        
    def connect_signal_tool(self, debugIp, localIp):
        sigSocket = MaintenanceToolModel().connect_signal_tool(debugIp, localIp)
        return sigSocket
    
    '''
                    关闭连接
    ''' 
    def disconnect_tool(self, Socket):
        MaintenanceToolModel().disconnect_tool(Socket)
        
    '''
                    开始捕获网口数据
    '''
    def start_capture_data(self, interfaceName):
        CaptureNetData().startCatputer(interfaceName)
    
    '''
                    停止捕获网口数据并保存文件
    '''    
    def stop_capture_data(self, packetSaveName): 
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        capturePath = BASE_DIR+'\\AutoTestMain\\captureData'
        if not os.path.exists(capturePath):
            os.makedirs(capturePath)  
        CaptureNetData().stopCatputer(capturePath+'/'+packetSaveName) 
    
    '''
                    网络数据分析
    '''    
    def network_data_analyse(self, debugIp, localIp, packetSaveName, isSaveSig=False, isSaveSvBasic=False, isSaveTrace=False, isSaveSvDetail=False):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        capturePath = BASE_DIR+'\\AutoTestMain\\captureData'
        capture_data_analyse(debugIp, localIp, capturePath+'/'+packetSaveName, isSaveSig=isSaveSig, isSaveSvBasic=isSaveSvBasic, isSaveTrace=isSaveTrace, isSaveSvDetail=isSaveSvDetail)
        
if __name__ == '__main__':
    MaintenanceToolService().stop_capture_data('123')