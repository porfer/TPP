from flask import Flask

from App.ext import init_ext
from App.settings import config
from App.apis import init_api


def create_app(env_name=None):
    app = Flask(__name__)

    # 配置
    app.config.from_object(config.get(env_name or 'default'))

    # 初始化
    init_ext(app)

    # api
    init_api(app)

    return app
