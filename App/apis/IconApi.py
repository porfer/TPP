import os

from flask_restful import Resource, marshal_with, fields, reqparse
import werkzeug

from werkzeug.utils import secure_filename

from App.ext import db
from App.models import User
from App.settings import UPLOAD_DIR

# post请求数据格式
parser = reqparse.RequestParser()
parser.add_argument('token', type=str, required=True, help='缺少token')
parser.add_argument('usericon', type=werkzeug.datastructures.FileStorage, location='files', required=True, help='请选择图片')


# 响应参数格式
class IconFormat(fields.Raw):
    def format(self, value):
        return "/static/img/" + value

user_fields = {
    'icon': IconFormat(attribute='icon')
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(user_fields, default=''),
    'error': fields.String(default='')
}


class IconResource(Resource):
    @marshal_with(result_fields)
    def post(self):
        parse = parser.parse_args()
        token = parse.get('token')

        returndagta = {}

        users = User.query.filter(User.token == token)
        if users.count()>0:

            user = users.first()
            # 获取图片数据
            imgfile = parse.get('usericon')
            # 图片名称
            filename = '%d-%s' % (user.id, secure_filename(imgfile.filename))
            # 图片的保存路径
            filepath = os.path.join(UPLOAD_DIR, filename)
            # 保存文件
            imgfile.save(filepath)

            # 更新数据库
            user.icon = filename
            db.session.add(user)
            db.session.commit()

            returndagta['status'] = 200
            returndagta['msg'] = '文件上传成功'
            returndagta['data'] = user

            return returndagta

        else:   # 找不到用户
            returndagta['status'] = 401
            returndagta['msg'] = '文件上传失败'
            returndagta['error'] = '用户不存在,检查token值'

            return returndagta
