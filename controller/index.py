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
    # u_app = App().user_app(24)
    # s_app = App_relation().select_app(1)
    # s_value = equipment(1)
    # control_used = App_control().control(1)
    # state = Control().state(1)
    return render_template('index.html', u_app=u_app)


@index.route('/app/<int:app_id>')
def read(app_id):
    u_app = App().user_app(session.get('uid'))
    # app_id = request.path[5:6]
    list1 = []
    result = App_relation().select_app(app_id)
    session['app_id'] = app_id
    # for i in result:
    #     s_id = i.sid
    #     row = Data().s_value(s_id)
    #     if len(row) == 0:
    #         row.value = 0
    #     list1.append([s_id, i.s_name, i.sno, i.port, row.value])
    # print(list1)
    return render_template('user_app.html', u_app=u_app, result=result)


@index.route('/equipment/<int:sid>')
def reading(sid):
    u_app = App().user_app(session.get('uid'))

    row = Data().s_value(sid)
    return render_template('app_user.html', u_app=u_app, row=row)
