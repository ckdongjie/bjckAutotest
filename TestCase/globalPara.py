# coding = 'utf-8'
'''
Created on 2023年2月21日

@author: auto
'''
def init():  # 初始化
    global isUpgrade 
    isUpgrade = False

def set_upgrade_status(value):
    #定义一个全局变量
    global isUpgrade
    isUpgrade = value

def get_upgrade_status():
    global isUpgrade
    return isUpgrade
