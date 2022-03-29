#!/usr/bin/python3
# coding=utf-8
# from airtest.core.api import *
from airtest.core.android import Android

from common.tools import *
from common.tools_action import *
from modules.stranger import Stranger
from const import *
from db.redisDB import RedisDB
from modules.friend_request import FriendRequest
from modules.friend_dynamic import FriendDynamic
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import re
from modules.history import History
import random


class Message(object):

    def __init__(self, deviceID, event):
        self.android = Android(deviceID)
        self.event = event
        self.poco = AndroidUiautomationPoco(self.android)
        self.deviceID = deviceID
        self.appCloneID = "1"
        projectPath = getProjectPath()
        init_logging(projectPath + "/log/" + deviceID + "/", "app.log")
        self.logger = getLogger()
        connect_device("android://127.0.0.1:5037/" + deviceID + "?cap_method=javacap&touch_method=adb")

        count = RedisDB.incr("incr_" + deviceID)
        self.logger.info(deviceID + "增长次数：" + str(count))
        if int(count) % 10 == 0:
            History.clearMemory(self.poco)
            raise Exception
        if self.android.is_locked():
            self.android.wake()
            sleep(1)
            self.poco("com.android.systemui:id/notification_stack_scroller").swipe([-0.0191, -0.3167])
            sleep(1)
            self.poco("com.android.systemui:id/notification_stack_scroller").swipe([-0.0191, -0.3167])

        sleep(0.5)

        self.startZalo()
        sleep(2)
        if self.poco(text="English").exists():
            raise Exception

        home(self.poco)
        if not exists(Template("picture/QRcode.png")):
            self.startZalo()
            sleep(2)

    # ----------------publish code start -------------------
    # =========================================================
    def code(self, code):
        print("--------发验证码开始---------")
        print("device_code:", self.deviceID)
        # 接受好友请求
        poco = self.poco

        poco.click([0.943, 0.073])
        poco(text="Add friend").wait_for_appearance(timeout=3)
        poco(text="Add friend").click()
        res_message = Stranger.sendStrangerMsg(poco, code["phone"], code["yzmCode"])
        if res_message == "success":
            ret = "0"
            status = 2
        elif res_message == "stranger":
            ret = "2"
            status = 3
        else:
            ret = "1"
            status = 3

        url = "https://notice.seven-clubs.com/pay/echo"
        params = {
            "phone": code["phone"],
            "code": code["yzmCode"],
            "do": "PhoneCode",
            "ret": ret
        }
        postRequest(url, params)
        params = {
            "platform": 'zalo',
            "ID": code["ID"],
            "remark": res_message,
            "status": status
        }

        url = getEnvUrl() + "/chat_code/publishChatCode"
        postRequest(url, params)
        home(poco)

    # ----------------spublish code end -------------------
    # =========================================================

    # ----------------send message start -------------------
    def publicMessage(self, chat):
        self.logger.info("-------------发消息开始--------------")
        poco = self.poco
        account = chat["account"]
        content = chat["content"]
        remark = chat["remark"]
        phone = chat["phone"]

        if remark == "marketing-stranger":
            poco.click([0.943, 0.073])
            poco(text="Add friend").wait_for_appearance(timeout=3)
            poco(text="Add friend").click()
            res_message = Stranger.sendStrangerMsg(poco, phone, content)
            if res_message == "":
                status = 2
            elif res_message == "success":
                status = 1
            else:
                status = 2
            params = {
                "platform": "zalo",
                "ID": int(chat["ID"]),
                "remark": "marketing-stranger",
                "status": status
            }
            url = getEnvUrl() + "/chat_message/publishChatMessage"
            postRequest(url, params)
            home(poco)
            return
        sleep(1)
        friend_list = poco("android.view.View")
        is_friend_chat = False

        for friend in friend_list:
            if friend.get_text() is None:
                continue
            friend_arr = friend.get_text().split("\n")
            # 如果会话列表里面能找到需要发消息的对象

            if friend_arr[0] == account:
                pos = friend.get_position()
                poco.click([pos[0], pos[1]])
                res_message = FriendRequest.sendMessage(poco, content)
                is_friend_chat = True
                self.__postMethod(res_message, chat)
                break
        # 如果好友会话找到了，继续循环下一个
        if is_friend_chat:
            home(poco)
            return
        is_search = FriendRequest.searchFriend(poco, account)

        if is_search:
            res_message = FriendRequest.sendMessage(poco, content)
            self.__postMethod(res_message, chat)
        else:
            self.__postMethod("该用户数据库没有电话记录，也不是好友关系，找不到此人发送失败", chat)

        self.logger.info("-------------发消息结束--------------")
        home(poco)

    def __postMethod(self, res_message, chat):
        platform = chat["platform"]
        ID = chat["ID"]

        if res_message == "":
            status = 2
        elif res_message == "success":
            status = 1
        else:
            status = 2

        if chat["remark"] == "marketing-friend":
            res_message = "marketing-friend"
        params = {
            "platform": platform,
            "ID": int(ID),
            "remark": res_message,
            "status": status
        }
        self.logger.info("-------------发消息请求参数开始--------------")
        url = getEnvUrl() + "/chat_message/publishChatMessage"
        postRequest(url, params)
        self.logger.info("-------------发消息请求参数结束--------------")

    # ----------------send message end -------------------
    # =========================================================

    # ----------------receive message start -------------------
    # =========================================================
    def receive(self):

        poco = self.poco
        self.logger.info("-------------接受好友开始--------------")
        FriendRequest.acceptFriendRequest(poco, self.deviceID, self.appCloneID)
        self.logger.info("-------------接受好友结束--------------")
        sleep(1)

        self.logger.info("-------------接收消息开始--------------")
        count = 0
        while count < 2:
            items = poco("android.view.View")
            if len(items) >= 6:
                if random.randint(1, 15) == 2:
                    History.deleteHistory(poco)
            count = count + 1
            for item in items:
                if item.get_text() is None:
                    continue
                messages = item.get_text().split("\n")
                # print("messages:", messages)
                if len(messages) < 4:
                    # print("len(messages):", len(messages))
                    continue

                message_num = messages[3]
                if message_num == "":
                    if messages[1] == "Group invitations":
                        message_num = 1
                    else:
                        continue

                pos = item.get_position()
                if pos[0] > 2:
                    continue
                receive_time = 0
                try:
                    poco.click([pos[0], pos[1]])
                    tmp_time = re.findall("\d+", messages[1])
                    if len(tmp_time) >= 1:
                        if int(tmp_time[0]) == 1:
                            receive_time = 0
                        else:
                            receive_time = int(tmp_time[0]) * 60 - 60
                except Exception:
                    continue
                sleep(0.5)
                print("messages:", messages[1])

                # 如果接收到了陌生人的会话窗口信息，里面还有一个会话列表
                if poco(nameMatches=IS_STRANGER_LIST).exists():
                    home(poco)
                else:
                    # print("=======chat_windows start========")
                    # 如果已经是会话列表，则直接进入了聊天窗口
                    self.__chatWindows(message_num, receive_time)
        self.logger.info("-------------接收消息结束--------------")
        home(poco)

    def __chatWindows(self, message_num, receive_time):
        poco = self.poco
        # 发消息之前先判断是不是有陌生人接收好友请求
        flag = FriendRequest.isGroup(poco)
        if flag:
            home(poco)
            return

        groups = poco("android.view.ViewGroup")
        groups_len = len(groups)
        if message_num == "N":
            sleep(0.5)
            message_num = 1
        elif message_num == "5+":
            message_num = groups_len
        try:
            message_num = int(message_num)
        except Exception:
            # keyevent("BACK")
            message_num = 1
        i = 0
        nickname = poco(nameMatches=NICKNAME).get_text()
        # 检查是否修改匿名
        # username = FriendRequest.updateAlis(poco, nickname)
        username = nickname
        sleep(0.5)
        env = getEnv()
        if env == "lazy" or env == "local":
            path = "/Users/denggang/github/picture/zalo"
        else:
            path = "/www/picture/zalo"
        # 截图聊天消息
        snapshot(path,
                 username + "-receive-" + str(int(time.time())) + "-" + self.deviceID + "-" + self.appCloneID)

        # 进入聊天窗口迅速获取消息， 然后返回再把消息推送给远端接口，
        # 避免在读取消息过程中又有消息进来则没有接收到
        # home(poco)
        sleep(0.5)
        list_msg = []
        for group in reversed(groups):
            i += 1
            infos = group.get_text().split("\n")
            if i <= message_num:
                dict_msg = {}
                infos_len = len(infos)

                if infos_len == 4:
                    match_obj = re.match(r'\d+:\d+', infos[2])
                    if match_obj is None:
                        dict_msg["msg"] = infos[2]
                        dict_msg["time"] = ""
                    else:
                        dict_msg["msg"] = infos[1]
                        dict_msg["time"] = infos[2]
                    if i != 1 and dict_msg["time"] != "":
                        break
                elif infos_len == 5:
                    dict_msg["msg"] = infos[2]
                    dict_msg["time"] = infos[3]
                    if i != 1 and dict_msg["time"] != "":
                        break
                else:
                    dict_msg["msg"] = infos[1]
                    dict_msg["time"] = ""
                if dict_msg["msg"] == "[Picture]":
                    sleep(1)
                    pos = group.get_position()
                    poco.click([pos[0], pos[1]])
                    # poco.click([0.5, 0.24])
                    sleep(5)
                    snapshot(path, username + "-receive-" + str(
                        int(time.time())) + "-" + self.deviceID + "-" + self.appCloneID)
                    sleep(0.5)
                    keyevent("BACK")

                list_msg.append(dict_msg)

        url = getEnvUrl()
        real_time = int(time.time()) + int(receive_time)
        for message in reversed(list_msg):
            params = {
                "platform": "zalo",
                "content": message["msg"],
                "deviceID": self.deviceID,
                "account": username,
                "nickname": nickname,
                "appCloneID": int(self.appCloneID),
                "receiveTime": real_time
            }
            self.logger.info("-------------接收消息请求参数开始--------------")
            print("params:", params)
            postRequest(url + "/chat_message/receiveChatMessage", params)
            self.logger.info("-------------接收消息请求参数结束--------------")
            sleep(0.5)
        keyevent("BACK")
        sleep(1)

    # ----------------receive message end -------------------
    # =========================================================

    def friendDynamic(self, ID, content, img_url):
        poco = self.poco
        count = RedisDB.incr("firendDynamic_" + self.deviceID + "_" + self.appCloneID)
        print("朋友圈尝试次数：", count)
        if count > 10:
            print("尝试发朋友圈失败")
            params = {
                "ID": int(ID),
                "status": 2
            }
            postRequest(getEnvUrl() + "/vestuser/info/postFriendDynamic", params)
            return

        picture_key = "firendDynamic_picture" + self.deviceID + "_" + self.appCloneID
        print("picture_key get value:", RedisDB.getKey(picture_key))
        picture_value = RedisDB.getKey(picture_key)
        if picture_value is not None:
            picture_value = picture_value.decode("utf-8")

        if picture_value == "post_success":
            # 提交成功接口
            params = {
                "ID": int(ID),
                "status": 3
            }
            postRequest(getEnvUrl() + "/vestuser/info/postFriendDynamic", params)
            return

        if picture_value == "download_success":
            FriendDynamic.sendFriendDynamic(poco, content)
            params = {
                "ID": int(ID),
                "status": 3
            }
            RedisDB.setKey(picture_key, "post_success")
            RedisDB.expireTime(picture_key)
            sleep(10)
            postRequest(getEnvUrl() + "/vestuser/info/postFriendDynamic", params)
            return

        is_search = FriendRequest.searchFriend(poco, "leiyue20161116")
        download_result = False
        if is_search:
            FriendRequest.sendMessage(poco, img_url)
            sleep(1)
            FriendRequest.sendMessage(poco, img_url)
            download_result = FriendDynamic.downloadPicture(poco)

        if download_result:
            RedisDB.setKey(picture_key, "download_success")
            RedisDB.expireTime(picture_key)
            sleep(10)

        home(poco)

    def startZalo(self):
        sleep(0.1)
        if self.poco(text="仅限充电").exists():
            sleep(0.5)
            self.poco(text="仅限充电").click()
            sleep(0.5)
        if self.poco(text="确定").exists():
            sleep(0.5)
            self.poco(text="确定").click()
            sleep(0.5)

        self.android.start_app(ZALO_APP)
