# -*- encoding=utf8 -*-

import os, re
# 获取设备多台设备号列表
import time

from airtest.core.api import connect_device
from common import tools_action as action


def getDeviceCodes():
    str_init = ' '
    all_info = os.popen('adb devices').readlines()

    for i in range(len(all_info)):
        str_init += all_info[i]
    devices_name = re.findall('\n(.+?)\t', str_init, re.S)

    return devices_name


deviceCodes = getDeviceCodes()
for deviceCode in deviceCodes:
    print("设备号：", deviceCode)
    connect_device("android://127.0.0.1:5037/" + deviceCode + "?cap_method=javacap&touch_method=adb")
    action.installApp("/Users/denggang/Documents/WhatsApp.apk")
# action.installApp("/www/pinduoduo.apk")
# connect_device("android://127.0.0.1:5037/" + deviceCode + "?cap_method=javacap&touch_method=adb")
