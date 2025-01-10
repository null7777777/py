import pandas as pd
from sqlalchemy import create_engine

con = create_engine('mysql+pymysql://root:1234@localhost:3306/dbmovie')
df = pd.read_sql('select * from movie  LIMIT 1000', con=con)

# 传入字段参数 返回一个列表
# def typeList(type):
#     type = df[type].values
#     # print(type)
#     type = list(map(lambda x: x.split(','), type))
#     # print(type)
#     typeList = []
#     for i in type:
#         for j in i:
#             if j != '0':
#                 typeList.append(j)
#     return typeList

# 优化版
def typeList(type):
    # 使用 Pandas 的 explode 函数将逗号分隔的字符串拆分为多行，并去除值为 '0' 的项
    type_values = df[type].str.split(',').explode().loc[lambda x: x != '0']
    return type_values.tolist()

# a = typeList('casts')
# print(a,type(a))
# for i in a:
#     if i == '0':
#         print(i)
