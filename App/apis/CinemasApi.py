from flask_restful import Resource, marshal_with, reqparse, fields

from App.models import Cinemas

# get请求数据格式
parser = reqparse.RequestParser()
parser.add_argument('city', type=str, default='全部')
parser.add_argument('district', type=str)
parser.add_argument('sort', type=int, default=-1) # -1倒序, 1正序
parser.add_argument('limit', type=int)


# 响应数据格式
cinemas_fields = {
    'id':fields.String,
    'name':fields.String,
    'city':fields.String,
    'district':fields.String,
    'address':fields.String,
    'phone':fields.String,
    'score':fields.String,
    'hallnum':fields.String,
    'servicecharge':fields.String,
    'astrict':fields.String,
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(cinemas_fields)),
    'error': fields.String(default='')
}


class CinemasResource(Resource):
    @marshal_with(result_fields)
    def get(self):
        parse = parser.parse_args()
        city = parse.get('city')
        district = parse.get('district')
        limit_num = parse.get('limit')
        sort = parse.get('sort')

        if sort == -1:  # 倒序
            cinemas=  Cinemas.query.order_by(-Cinemas.score)
        else:
            cinemas = Cinemas.query.order_by(Cinemas.score)

        if city == '全部':
            cinemas = cinemas
        else:
            cinemas = cinemas.filter(Cinemas.city == city)

        if district:
            cinemas = cinemas.filter(Cinemas.district == district)

        if limit_num:
            cinemas = cinemas.limit(limit_num)

        returndata = {
            'status': 200,
            'msg': '获取影院列表成功',
            'data': cinemas
        }

        return returndata