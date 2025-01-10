from .utils import *


def getTypeData():
    typesList = typeList('types')
    typesObj = {}
    for i in typesList:
        if typesObj.get(i, -1) == -1:
            typesObj[i] = 1
        else:
            typesObj[i] += 1

    typesData = []
    for key, item in typesObj.items():
        typesData.append(
            {
                'name': key,
                'value': item
            }
        )
    return typesData
