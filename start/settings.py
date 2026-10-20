"""整个项目的配置文件"""
from pathlib import Path
# 开启调试模式
DEBUG = True


#数据库的链接信息
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog?charset=utf8mb4'
BASE_DIR = Path(__file__).resolve().parent.parent