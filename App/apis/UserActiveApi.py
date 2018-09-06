import uuid

from flask_restful import Resource, fields, reqparse, marshal_with


from App.ext import cache, db
from App.models import User


# post请求数据格式
parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='请输入token!')

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


class UserActive(Resource):
    @marshal_with(result_fields)
    def get(self):
        parse = parser.parse_args()
        token = parse.get('token')

        returndata = {}

        # 根据token获取userid
        userid = cache.get(token)

        if not userid:  # 超时
            returndata['status'] = 201
            returndata['msg'] = '激活过期,请联系管理员! xxx-xxx'
            returndata['error'] = '激活失败,超时'
            return returndata
        else:
            # 删除token
            cache.delete(token)

            # 获取用户信息
            user = User.query.get(userid)

            # 修改状态,生成新的token, 并存入数据库。
            user.isactive = True
            user.token = str(uuid.uuid4())
            db.session.add(user)
            db.session.commit()

            returndata['status'] = 200
            returndata['msg'] = '用户激活成功'
            returndata['data'] = user

            return returndata


