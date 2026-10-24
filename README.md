# YL_blog · 基于 Flask 的个人博客系统

一个前后台一体的个人博客项目：前台负责文章、笔记、归档、留言与评论展示，后台提供基于 Markdown 的内容管理，覆盖分类、标签、图片上传与「关于我」维护。项目采用 Flask 应用工厂 + 蓝图的方式组织代码，使用 MySQL 持久化数据，并通过 APScheduler 每日抓取 Bing 壁纸作为站点配图。

## 功能特性

### 博客前台

- **首页文章流**：分页展示文章（每页 5 篇），显示标题、摘要、作者、分类、发布时间与阅读数。
- **文章详情**：渲染 Markdown 转换后的 HTML，Prism.js 代码高亮并带行号；自动统计阅读次数，提供上一篇 / 下一篇跳转。
- **评论系统**：游客可提交评论，支持多层嵌套回复；根据访问 IP 自动解析归属地（离线 ip2region 库，不依赖第三方接口）。
- **分类与标签**：按分类、按标签筛选文章，分页展示。
- **归档**：按年月分组展示全部已发布文章。
- **笔记**：短内容笔记列表与分页，和文章一样支持 Markdown、分类和标签。
- **留言板**：独立留言页面，记录留言者昵称、邮箱与 IP 归属地。
- **搜索**：支持文章搜索与笔记搜索，匹配标题和 Markdown 正文。
- **关于页**：展示后台维护的个人介绍（Markdown 渲染）。
- **界面**：Layui 响应式布局，canvas-nest 粒子背景，侧边栏包含分类统计、最新文章、标签云与个人卡片。
- **安全**：全站 CSRF 防护，Layui 的 AJAX 请求统一携带 CSRF Token。

### 管理后台（`/qd_admin`）

- **登录 / 登出**：Flask-Login 会话管理，Werkzeug 哈希校验密码，未登录访问自动跳转登录页。
- **文章管理**：分页列表（Layui 数据表格），显示标题、分类、阅读数、创建与更新时间。
- **文章编辑**：Toast UI Editor 双栏 Markdown 编辑与实时预览，支持代码高亮、颜色语法；可直接粘贴 / 上传图片，附件信息写入数据库并与文章关联。
- **分类管理**：新增分类、分页查询，名称唯一性校验。
- **标签管理**：新增标签（含颜色）、分页查询，名称唯一性校验。
- **笔记管理**：笔记列表、Markdown 编辑与新增。
- **关于我管理**：Markdown 编辑并保存为 HTML，前台关于页直接读取。
- **CSRF 保护**：后台写接口按需豁免，其余请求由 Flask-WTF 校验。

### 定时任务

- 每天 00:20（Asia/Shanghai）通过 APScheduler 抓取 Bing 当日壁纸，保存为 `app/blog/static/imgs/bing.jpg`，用作站点背景图。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 语言 | Python 3.10 |
| Web 框架 | Flask 2.3 |
| ORM / 迁移 | Flask-SQLAlchemy（SQLAlchemy 2.0）、Flask-Migrate（Alembic） |
| 数据库 | MySQL（utf8mb4），驱动 mysqlclient |
| 认证与安全 | Flask-Login、Flask-WTF / CSRFProtect、Werkzeug 密码哈希 |
| 定时任务 | Flask-APScheduler（cron 触发器） |
| 数据采集 | requests + parsel（Bing 壁纸） |
| IP 归属地 | ip2region 离线库（随项目内置 xdb 数据） |
| 前端 | Layui、Toast UI Editor、Prism.js、canvas-nest.js、activate-power-mode |

## 项目结构

