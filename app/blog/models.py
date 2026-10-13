from start import db
from datetime import datetime


class Article(db.Model):
    __tablename__ = "db_article"
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    title = db.Column(db.String(256), comment='标题')
    content = db.Column(db.Text, comment='内容')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    # onupdate=datetime.now()每次更新文章时自动更新此字段的值为当前时间
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')
