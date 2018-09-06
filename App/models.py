from App.ext import db


# 用户模型类
class User(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(20))
    token = db.Column(db.String(255))
    permissions = db.Column(db.Integer, default=1)
    icon = db.Column(db.String(50), default='head.png')
    isactive = db.Column(db.Boolean, default=False)
    isdelete = db.Column(db.Boolean, default=False)



# 一对多(一个字母中对应多个城市)
"""
 'A': [
    {},
    {},
    {},
 ]
"""
# 字母模型类
class Letter(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(5))
    # 该字母对应的城市
    l_citys = db.relationship('City', backref='letter', lazy=True)

# 城市模型类
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regionName = db.Column(db.String(255))
    cityCode = db.Column(db.Integer)
    pinYin = db.Column(db.String(255))
    # 外键,哪个字母中
    c_letter = db.Column(db.Integer, db.ForeignKey(Letter.id))



# 电影信息模型类
# insert into
# movies(  , , )
# values( "i1/TB19_XCoLDH8KJjy1XcXXcpdXXa_.jpg",1,0);
class Movie(db.Model):
    __tablename__ = 'movies'
    # id
    id = db.Column(db.Integer, primary_key=True)
    # 电影中文名
    showname = db.Column(db.String(255))
    # 英文名称
    shownameen = db.Column(db.String(255))
    # 导演
    director = db.Column(db.String(100))
    # 主演
    leadingRole = db.Column(db.String(255))
    # 电影分类
    type = db.Column(db.String(255))
    # 产地
    country = db.Column(db.String(255))
    # 语言
    language = db.Column(db.String(255))
    # 时长
    duration = db.Column(db.Integer)
    # 放映(2D/3D/4D)
    screeningmodel = db.Column(db.String(10))
    # 上映时间
    openday = db.Column(db.Date)
    # 图片
    backgroundpicture = db.Column(db.String(255))
    # 标志位 flag=1 热映,  flag=2即将上映  [flag=0全部]
    flag = db.Column(db.Integer)
    # 是否删除
    isdelete = db.Column(db.Boolean, default=False)


# 影院模型类
# insert into
# cinemas(,,,,,,,,,flag,isdelete)
# values("","","","","",,9,1.2,20,1,0);
class Cinemas(db.Model):
    # id
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    # 名称
    name = db.Column(db.String(255))
    # 城市
    city = db.Column(db.String(100))
    # 区域
    district = db.Column(db.String(100))
    # 具体地址
    address = db.Column(db.String(255))
    # 联系方式
    phone = db.Column(db.String(100))
    # 评分
    score = db.Column(db.Float)
    # 放映厅个数
    hallnum = db.Column(db.Integer)
    # 服务评分
    servicecharge = db.Column(db.Float)
    # 限制
    astrict = db.Column(db.Integer)
    # 标志位
    flag = db.Column(db.Integer)
    # 逻辑删除
    isdelete = db.Column(db.Boolean, default=False)
