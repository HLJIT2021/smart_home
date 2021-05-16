from re import A
from flask import Blueprint, render_template, request, redirect, session
from module.app import App, App_relation, Data, Control, App_control, equipment

index = Blueprint('index', __name__)


@index.route('/', methods=['get', 'post'])
def user_login():
    if session.get('islogin') == 'true':
        return redirect('/index')
    else:
        return render_template('登录页面.html')


@index.route('/index')
def home():
    u_app = App().user_app(session.get('uid'))
    return render_template('index.html', u_app=u_app)


@index.route('/app/<int:app_id>')
def read(app_id):
    u_app = App().user_app(session.get('uid'))
    result = App_relation().select_app(app_id)
    session['app_id'] = app_id
    return render_template('user_app.html', u_app=u_app, result=result)


@index.route('/equipment/<int:sid>')
def reading(sid):
    u_app = App().user_app(session.get('uid'))
    row = Data().s_value(sid)
    session['sid'] = sid
    app_info = App_relation().app_info(sid)
    return render_template('设备详细信息.html', u_app=u_app, row=row, app_info=app_info)
