


# 拼接操作
import os


def get_database_uri(DATABASE):
    db = DATABASE.get('DB') or 'mysql'
    driver = DATABASE.get('DRIVER') or 'pymysql'
    username = DATABASE.get('USERNAME') or 'root'
    password = DATABASE.get('PASSWORD') or '123456'
    hort = DATABASE.get('HORT') or '127.0.0.1'
    port = DATABASE.get('PORT') or '3306'
    dbname = DATABASE.get('DBNAME') or 'test02'

    return '{}+{}://{}:{}@{}:{}/{}'.format(db,driver,username,password,hort,port,dbname)

# 上传文件目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'App/static/img/')

# 配置基类
class BaseConfig():
    DEBUG = False
    TESING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '!@#$%^&*DGHJKL%^&*(CVBERTYU1231'


# 开发环境
class DevelopConfig(BaseConfig):
    DEBUG = True

    MAIL_SERVER = "smtp.163.com"
    MAIL_USERNAME = "18924235915@163.com"
    MAIL_PASSWORD = "zyz123"

    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': '123456',
        'HORT': '127.0.0.1',
        'PORT': '3306',
        'DBNAME': 'PTT'
    }

    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)


# 测试环境
class TestingConfig(BaseConfig):
    TESTING = True

    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': '123456',
        'HORT': '127.0.0.1',
        'PORT': '3306',
        'DBNAME': 'testing'
    }

    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)


# 演示环境
class StagingConfig(BaseConfig):
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': '123456',
        'HORT': '127.0.0.1',
        'PORT': '3306',
        'DBNAME': 'flask02'
    }

    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)


# 线上环境
class ProductConfig(BaseConfig):
    DATABASE = {
        'DB': 'mysql',
        'DRIVER': 'pymysql',
        'USERNAME': 'root',
        'PASSWORD': '123456',
        'HORT': '127.0.0.1',
        'PORT': '3306',
        'DBNAME': 'flask02'
    }

    SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)



config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig
}