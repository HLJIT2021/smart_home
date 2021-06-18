from flask import Blueprint, render_template, request, redirect, session

from modules import apps

project = Blueprint('project', __name__)


@project.route('/add')
def add_app():
    u_app = apps.user_project(session.get('uid'))
    type = apps.type()
    return render_template('添加设备.html', u_app=u_app, type=type)

@project.route('/add/control')
def add_co():
    u_app = apps.user_project(session.get('uid'))
    result = apps.select_sensor(session.get('app_id'))
    return render_template('添加控制方案.html', u_app=u_app, result=result)

@project.route('/add_control', methods=['POST'])
def add_control():
    app_id = session.get('app_id')
    s_name = request.form.get('s_name').strip()
    sno = request.form.get('sno').strip()
    ssid = request.form.get('ssid')
    port = request.form.get('port').strip()
    tid = 4
    kind = '开关控制'

    if len(apps.ports(app_id, port)) > 0:
        return 'add-fail'
    else:
        apps.insert_app(app_id, sno, tid, s_name, kind, port)
        row = apps.app_rela(app_id, sno, port)
        print(ssid)
        dsid = row.sid
        apps.insert_control(ssid, dsid)
        return 'add-pass'

@project.route('/app/add', methods=['GET', 'POST'])
def project_add():
    u_app = apps.user_project(session.get('uid'))
    return render_template('新增项目.html', u_app=u_app)


@project.route('/project_add', methods=['POST'])
def projectadd():
    app_name = request.form.get('app_name').strip()
    apps.insert_project(app_name)
    return 'add-pass'

@project.route('/app_add', methods=['POST'])
def app_add():
    app_id = session.get('app_id')
    # app_id = 1
    s_name = request.form.get('s_name').strip()
    sno = request.form.get('sno').strip()
    port = request.form.get('port').strip()
    tid = request.form.get('tid')
    if tid == "5":
        kind = '开关控制'
    else:
        kind = '数据采集'

    if len(apps.ports(app_id, port)) > 0:
        return 'add-fail'
    else:
        apps.insert_app(app_id, sno, tid, s_name, kind, port)
        return 'add-pass'

@project.route('/project/<int:app_id>/control')
def controls(app_id):
    u_app = apps.user_project(session.get('uid'))
    app = apps.id_app(session.get('app_id'))
    result = apps.app_control(app_id)
    return render_template('控制逻辑.html', u_app=u_app, app=app, result=result)


@project.route('/del/project')
def delpro():
    u_app = apps.user_project(session.get('uid'))
    return render_template('删除项目.html', u_app=u_app)

@project.route('/del-project', methods=['POST'])
def delproject():
    apps.del_project(session.get('app_id'))
    return 'del-pass'

@project.route('/threshold', methods=['POST'])
def threshold():
    high = request.form.get('high')
    low = request.form.get('low')
    sid = session.get('sid')

    apps.threshold(sid, high, low)
    return 'modify-pass'

@project.route('/control-switch', methods=['POST'])
def control_switch():
    sid = session.get('sid')
    state = apps.state(sid)
    if state == '开':
        newstate = '关'
        apps.newst(sid, newstate)
        return 'close'
    else:
        newstate = '开'
        apps.newst(sid, newstate)
        return 'open'


@project.route('/control-automatic', methods=['POST'])
def control_automatic():
    sid = session.get('sid')
    used = apps.cont(sid).used
    if used == '生效':
        newused = '不生效'
        apps.automatic(sid, newused)
        return 'close'
    else:
        newused = '生效'
        apps.automatic(sid, newused)
        return 'open'


@project.route('/del-app', methods=['POST'])
def drop_app():
    sid = request.form.get('sid')
    print(sid)
    apps.del_app(sid)
    return 'del-pass'



