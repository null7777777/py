from .utils import *


def getMapData():
    mapList = typeList('country')
    # print(mapList)
    mapObj = {}
    for i in mapList:
        if mapObj.get(i, -1) == -1:
            mapObj[i] = 1
        else:
            mapObj[i] += 1
    mapObj = sorted(mapObj.items(), key=lambda x: x[1], reverse=True)[:20]
    row = []
    columns = []
    for i in mapObj:
        row.append(i[0])
        columns.append(i[1])
    return row, columns


def getLangData():
    langList = typeList('lang')
    # print(mapList)
    langObj = {}
    for i in langList:
        if langObj.get(i, -1) == -1:
            langObj[i] = 1
        else:
            langObj[i] += 1
    # return list(langObj.keys()), list(langObj.values())
    langObj = sorted(langObj.items(), key=lambda x: x[1], reverse=True)[:10]
    row = []
    columns = []
    for i in langObj:
        row.append(i[0])
        columns.append(i[1])
    return row, columns