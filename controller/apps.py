from flask import Blueprint, render_template, request, redirect, session

from module.app import App

apps = Blueprint('apps', __name__)


@apps.route('/add')
def add_app():
    u_app = App().user_app(24)
    # s_name = request.form.get('a_name').strip()
    # sno = request.form.get('a_name').strip()
    # port = request.form.get('port').strip()
    # type = request.form.get('type').strip()
    # app_id = session.get('app_id')
    return render_template('添加设备.html', u_app=u_app)


@apps.route('/app/add', methods=['GET', 'POST'])
def project_add():
    u_app = App().user_app(session.get('uid'))
    return render_template('新增项目.html', u_app=u_app)


@apps.route('/app_add', methods=['POST'])
def app_add():
    project = App()
    a_name = request.form.get('app_name').strip()
    project.insert_app(a_name)
    return 'add-pass'
