from sqlalchemy import Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# 定义 Player 对象:
class DouyinUsers(Base):
    # 表的名字:
    __tablename__ = 'goadmin_douyin_users'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    douyinid = Column(String(20))
    nickname = Column(String(50))
    brief = Column(String)
    main_link = Column(String)
    follow = Column(Integer)
    fans = Column(Integer)
    fans_level = Column(CHAR)
    likes = Column(Integer)
    composition = Column(Integer)
    city = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    # brief = Column(Float(3, 2))
