from flask import session
from sqlalchemy import Table, MetaData, Column, String
from common.database import dbconnect
import time
import random


dbsesion, md, DBase = dbconnect()


class Users(DBase):
    __table__ = Table('user', md, autoload=True)

    # 查询用户名
    def find_by_username(self, username):
        result = dbsesion.query(Users).filter_by(username=username).all()
        return result

    # 注册
    def do_register(self, username, password):
        # now = time.strftime('%Y-%m-%d %H:%M:%S')  # 时间
        nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
        user = Users(username=username, password=password,
                     nickname=nickname)
        dbsesion.add(user)
        dbsesion.commit()
        return user

    # 根据uid查用户名
    def user_name(self, uid):
        row = dbsesion.query(Users).filter_by(uid=uid).first()
        return row

    # 修改用户名
    def newnick(self, uid, newnick):
        row = dbsesion.query(Users).filter_by(uid=uid).first()
        row.nickname = newnick
        dbsesion.commit()

    def newpass(self, uid, newpass):
        row = dbsesion.query(Users).filter_by(uid=uid).first()
        row.password = newpass
        dbsesion.commit()


class User_info(DBase):
    __table__ = Table('user_info', md, autoload=True)

    def info(self, uid, username):
        info = User_info(uid=uid, email=username)
        dbsesion.add(info)
        dbsesion.commit()

    def info_user(self, uid):
        row = dbsesion.query(User_info).filter_by(uid=uid).first()
        return row
