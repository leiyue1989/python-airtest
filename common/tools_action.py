from airtest.core.api import *
from const import *
from airtest.aircv.utils import cv2_2_pil


# 向上滑动
def swapUp(poCo, duration=0.05):
    xy = poCo.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe((0.5 * x, 0.8 * y), (0.5 * x, duration * y), duration)


# 向下滑动
def swapDown(poCo, duration=0.3):
    xy = poCo.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe((0.5 * x, 0.4 * y), (0.5 * x, 0.8 * y), duration)


# 向左滑动
def swapLeft(poCo, duration=0.3):
    xy = poCo.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe((0.9 * x, 0.5 * y), (0.5 * x, 0.5 * y), duration)


# 向右滑动
def swapRight(poCo, duration=0.3):
    xy = poCo.get_screen_size()
    x = xy[0]
    y = xy[1]
    swipe((0.5 * x, 0.5 * y), (0.9 * x, 0.5 * y), duration)


# 关闭app应用
def closeApp(package):
    stop_app(package)


# 卸载应用
def unInstallApp(package):
    uninstall(package)


# 安装app
def installApp(filepath):
    install(filepath)


def getPhoneXYPos(x, y):
    width = G.DEVICE.display_info['width']
    height = G.DEVICE.display_info['height']
    return {"x": width / x, "y": y / height}


def home(poco):
    for num in range(1, 8):
        sleep(0.7)
        if not poco(nameMatches=MAIN_SELECT_BUTTON).exists():
            keyevent("BACK")
        else:
            if poco("android.widget.TextView").exists():
                msg = poco("android.widget.TextView").get_text()
                if msg == "Messages":
                    break
                poco.click([0.0888, 0.9675])
            break


def snapshot(path, name):
    screen = G.DEVICE.snapshot()
    pil_img = cv2_2_pil(screen)
    pil_img.save(path + "/" + name + ".png", quality=99, optimize=True)
