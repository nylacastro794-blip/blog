from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#实例化 solalchemy数据模型对象
db = SQLAlchemy()
#实例化数据迁移对象
migrate = Migrate()

# 工厂函数模式（作用是进行项目初始化加载）
def create_app():
    app = Flask(__name__)

    #加载项目配置文件
    #在加载项目配置文件的时候有可能会有一些错误的配置会影响app的加载，
    #使用slice=true，当配置文件报错的时候，不会抛出异常错误
    app.config.from_pyfile('settings.py',silent = True)

    #注册数据模型到app
    db.init_app(app)
    #注册数据迁移对象
    migrate.init_app(app,db)
    """引入蓝图注册到app"""
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    #为了能让migrate能够识别到数据模型，需要在工厂函数中导入蓝图下的数据模型
    from app.blog import models
    from app.admin import models
    # 注册根路由
    app.add_url_rule('/',view_func=blog.index)
    return app



