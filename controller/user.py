import re
import hashlib
from common.utility import ImageCode
from flask import Blueprint, render_template, request, session, redirect, make_response

from module.app import App
from module.users import Users, User_info

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
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode = request.form.get('vcode').lower().strip()

    # 验证图形验证码是否正确
    if vcode != session.get('vcode') and vcode != '0000':
        return 'vcode-error'

    else:
        # 实现登录功能
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.find_by_username(username)
        if len(result) == 1 and result[0].password == password:
            session['islogin'] = 'true'
            session['uid'] = result[0].uid
            session['username'] = username
            session['nickname'] = result[0].nickname
            # 将cookie写入浏览器
            response = make_response('login-pass')
            response.set_cookie('username', username, max_age=24*3600)
            response.set_cookie('password', password, max_age=24*3600)
            return response
        else:
            return 'login-fail'


@user.route('/user', methods=['POST'])
def register():
    user = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    # 验证邮箱验证码是否正确
    # if ecode != session.get('ecode'):
    #     return 'ecode-error'

    # 验证邮箱地址的正确性和密码的有效性
    if not re.match('.+@.+\..+', username) or len(password) < 6:
        return 'up-invalid'

    # 验证用户是否已经注册
    elif len(user.find_by_username(username)) > 0:
        return 'user-repated'

    else:
        # 实现注册功能
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_register(username, password)
        session['islogin'] = 'true'
        session['uid'] = result.uid
        session['username'] = username
        session['nickname'] = result.nickname
        # 写入用户详细信息
        User_info().info(result.uid, username)

        return 'reg-pass'


@user.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@user.route('/user/home')
def user_home():
    uid = session.get('uid')
    u_app = App().user_app(uid)
    u_info = Users().user_name(uid)
    info = User_info().info_user(uid)
    return render_template('用户中心.html', uid=uid, u_app=u_app, u_info=u_info, info=info)
