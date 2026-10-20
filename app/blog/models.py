from start import db
from datetime import datetime
"""文章表与标签表多对多中间表"""
post_tag = db.Table(
    "post-tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post_db.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag_db.id"), primary_key=True),

)
# 笔记与标签多对多中间表
note_tag = db.Table(
    'note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note_db.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag_db.id'), primary_key=True)
)

class BaseModel(db.Model):
    """数据表基类模型"""
    __abstract__ = True  # 标识抽象类，用于其他类的继承
    id = db.Column(db.Integer, primary_key=True, comment='id主键')
    add_time = db.Column(db.DateTime, default=datetime.now(), comment='创建时间')
    # onupdate=datetime.now()每次更新文章时自动更新此字段的值为当前时间
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), comment='更新时间')


class Post(BaseModel):
    __tablename__ = "post_db"
    title = db.Column(db.String(256), comment='标题')
    cover = db.Column(db.String(512), comment='文章封面')
    contend_md = db.Column(db.Text, comment='markdown源文档格式')
    contend_html = db.Column(db.Text, comment='html内容')
    read_count = db.Column(db.Integer, comment='阅读次数',default = 0)
    draft_flag = db.Column(db.Boolean, default=False, comment='是否为草稿')
    # onupdate=datetime.now()每次更新文章时自动更新此字段的值为当前时间
    #设置表关联
    category_id = db.Column(db.Integer,db.ForeignKey("category_db.id"),comment = "关联分类表id")
    tags = db.relationship("Tag", secondary=post_tag,backref="posts")#设置文章表与标签表多对多关联
    Comments = db.relationship("Comment", cascade = "delete",backref="post")#设置文章表与评论表多对多关联
    attachments = db.relationship("Attachment", backref="post")#设置文章表与附件表多对多关联
    user_id = db.Column(db.Integer, db.ForeignKey('user_db.id'), comment='用户id')

class Category(BaseModel):
    __tablename__ = "category_db"
    name = db.Column(db.String(64), unique=True, comment="分类名字")
    posts = db.relationship("Post", backref="category")#文章表与分类表关联
    notes = db.relationship('Note', backref='category')#分类表与笔记表关联

class Tag(BaseModel):
    __tablename__ = "tag_db"
    name = db.Column(db.String(64), unique=True, comment="标签名字")
    color = db.Column(db.String(32), comment="标签颜色字段")


class Note(BaseModel):
    __tablename__ = "note_db"
    title = db.Column(db.String(256), comment='标题')
    contend_md = db.Column(db.Text, comment='markdown源文档格式')
    contend_html = db.Column(db.Text, comment='html内容')
    read_count = db.Column(db.Integer, comment='阅读次数')
    category_id = db.Column(db.Integer, db.ForeignKey('category_db.id'), comment='分类id')
    tags = db.relationship('Tag', secondary=note_tag, backref='note')#笔记表与标签表多对多关联
    attachments = db.relationship('Attachment', backref='note')
    user_id = db.Column(db.Integer, db.ForeignKey('user_db.id'), comment='用户id')#用户表与笔记表一对多关联

class Comment(BaseModel):
    __tablename__ = "comment_db"
    content = db.Column(db.Text, comment="评论内容")
    visitor_name = db.Column(db.String(64), comment="游客名字")
    visitor_email = db.Column(db.String(64), comment="游客邮箱")
    visitor_ip = db.Column(db.String(64), comment="游客ip")
    visitor_address = db.Column(db.String(64), comment="游客地址")
    post_id = db.Column(db.Integer,db.ForeignKey("post_db.id"),comment="关联文章表id"  )
    replied_id = db.Column(db.Integer, db.ForeignKey('comment_db.id'))
    replied = db.relationship('Comment', backref='replies', remote_side='Comment.id', cascade='delete')

class Message(BaseModel):
    __tablename__ = "message_db"
    content = db.Column(db.Text, comment="留言内容")
    visitor_name = db.Column(db.String(64), comment="留言名字")
    visitor_email = db.Column(db.String(64), comment="留言邮箱")
    visitor_ip = db.Column(db.String(64), comment="留言ip")
    visitor_address = db.Column(db.String(64), comment="留言地址")


class Attachment(BaseModel):
    __tablename__ = "attachment_db"
    file_name = db.Column(db.String(256), comment="文件名")
    file_size = db.Column(db.String(64), comment="文件大小")
    file_path = db.Column(db.String(64), comment="文件路径")
    post_id = db.Column(db.Integer, db.ForeignKey('post_db.id'), comment='关联文章表id')
    note_id = db.Column(db.Integer, db.ForeignKey('note_db.id'), comment='笔记id')
