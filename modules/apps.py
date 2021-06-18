from flask import session

from common.database import *

# 查找用户下的项目
def user_project(uid):
    result = db.session.query(User_app).filter_by(uid=uid, condition='0').all()
    return result

# 通过app_id查找设备
def select_app(app_id):
    result = db.session.query(App_relation).filter(
        App_relation.app_id == app_id).all()
    return result

# app_id查找传感器
def select_sensor(app_id):
    result = db.session.query(App_relation).filter(App_relation.app_id == app_id,
                                                   App_relation.tid != 4, App_relation.condi == '0').all()
    return result

def shebei(uid, start):
    result = db.session.query(User_app).filter_by(uid=uid).limit(start, 7)
    return result

# 新增项目
def insert_project(app_name):
    uid = session.get('uid')
    app = User_app(uid=uid, app_name=app_name, detail=app_name, condition='0')
    db.session.add(app)
    db.session.commit()

# 删除项目
def del_project(app_id):
    row = db.session.query(User_app).filter_by(app_id=app_id).first()
    row.condition = '1'
    db.session.commit()

# 根据app_id查找项目
def id_app(app_id):
    row = db.session.query(User_app).filter_by(app_id=app_id).first()
    return row


# 新增设备
def insert_app(app_id, sno, tid, s_name, kind, port):
    relation = App_relation(app_id=app_id, sno=sno, tid=tid,
                            s_name=s_name, kind=kind, port=port, condi='0')
    db.session.add(relation)
    db.session.commit()

# 配置控制器
def insert_control(ssid, dsid):
    relation = App_control(ssid=ssid, dsid=dsid, used='不生效')
    db.session.add(relation)
    db.session.commit()
    row = State(sid=dsid, state='关')
    db.session.add(row)
    db.session.commit()

# 删除设备
def del_app(sid):
    row = db.session.query(App_relation).filter_by(sid=sid).first()
    row.condi = '1'
    db.session.commit()

# 根据sid查找设备
def app_info(sid):
    row = db.session.query(App_relation).filter_by(sid=sid, condi='0').first()
    return row

# 精确查找设备
def app_rela(app_id, sno, port):
    row = db.session.query(App_relation).filter_by(app_id=app_id, sno=sno, port=port, condi='0').first()
    return row

# 判断接口是否已使用
def ports(app_id, port):
    result = db.session.query(App_relation).filter_by(
        app_id=app_id, port=port).all()
    return result

# 查找项目下的控制器
def app_control(app_id):
    result = db.session.query(App_relation).filter(
        App_relation.app_id == app_id, App_relation.tid == 4).all()
    return result


# 在app_control表中通过sid查找控制器
def cont(sid):
    row = db.session.query(App_control).filter(
        App_control.dsid == sid).first()
    return row

# 找出所有的类别
def type():
    result = db.session.query(Type).all()
    return result

# 通过tid查询类别
def app_type(tid):
    row = db.session.query(Type).filter_by(tid=tid).all()
    return row

# 查找值
def data(sid):
    result = db.session.query(Data).filter_by(sid=sid).order_by(Data.dt.desc()).limit(8)
    return result

# 修改控制区间
def threshold(sid, high, low):
    row = db.session.query(App_control).filter_by(dsid=sid).first()
    row.threshold_low = low
    row.threshold_high = high
    db.session.commit()

# 返回开关状态
def state(sid):
    row = db.session.query(State).filter_by(sid=sid).first()
    return row.state

# 变更开关状态
def newst(sid, newstate):
    row = db.session.query(State).filter_by(sid=sid).first()
    row.state = newstate
    db.session.commit()

# 变更自动控制开关
def automatic(sid, newused):
    row = db.session.query(App_control).filter_by(dsid=sid).first()
    row.used = newused
    db.session.commit()