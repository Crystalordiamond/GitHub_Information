import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_session import Session
from config import config_dict

# 暂时没有app对象，就不会去初始化，只是声明一下.为什么能这样做:点进去源码
# 没有就申明一下  有就进入判断去执行  （懒加载思想）
db = SQLAlchemy()
# redis_store没有像SQLAlchemy封装一个这样到方法 就直接设置为全局变量
redis_store = None  # type: StrictRedis

"""记录日志的配置"""


def setup_log(config_name):
    # 下面到函数调用后 根据传入的参数 找不到不同的项目配置类
    # 将configClass传入到logging.basicConfig(level=configClass)，但是需要不同环境中设置好日志级别，来调用。
    configClass = config_dict[config_name]
    # 设置日志的记录等级
    logging.basicConfig(level=configClass.LOG_LEVEL)  # 调试debug级 调用不同环境中到日志等级
    # 创建日志记录器，指明日志保存的路径、每个日志文件100兆、保存的日志文件个数上限10个
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


"""
# ofo生产单车：原材料--->车间--->小黄
# 工厂方法：传入配置名称--->返回对应配置的app对象
# development: --> app开发模式的app对象
# production: --> app线上模式的app对象
"""
# todo 谁传给你参数
"""创建app  create_app方法：工厂方法"""


def craete_app(config_name):
    # 之所以在这里调用日志函数  是因为日志和运行环境有关系，要是运行环境日志就不用经常显示错误 增加服务器压力。开发环境就不一样
    setup_log(config_name)

    app = Flask(__name__)
    configClass = config_dict[config_name]
    app.config.from_object(configClass)  # 添加配置类到app
    """
    SQLALchemy 实际上是对数据库的抽象，让开发者不用直接和 SQL 语句打交道，而是通过 Python 对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升
    SQLAlchemy是一个关系型数据库框架，它提供了高层的 ORM 和底层的原生数据库的操作。flask-sqlalchemy 是一个简化了 SQLAlchemy 操作的flask扩展。
    文档地址：http://docs.jinkan.org/docs/flask-sqlalchemy
    """
    # 创建数据库对象
    db = SQLAlchemy(app)
    # 创建redis数据库对象
    global redis_store
    redis_store = StrictRedis(host=configClass.REDIS_HOST, port=configClass.REDIS_PORT, db=configClass.REDIS_NUM)
    # 4.开启csrf保护机制
    """
    1.自动获取cookie中的csrf_token,
    2.自动获取ajax请求头中的csrf_token
    3.自己校验这两个值
    """
    csrf = CSRFProtect(app)
    # 创建Session对象，将Session的存储方法进行调整（flask后端内存调整到redis服务器）
    Session(app)

    # 注册首页蓝图对象
    from info.moduls.index import index_bp
    app.register_blueprint(index_bp)

    # 返回不同模式下的app对象  开发模式  生产模式
    return app
