# coding = 'utf-8'
from BasicModel.ue.qutsModel import qutsModel
'''
Created on 2022年12月16日

@author: autotest
'''

class QutsService():
    '''
    classdocs
    '''

    '''
                开始ue log跟踪
    '''
    def startUeLogTrace(self):
        dev_manager, qxdm_window, diagService = qutsModel().startLogTrace()
        return dev_manager, qxdm_window, diagService
    
    '''
                停止ue log跟踪
    '''
    def stopUeLogTrace(self, dev_manager, qxdm_window, diagService, logSavePath):
        logFilePath = qutsModel().stopLogTrace(dev_manager, qxdm_window, diagService, logSavePath)
        return logFilePath