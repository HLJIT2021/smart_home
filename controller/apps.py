from flask import Blueprint, render_template, request, redirect, session

from module.app import App, App_relation, control

apps = Blueprint('apps', __name__)


@apps.route('/add')
def add_app():
    u_app = App().user_app(session.get('uid'))
    return render_template('添加设备.html', u_app=u_app)


@apps.route('/app/add', methods=['GET', 'POST'])
def project_add():
    u_app = App().user_app(session.get('uid'))
    return render_template('新增项目.html', u_app=u_app)


@apps.route('/app_add', methods=['POST'])
def app_add():
    project = App()
    app_name = request.form.get('app_name').strip()
    print(app_name)
    project.insert_app(app_name)
    return 'add-pass'



@apps.route('/app/<int:app_id>/control')
def controls(app_id):
    u_app = App().user_app(session.get('uid'))
    app = App().id_app(session.get('app_id'))
    result = control(app_id)
    return render_template('控制逻辑.html', u_app=u_app, app=app, result=result)


@apps.route('/del/project')
def delpro():
    u_app = App().user_app(session.get('uid'))
    return render_template('删除项目.html', u_app=u_app)

@apps.route('/del-project', methods=['POST'])
def delproject():
    project = App().del_project(session.get('app_id'))