from re import A
from flask import Blueprint, render_template, request, redirect, session
from modules import apps


index = Blueprint('index', __name__)


@index.route('/', methods=['get', 'post'])
def user_login():
    if session.get('islogin') == 'true':
        return redirect('/index')
    else:
        return render_template('登录页面.html')



@index.route('/index')
def home():
    u_app = apps.user_project(session.get('uid'))
    return render_template('index.html', u_app=u_app)


@index.route('/project/<int:app_id>')
def read(app_id):
    u_app = apps.user_project(session.get('uid'))
    result = apps.select_sensor(app_id)
    session['app_id'] = app_id
    # control = App_relation().app_control(app_id)
    return render_template('user_app.html', u_app=u_app, result=result)


@index.route('/equipment/<int:sid>')
def reading(sid):
    u_app = apps.user_project(session.get('uid'))
    # row = Data().s_value(sid)
    result = apps.data(sid)
    app = apps.id_app(session.get('app_id'))
    session['sid'] = sid
    app_info = apps.app_info(sid)
    return render_template('设备.html', u_app=u_app, app=app, result=result, app_info=app_info)

@index.route('/controls/<int:sid>')
def controls(sid):
    u_app = apps.user_project(session.get('uid'))
    app = apps.id_app(session.get('app_id'))
    session['sid'] = sid
    row = apps.cont(sid)
    info = apps.app_info(sid)
    return render_template('控制器详细.html', u_app=u_app, app=app, row=row, info=info)


