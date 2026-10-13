from flask import Blueprint,render_template
from app.blog.models import Article

bp = Blueprint("blog", __name__, url_prefix="/blog",static_folder="static",template_folder="templates")

@bp.route("/index")
def index():
    title = "yunlong的小站"
    return render_template("index.html", **locals())
@bp.route("/post")
def post():
    title = "yunlong的小站"
    post = Article.query.get(1)
    return render_template("post.html", **locals())