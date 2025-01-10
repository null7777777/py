from .utils import *
import re


def getAllTypes():
    return list(set(typeList('types')))


# 评分
def getAllRateDataByType(type):
    if type == 'all':
        rateList = df['rate'].values
        # rateList = df['rate'].map(lambda x: float(x)).values
        rateList.sort()
    else:
        typeList = df['types'].map(lambda x: x.split(sep=','))
        oldRateList = df['rate'].values
        rateList = []
        for i, item in enumerate(typeList):
            if type in item:
                rateList.append(oldRateList[i])

    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()), list(rateObj.values())


def getStart(searchIpt):
    searchdata = list(df.loc[df['title'].str.contains(searchIpt)]['title'])
    if searchdata:
        # print(startes, searchName)
        searchName = searchdata[0]
        startes = list(df.loc[df['title'].str.contains(searchIpt)]['starts'])[0].split(',')
        startData = [
            {
                'name': '五星',
                'value': 0
            },
            {
                'name': '四星',
                'value': 0
            },
            {
                'name': '三星',
                'value': 0
            },
            {
                'name': '二星',
                'value': 0
            },
            {
                'name': '一星',
                'value': 0
            }
        ]
        for i, item in enumerate(startes):
            # startData[i]['value'] = float(re.sub('%', '', item))
            startData[i]['value'] = float(re.sub('%', '', item))
    else:
        searchName = '无此电影'
        startData = ''
    return startData, searchName


# 豆瓣年度评价评分柱状图
def getYearMeanData():
    # 确保 'rate' , 'year' 列是数值类型
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    # 将非数值类型的数据转换为 NaN
    df.dropna(subset=['rate', 'year'], inplace=True)

    # 获取唯一的年份列表，并去除可能的 NaN 值
    yearList = list(set(df['year'].dropna().unique()))

    # 尝试删除列表中的第一个 0，如果它存在的话
    if 0 in yearList:
        yearList.remove(0)

    # # 计算每个年份的电影评分平均值
    # meanList = []
    # for year in yearList:
    #     meanList.append(df[df['year'] == year]['rate'].mean())
    #
    # return yearList, meanList

    # 计算每个年份的电影评分平均值
    meanList = []
    for year in yearList:
        mean = df[df['year'] == year]['rate'].mean()
        meanList.append(round(mean, 3))  # 保留三位小数

    return yearList, meanList
