# -*- encoding=utf8 -*-
import multiprocessing
import signal

from modules.message import *
from common import request_util
import configparser
from apscheduler.schedulers.blocking import BlockingScheduler

config = configparser.ConfigParser()
config.read("devices.ini")
deviceStr = config.get("Devices", "code")
devices = deviceStr.split(",")
print("devices: ", devices)


# devices = ["R485OFDE5DXOAEQS"]


def publishMessage(task, deviceID):
    try:
        msg = Message(deviceID, "publishMessage")
        print("publishMessage msg:", task)
        msg.publicMessage(task)
    except Exception as e:
        print("deviceID:", deviceID, "----exception:", e)
        print("deviceID:", deviceID, "----os.getpid():", os.getpid())
        os.kill(os.getpid(), signal.SIGKILL)
        sleep(2)


def publishCode(task, deviceID):
    try:
        msg = Message(deviceID, "publishCode")
        print("publishCode msg:", task)
        msg.code(task)
    except Exception as e:
        print("deviceID:", deviceID, "----exception:", e)
        print("deviceID:", deviceID, "----os.getpid():", os.getpid())
        os.kill(os.getpid(), signal.SIGKILL)
        sleep(2)


def receiveMessage(deviceID):
    # print("deviceID:" + deviceID + "---appCloneID:", appCloneID)
    try:
        msg = Message(deviceID, "receiveMessage")
        msg.receive()
    except Exception as e:
        print("deviceID:", deviceID, "----exception:", e)
        print("deviceID:", deviceID, "----os.getpid():", os.getpid())
        os.kill(os.getpid(), signal.SIGKILL)
        sleep(2)


def sendFriendDynamic(friends, deviceID):
    if len(friends) > 0:
        try:
            msg = Message(deviceID, "sendFriendDynamic")
            msg.friendDynamic(friends["ID"], friends["content"], friends["imgUrl"])
        except Exception as e:
            print("deviceID:", deviceID, "----exception:", e)
            print("deviceID:", deviceID, "----os.getpid():", os.getpid())
            os.kill(os.getpid(), signal.SIGKILL)
            sleep(2)


def executeTask(deviceID):
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.ERROR)
    auto_setup(__file__)

    cycle_num = RedisDB.incr("send_receive_" + deviceID)
    if int(cycle_num) % 2 == 0:
        url = getEnvUrl() + "/chat_message/getMoreOpenMessageList?deviceID=" + deviceID + "&platform=zalo"
        tasks = request_util.requestGet(url)
        print("tasks:", tasks)
        if len(tasks) > 0:
            tasks_list = tasks["data"]["list"]
            for task in tasks_list:
                strSplit = task["deviceID"]
                arr = strSplit.split("-")
                if deviceID != arr[0]:
                    print("注意" + deviceID + "跟" + arr[0] + "不匹配")
                if task["type"] == "sendMessage":
                    publishMessage(task, deviceID)
                elif task["type"] == "sendFriendDynamic":
                    sendFriendDynamic(task, deviceID)
        else:
            receiveMessage(deviceID)
    else:
        receiveMessage(deviceID)


def job0():
    jobZalo(0)


def job1():
    jobZalo(1)


i = 0


def jobZalo(index):
    global i

    try:
        devices[index]
    except IndexError:
        # print(index, "not exists")
        return False

    i = i + 1
    index = int(index)
    if i > 300:
        os.system("ps aux | grep zalo_double_open | awk '{print $2}' | xargs kill -9")

    print("i:", i)
    p = multiprocessing.Process(target=executeTask, args=(devices[index],))
    p.start()
    p.join(timeout=100)
    p.terminate()
    p.close()
    # print("multiprocessing PID1: ", multiprocessing.current_process().pid)


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(job0, "interval", seconds=6)
    scheduler.add_job(job1, "interval", seconds=6)
    scheduler.start()
    # devices = ["R485OFDE5DXOAEQS", "WSSWAUX8IJRGCYQS"]
