"""整个项目的配置文件"""
from pathlib import Path
# 开启调试模式
DEBUG = True


#数据库的链接信息
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/blog?charset=utf8mb4'
BASE_DIR = Path(__file__).resolve().parent.parent
from utils.time_task import spider_bing

# APScheduler会识别JOBS，一个dict为一个任务，func为任务执行的函数，定时的方式时间定义在trigger中，以下为3秒一次
JOBS = [
        {
            'id': 'task1',  # 任务id
            'func': spider_bing,  # 任务执行程序
            'args': None,  # 执行程序参数
            'trigger': 'cron',
            'minute':'20',
            'hour': '0',
            'second': '0',
        }
    ]

# 设置时区，时区不一致会导致定时任务的时间错误
SCHEDULER_TIMEZONE = 'Asia/Shanghai'
# 开启API功能，这样才可以用api的方式去查看定时任务
# SCHEDULER_API_ENABLED = True
# # api前缀（默认是/scheduler）
# SCHEDULER_API_PREFIX = '/scheduler'
SECRET_KEY = 'FBRAE FGB SDRABGVUIL FDA'