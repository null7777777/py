from .utils import *


def getYearData():
    timeList = list(df['time'].map(lambda x: int(x[:4])))
    timeList.sort()
    timeObj = {}
    for i in timeList:
        if i != 0:
            if timeObj.get(i, -1) == -1:
                timeObj[i] = 1
            else:
                timeObj[i] = timeObj[i] + 1
    return list(timeObj.keys()), list(timeObj.values())


def getMovieTimeData():
    movieTime = list(df['movieTime'])
    moveTimeDate = [
        {
            'name': '短',
            'value': 0
        },
        {
            'name': '中',
            'value': 0
        },
        {
            'name': '长',
            'value': 0
        },
        {
            'name': '特长',
            'value': 0
        },
    ]
    for i in movieTime:
        if int(i) > 0:
            if int(i) <= 60:
                moveTimeDate[0]['value'] = moveTimeDate[0]['value'] + 1
            elif int(i) <= 120:
                moveTimeDate[1]['value'] = moveTimeDate[1]['value'] + 1
            elif int(i) <= 150:
                moveTimeDate[2]['value'] = moveTimeDate[2]['value'] + 1
            else:
                moveTimeDate[3]['value'] = moveTimeDate[3]['value'] + 1
    return moveTimeDate
