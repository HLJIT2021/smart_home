from common.database import User, User_info, db

# 查询用户名
def find_by_username(username):
    result = User.query.filter_by(username=username).all()
    return result

# 注册
def do_register(username, password):
    nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
    user = User(username=username, password=password,
                 nickname=nickname, id=1)
    db.session.add(user)
    db.session.commit()
    return user

# 根据uid查用户名
def user_name(uid):
    row = db.session.query(User).filter_by(uid=uid).first()
    return row

# 修改用户名
def newnick(uid, newnick):
    row = db.session.query(User).filter_by(uid=uid).first()
    row.nickname = newnick
    db.session.commit()

# 修改密码
def newpass(uid, newpass):
    row = db.session.query(User).filter_by(uid=uid).first()
    row.password = newpass
    db.session.commit()

# 新增用户详细信息
def info(uid, username):
    info = User_info(uid=uid, email=username)
    db.session.add(info)
    db.session.commit()

# 根据uid查找用户详细信息
def info_user(uid):
    row = db.session.query(User_info).filter_by(uid=uid).first()
    return row

def newinfo(uid, nickname, email, phone):
    result = db.session.query(User).filter_by(uid=uid).first()
    result.nickname = nickname
    db.session.commit()
    row = db.session.query(User_info).filter_by(uid=uid).first()
    row.email = email
    row.phone = phone
    db.session.commit()