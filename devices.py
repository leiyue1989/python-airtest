#!/usr/bin/python3

import os, re
import configparser

def getDeviceCodes():
    str_init = ' '
    all_info = os.popen('adb devices').readlines()

    for i in range(len(all_info)):
        str_init += all_info[i]
    devices_name = re.findall('\n(.+?)\t', str_init, re.S)

    return devices_name


if __name__ == '__main__':
    deviceCodes = getDeviceCodes()

    print(deviceCodes)
    str = ''
    for deviceCode in deviceCodes:
        str = str + "," + deviceCode

    str = str.lstrip(",")
    print(str)
    config = configparser.ConfigParser()
    config.read("devices.ini")
    config.remove_section("Devices")
    config.add_section("Devices")
    config.set("Devices", "code", str)
    config.write(open("devices.ini", "w"))


