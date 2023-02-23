# coding = 'utf-8'
'''
Created on 2022年12月2日

@author: dj

'''

import win32com.client
import logging
import sys

class QCatModel():
    '''
    classdocs
    '''


    def init_QCat(self):
        try:
            qcatApp = win32com.client.Dispatch('QCAT6.Application')
        except:
            logging.info('Connect QCAT Error, Please Check!')
            sys.exit(1)
        return qcatApp
    
    def load_ue_log(self, qcatApp, ueLogFilePath, logId, **kwargs):
        logContextList = []
        SIBFilter = qcatApp.PacketFilter
        SIBFilter.SetAll(False)
        self.TargetLogId = logId
        SIBFilter.Set(self.TargetLogId, True)
        SIBFilter.Commit()
        if 'subTitle' in kwargs:
            subTitle = kwargs['subTitle']
        else:
            subTitle = ''
        if 'filterContext' in kwargs:
            filterContext = kwargs['filterContext']
            isFilter = False
        else:
            isFilter = True
        if qcatApp.OpenLog(ueLogFilePath) != 1:
            logging.warning('Open Ue Log Error, Please Check!')
            exit()
        logging.info('Open Ue Log Success')
        QcatPacket = qcatApp.FirstPacket
        while QcatPacket.Next() != False:
            context = QcatPacket.text
#             print(context)
            if isFilter == False:
                if filterContext in context:
                    isFilter == True
            else :
                if subTitle == '':
                    logContextList.append(context)
                elif subTitle in context:
                    logContextList.append(context)
                    break
        return logContextList
        