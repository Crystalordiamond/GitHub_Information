import logging

from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info  import craete_app, db
"""
从单一职责考虑：manage.py文件仅仅作为项目启动文件即可
"""
# 调用create_app()工厂方法  返回app
app = craete_app("development")
# 创建管理对象
manager = Manager(app)
# 数据库迁移对象
Migrate(app, db)  #这个db对象在info.__init__是局部变量，需要把它拿出来变成全局变量
# 添加数据库迁移指令
manager.add_command("db", MigrateCommand)


@app.route('/')
def hello_world():
    logging.debug("我是debug级别日志")
    logging.info("我是infog级别日志")
    logging.warning("我是warning级别日志")
    logging.error("我是error级别日志")
    logging.critical("我是critical级别日志")
    # flask中对logging模块进行封装，直接用current_app调用（常见）
    current_app.logger.debug("falsk中记录的debug日志")
    return "Hello World"


if __name__ == '__main__':
    manager.run()
