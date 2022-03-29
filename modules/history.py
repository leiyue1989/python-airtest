#!/usr/bin/python3
# coding=utf-8

import random
import re
import time

from airtest.core.api import sleep, keyevent

from common import tools_action
from const import *


class History(object):

    @staticmethod
    def deleteHistory(poco):
        tools_action.swapUp(poco, 0.01)
        sleep(1)
        items = poco("android.view.View")
        print("-------------删除历史消息开始---------------")
        i = 0
        for item in items:
            sleep(1)
            if item.get_text() is None:
                continue
            messages = item.get_text().split("\n")
            print("mesasges:", messages)
            if len(messages) < 4:
                message_num = ""
            else:
                message_num = messages[3]
            if message_num == "":
                pos = item.get_position()
                if pos[0] > 2:
                    continue
                poco.long_click((pos[0], pos[1]), duration=2)
                sleep(0.8)
                if poco(text="Delete").exists():
                    poco(text="Delete").click()
                elif poco(text="DELETE").exists():
                    poco(text="DELETE").click()
                sleep(0.8)
                if poco(textMatches="DELE.*").exists():
                    poco(textMatches="DELE.*").click()
                # poco.click([pos[0], pos[1]])
                # sleep(1)
                # poco.click([0.926, 0.07])
                # sleep(0.5)
                # tools_action.swapUp(poco, 0.01)
                # poco.click([0.336, 0.958])
                # sleep(0.5)
                # if poco(text="LEAVE GROUP").exists():
                #     poco(text="LEAVE GROUP").click()
                # elif poco(text="DELETE").exists():
                #     poco(text="DELETE").click()
            i = i + 1
            if i >= 1:
                break
        tools_action.home(poco)

    @staticmethod
    def clearMemory(poco):
        keyevent("home")
        sleep(1)
        keyevent("home")
        sleep(1)
        poco("com.miui.home:id/background").click()
        sleep(5)
