from flask import Blueprint,render_template
from app.blog.models import Post

bp = Blueprint("blog", __name__, url_prefix="/blog",static_folder="static",template_folder="templates")
#因为在初始化文件中注册了首页路由，这里的路由规则就不适用了
# @bp.route("/index")
def index():
    title = "yunlong的小站"
    return render_template("index.html", **locals())

# @bp.route("/post")
# def post():
#     title = "yunlong的小站"
#     post = Article.query.get(1)
#     return render_template("post.html", **locals())