# FileName : DBHandle.py
# Author   : Adil
# DateTime : 2018/11/29 2:03 PM
# SoftWare : PyCharm

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.tools import getDbConfig, getLogger


class DataBaseHandle:
    def __init__(self, host=None, username=None, password=None, database=None):
        if host is None and username is None:
            cf = getDbConfig()
            logger = getLogger()
            logger.info("数据库链接：" + str(cf))
            self.host = cf["host"]
            self.username = cf["username"]
            self.password = cf["password"]
            self.database = cf["db"]
        else:
            self.host = host
            self.username = username
            self.password = password
            self.database = database

    def connect(self):
        engine = create_engine("mysql+{driver}://{username}:{password}@{server}:3306/{database}?charset={charset}"
                               .format(driver="pymysql",
                                       username=self.username,
                                       password=self.password,
                                       server=self.host,
                                       database=self.database,
                                       charset="utf8mb4"),
                               pool_size=100,
                               max_overflow=100,
                               pool_recycle=1,
                               pool_pre_ping=True,
                               echo=False)
        DBSession = sessionmaker(bind=engine)
        # 创建 session 对象:
        session = DBSession()
        return session
