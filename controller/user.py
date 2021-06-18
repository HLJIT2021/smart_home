import re
import hashlib
from common.utility import ImageCode
from flask import Blueprint, render_template, request, session, redirect, make_response

from modules import users
from modules import apps

user = Blueprint('user', __name__)


@user.route('/vcode')
def vcode():
    code, bstring = ImageCode().get_code()
    response = make_response(bstring)
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()
    return response



@user.route('/login', methods=['POST'])
def login():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()

    # 验证图形验证码是否正确
    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'

    else:
        # 实现登录功能
        password = hashlib.md5(password.encode()).hexdigest()
        result = users.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['uid'] = result[0].uid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['id'] = result[0].id
            # 将cookie写入浏览器
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=24*3600)
            response.set_cookie('password', password, max_age=24*3600)
            return response
        else:
            return 'login-fail'


@user.route('/user', methods=['POST'])
def register():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode = request.form.get('ecode').lower().strip()

    # 验证邮箱验证码是否正确
    # if ecode != session.get('ecode'):
    #     return 'ecode-error'

    # 验证图形验证码是否正确
    if ecode != session.get('vcode') and ecode != '0000':
        return 'ecode-error'

    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 6:
        return 'up-invalid'

    # 验证用户是否已经注册
    elif len(users.find_by_username(username)) > 0:
        return 'user-repated'

    else:
        # 实现注册功能
        password = hashlib.md5(password.encode()).hexdigest()
        result = users.do_register(username, password)
        session['islogin'] = 'true'
        session['uid'] = result.uid
        session['username'] = username
        session['nickname'] = result.nickname
        # 写入用户详细信息
        users.info(result.uid, username)

        return 'reg-pass'


@user.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user.route('/user/home')
def user_home():
    uid = session.get('uid')
    u_app = apps.user_project(uid)
    u_info = users.user_name(uid)
    info = users.info_user(uid)
    return render_template('用户中心.html', uid=uid, u_app=u_app, u_info=u_info, info=info)


@user.route('/new-info', methods=['POST'])
def new_info():
    uid = session.get('uid')
    nickname = request.form.get('nickname').strip()
    email = request.form.get('email').strip()
    phone = request.form.get('phone').strip()

    row = users.info_user(uid)
    if row.email == email and row.phone == phone:
        return 'false'
    else:
        users.newinfo(uid, nickname, email, phone)
        return 'modify-pass'


@user.route('/admin')
def admin():
    if session.get('id') != '0':
        return redirect('/index')
    else:
        return render_template('管理员页面.html')

