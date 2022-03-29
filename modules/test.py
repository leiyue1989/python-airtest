#!/usr/bin/python3
# coding=utf-8
from common.tools_action import *
from const import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import re
from modules.history import History


class Test(object):

    def __init__(self, deviceID):
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        self.deviceID = deviceID

        sleep(1)
        if not self.poco(nameMatches=MAIN_NOT_SELECT_BUTTON).exists():
            start_app(ZALO_APP)
            sleep(1)

        # self.__home()

    def chatMessage(self):
        poco = self.poco
        flag = True
        print("111")
        if poco(text="Message, @").exists():
            print("222")
            sleep(0.5)
            if poco("com.zing.zalo:id/menu_drawer").exists():
                flag = False
                poco("com.zing.zalo:id/menu_drawer").click()
                sleep(1)
                swapUp(poco, duration=0.1)
                sleep(1)
                swapUp(poco, duration=0.1)
                sleep(1)
                poco.click([0.38, 0.96])
                sleep(1)
                if poco(text="LEAVE GROUP").exists():
                    poco(text="LEAVE GROUP").click()
                    flag = True
                    sleep(2.5)
                elif poco(text="DELETE").exists():
                    poco(text="DELETE").click()
                    flag = True
                    sleep(2.5)

        if not flag:
            print("3333")
            keyevent("BACK")
        print("9999")
        # History.deleteHistory(poco)
        # items = poco("android.view.View")
        # print("items:", len(items))

    def __home(self):
        poco = self.poco
        for num in range(1, 8):
            sleep(1)
            if not poco(nameMatches=MAIN_SELECT_BUTTON).exists():
                keyevent("BACK")
            else:
                if poco("android.widget.TextView").exists():
                    msg = poco("android.widget.TextView").get_text()
                    if msg == "Messages":
                        break
                    poco.click([0.0888, 0.9675])
                break
