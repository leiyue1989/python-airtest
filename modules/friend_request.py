#!/usr/bin/python3
# coding=utf-8

# import random
import re
import time

from airtest.core.api import sleep, keyevent, touch, Template
from poco.exceptions import PocoTargetTimeout

from common import tools_action
from common import tools
from const import *


class FriendRequest(object):

    @staticmethod
    def acceptFriendRequest(poco, deviceID, appCloneID):
        flag = False
        # if poco(nameMatches=MAIN_NOT_SELECT_BUTTON).exists():
        #     if random.randint(1, 2) == 2:
        #         flag = True
        #         poco.click([0.3777, 0.9675])
        poco.click([0.3777, 0.9675])
        i = 0
        while i < 2:
            sleep(0.5)
            if poco(nameMatches=SEE_MORE).exists():
                poco(nameMatches=SEE_MORE).click()
                sleep(0.5)
            elif poco(text="Friend request").exists():
                poco(text="Friend request").click()
                sleep(0.5)
                if poco(text="RETRY").exists():
                    poco(text="RETRY").click()
                    sleep(5)
            elif poco(nameMatches=FRIEND_SUGGEST).exists():
                poco(nameMatches=FRIEND_SUGGEST).click()
                sleep(0.5)
            n = 0
            while n < 2:
                sleep(1)
                if poco(nameMatches=ACCEPT_FRIEND).exists():
                    poco(nameMatches=ACCEPT_FRIEND).click()
                    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    params = {
                        "eventId": 0,
                        "startTime": now,
                        "endTime": now,
                        "product": "7C",
                        "platform": "zalo",
                        "eventType": "bot_accept_friend",
                        "deviceID": deviceID,
                        "appCloneID": int(appCloneID)
                    }
                    tools.postRequest(tools.getEnvUrl() + "/eventStatistics/acceptFriends", params)
                    # 接受好友直接修改匿名
                    if poco(nameMatches=EDIT_ALIAS).exists():
                        # nickname = poco(nameMatches=EDIT_ALIAS).get_text()
                        nickname = poco(nameMatches=TV_NAME).get_text()
                        FriendRequest.acceptFriendUpdateAlis(poco, nickname)
                    keyevent("BACK")
                    n = n + 1
                else:
                    break
            if n == 0:
                break
            i = i + 1
            sleep(0.3)
            if not poco(text="Friend request").exists():
                keyevent("BACK")
            elif not poco(nameMatches=MAIN_SELECT_BUTTON).exists():
                keyevent("BACK")

        tools_action.home(poco)
        return flag

    @staticmethod
    def isGroup(poco):
        flag = True
        isGroup = False
        print(poco(text="Message, @").exists())
        if poco(text="Message, @").exists():
            isGroup = True
            sleep(0.5)
            if poco("com.zing.zalo:id/menu_drawer").exists():
                flag = False
                poco("com.zing.zalo:id/menu_drawer").click()
                sleep(1)
                tools_action.swapUp(poco, duration=0.1)
                sleep(1)
                tools_action.swapUp(poco, duration=0.1)
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
            keyevent("BACK")

        return isGroup

    # @staticmethod
    # def isGroup(poco):
    #     if poco(text="Group invitations").exists():
    #         sleep(0.3)
    #         touch(Template("picture/group_point.png"))
    #         try:
    #             poco(text="Decline").wait_for_appearance(timeout=3)
    #             poco(text="Decline").click()
    #             poco(text="DECLINE").wait_for_appearance(timeout=3)
    #             poco(text="DECLINE").click()
    #         except PocoTargetTimeout:
    #             print("Group invitations Decline timeout")
    #
    #         return True
    #     else:
    #         return False

    @staticmethod
    def updateAlis(poco, nickname):
        match_obj = re.match(r'.+[0-9]{10}$', nickname)
        if match_obj is None:
            now_time = int(time.time())
            username = nickname + str(now_time)
            if poco(descMatches="View.*").exists():
                poco(descMatches="View.*").click()
                sleep(0.8)
                poco.click([0.5, 0.450])
                sleep(0.5)
                if poco(nameMatches=ALIAS_TEXT).exists():
                    poco(nameMatches=ALIAS_TEXT).set_text(username)
                    sleep(0.5)
                    poco(text="CHANGE").click()

                    keyevent("BACK")
                    return username

                keyevent("BACK")
                return nickname
        else:
            return nickname

    @staticmethod
    def acceptFriendUpdateAlis(poco, nickname):
        print("nickname:", nickname)
        username = nickname
        match_obj = re.match(r'.+[0-9]{10}$', nickname)
        if match_obj is None:
            now_time = int(time.time())
            username = nickname + str(now_time)
            print("username:", username)
            poco(nameMatches=EDIT_ALIAS).set_text(username)
            sleep(0.2)
            poco(nameMatches=BTN_ACCEPT).click()
            sleep(0.2)
        return username

    @staticmethod
    def searchFriend(poco, keyword):
        poco(textMatches="Search friends.*").click()
        sleep(1)
        poco(textMatches="Search friends.*").set_text(keyword)
        sleep(2)

        if poco(nameMatches=RECEIVE_STRANGER_LABEL).exists():
            label_friend = poco(nameMatches=RECEIVE_STRANGER_LABEL).get_text()
            if label_friend.find("Friends") >= 0:
                poco.click([0.5, 0.248125])
                sleep(1)
                # 如果不是好友，会有个message模式界面
                if poco(nameMatches=STRANGER_MESSAGE_BUTTON).exists():
                    poco(nameMatches=STRANGER_MESSAGE_BUTTON).click()
                return True

        return False

    @staticmethod
    def sendMessage(poco, content):
        return_msg = ""
        if content.find("aocbmj") != -1:
            pass
        elif content.find(".png", 5) > 0:
            content = 'https://aocbmj.s3.ap-east-1.amazonaws.com/' + content
        # 发消息之前先判断是不是有陌生人接收好友请求
        # FriendRequest.isFriendRequest(poco)
        if poco(text="Message").exists():
            send_message = content
            poco(text="Message").set_text(send_message)
            sleep(0.5)
            poco(desc="Send Message").click()
            sleep(1)
            return_msg = FriendRequest.checkMsgStatus(poco)
            print("return_msg", return_msg)

            # username = poco(nameMatches=NICKNAME).get_text() tools_action.snapshot(path, username + "-send-" + str(
            # int(time.time())) + "-" + deviceID + "-" + appCloneID)

        elif poco(nameMatches=INPUT_TEXT).exists():
            send_message = content
            poco(nameMatches=INPUT_TEXT).set_text(send_message)
            sleep(0.5)
            poco(desc="Send Message").click()
            sleep(1)

            return_msg = FriendRequest.checkMsgStatus(poco)
            # username = poco(nameMatches=NICKNAME).get_text() tools_action.snapshot(path, username + "-send-" + str(
            # int(time.time())) + "-" + deviceID + "-" + appCloneID)

        return return_msg

    @staticmethod
    def checkMsgStatus(poco):
        i = 0
        return_msg = "success"
        while i < 2:
            groups = poco("android.view.ViewGroup")
            groups_len = len(groups)
            end_messages = groups[groups_len - 1].get_text().split("\n")
            # print(end_messages)
            sleep(0.5)
            for msg in end_messages:
                if msg == "Sending":
                    return_msg = "消息一直在发送中，请检查网络问题"
                elif msg.find("strangers") > 0:
                    return_msg = "发送失败，不能发送陌生人消息"
            i = i + 1
            if return_msg == "success":
                break

        return return_msg
