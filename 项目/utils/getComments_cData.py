from .utils import *
import json
import sys

sys.path.append('..')
from word_cloud import *


# def getCommentsImage(searchIpt):
#     searchName = list(df.loc[df['title'].str.contains(searchIpt)]['title'])[0]
#     comments = df[df['title'] == searchName]['comments'].values[0]
#     comments = json.loads(comments)
#     resSrc = getImageByComments(comments)
#     return resSrc, searchName

def getCommentsImage(searchIpt):
    searchResults = df.loc[df['title'].str.contains(searchIpt)]
    if searchResults.empty:
        return '', ''  # 如果没有搜索结果，返回消息和 None

    searchName = searchResults['title'].values[0]
    comments = df[df['title'] == searchName]['comments'].values[0]
    comments = json.loads(comments)
    resSrc = getImageByComments(comments)
    return resSrc, searchName
