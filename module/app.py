from flask import session
from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from common.database import dbconnect
import time
import random

from module.users import Users

dbsession, md, DBase = dbconnect()

# 用户与项目关联的表


class App(DBase):
    __table__ = Table('user_app_relation', md, autoload=True)

    # 查找用户下的项目
    def user_app(self, uid):
        result = dbsession.query(App).filter_by(uid=uid, detail=0).all()
        return result

    def shebei(self, uid, start):
        result = dbsession.query(App).filter_by(uid=uid).limit(start, 7)
        return result

    # 新增项目
    def insert_app(self, app_name):
        uid = session.get('uid')
        app = App(uid=uid, app_name=app_name)
        dbsession.add(app)
        dbsession.commit()

    # 删除项目
    def del_project(self, app_id):
        row = dbsession.query(App).filter_by(app_id).frist()
        row.detail = 1
        dbsession.commit()


# 采集回的数据表
class Data(DBase):
    __table__ = Table('data', md, autoload=True)

    def s_value(self, sid):
        result = dbsession.query(Data).filter_by(
            sid=sid).order_by(Data.dt.desc()).first()
        return result

# 系统跟设备关联的表


class App_relation(DBase):
    __table__ = Table('app_relation', md, autoload=True)

    # 查找状态为未删除的设备
    def select_app(self, app_id):
        result = dbsession.query(App_relation).filter(
            App_relation.app_id == app_id, App_relation.tid < 4).all()
        return result

    # 新增设备
    def insert_relation(self, app_id, sno, s_name, port):
        relation = App_relation(app_id=app_id, sno=sno,
                                s_name=s_name, port=port)
        dbsession.add(relation)
        dbsession.commit()

    # 删除设备
    def del_app(self, sid):
        result = dbsession.query(App_relation).filter_by(sid=sid).delete()
        return result

    # 根据sid查找设备
    def app_info(self, sid):
        row = dbsession.query(App_relation).filter_by(sid=sid).first()
        return row


class App_control(DBase):
    __table__ = Table('app_control', md, autoload=True)

    # 查找控制器
    def control(self, sid):
        row = dbsession.query(App_control).filter_by(sid=sid).first()
        return row


class Control(DBase):
    __table__ = Table('control_state', md, autoload=True)

    def state(self, cid):
        row = dbsession.query(Control).filter_by(cid=cid).first()
        return row


def equipment(sid):
    result = dbsession.query(App_relation, Data).join(
        App_relation, Data.sid == App_relation.sid).filter_by(sid=sid).order_by(Data.dt.desc()).first()
    return result
