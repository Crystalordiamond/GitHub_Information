import logging
from redis import StrictRedis


class Config(object):
    """工程配置信息(父类)"""
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


class DevelopmentConfig(Config):
    """development开发环境"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """production生产环境"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING

# 给外界暴露一个使用配置类到接口
# 使用方法： config_dict['development'] --> DevelopmentConfig 开发环境的配置类  字典根据键取值
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}