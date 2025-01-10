import os

from werkzeug.utils import secure_filename

from .query import *


def get_user(email):
    sql = 'SELECT * FROM user WHERE email = %s'
    data = querys(sql, [email], 'select')
    return [list(item) for item in data]


def update_user(email, user_data, avatar_file):
    # 如果有上传的头像文件，保存文件并更新数据库中的头像文件名
    if avatar_file:
        # 获取上传文件的安全文件名
        filename = secure_filename(avatar_file.filename)
        # 构建保存在静态资源目录下的文件路径
        avatar_path = os.path.join('img', filename)
        # 保存头像文件到指定目录
        avatar_file.save(os.path.join('static', avatar_path))
        # 构建更新语句
        sql = 'UPDATE user SET name = %s, age = %s, sex = %s, birthday = %s, password = %s, introduction = %s, avatar = %s WHERE email = %s'
        # 为 user_data 中可能缺失的键提供默认值
        default_sex = '未知'  # 你可以根据需要设置一个合适的默认值
        values = (
            user_data.get('name', ''),
            user_data.get('age', ''),
            user_data.get('sex', default_sex),  # 如果 'sex' 键不存在，使用默认值
            user_data.get('birthday', ''),
            user_data.get('password', ''),
            user_data.get('introduction', ''),
            filename,  # 保存文件名，而不是文件路径
            email
        )
        # 执行更新操作
        querys(sql, values)
        return 1
    else:
        # 如果没有上传头像文件，则只更新用户信息，不需要保存文件
        sql = 'UPDATE user SET name = %s, age = %s, sex = %s, birthday = %s, password = %s, introduction = %s WHERE email = %s'
        # 为 user_data 中可能缺失的键提供默认值
        default_sex = '未知'  # 你可以根据需要设置一个合适的默认值
        values = (
            user_data.get('name', ''),
            user_data.get('age', ''),
            user_data.get('sex', default_sex),  # 如果 'sex' 键不存在，使用默认值
            user_data.get('birthday', ''),
            user_data.get('password', ''),
            user_data.get('introduction', ''),
            email
        )
        # 执行更新操作
        querys(sql, values)
        return 1


def get_user_gl(email):
    sql = 'SELECT * FROM usergl WHERE email = %s'
    data = querys(sql, [email], 'select')
    return [list(item) for item in data]



def update_user_gl(email, user_data, avatar_file):
    # 如果有上传的头像文件，保存文件并更新数据库中的头像文件名
    if avatar_file:
        # 获取上传文件的安全文件名
        filename = secure_filename(avatar_file.filename)
        # 构建保存在静态资源目录下的文件路径
        avatar_path = os.path.join('img', filename)
        # 保存头像文件到指定目录
        avatar_file.save(os.path.join('static', avatar_path))
        # 构建更新语句
        sql = 'UPDATE usergl SET name = %s, age = %s, sex = %s, birthday = %s, password = %s, introduction = %s, avatar = %s WHERE email = %s'
        # 为 user_data 中可能缺失的键提供默认值
        default_sex = '未知'  # 你可以根据需要设置一个合适的默认值
        values = (
            user_data.get('name', ''),
            user_data.get('age', ''),
            user_data.get('sex', default_sex),  # 如果 'sex' 键不存在，使用默认值
            user_data.get('birthday', ''),
            user_data.get('password', ''),
            user_data.get('introduction', ''),
            filename,  # 保存文件名，而不是文件路径
            email
        )
        # 执行更新操作
        querys(sql, values)
        return 1
    else:
        # 如果没有上传头像文件，则只更新用户信息，不需要保存文件
        sql = 'UPDATE usergl SET name = %s, age = %s, sex = %s, birthday = %s, password = %s, introduction = %s WHERE email = %s'
        # 为 user_data 中可能缺失的键提供默认值
        default_sex = '未知'  # 你可以根据需要设置一个合适的默认值
        values = (
            user_data.get('name', ''),
            user_data.get('age', ''),
            user_data.get('sex', default_sex),  # 如果 'sex' 键不存在，使用默认值
            user_data.get('birthday', ''),
            user_data.get('password', ''),
            user_data.get('introduction', ''),
            email
        )
        # 执行更新操作
        querys(sql, values)
        return 1
