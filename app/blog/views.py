from flask import Blueprint, render_template, request
from app.blog.models import Post, Comment, Message,Note
from sqlalchemy import or_
from start import db
from ..admin.models import BlogInfo
from .static.ip2region import search_with_file

bp = Blueprint("blog", __name__, url_prefix="/blog", static_folder="static", template_folder="templates")


# 因为在初始化文件中注册了首页路由，这里的路由规则就不适用了
@bp.route("/page/<int:page>")
def index(page=1):
    title = "yunlong的小站",
    post_pg = Post.query.paginate(page=page, per_page=5)
    count = post_pg.total
    return render_template("index.html", **locals())


# @bp.route("/post")
# def post():
#     title = "yunlong的小站"
#     post = Article.query.get(1)
#     return render_template("post.html", **locals())
@bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return "404"
    post.read_count += 1
    db.session.commit()
    prev_post = Post.query.filter(Post.id < post.id).order_by(Post.id.desc()).first()  # 查询比当前文章id还要小的第一篇文章id
    prev_post = prev_post if prev_post else None

    next_post = Post.query.filter(Post.id > post.id).first()
    next_post = next_post if next_post else None
    # comments = Comment.query.filter(Comment.post_id == post.id).order_by(Comment.id.desc()).all()
    main_comments = Comment.query.filter_by(post_id=post_id, replied=None).order_by(Comment.add_time.desc()).all()

    all_comments = []
    for main_comment in main_comments:
        # print(main_comment)
        # print(main_comment.replies)
        # print('==============================')
        replies = get_replies(comment_id=main_comment.id, reply_target_name=None)
        replies = sorted(replies, key=lambda x: x["add_time"], reverse=True)
        comment_data = {
            'id': main_comment.id,
            'content': main_comment.content,
            'visitor_name': main_comment.visitor_name,
            'visitor_address': main_comment.visitor_address,
            'add_time': main_comment.add_time,
            'replies': replies,

        }
        all_comments.append(comment_data)
    return render_template("post.html", **locals())


def get_replies(comment_id, reply_target_name):
    replies = Comment.query.filter_by(replied_id=comment_id).all()
    reply_data = []
    for reply in replies:
        reply_child = {
            'id': reply.id,
            'content': reply.content,
            'visitor_name': reply.visitor_name,
            'visitor_address': reply.visitor_address,
            'add_time': reply.add_time,
            'reply_target_name': reply_target_name,
        }
        reply_data.append(reply_child)
        reply_data.extend(get_replies(comment_id=reply.id,reply_target_name=reply.visitor_name))
    return reply_data


@bp.route('/comment_add', methods=['POST'])
def comment_add():
    form_data = request.form
    visitor_ip = request.remote_addr
    visitor_address = search_with_file(visitor_ip)
    comment = Comment(
        content=form_data['comment'],
        visitor_name=form_data['name'],
        visitor_email=form_data['email'],
        visitor_ip=visitor_ip,
        visitor_address=visitor_address,
        post_id=form_data['post_id']
    )
    db.session.add(comment)
    db.session.commit()
    return 'success'


@bp.route('/comment_reply', methods=['post'])
def comment_reply():
    """
    评论回复-API
    :return:
    """
    form_data = request.form
    visitor_ip = request.remote_addr
    visitor_address = search_with_file(visitor_ip)
    comment = Comment(
        content=form_data['comment'],
        visitor_name=form_data['name'],
        visitor_email=form_data['email'],
        visitor_ip=visitor_ip,
        visitor_address=visitor_address,
        post_id=form_data['post_id'],
        replied_id=form_data['replied_id']
    )
    db.session.add(comment)
    db.session.commit()
    return 'success'
@bp.route('/record')
def record():
    """
    归档页面
    :return:
    """
    posts = Post.query.filter_by(draft_flag=False).order_by(Post.add_time.desc()).all()
    record_list = {}
    for post in posts:
        date = str(post.add_time.strftime("%Y-%m"))
        record_list.setdefault(date, []).append(post)

    return render_template('record.html', **locals())


@bp.route('/note/<int:curr>')
def note(curr=1):
    """
    笔记管理-查询笔记API
    :return:
    """
    note_pg = Note.query.paginate(page=curr, per_page=5)
    count = note_pg.total
    current_route = 'note'
    return render_template('note.html', **locals())


@bp.route('/message')
def message():
    """
    留言页面
    :return:
    """
    message = Message.query.order_by(Message.add_time.desc()).all()
    return render_template('message.html',**locals())
@bp.route('/message_add', methods=['post'])
def message_add():
    form_data = request.form
    visitor_ip = request.remote_addr
    visitor_address = search_with_file(visitor_ip)
    message = Message(
        content=form_data['comment'],
        visitor_name=form_data['name'],
        visitor_email=form_data['email'],
        visitor_ip=visitor_ip,
        visitor_address=visitor_address,
    )
    db.session.add(message)
    db.session.commit()
    return 'success'

@bp.route('/about')
def about():
    """
    关于页面
    :return:
    """
    blog_info = BlogInfo.query.first()
    about_me_html = blog_info.about_me_html if blog_info else ''
    return render_template('about.html',**locals())
@bp.route('/post_search')
@bp.route('/note_search')
def search():
    """
    文章搜索API
    :return:
    """
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=5)
    word = request.args.get('word')
    current_route = request.url.split('/')[-1].split('_')[0]
    if current_route == 'note':
            base_query = Note.query.filter(or_(Note.title.ilike(f"%{word}%"), Note.contend_md.ilike(f"%{word}%")))

    else:
        base_query = Post.query.filter(or_(Post.title.ilike(f"%{word}%"), Post.contend_md.ilike(f"%{word}%")))

    post_pg = base_query.paginate(page=page, per_page=limit)
    count = post_pg.total

    return render_template('search.html', **locals())

