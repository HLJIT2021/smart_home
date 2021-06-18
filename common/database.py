from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/sqldb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/iotcloud?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    id = db.Column(db.Integer, nullable=False)
    info = db.relationship('User_info', backref='uinfo')
    app = db.relationship('User_app', backref='uapp')

class User_info(db.Model):
    __tablename__ = 'user_info'
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(11), nullable=True)

class User_app(db.Model):
    __tablename__ = 'user_app_relation'
    app_id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    app_name = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    condition = db.Column(db.Enum('0', '1'), nullable=False)

    app_relation = db.relationship('App_relation', backref='user_app_relation')

class App_relation(db.Model):
    __tablename__ = 'app_relation'
    sid = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey('user_app_relation.app_id'), nullable=False)
    sno = db.Column(db.String(50), nullable=False)
    tid = db.Column(db.Integer, db.ForeignKey('type.tid'), nullable=False)
    s_name = db.Column(db.String(50), nullable=False)
    kind = db.Column(db.Enum('数据采集', '开关控制'), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    condi = db.Column(db.Enum('0', '1'), nullable=False)

    state = db.relationship('State', backref='control_state')
    data = db.relationship('Data', backref='data')

class App_control(db.Model):
    __tablename__ = 'app_control'
    id = db.Column(db.Integer, primary_key=True)
    ssid = db.Column(db.Integer, db.ForeignKey('app_relation.sid'), nullable=False)
    dsid = db.Column(db.Integer, db.ForeignKey('app_relation.sid'), nullable=False)
    used = db.Column(db.Enum('生效', '不生效'), nullable=False)
    threshold_low = db.Column(db.Float(0), nullable=True)
    threshold_high = db.Column(db.Float(0), nullable=True)

    sensor = db.relationship('App_relation', backref='sensor', foreign_keys=[ssid])
    control = db.relationship('App_relation', backref='control', foreign_keys=[dsid])

class State(db.Model):
    __tablename__ = 'control_state'
    sid = db.Column(db.Integer, db.ForeignKey('app_relation.sid'), primary_key=True)
    state = db.Column(db.Enum('开', '关'), nullable=False)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, db.ForeignKey('app_relation.sid'), nullable=False)
    value = db.Column(db.Float(0), nullable=False)
    dt = db.Column(db.TIMESTAMP, nullable=False)

class Type(db.Model):
    __tablename__ = 'type'
    tid = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255), nullable=True)
    type = db.relationship('App_relation', backref='app_relation')


# if __name__ == '__main__':
#     db.create_all()
    # db.drop_all()
    # result = User.query.filter_by(username='1621276156@qq.com').all()
    # for i in result:
    #     print(i.username, i.password, i.id)


# row1 = Type(tid=1, typename='温度传感器', unit='摄氏度')
# row2 = Type(tid=2, typename='压力传感器'， unit='帕斯卡')
# row3 = Type(tid=3, typename='光照强度传感器', unit='亮度')
# row4 = Type(tid=4, typename='开关控制')
#
# db.session.add_all([row1, row2, row3, row4])
# db.session.commit()

