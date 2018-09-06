from flask import render_template
from flask_caching import Cache
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

#配置缓存数据库
cache = Cache(config={
    'CACHE_TYPE': 'redis'
})

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    cache.init_app(app)



# 发送邮件
def send_mail(user):
    msg = Message(
        subject='PTT激活邮件',  # 主题
        recipients=[user.email],  # 发给谁
        sender='18924235915@163.com'  # 谁发
    )
    active_url = 'http://127.0.0.1:5000/api/v1/useractive/?token=' + user.token
    body_html = render_template('useractive.html', name=user.name, active_url=active_url)
    msg.html = body_html
    mail.send(msg)
