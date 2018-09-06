from flask_restful import Resource, fields, marshal_with, marshal
from App.models import City, Letter

# 请求数据格式

# 响应数据格式
"""
{
    'stauts': 200,
    'msg': '获取城市列表成功',
    'data': {
        'A': [
        {
            "id":430,
            "regionName":"沧州",
            "cityCode":130900,
            "pinYin":"CANGZHOU"
        },
        {},
        {}
        ],
        'B': [{},{},{}],
        ...
    },
    'error': ''
}
"""
city_fields = {
    'id': fields.Integer,
    'regionName': fields.String,
    'cityCode': fields.Integer,
    'pinYin': fields.String
}

letter_fields = {
    'A': fields.List(fields.Nested(city_fields)),
    'B': fields.List(fields.Nested(city_fields)),
    'C': fields.List(fields.Nested(city_fields)),
    'D': fields.List(fields.Nested(city_fields)),
    'E': fields.List(fields.Nested(city_fields)),
    'F': fields.List(fields.Nested(city_fields)),
    'G': fields.List(fields.Nested(city_fields)),
    'H': fields.List(fields.Nested(city_fields)),
    'J': fields.List(fields.Nested(city_fields)),
    'K': fields.List(fields.Nested(city_fields)),
    'L': fields.List(fields.Nested(city_fields)),
    'M': fields.List(fields.Nested(city_fields)),
    'N': fields.List(fields.Nested(city_fields)),
    'P': fields.List(fields.Nested(city_fields)),
    'Q': fields.List(fields.Nested(city_fields)),
    'R': fields.List(fields.Nested(city_fields)),
    'S': fields.List(fields.Nested(city_fields)),
    'T': fields.List(fields.Nested(city_fields)),
    'W': fields.List(fields.Nested(city_fields)),
    'X': fields.List(fields.Nested(city_fields)),
    'Y': fields.List(fields.Nested(city_fields)),
    'Z': fields.List(fields.Nested(city_fields)),
}

result_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data':fields.Nested(letter_fields),
    'error': fields.String
}


class CityResource(Resource):
    # 通过装饰器的方式实现格式 [格式是固定死的]
    @marshal_with(result_fields)
    def get(self):
        # 所有字母
        letters = Letter.query.all()

        # 数据列表
        data = {}
        # 返回数据
        returndata  = {}

        # 遍历获取每个字母对应的城市
        for item in letters:
            # print(item.l_citys)
            data[item.name] = item.l_citys

        # 拼接
        returndata['status'] = 200
        returndata['msg'] = '城市列表数据获取成功!'
        returndata['data'] = data
        returndata['error'] = ''

        return returndata

    # 响应是动态生成
    def post(self):
        # 所有字母
        letters = Letter.query.all()

        # 数据列表
        data = {}
        # 返回数据
        returndata = {}


        # 动态格式列表(字母)
        #  'A': fields.List(fields.Nested(city_fields))
        #  'B': fields.List(fields.Nested(city_fields))
        letter_fields_dynamic = {}

        # 遍历获取每个字母对应的城市
        for item in letters:
            # 添加数据
            data[item.name] = item.l_citys
            # 添加格式
            # 'B': fields.List(fields.Nested(city_fields))
            letter_fields_dynamic[item.name] = fields.List(fields.Nested(city_fields))


        # 最终数据
        returndata['status'] = 200
        returndata['msg'] = '城市列表数据获取成功!'
        returndata['data'] = data
        returndata['error'] = ''

        # 动态格式
        result_fields_dynamic = {
            'status': fields.Integer,
            'msg': fields.String,
            'data': fields.Nested(letter_fields_dynamic),
            'error': fields.String
        }

        # 根据格式,对应生成json数据
        result = marshal(returndata, result_fields_dynamic)

        return result