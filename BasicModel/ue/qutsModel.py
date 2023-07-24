## For detailed description of the QUTS APIs, please refer to QUTS documentation at "C:\Program Files (x86)\Qualcomm\QUTS\QUTS_User_Guide.docm"
##This sample includes connecting to device, using Diag, sending commands and collecting logs.
import decimal
import logging
import os
import re
import sys
import time

import Common.ttypes
import DiagService.DiagService
import DiagService.constants
import QutsClient
from win32com.client import Dispatch

##The path where QUTS files are installed
# import LogSession.LogSession
# import LogSession.constants
# import LogSession.ttypes
# import DiagService.ttypes
global handle
global diagService

class qutsModel():

    def onDataQueueUpdated(self, queueName, queueSize):
        logging.info(queueName, " update ", queueSize)
        '''
        diag_packets = diagService.getDataQueueItems(queueName, queueSize, 2000)
    	
        print (len(diag_packets))
        print(diag_packets)
        print("####################################################")
        '''
    
    
    def onMessage(self, level, location, title, description):
        logging.info("Message Received " + title + " " + description)
    
    
    def load_automation_window(self):
        """Initialize QXDM instance and return its automation window"""
        qxdm_instance = Dispatch("QXDM.QXDM5AutoApplication")
    
        auto_window = None
    
        if not bool(qxdm_instance):
            logging.warning("Unable to obtain ISF interface")
        else:
            auto_window = qxdm_instance.GetAutomationWindow2()
            auto_window.SetVisible(True)  # change to False to hide QXDM UI
    
        return auto_window
    
    
    def qxdm_exit_gracef(self, automation_window):
        automation_window.QuitApplication()
    
    
    def startLogTrace(self):
        quts_client = QutsClient.QutsClient("LogSessionLiveSample")
        if not quts_client:
            logging.info("quts client is null upon instantiation")
            return
    
        # Set the callback functions to receive notification whenever the Dataqueue is changed.
        quts_client.setOnDataQueueUpdatedCallback(self.onDataQueueUpdated)
    
        # QUTS sends messages on the what is going on in the system.
        quts_client.setOnMessageCallback(self.onMessage)
    
        # Get a handle to the device Manager. Device manager has all the device related info.
        dev_manager = quts_client.getDeviceManager()
        if not dev_manager:
            logging.info("dev_manager is null upon instantiation")
            return
    
        # Get the list of devices connected to the PC that supports Diag.
        device_list = dev_manager.getDevicesForService(DiagService.constants.DIAG_SERVICE_NAME)
        if not device_list or len(device_list) == 0:
            logging.info("no device found in devlice_list")
            return
    
        # print the properties of the first device
        devicehandle = device_list[0]
        listOfProtocols = dev_manager.getProtocolList(devicehandle)
        diag_prot_handle = None
        logging.info("printing the chip name of the first device with DIAG_PROT:")
        for i in range(len(listOfProtocols)):
            if listOfProtocols[i].protocolType == Common.ttypes.ProtocolType.PROT_DIAG:
                diag_prot_handle = listOfProtocols[i].protocolHandle
                logging.info(dev_manager.getChipName(devicehandle, listOfProtocols[i].protocolHandle))
        print("")
    
        # Get the DiagService for the device. This handle will be used for manipulating Diag (send/receive commands etc).
        # The following line get the first Diag device connected in the PC.
        diagService = DiagService.DiagService.Client(
            quts_client.createService(DiagService.constants.DIAG_SERVICE_NAME, devicehandle))
    
        # for a single modem device
        if 0 != diagService.initializeService():
            logging.info("Diag service init failed")
            return
    
        # start QXDM
        qxdm_window = self.load_automation_window()
        if qxdm_window is None:
            logging.warning("failed to get QXDM automation interface")
        else:
            logging.info("QXDM automation interface successfully launched")
    
        dev_handle_digits = len(str(devicehandle))
        prot_handle_digits = len(str(diag_prot_handle))
        logging.info("connecting to device with devicehandle={}, len={}; protoHandle={}, len={}".format(
            decimal.Decimal(devicehandle), dev_handle_digits, decimal.Decimal(diag_prot_handle), prot_handle_digits))
        device_connect_result = qxdm_window.ConnectToDevice(str(devicehandle), str(diag_prot_handle), False)
        if not device_connect_result:
            logging.warning("qxdm failed to connect to device")
        else:
            logging.info("QXDM successfully connects to device with deviceHandle={0}, protHandle={1}".format(devicehandle,                                                                                       diag_prot_handle))
        # all the data collected from this point will be saved in a HDF file when saveLogFiles is called.
        dev_manager.startLogging()
        # Set the filters for items of interest.
        time.sleep(3)
        
        return dev_manager, qxdm_window, diagService
    
        
    def stopLogTrace(self, dev_manager, qxdm_window, diagService, logSavePath):
        # Disconnect device
        qxdm_window.disconnectFromDevice()
    
        # save the data. This saves all the data that was generated in the device
        HDF_path = dev_manager.saveLogFiles(logSavePath)  # size correlated with logs logged in QXDM
    
#         logging.info("hdf is saved to {}".format(HDF_path))
    
        diagService.destroyService()
        self.qxdm_exit_gracef(qxdm_window)
       
        return HDF_path[0]

if __name__ == "__main__":
    logSavePath = 'D:\\autotestPro\\AutoTestMain\\qxdmLog'
    dev_manager, qxdm_window, diagService = qutsModel().startLogTrace()
    print('=======================')
    time.sleep(60)
    qutsModel().stopLogTrace(dev_manager, qxdm_window, diagService, logSavePath)
