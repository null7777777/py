from .utils import *


def getDirectorsDataTop20():
    directorsList = typeList('directors')
    directorsObj = {}
    for i in directorsList:
        if directorsObj.get(i, -1) == -1:
            directorsObj[i] = 1
        else:
            directorsObj[i] = directorsObj[i] + 1
    directorsObj = sorted(directorsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    row = []
    columns = []
    for i in directorsObj:
        row.append(i[0])
        columns.append(i[1])
    return row, columns


def getCastsDataTop20():
    castsList = typeList('casts')
    castsObj = {}
    for i in castsList:
        if castsObj.get(i, -1) == -1:
            castsObj[i] = 1
        else:
            castsObj[i] = castsObj[i] + 1
    castsObj = sorted(castsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    row = []
    columns = []
    for i in castsObj:
        row.append(i[0])
        columns.append(i[1])
    return row, columns