```text
blog/
├── manage.py                  # 项目启动入口
├── manage_test.py             # 早期的 Flask 连通性测试脚本
├── start/
│   ├── __init__.py            # 应用工厂 create_app()，扩展与蓝图注册
│   └── settings.py            # 全局配置：数据库、定时任务、时区、密钥
├── app/
│   ├── blog/                  # 前台蓝图（/blog）
│   │   ├── views.py           # 首页、文章、分类、标签、归档、笔记、留言、搜索
│   │   ├── models.py          # 文章 / 分类 / 标签 / 笔记 / 评论 / 留言 / 附件模型
│   │   ├── templates/         # 前台页面与公共组件（侧边栏、评论、搜索等）
│   │   └── static/            # Layui、Prism、ip2region、JS、CSS、图片、上传目录
│   └── admin/                 # 后台蓝图（/qd_admin）
│       ├── views.py           # 登录、文章 / 分类 / 标签 / 笔记 / 关于我管理、上传
│       ├── models.py          # 用户、站点信息模型
│       ├── templates/         # 后台页面（含登录页、编辑器）
│       └── static/            # 后台样式与 Toast UI Editor 资源
├── migrations/                # Alembic 迁移脚本
├── utils/
│   ├── filters.py             # Jinja 过滤器：时间格式化、地址清洗、去 HTML 标签
│   └── time_task.py           # Bing 壁纸爬虫（定时任务调用）
└── .vscode/                   # VS Code 调试配置（F5 启动 manage.py）
```

## 数据模型

| 表名 | 说明 |
| --- | --- |
| `post_db` | 文章：标题、封面、Markdown / HTML 正文、阅读数、草稿标记、分类、作者 |
| `category_db` | 分类，与文章、笔记一对多 |
| `tag_db` | 标签（含颜色），与文章、笔记多对多 |
| `post-tags` / `note_tags` | 文章 / 笔记与标签的关联表 |
| `note_db` | 笔记：标题、Markdown / HTML 正文、阅读数、分类、作者 |
| `comment_db` | 评论：内容、访客信息、IP 归属地、所属文章、`replied_id` 自关联实现嵌套回复 |
| `message_db` | 留言：内容、访客信息、IP 归属地 |
| `attachment_db` | 附件：文件名、大小、路径，关联文章或笔记 |
| `user_db` | 后台用户：用户名、密码哈希、昵称、头像、上次登录时间 |
| `bloginfo_db` | 站点信息：标题、副标题、「关于我」的 Markdown / HTML |

## 快速开始

### 1. 环境要求

- Python 3.10
- MySQL 5.7 / 8.0，字符集 `utf8mb4`

### 2. 安装依赖

项目当前未锁定依赖版本，可直接安装以下包：

```bash
pip install flask flask-sqlalchemy flask-migrate flask-apscheduler \
            flask-login flask-wtf mysqlclient requests parsel
```

> Windows 下 `mysqlclient` 需要本机具备 MySQL 客户端库；若安装失败，也可以改用 PyMySQL，并把数据库连接串改成 `mysql+pymysql://...`。

### 3. 创建数据库

```sql
CREATE DATABASE blog DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后修改 [start/settings.py](start/settings.py) 中的连接串：

```python
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog?charset=utf8mb4'
```

### 4. 执行数据库迁移

```bash
# PowerShell
$env:FLASK_APP = "manage.py"
flask db upgrade
```

### 5. 创建后台账号

项目没有开放注册入口，可执行一次下面的脚本初始化管理员（用户名 / 密码请自行替换）：

```python
from start import create_app, db
from app.admin.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    db.session.add(User(
        username="admin",
        password=generate_password_hash("123456", method="pbkdf2:sha256:600000"),
        nickname="管理员",
    ))
    db.session.commit()
```

### 6. 准备上传目录

```bash
mkdir app/blog/static/upload
```

该目录用于保存文章编辑器上传的图片。目录为空时 Git 不会跟踪它，重新克隆项目后需要手动创建。

### 7. 启动

```bash
python manage.py
```

| 入口 | 地址 |
| --- | --- |
| 博客前台 | http://127.0.0.1:5000/ |
| 管理后台 | http://127.0.0.1:5000/qd_admin/login |

> 默认只监听 `127.0.0.1:5000`。如需局域网或服务器访问，可在 `manage.py` 中改为 `app.run(host='0.0.0.0', port=5000)`。

### 在 VS Code 中运行

仓库内已提供 [.vscode/launch.json](.vscode/launch.json) 与 [.vscode/settings.json](.vscode/settings.json)：选择项目所用的 Python 解释器后，按 `F5` 选择「启动博客网站 (Flask)」即可调试运行；也可在集成终端执行 `python manage.py`。

## 路由一览

### 前台

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/`、`/blog/page/<page>` | 首页文章分页 |
| GET | `/blog/post/<post_id>` | 文章详情、评论列表、上下篇 |
| GET | `/blog/category/<category_id>` | 分类文章列表 |
| GET | `/blog/tag/<tag_id>` | 标签文章列表 |
| GET | `/blog/record` | 按年月归档 |
| GET | `/blog/note/<curr>` | 笔记分页 |
| GET | `/blog/message` | 留言板 |
| GET | `/blog/about` | 关于我 |
| GET | `/blog/post_search`、`/blog/note_search` | 文章 / 笔记搜索 |
| POST | `/blog/comment_add`、`/blog/comment_reply` | 发表评论 / 回复评论 |
| POST | `/blog/message_add` | 发表留言 |

