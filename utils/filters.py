from datetime import datetime


def strftime(data):
    return data.strftime('%Y年 %m月 %d日 %H:%M')


def strftime_comment(date):
    # 格式化评论区的时间
    return date.strftime('%m月%d日 %H:%M')


def address(data):
    # 中国|0|湖南省|长沙市|联通
    list_ = data.split('|')
    return list_[2] + ' ' + list_[3]


FILTERS = {
    'strftime': strftime,
    'strftime_comment': strftime_comment,
    'address': address
}
