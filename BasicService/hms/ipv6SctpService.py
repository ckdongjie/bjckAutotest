# coding = 'utf-8'
'''
Created on 2023年3月2日

@author: auto
'''

from BasicModel.hms.IPv6SctpModel import IPv6SctpModel


class IPv6SctpService(object):

    '''
                说明：修改IPv6 SCTP目的ip地址
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        destIp:目的ip地址
    '''
    def update_ipv6_sctp_dest_ip(self, hmsObj, enbId, destIp):
        paramsDict = {'primaryPeerAddress':destIp}
        resCode,resInfo = IPv6SctpModel(hmsObj).update_ipv6_sctp_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    
    '''
                说明：修改IPv6 SCTP本地端口号
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        localPort:本地端口号
    '''
    def update_ipv6_sctp_local_port(self, hmsObj, enbId, localPort):
        paramsDict = {'localPort':str(localPort)}
        resCode,resInfo = IPv6SctpModel(hmsObj).update_ipv6_sctp_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
        
    '''
                说明：修改IPv6 SCTP远端端口号
                参数：
        hmsObj:hms对象
        enbId:基站enbId
        remotePort:远端端口号
    '''
    def update_ipv6_sctp_remote_port(self, hmsObj, enbId, remotePort):
        paramsDict = {'remotePort':str(remotePort)}
        resCode,resInfo = IPv6SctpModel(hmsObj).update_ipv6_sctp_params(enbId, paramsDict)
        if resCode == 200 and resInfo['result']=='0':
            return True
        else:
            return False
    