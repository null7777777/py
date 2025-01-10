from .query import *


def delMovieByMoiveName_user(movieName):
    sql = 'delete from user where email = %s'
    # print(movieName)
    querys(sql, [movieName])
    return getTableDataByTablePage_user()


def getTableDataByTablePage_user():
    # sql = 'select * from movie'
    sql = 'SELECT * FROM user'
    data = list(querys(sql, [], 'select'))

    def map_fn(item):
        item = list(item)
        return item

    data = map(map_fn, data)
    return data



# 过滤无视频无图片
# def getTableDataByTablePage():
#     sql = 'select * from movie'
#     data = list(querys(sql, [], 'select'))
#
#     def map_fn(item):
#         item = list(item)
#         if len(item[17]) > 1:
#             item[17] = item[17].split(sep=',')
#             return item
#         return None
#
#     # 过滤掉值为 None 的元素
#     data = filter(lambda x: x is not None, map(map_fn, data))
#
#     return data
