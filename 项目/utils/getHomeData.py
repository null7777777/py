from .utils import *
from .query import *


def getHomeData():
    maxMovieLen = len(df)  # 电影总个数

    maxRate = df['rate'].max()  # 最高评分

    # 计算最多演员出场
    castsList = typeList('casts')
    maxCasts = max(castsList, key=castsList.count)

    # 计算最多制片国家数
    countryList = typeList('country')
    maxCountry = max(countryList, key=countryList.count)

    # 计算总共类型个数
    typesList = typeList('types')
    maxTypes = len(set(typesList))

    # 计算最多语言
    langList = typeList('lang')
    maxLang = max(langList, key=langList.count)

    return maxMovieLen, maxRate, maxCasts, maxCountry, maxTypes, maxLang


# def getHomeData():
#     df = pd.read_sql('select * from movie', con=con)
#     maxMovieLen = len(df.values)  # 电影总个数
#
#
#     maxRate = df['rate'].max()  # 最高评分
#
#     castsList = typeList('casts')
#     maxCasts = max(castsList, key=castsList.count)  # 最多演员出场
#
#     countryList = typeList('country')
#     maxCountry = max(countryList, key=countryList.count)  # 最多制片国家数
#
#     typesList = typeList('types')
#     maxTypes = len(set(typesList))  # 总共类型个数
#
#     langList = typeList('lang')
#     maxLang = max(langList, key=langList.count)  # 最多语言
#
#     return maxMovieLen, maxRate, maxCasts, maxCountry, maxTypes, maxLang


# 电影种类饼状图
def getTypesEcharData():
    typesList = typeList('types')  # [xx,xx,xx]
    typeObj = {}
    for i in typesList:
        if typeObj.get(i, -1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] = typeObj[i] + 1

    typeEcharData = []
    for key, value in typeObj.items():
        typeEcharData.append(
            {
                'name': key,
                'value': value
            }
        )
    return typeEcharData


def getRateEcharData():
    rateList = df['rate'].map(lambda x: float(x)).values
    rateList.sort()
    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()), list(rateObj.values())


def getTableData():
    # 执行查询
    sql = 'SELECT * FROM movie LIMIT 300'

    data = list(querys(sql, [], 'select'))

    def map_fn(item):
        item = list(item)
        # row_list[2] = float(row_list[2])  # 将评分转换为浮点数
        # row_list[12] = int(row_list[12])  # 将片长转换为整数
        # row_list[7] = int(row_list[7])  # 将电影类型转换为整数
        item[17] = item[17].split(sep=',')
        return item

    data = map(map_fn, data)
    return data


# def getTableData():
#     tableData = df.values
#     for i, item in enumerate(tableData):
#         item[17] = item[17].split(sep=',')
#     return tableData


def getMovieUrlById(movieName):
    tableData = df[df['title'] == movieName].values[0]
    # print(tableData[id - 1])
    return tableData[-1]

# def getMovieUrlById(id):
#     tableData = df.values
#     # print(tableData[id - 1])
#     return tableData[id - 1][-1]


# getHomeData()
