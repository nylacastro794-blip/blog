from flask import Blueprint, render_template, request, jsonify
from app.blog.models import Category, Tag
from start import db

bp = Blueprint('admin',__name__,url_prefix='/qd_admin',template_folder='templates',static_folder='static')


@bp.route('/')
def login():
    return render_template('admin/index.html',**locals())



@bp.route('/post')
def post():
    return render_template('admin/post.html',**locals())
@bp.route('/category')
def category():
    return render_template('admin/category.html',**locals())

@bp.route("/add_category", methods=['POST','GET'])
def category_add():
    print("数据进来了")
    print(request.form)
    category_name = request.form.get('value')
    category_ = Category.query.filter_by(name=category_name).first()
    if not category_:
        category_boj = Category(name = category_name)
        db.session.add(category_boj)
        db.session.commit()
        return "success"
    return "existed"

@bp.route("/category_query")
def category_query():
    page = request.args.get('page',type=int,default=1)
    limit = request.args.get('limit',type=int,default=5)
    category_pg = Category.query.paginate(page=page,per_page = limit)

    category_list = []
    for item in category_pg.items:
        row = {
            "id":item.id,
            "name":item.name,
            "add_time":item.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time":item.update_time.strftime('%Y-%m-%d %H:%M:%S'),

        }
        category_list.append(row)

    data = {
        "code":0,
        "msg":"",
        "count":category_pg.total,
        "data":category_list
    }
    return jsonify(data)
@bp.route('/tag')
def tag():
    return render_template('admin/tag.html',**locals())


@bp.route('/tag_add', methods=['post'])
def tag_add():
    """
    标签管理-新增标签API
    :return:
    """
    tag_name = request.form['tag_name']
    tag_color = request.form['tag_color']
    print(tag_name)
    tag_ = Tag.query.filter_by(name=tag_name).first()
    if not tag_:
        tag_obj = Tag(name=tag_name, color=tag_color)
        db.session.add(tag_obj)
        db.session.commit()
        return 'success'
    return 'existed'



@bp.route('/tag_query')
def tag_query():
    page = request.args.get('page', type=int, default=1)
    limit = request.args.get('limit', type=int, default=5)
    tag_pg = Tag.query.paginate(page=page, per_page=limit)

    category_list = []
    for item in tag_pg.items:
        row = {
            "id": item.id,
            "name": item.name,
            "color": item.color,
            "add_time": item.add_time.strftime('%Y-%m-%d %H:%M:%S'),
            "update_time": item.update_time.strftime('%Y-%m-%d %H:%M:%S'),

        }
        category_list.append(row)

    data = {
        "code": 0,
        "msg": "",
        "count": tag_pg.total,
        "data": category_list
    }
    return jsonify(data)

