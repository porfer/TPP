from flask_restful import Resource, reqparse, marshal_with, fields

from werkzeug.security import check_password_hash, generate_password_hash

from App.ext import db
from App.models import User

# post请求参数格式
parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='缺少token')
parser.add_argument('oldpassword', type=str, required=True, help='缺少旧密码')
parser.add_argument('newpassword', type=str, required=True, help='缺少新密码')

# 响应参数格式
result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.String(default=''),
    'error': fields.String(default='')
}

class PasswordChange(Resource):
    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        token = parse.get('token')
        oldpassword = parse.get('oldpassword')
        newpassword = parse.get('newpassword')

        returndata = {}

        users = User.query.filter(User.token == token)
        if users.count()>0: # 存在
            user = users.first()
            if check_password_hash(user.password, oldpassword): # 密码正确
                user.password = generate_password_hash(newpassword)

                db.session.add(user)
                db.session.commit()

                returndata['status'] = 200
                returndata['msg'] = '修改密码成功.'
                return returndata

            else:   # 密码错误
                returndata['status'] = 401
                returndata['msg'] = '修改密码错误'
                returndata['error'] = '旧密码错误!'
                return returndata

        else:   # 不存在
            returndata['status'] = 401
            returndata['msg'] = '小伙子,空手套白狼了.'
            returndata['error'] = 'token错误!'
            return returndata
