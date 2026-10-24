from start import db
from datetime import datetime
from flask_login import  UserMixin

class BaseModel(db.Model):
    """数据表基类模型"""
    __abstract__ = True  # 标识抽象类，用于其他类的继承
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    # onupdate=datetime.now()每次更新文章时自动更新此字段的值为当前时间
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')


class User(UserMixin,BaseModel):
    __tablename__ = "user_db"
    username = db.Column(db.String(64), unique=True, nullable=False, comment="用户名")
    password = db.Column(db.String(128), comment="用户密码")
    last_login = db.Column(db.DateTime, comment="上次登录时间")
    nickname = db.Column(db.String(64), comment="用户昵称")
    avatar_path = db.Column(db.String(64), comment="用户头像路径")
    posts = db.relationship('Post', backref='user')  #设置目前文章表与用户表多对一关联
    notes = db.relationship('Note', backref='user')

class BlogInfo(BaseModel):
    __tablename__ = "bloginfo_db"
    title = db.Column(db.String(64), comment="网站标题")
    subtitle = db.Column(db.String(64), comment="网站副标题")
    about_me_mk = db.Column(db.Text, comment="关于我的markdown格式")
    about_me_html = db.Column(db.Text, comment="关于我的html格式")
