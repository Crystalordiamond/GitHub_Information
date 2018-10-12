import logging
from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import craete_app, db

"""
从单一职责考虑：manage.py文件仅仅作为项目启动文件即可
"""

# 调用create_app()工厂方法  返回app
app = craete_app("development")
# 创建管理对象
manager = Manager(app)
# 数据库迁移对象
Migrate(app, db)  # 这个db对象在info.__init__是局部变量，需要把它拿出来变成全局变量
# 添加数据库迁移指令
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
