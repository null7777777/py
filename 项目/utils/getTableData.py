from .query import *


def delMovieByMoiveName(movieName):
    sql = 'delete from movie where title = %s'
    querys(sql, [movieName])
    return getTableDataByTablePage()


def getTableDataByTablePage():
    # sql = 'select * from movie'
    sql = 'SELECT * FROM movie LIMIT 300'
    data = list(querys(sql, [], 'select'))

    def map_fn(item):
        item = list(item)
        item[17] = item[17].split(sep=',')
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
