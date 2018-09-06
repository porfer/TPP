from flask_restful import Resource, reqparse, fields, marshal_with, abort

from App.models import User

""" 视频API
0 未登录
    列表A(预览/广告)+列表B(预览/广告)  
    
1 登录
    列表A(完整/广告)+列表B(预览/广告)
    
2 会员
    列表A(完整/无广告) + 列表B(完整/无广告)
    
3 超级会员
    列表A(完整/无广告) + 列表B(完整/无广告) + 列表C(完成/无广告/下载)
"""


# post请求数据格式
parser = reqparse.RequestParser()
parser.add_argument('token', type=str)


# 响应数据格式
result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.String,
    'error': fields.String(default='')
}

# 权限 1查看/2可下载/4可添加   [限制接口的权限] 装饰器
def check_permission_control(permission):
    def check_permission(func):
        def check(*args, **kwargs):
            parse = parser.parse_args()
            token = parse.get('token')
            returndata = {}


            if token:  # 有token
                users = User.query.filter(User.token == token)
                if users.count() > 0:  # 存在用户
                    user = users.first()
                    # 有无对应操作的权限
                    # 用户权限user: 4    100
                    # 接口限制权限permission: 2    010
                    # 接口限制权限permission: 4    100
                    if user.permissions & permission == permission: # 该用户有权限使用此接口
                        return func(*args, **kwargs)
                    else:
                        abort(403, message='你没有该操作权限,请联系管理员!')
                else:  # 不存在
                    abort(401, message='你还没有登录,请登录后操作')
            else:  # 无token
                abort(401, message='你还没有登录,请登录后操作')
        return check
    return check_permission


class MoviesTestResource(Resource):
    # 通过装饰器的方式,实现权限管理
    @check_permission_control(4)
    @marshal_with(result_fields)
    def get(self):
        returndata = {}

        returndata['status'] = 200
        returndata['msg'] = '添加电影成功!'
        returndata['data'] = '电影信息: 我不是药神...'

        return returndata

    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        token = parse.get('token')

        returndata = {}

        if token:   # 有token
            users = User.query.filter(User.token == token)
            if users.count()>0: # 存在用户

                user = users.first()
                returndata['status'] = 200
                returndata['msg'] = '获取电影列表成功!'
                if user.permissions == 1:
                    returndata['data'] = '列表A(完整/广告)+列表B(预览/广告)'
                elif user.permissions == 2:
                    returndata['data'] = '列表A(完整/无广告) + 列表B(完整/无广告)'
                elif user.permissions == 3:
                    returndata['data'] = '列表A(完整/无广告) + 列表B(完整/无广告) + 列表C(完成/无广告/下载)'

                return returndata

            else:   #  用户存在但未登录，所以token不存在
                returndata['status'] = 200
                returndata['msg'] = '获取电影列表成功!'
                returndata['data'] = '列表A(预览/广告)+列表B(预览/广告)'

                return returndata

        else:   # 无token
            returndata['status'] = 200
            returndata['msg'] = '获取电影列表成功!'
            returndata['data'] = '列表A(预览/广告)+列表B(预览/广告)'

            return returndata
