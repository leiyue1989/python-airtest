import sys, os
import configparser
import logging
from logging import handlers
import requests, json
from airtest.core.api import sleep

from common import arguments
from const import *

env = ""
projectPath = ""


def converNum(num):
    if num.find("w") != -1:
        tmp = num.replace("w", "")
        if tmp.find(".") != -1:
            res = float(tmp) * 10000
        else:
            res = int(tmp) * 10000
    elif num.find("亿") != -1:
        tmp = num.replace("亿", "")
        if tmp.find(".") != -1:
            res = float(tmp) * 100000000
        else:
            res = int(tmp) * 100000000
    else:
        res = int(num)

    return int(res)


def fansLeve(fans):
    if fans < 1000:
        return "T4"
    elif 1000 <= fans < 5000:
        return "T3"
    elif 5000 <= fans < 10000:
        return "T2"
    else:
        return "T1"


def getDeviceCode():
    if len(sys.argv) < 3:
        return False
    return sys.argv[2]


def getDbConfig():
    environment = getEnv()
    cf = configparser.ConfigParser()
    path = getProjectPath()
    cf.read(path + "/config.ini")
    print(path + "/config.ini")
    print("mysql-db-" + environment + "")
    items = cf.items("mysql-db-" + environment + "")
    return {"host": items[0][1], "username": items[1][1], "password": items[2][1], "db": items[3][1]}


def getEnv():
    env = arguments.getEnv()
    return env


def init_logging(filepath, filename):
    logger = logging.getLogger("airtest")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                  datefmt="%m/%d/%Y %I:%M:%S %p")  # 创建一个格式化对象
    console = logging.StreamHandler()  # 配置日志输出到控制台
    console.setLevel(logging.ERROR)  # 设置输出到控制台的最低日志级别
    console.setFormatter(formatter)  # 设置格式
    logger.addHandler(console)

    if not os.path.exists(filepath):
        os.makedirs(filepath, mode=0o777)

    file_time_rotating = handlers.TimedRotatingFileHandler(filepath + filename, when="h", interval=6,
                                                           backupCount=5)
    file_time_rotating.setLevel(logging.DEBUG)
    file_time_rotating.setFormatter(formatter)
    logger.addHandler(file_time_rotating)


def getLogger():
    return logging.getLogger("airtest")


def postRequest(url, params):
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    response = requests.post(url, data=json.dumps(params), headers=headers, timeout=6).text
    return response


def getEnvUrl():
    environment = getEnv()
    if environment == "local":
        url = "http://localhost:7778"
    elif environment == "test":
        url = "http://session-notice-api.test.goooxi.com"
    elif environment == "product" or environment == "lazy":
        url = "http://session-notice-api.goooxi.com"
    else:
        url = "http://session-notice-api.goooxi.com"
    return url


def getProjectPath():
    global projectPath
    if projectPath != "":
        return projectPath
    projectPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return projectPath







