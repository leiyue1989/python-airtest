# -*- encoding=utf8 -*-
import signal
from modules.message import *
from common import request_util

env = arguments.getEnv()
deviceID = arguments.getDeviceCode()
taskName = arguments.getDoing()

# 获取项目路径
projectPath = getProjectPath()
if not deviceID:
    exit("设备号参数没有传")

# 初始化日志
init_logging(projectPath + "/log/" + deviceID + "/", "app.log")
logger = getLogger()


def publishMessage(task):
    try:
        print(task)
        msg = Message(deviceID, "publishMessage")
        print("publishMessage msg:", task)
        msg.publicMessage(task)
    except Exception as e:
        logger.error("deviceID:" + deviceID + "----exception:" + str(e.args))
        os.kill(os.getpid(), signal.SIGKILL)


def publishCode(task):
    try:
        msg = Message(deviceID, "publishCode")
        print("publishCode msg:", task)
        msg.code(task)
    except Exception as e:
        logger.error("deviceID:" + deviceID + "----exception:" + str(e.args))
        os.kill(os.getpid(), signal.SIGKILL)


def receiveMessage():
    # print("deviceID:" + deviceID + "---appCloneID:", appCloneID)
    try:
        msg = Message(deviceID, "receiveMessage")
        msg.receive()
    except Exception as e:
        logger.error("deviceID:" + deviceID + "----exception:" + str(e.args))
        os.kill(os.getpid(), signal.SIGKILL)


def sendFriendDynamic(friends):
    if len(friends) > 0:
        try:
            msg = Message(deviceID, "sendFriendDynamic")
            msg.friendDynamic(friends["ID"], friends["content"], friends["imgUrl"])
        except Exception as e:
            logger.error("deviceID:" + deviceID + "----exception:" + str(e.args))
            os.kill(os.getpid(), signal.SIGKILL)


def executeTask():
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
                    publishMessage(task)
                elif task["type"] == "sendFriendDynamic":
                    sendFriendDynamic(task)
    else:
        receiveMessage()


callfunDict = {
    "publish_message": publishMessage,
    "receive_message": receiveMessage,
    "publish_code": publishCode,
    "execute_task": executeTask,
}


def callfunMethod(call):
    fun = callfunDict.get(call)
    return fun()


callfunMethod(taskName)
