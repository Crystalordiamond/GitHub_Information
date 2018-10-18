import logging
from flask import current_app, render_template
from . import index_bp
from info import redis_store
from info.models import User


@index_bp.route('/index')
def index():
    # 模板文件名称templates写错了就找不到位置了
    # print(current_app.url_map)
    return render_template('news/index.html')

# 浏览器上面的头标
@index_bp.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')

@index_bp.route('/')
def hello_world():

    # redis_store.set("name", "durant")
    # logging.debug("我是debug级别日志")
    # logging.info("我是infog级别日志")
    # logging.warning("我是warning级别日志")
    # logging.error("我是error级别日志")
    # logging.critical("我是critical级别日志")
    # # flask中对logging模块进行封装，直接用current_app调用（常见）
    # current_app.logger.debug("falsk中记录的debug日志")
    return "Hello World777"
