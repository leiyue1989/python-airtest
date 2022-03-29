from modules.friend_request import FriendRequest
from airtest.core.api import sleep, keyevent
from const import *


class Stranger(object):

    @staticmethod
    def sendStrangerMsg(poco, phone, content):
        return_msg = ""
        print("phone:", phone)
        print("content:", content)

        if poco(nameMatches=EDIT_PHONE_NUMBER).exists():
            phone = phone.replace("84", "", 1)
            poco(nameMatches=EDIT_PHONE_NUMBER).set_text(phone)
            sleep(0.7)
            poco(textMatches="SEARCH").click()
            sleep(0.7)
            flag = False
            if poco(text="Message").exists():
                flag = True
                poco(text="Message").click()
            elif poco(text="MESSAGE").exists():
                flag = True
                poco(text="MESSAGE").click()

            if flag:
                sleep(0.8)
                return_msg = FriendRequest.sendMessage(poco, content)
                keyevent("BACK")
                sleep(0.5)
                keyevent("BACK")

            if poco(text="NO").exists():
                poco(text="NO").click()
                sleep(0.5)
                poco(nameMatches=EDIT_PHONE_NUMBER).set_text("")
            elif poco(text="CLOSE").exists():
                poco(text="CLOSE").click()
                sleep(0.5)
                poco(nameMatches=EDIT_PHONE_NUMBER).set_text("")

        return return_msg
