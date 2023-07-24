# coding = 'utf-8'
'''
Created on 2023年5月31日

@author: auto

'''
'''
    程控电源上电
'''

from TestCaseData.basicConfig import BASIC_DATA
from UserKeywords.power.APS7100 import key_login_aps7100, key_power_on_aps7100, \
    key_logout_aps7100, key_power_off_aps7100
from UserKeywords.power.Delixi import key_login_delixi, key_power_on_delixi, key_logout_delixi, \
    key_power_off_delixi

def key_power_on(powerType=BASIC_DATA['power']['powerType']):
    if powerType == 'aps7100':
        aps7100 = key_login_aps7100()
        key_power_on_aps7100(aps7100)
        key_logout_aps7100(aps7100)
    else:
        delixi = key_login_delixi()
        key_power_on_delixi(delixi)
        key_logout_delixi(delixi)

'''
    程控电源下电
'''
def key_power_off(powerType=BASIC_DATA['power']['powerType']):
    if powerType == 'aps7100':
        aps7100 = key_login_aps7100()
        key_power_off_aps7100(aps7100)
        key_logout_aps7100(aps7100)
    else:
        delixi = key_login_delixi()
        key_power_off_delixi(delixi)
        key_logout_delixi(delixi)