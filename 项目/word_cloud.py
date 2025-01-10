import os
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import random
import matplotlib
import re
from DBUtils.PooledDB import PooledDB
import pymysql
import pandas as pd
from sqlalchemy import create_engine

# 使用非交互式后端
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# 创建数据库连接池
pool = PooledDB(
    creator=pymysql,
    host='localhost',
    user='root',
    password='1234',
    database='dbmovie',
    port=3306,
    maxconnections=5,
)

def querys(sql, params, type='no_select'):
    """数据库查询函数"""
    conn = pool.connection()
    params = tuple(params)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if type != 'no_select':
                data_list = cursor.fetchall()
                return data_list
            conn.commit()
            return '数据库语句执行成功!'
    finally:
        conn.close()

# 创建SQLAlchemy引擎
con = create_engine('mysql+pymysql://root:1234@localhost:3306/dbmovie')

# 读取电影数据
def get_movie_data():
    """获取电影数据"""
    return pd.read_sql('select * from movie LIMIT 1000', con=con)

def typeList(type):
    """获取类型列表"""
    df = get_movie_data()
    type_values = df[type].str.split(',').explode().loc[lambda x: x != '0']
    return type_values.tolist()

def ensure_directory_exists(file_path):
    """确保目录存在"""
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def get_font_path():
    """获取字体文件的绝对路径"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '飞波正点体.otf'))

def create_wordcloud(text, mask_path, output_path, font_path=None):
    """创建词云"""
    if font_path is None:
        font_path = get_font_path()

    # 确保字体文件存在
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"字体文件未找到: {font_path}")

    # 确保输出目录存在
    ensure_directory_exists(output_path)

    # 打开模板图片
    mask = np.array(Image.open(mask_path))

    # 创建WordCloud对象
    wc = WordCloud(
        background_color='white',
        mask=mask,
        font_path=font_path,
        max_words=200,
        max_font_size=100,
        random_state=42
    )

    # 生成词云
    wc.generate_from_text(text)

    # 保存词云图
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

def getImageByComments(comments):
    """根据评论生成词云"""
    # 合并评论内容
    text = ' '.join(comment['content'] for comment in comments)

    # 分词
    text = ' '.join(jieba.cut(text))

    # 生成随机文件名
    random_id = random.randint(1, 100000000)
    output_path = f'./static/img/{random_id}.png'

    # 创建词云
    create_wordcloud(text, './static/img/2.png', output_path)

    return output_path

def getImageByAuthor(field, targetImage, resImage):
    """根据字段生成词云"""
    # 获取数据
    data = querys(f'select {field} from movie', [], 'select')

    # 合并文本
    text = ' '.join(str(item[0]) for item in data if item[0] is not None)

    # 分词
    text = ' '.join(jieba.cut(text))

    # 创建词云
    create_wordcloud(text, targetImage, resImage)

def getCastsDataTop():
    """获取演员数据"""
    castsList = typeList('casts')
    # 统计演员出现频率
    castsObj = {}
    for i in castsList:
        castsObj[i] = castsObj.get(i, 0) + 1

    # 排序并获取前100名
    return sorted(castsObj.items(), key=lambda x: x[1], reverse=True)[:100]

def getImageByCasts(targetImage, resImage):
    """根据演员数据生成词云"""
    # 获取演员数据
    casts_data = getCastsDataTop()

    # 创建频率字典
    frequency_dict = dict(casts_data)

    # 确保字体文件存在
    font_path = get_font_path()
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"字体文件未找到: {font_path}")

    # 确保输出目录存在
    ensure_directory_exists(resImage)

    # 创建WordCloud对象
    mask = np.array(Image.open(targetImage))
    wc = WordCloud(
        background_color='white',
        mask=mask,
        font_path=font_path,
        max_words=200,
        max_font_size=100,
        random_state=42
    )

    # 根据频率生成词云
    wc.generate_from_frequencies(frequency_dict)

    # 保存词云图
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(resImage, bbox_inches='tight', dpi=300)
    plt.close()

# 生成初始词云图
try:
    # 生成演员词云
    getImageByCasts('./static/img/2.png', './static/img/cloud_cloud.png')
    # 生成简介词云
    getImageByAuthor('summary', './static/img/2.png', './static/img/summary_cloud.png')
    # 生成标题词云
    getImageByAuthor('title', './static/img/2.png', './static/img/title_cloud.png')
    print('生成词云图成功！')
except Exception as e:
    print(f'生成词云图失败：{str(e)}')