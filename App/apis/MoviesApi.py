from flask_restful import Resource, reqparse, marshal_with, fields, abort

from App.ext import db
from App.models import Movie, User

# get请求数据格式
parser_get = reqparse.RequestParser()
parser_get.add_argument('flag', type=int)

# post请求数据格式
parser_post = reqparse.RequestParser()
parser_post.add_argument('token', type=str, required=True, help='缺少token')
parser_post.add_argument('id', type=int, required=True, help='缺少id')
parser_post.add_argument('showname', type=str, required=True, help='缺少电影中文名')
parser_post.add_argument('shownameen', type=str, required=True, help='缺少英文名称')
parser_post.add_argument('director', type=str, required=True, help='缺少导演')
parser_post.add_argument('leadingRole', type=str, required=True, help='缺少主演')
parser_post.add_argument('type', type=str, required=True, help='缺少电影分类')
parser_post.add_argument('country', type=str, required=True, help='缺少产地')
parser_post.add_argument('language', type=str, required=True, help='缺少语言')
parser_post.add_argument('duration', type=int, required=True, help='缺少时长')
parser_post.add_argument('screeningmodel', type=str, required=True, help='缺少放映')
parser_post.add_argument('openday', type=str, required=True, help='缺少上映时间')
parser_post.add_argument('backgroundpicture', type=str, required=True, help='缺少图片')
parser_post.add_argument('flag', type=int, required=True, help='缺少标志位')


# 响应数据格式
movie_fields = {
    'id':fields.Integer,
    'showname':fields.String,
    'shownameen':fields.String,
    'director':fields.String,
    'leadingRole':fields.String,
    'type':fields.String,
    'country':fields.String,
    'language':fields.String,
    'duration':fields.Integer,
    'screeningmodel':fields.String,
    'openday':fields.String,
    'backgroundpicture':fields.String,
    'flag':fields.Integer,
}

result_fields_get = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(movie_fields)),
    'error': fields.String(default='')
}

result_fields_post = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(movie_fields),
    'error': fields.String(default='')
}


# 权限管理装饰器  8添加权限
ADMIN = 8
def check_permission_control(permission):
    def check_permission(func):
        def check(*args, **kwargs):
            parse = parser_post.parse_args()
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

class MoviesResource(Resource):
    @marshal_with(result_fields_get)
    def get(self):  # 获取电影信息
        parse = parser_get.parse_args()
        # flag=1 热映,  flag=2即将上映  [flag=0全部]
        flag = parse.get('flag') or 0

        if flag:
            movies = Movie.query.filter(Movie.flag == flag)
        else:
            movies = Movie.query.all()

        returndata = {
            'status': 200,
            'msg': '获取电影列表信息成功',
            'data': movies
        }

        return returndata


    @check_permission_control(ADMIN)
    @marshal_with(result_fields_post)
    def post(self): # 添加新电影
        parse = parser_post.parse_args()

        movie = Movie()
        movie.id = parse.get('id')
        movie.showname = parse.get('showname')
        movie.shownameen = parse.get('shownameen')
        movie.director = parse.get('director')
        movie.leadingRole = parse.get('leadingRole')
        movie.type = parse.get('type')
        movie.country = parse.get('country')
        movie.language = parse.get('language')
        movie.duration = parse.get('duration')
        movie.screeningmodel = parse.get('screeningmodel')
        movie.openday = parse.get('openday')
        movie.backgroundpicture = parse.get('backgroundpicture')
        movie.flag = parse.get('flag')

        db.session.add(movie)
        db.session.commit()

        returndata = {
            'status': 200,
            'msg': '获取电影列表信息成功',
            'data': movie
        }

        return returndata


