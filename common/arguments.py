import argparse

# 解析命令行传入参数

parser = argparse.ArgumentParser(description='manual to this script')
# parser.add_argument('--deviceCode', type=str, default=None)
parser.add_argument('--env', type=str, default="local")
parser.add_argument('--device', type=str, default="")
parser.add_argument('--doing', type=str, default="")
parser.add_argument('--param1', type=str, default="")

args = parser.parse_args()


# 获取传入的设备号
def getDeviceCode():
    return args.device


# 获取传入的执行环境
def getEnv():
    return args.env


def getDoing():
    return args.doing


def getParam1():
    return args.param1