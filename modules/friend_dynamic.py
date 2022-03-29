from airtest.core.cv import Template

from modules.friend_request import FriendRequest
from airtest.core.api import sleep, touch
from db.redisDB import RedisDB
from common import tools


class FriendDynamic(object):

    @staticmethod
    def sendFriendDynamic(poco, content):
        poco("com.zing.zalo:id/zalo_view_container").offspring("com.zing.zalo:id/sliding_tabs").child(
            "android.widget.LinearLayout").child("android.widget.FrameLayout")[3].offspring(
            "com.zing.zalo:id/icon").click()
        sleep(1.5)
        touch(Template("picture/howareyou.png"))
        poco(name="com.zing.zalo:id/etDesc").wait_for_appearance(timeout=5)
        poco(name="com.zing.zalo:id/etDesc").set_text(content)
        sleep(2)
        poco("com.zing.zalo:id/zalo_view_container").offspring(
            "com.zing.zalo:id/quick_picker_container").offspring(
            "com.zing.zalo:id/update_status_draggable_layout").offspring(
            "com.zing.zalo:id/recycler_view").child(
            "android.view.View")[0].click()
        poco("com.zing.zalo:id/landing_page_checkbox_select").wait_for_appearance(timeout=5)
        poco("com.zing.zalo:id/landing_page_checkbox_select").click()  # 选中照片复选框

        poco("com.zing.zalo:id/landing_page_btn_done").wait_for_appearance(timeout=5)
        poco("com.zing.zalo:id/landing_page_btn_done").click()  # 选择照片打勾
        sleep(1)
        poco("com.zing.zalo:id/menu_done").wait_for_appearance(timeout=5)
        poco("com.zing.zalo:id/menu_done").click()  # post提交
        return True

    @staticmethod
    def downloadPicture(poco):
        sleep(3)
        print("开始点击前")
        poco.click([0.5, 0.74])
        sleep(3)
        isDownload = False
        if poco(name="com.zing.zalo:id/view_hd_image").exists():
            isDownload = True
        else:
            i = 0
            while i < 30:
                i = i + 1
                if poco(name="com.zing.zalo:id/btn_load_hq_image").exists():
                    isDownload = True
                    break
                if poco(text="RETRY").exists():
                    poco(text="RETRY").click()
                sleep(1)

        if isDownload:
            if poco(name="com.zing.zalo:id/menu_photo_download").exists():
                poco(name="com.zing.zalo:id/menu_photo_download").click()
                return True
        else:
            if poco("android.widget.ImageView").exists():
                sleep(3)
                poco.long_click((0.5, 0.5), duration=2)
                if poco(text="Save photo").exists():
                    poco(text="Save photo").click()
                    sleep(10)
                    return True

        return False
