# -*- encoding=utf8 -*-
import tornado
from tornado import ioloop, web

from modules.message import *
import configparser
from tornado.process import Subprocess
from common import tools

projectPath = tools.getProjectPath()
tools.init_logging(projectPath + "/log/", "app.log")
logger = tools.getLogger()

config = configparser.ConfigParser()
config.read("devices.ini")
deviceStr = config.get("Devices", "code")
devices = deviceStr.split(",")

env = arguments.getEnv()


@tornado.gen.coroutine
def run_command(command):
    """run command"""
    process = Subprocess(
        [command],
        stdout=Subprocess.STREAM,
        stderr=Subprocess.STREAM,
        shell=True
    )
    out, err = yield [process.stdout.read_until_close(), process.stderr.read_until_close()]
    raise tornado.gen.Return((out, err))


i = 0


async def jobZalo(index):
    global i
    try:
        devices[index]
    except IndexError:
        # print(index, "not exists")
        return False
    logging.info("i: ", i)
    i = i + 1
    index = int(index)
    if i > 300:
        await run_command("ps aux | grep zalo_single_open | awk '{print $2}' | xargs kill -9")

    cmd_psef = "ps -ef | grep 'timeout.*" + devices[index] + "' | grep -v grep | wc -l"
    res, err = await run_command(cmd_psef)
    num = res.decode("utf-8")

    logging.info("num:" + str(num) + "-----" + devices[index])
    if int(num) < 1:
        kill_gw = "ps aux | grep " + devices[index] + " | awk '{print $2}' | xargs kill -9"
        await run_command(kill_gw)
        if env != 'product':
            cmd_gw = 'gtimeout 120 /usr/bin/python3 /Users/denggang/github/project/zalo-autotest/zalo.py ' \
                     '--doing execute_task --env ' + env + ' --device ' + devices[index]
        else:
            cmd_gw = 'timeout 120 /usr/bin/python3 /home/denggang/github/project/zalo-autotest/zalo.py ' \
                     '--doing execute_task --env ' + env + ' --device ' + devices[index]

        r_cmd_res, r_cmd_err = await run_command(cmd_gw)


if __name__ == "__main__":
    io = tornado.ioloop.IOLoop.current()
    ioloop.PeriodicCallback(lambda: jobZalo(0), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(1), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(2), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(3), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(4), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(5), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(6), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(7), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(8), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(9), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(10), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(11), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(12), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(13), 7000).start()
    ioloop.PeriodicCallback(lambda: jobZalo(14), 7000).start()

    io.start()
