import uuid

from flask_restful import Resource, marshal_with, reqparse, fields

from werkzeug.security import check_password_hash

from App.ext import send_mail, db
from App.models import User

#post请求数据格式
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='请输入用户名')
parser.add_argument('password', type=str, required=True, help='请输入名')

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

class Login(Resource):
    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        username = parse.get('username')
        password = parse.get('password')

        returndata = {}

        users = User.query.filter(User.name == username)
        if users.count()>0: # 有
            user = users.first()

            # 密码校验
            if check_password_hash(user.password, password): # 验证通过
                if user.isdelete == True:  # 已被删除
                    returndata['status'] = 401
                    returndata['msg'] = '登录失败'
                    returndata['error'] = '用户已经被注销'
                    return returndata

                if user.isactive == False:  # 未激活
                    returndata['status'] = 401
                    returndata['msg'] = '登录失败'
                    returndata['error'] = '用户未激活,请激活后再登录,查看邮箱!'

                    # 发邮件
                    send_mail(user)

                    return returndata

                    # 验证成功

                # 更新token, 并存入数据库
                user.token = str(uuid.uuid4())
                db.session.add(user)
                db.session.commit()

                returndata['status'] = 200
                returndata['msg'] = '登录成功'
                returndata['data'] = user

                return returndata
            else: # 密码错误
                returndata['status'] = 401
                returndata['msg'] = '登录失败'
                returndata['error'] = '密码错误!'
                return returndata
        else:   # 账号或密码错误
            returndata['status'] = 401
            returndata['msg'] = '登录失败'
            returndata['error'] = '用户名错误!'
            return returndata