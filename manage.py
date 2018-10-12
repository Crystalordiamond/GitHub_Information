from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    """工程配置信息"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/GitHub_Information"
    # 关闭数据库修改跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_NUM = 9
    # 通过falsk-session拓展，将flask中的session调整到redis配置信息数据库类型有好几种 点进源码可以看到
    # 存储数据库类型
    SESSION_TYPE = "redis"
    # 将redis实例对象进行传入
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_NUM)
    # 对session数据进行加密处理
    SESSION_USE_SIGNER = True
    # 关闭永久存储
    SESSION_PERMANENT = False
    # 过期时长 24小时
    PERMANENT_SESSION_LIFETIME = 86400


app = Flask(__name__)
app.config.from_object(Config) # 添加配置类到app
"""
SQLALchemy 实际上是对数据库的抽象，让开发者不用直接和 SQL 语句打交道，而是通过 Python 对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升
SQLAlchemy是一个关系型数据库框架，它提供了高层的 ORM 和底层的原生数据库的操作。flask-sqlalchemy 是一个简化了 SQLAlchemy 操作的flask扩展。
文档地址：http://docs.jinkan.org/docs/flask-sqlalchemy
"""
# 创建数据库对象
db = SQLAlchemy(app)
# 创建redis数据库对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_NUM)
# 4.开启csrf保护机制
"""
1.自动获取cookie中的csrf_token,
2.自动获取ajax请求头中的csrf_token
3.自己校验这两个值
"""
csrf = CSRFProtect(app)
# 创建Session对象，将Session的存储方法进行调整（flask后端内存调整到redis服务器）
Session(app)
# 创建管理对象
manager = Manager(app)
# 数据库迁移对象
Migrate(app, db)
# 添加数据库迁移指令
manager.add_command("db", MigrateCommand)


@app.route('/')
def hello_world():
    return "Hello World"


if __name__ == '__main__':
    manager.run()
