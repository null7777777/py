from .utils import *
from .query import *


def getMovieDetailById(movieId):
    # 执行查询
    sql = 'SELECT * FROM movie where id = %s'

    data = list(querys(sql, [movieId], 'select'))

    def map_fn(item):
        item = list(item)
        item[17] = item[17].split(sep=',')
        return item

    data = map(map_fn, data)
    return data
    # tableData = df.values
    # resultData = []
    # for i in tableData:
    #     if i[0] == movieId:
    #         i[17] = i[17].split(sep=',')
    #         resultData.append(list(i))
    # return resultData


def getMovieDetailBySearchWord(searchWord):
    # 执行查询
    sql = 'SELECT * FROM movie WHERE title LIKE %s'

    # 修改这里，传入参数为字符串而不是列表，并且不需要在参数中添加 %
    data = list(querys(sql, [f'%{searchWord}%'], 'select'))

    def map_fn(item):
        item = list(item)
        item[17] = item[17].split(sep=',')
        return item

    if data:
        # 使用 map 函数进行数据处理
        data = map(map_fn, data)

    else:
        data = []
    return data
    # print(searchWord)
    # tableData = df.values
    # resultData = []
    # for i in tableData:
    #     if i[3].find(searchWord) != -1:
    #         i[17] = i[17].split(sep=',')
    #         resultData.append(list(i))
    #         # resultData.append(i)
    # return resultData