### 后台

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET/POST | `/qd_admin/login` | 登录 |
| GET | `/qd_admin/logout` | 登出 |
| GET | `/qd_admin/post`、`/qd_admin/post_query` | 文章列表页 / 列表数据 |
| GET | `/qd_admin/category`、`/qd_admin/category_query` | 分类列表页 / 列表数据 |
| POST | `/qd_admin/add_category` | 新增分类 |
| GET | `/qd_admin/tag`、`/qd_admin/tag_query` | 标签列表页 / 列表数据 |
| POST | `/qd_admin/tag_add` | 新增标签 |
| GET | `/qd_admin/editor_post` | 文章编辑页 |
| POST | `/qd_admin/post_add` | 新增文章 |
| POST | `/qd_admin/upload` | 图片上传 |
| GET | `/qd_admin/note`、`/qd_admin/note_query` | 笔记列表页 / 列表数据 |
| GET | `/qd_admin/editor_note` | 笔记编辑页 |
| POST | `/qd_admin/note_add` | 新增笔记 |
| GET | `/qd_admin/about` | 「关于我」编辑页 |
| POST | `/qd_admin/about_add` | 保存「关于我」 |

## 配置说明

所有配置集中在 [start/settings.py](start/settings.py)：

| 配置项 | 作用 |
| --- | --- |
| `DEBUG` | 调试模式，当前为 `True` |
| `SQLALCHEMY_DATABASE_URI` | MySQL 连接串 |
| `JOBS` | APScheduler 任务列表，当前为每天 00:20 抓取 Bing 壁纸 |
| `SCHEDULER_TIMEZONE` | 调度时区，`Asia/Shanghai` |
| `SECRET_KEY` | 会话与 CSRF 签名密钥 |

## 实现要点

- **应用工厂**：`start/create_app()` 统一完成配置加载、扩展初始化、蓝图注册与 Jinja 过滤器挂载，便于测试和多实例部署。
- **蓝图隔离**：前台 `/blog` 与后台 `/qd_admin` 各自持有模板与静态资源；后台页面通过 `request.blueprint` 判断，避免注入前台侧边栏数据。
- **全局侧边栏**：使用 `app_context_processor` 注入分类文章数、最新文章和标签，所有前台页面共享。
- **评论树**：`comment_db.replied_id` 自关联，递归拼装多层回复并按时间排序。
- **离线 IP 库**：评论 / 留言写入时调用 ip2region 查询归属地，无需外部 API。
- **CSRF 处理**：`CSRFProtect` 全局开启，模板通过 `<meta name="csrf-token">` 暴露 token，Layui 的 `$.ajaxSetup` 自动带上请求头。
- **定时任务**：APScheduler 随应用启动，使用 cron 触发器按上海时区执行壁纸抓取。

## 已知限制与后续计划

- 文章和笔记目前只支持新增，暂未提供编辑 / 删除已发布内容的入口。
- 图片上传的文件名生成规则待统一：建议统一为 `时间戳 + 扩展名`，并在服务端自动创建上传目录。
- 配置中的数据库密码与 `SECRET_KEY` 为明文，生产环境应改为环境变量管理。
- 依赖版本与 `requirements.txt` 尚未固定，自动化测试与部署脚本也还未补充。
- 后续可考虑：文章编辑与删除、附件管理页、全文检索、后台数据统计、Gunicorn + Nginx 部署与 Docker 化。

## License

未指定许可证。如需开源，请补充 LICENSE 文件。
