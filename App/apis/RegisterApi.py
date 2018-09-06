import uuid
from flask_restful import Resource, marshal_with, fields, reqparse

from werkzeug.security import generate_password_hash

from App.ext import db, mail, cache, send_mail
from App.models import User

# post请求参数格式
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='请输入用户名')
parser.add_argument('password', type=str, required=True, help='请输入密码')
parser.add_argument('email', type=str, required=True, help='请输入邮箱')
parser.add_argument('phone', type=str, required=True, help='请输入手机号')

# 响应参数格式
user_fields = {
    'name': fields.String,
    'token': fields.String,
    'icon': fields.String,
    'permissions': fields.Integer
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(user_fields, default=''),
    'error': fields.String(default='')
}


class RegisterResouce(Resource):
    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()

        # 用户信息
        user = User()
        user.name = parse.get('name')
        user.password = generate_password_hash(parse.get('password'))  #通过哈希列表对输入的密码进行加密，并存入数据库。
        user.email = parse.get('email')
        user.phone = parse.get('phone')
        user.token = str(uuid.uuid4())

        # 返回数据
        returndata = {}

        # 异常
        users = User.query.filter(User.name == user.name).filter(User.email == user.email)
        if users.count()>0:  # 用户存在
            returndata['status'] = 406
            returndata['msg'] = '注册失败'
            returndata['error'] = '该用户已经注册过,直接登录即可!'
            return returndata
        else:
            users = User.query.filter(User.email == user.email)
            if users.count()>0:  # 邮箱已经存在
                returndata['status'] = 406
                returndata['msg'] = '注册失败'
                returndata['error'] = '邮箱已存在'
                return returndata

            users = User.query.filter(User.name == user.name)
            if users.count()>0:
                returndata['status'] = 406
                returndata['msg'] = '注册失败'
                returndata['error'] = '用户名已存在'
                return returndata


        # 存入数据库
        db.session.add(user)
        db.session.commit()

        # 发邮件
        send_mail(user)

        # 通过redis, token:userid
        cache.set(user.token,user.id, timeout=30)

        returndata['status'] = 200
        returndata['msg'] = '注册成功'
        returndata['data'] = user

        return returndata
