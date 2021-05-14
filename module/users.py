from flask import session
from sqlalchemy import Table, MetaData, Column, String
from common.database import dbconnect
import time, random


dbsesion, md, DBase = dbconnect()

class Users(DBase):
    __table__ = Table('user', md, autoload=True)

    # uid = Column(String(20), primary_key=True)
    # username = Column(String(20))
    # password = Column(String(20))
    # nickname = Column(String(20))

    # 查询用户名
    def find_by_username(self, username):
        result = dbsesion.query(Users).filter_by(username=username).all()
        return result


    def do_register(self, username,password):
        # now = time.strftime('%Y-%m-%d %H:%M:%S')  # 时间
        nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
        user = Users(username=username, password=password,
                     nickname=nickname)
        dbsesion.add(user)
        dbsesion.commit()
        return user

    def newnick(self, uid, newnick):
        row = dbsesion.query(Users).filter_by(uid=uid).frist()
        row.nickname = newnick
        dbsesion.commit()

    def newpass(self, uid, newpass):
        row = dbsesion.query(Users).filter_by(uid=uid).frist()
        row.password = newpass
        dbsesion.commit()

class User_info(DBase):
    __table__ = Table('user_info', md, autoload=True)

    def info(self, uid, username):
        info = User_info(uid=uid, email=username)
        dbsesion.add(info)
        dbsesion.commit()


