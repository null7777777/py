from flask import Flask, request, render_template, session, redirect, jsonify
from utils import query
from utils.getHomeData import *
from utils.getSearchData import *
from utils.getTime_tData import *
from utils.getRate_tData import *
from utils.getMapData import *
from utils.getType_tData import *
from utils.getActor_tData import *
from utils.getTableData import *
from utils.getComments_cData import *
from utils.getTableData_user import *
from utils.getuser_profileData import *
import re

app = Flask(__name__)
app.secret_key = 'This is secret_key you know ?'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # 根据邮箱查询普通用户
        users = query.querys('SELECT * FROM user WHERE email = %s', [email], 'select')

        usersgl = query.querys('SELECT * FROM usergl WHERE email = %s', [email], 'select')

        # 检查查询结果
        if users and len(users) > 0:
            user = users[0]
        elif usersgl and len(usersgl) > 0:
            user = usersgl[0]
        else:
            error_message = '不存在该用户！'
            return render_template('login.html', error_message=error_message)

        # 验证密码
        if user[2] == password:  # 假设密码是第三列
            # 检查是否为管理员，假设管理员标识在第四列
            session['email'] = email
            session['is_admin'] = user[3]
            # 登录成功后跳转到相应的主页
            return redirect('/home')
        else:
            error_message = '密码错误！'

    return render_template('login.html', error_message=error_message)


@app.route('/loginout')
def loginout():
    session.clear()
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        request.form = dict(request.form)
        if request.form['password'] != request.form['passwordChecked']:
            return render_template('register.html', error_message='两次密码不符合！')

    def filter_fn(item):
        return request.form['email'] in item

    users = query.querys('select * from user', [], 'select')
    filter_list = list(filter(filter_fn, users))

    if len(filter_list):
        return render_template('register.html', error_message='该用户已被注册！')
    else:
        query.querys('insert into user(email,password) values (%s,%s)',
                     [request.form['email'], request.form['password']])
        return redirect('/login')


# @app.route('/login', methods=['GET', 'POST'])
#
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     elif request.method == 'POST':
#         request.form = dict(request.form)
#
#     def filter_fn(item):
#         return request.form['email'] in item
#
#     users = query.querys('select * from user where email = %s', [request.form['email']], 'select')
#     filter_list = list(filter(filter_fn, users))
#
#     if len(filter_list):
#         if request.form['password'] == filter_list[0][2]:
#             session['email'] = request.form['email']
#             return redirect('/home')
#             # return render_template('error.html', message='登陆成功！')
#         else:
#             return render_template('error.html', message='密码错误！')
#     else:
#         return render_template('error.html', message='不存在该用户！')
#
#
# @app.route('/loginout')
# def loginout():
#     session.clear()
#     return redirect('/login')
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'GET':
#         return render_template('register.html')
#     elif request.method == 'POST':
#         request.form = dict(request.form)
#         if request.form['password'] != request.form['passwordChecked']:
#             return render_template('error.html', message='两次密码不符合！')
#
#     def filter_fn(item):
#         return request.form['email'] in item
#
#     users = query.querys('select * from user', [], 'select')
#     filter_list = list(filter(filter_fn, users))
#
#     if len(filter_list):
#         return render_template('error.html', message='该用户已被注册！')
#     else:
#         query.querys('insert into user(email,password) values (%s,%s)',
#                      [request.form['email'], request.form['password']])
#         return redirect('/login')


@app.route('/home', methods=['GET', 'POST'])
def home():
    email = session.get('email')
    global firstItem
    if session.get('is_admin') == '1':
        firstItem = session.get('firstItem') or get_user_gl(email)  # 使用会话中的数据或重新获取
    else:
        firstItem = session.get('firstItem') or get_user(email)  # 使用会话中的数据或重新获取

    maxMovieLen, maxRate, maxCasts, maxCountry, maxTypes, maxLang = getHomeData()
    typeEcharData = getTypesEcharData()
    row, columns = getRateEcharData()

    tableData = getTableData()

    return render_template(
        'index.html',
        email=email,
        maxMovieLen=maxMovieLen,
        maxRate=maxRate,
        maxCasts=maxCasts,
        maxCountry=maxCountry,
        maxTypes=maxTypes,
        maxLang=maxLang,
        typeEcharData=typeEcharData,
        row=row,
        columns=columns,
        tableData=tableData,
        firstItem=firstItem,
    )


# 个人中心
@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    email = session.get('email')
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        if session.get('is_admin') == '1':
            request.form = dict(request.form)
            avatar_file = request.files.get('avatar')
            resultData_user = update_user_gl(email, request.form, avatar_file)
            # 更新会话中的用户信息
            session['firstItem'] = get_user_gl(email)  # 假设 get_user_gl 返回管理信息字典
        else:
            request.form = dict(request.form)
            avatar_file = request.files.get('avatar')
            resultData_user = update_user(email, request.form, avatar_file)
            # 更新会话中的用户信息
            session['firstItem'] = get_user(email)  # 假设 get_user 返回用户信息字典
        return redirect('/home')

    # 渲染用户个人中心页面
    return render_template('user_profile.html', email=email, firstItem=firstItem)


# 用户管理
@app.route('/table_user/<movieName>')
def table_user(movieName):
    email = session.get('email')
    tableData = delMovieByMoiveName_user(movieName)
    return render_template('table_user.html', email=email, tableData=tableData, firstItem=firstItem)


# 电影预告片
@app.route('/movie/<movieName>')
def movie(movieName):
    movieUrl = getMovieUrlById(movieName)
    return render_template('movie.html', movieUrl=movieUrl)


# @app.route('/movie/<int:movieid>')
# def movie(movieid):
#     movieUrl = getMovieUrlById(movieid)
#     print(movieUrl)
#     return render_template('movie.html', movieUrl=movieUrl)

# 搜索
@app.route('/search/<int:movieId>', methods=['GET', 'POST'])
def search(movieId):
    email = session.get('email')
    if request.method == 'GET':
        resultData = getMovieDetailById(movieId)
    else:
        request.form = dict(request.form)
        resultData = getMovieDetailBySearchWord(request.form['searchWord'])
    return render_template('search.html', email=email, resultData=resultData, firstItem=firstItem)


# 时间
@app.route('/time_t')
def time_t():
    email = session.get('email')

    row, columns = getYearData()
    moveTimeDate = getMovieTimeData()

    return render_template('time_t.html', email=email, row=row, columns=columns, moveTimeDate=moveTimeDate,
                           firstItem=firstItem)


# 评分
@app.route('/rate_t/<type>', methods=['GET', 'POST'])
def rate_t(type):
    email = session.get('email')

    typeList = getAllTypes()
    row, columns = getAllRateDataByType(type)
    yearMenRow, yearMenColumns = getYearMeanData()
    if request.method == 'GET':
        startData, searchName = getStart('')
    else:
        request.form = dict(request.form)
        startData, searchName = getStart(request.form['searchIpt'])
    return render_template(
        'rate_t.html',
        email=email,
        typeList=typeList,
        type=type,
        row=row,
        columns=columns,
        startData=startData,
        searchName=searchName,
        yearMenRow=yearMenRow,
        yearMenColumns=yearMenColumns, firstItem=firstItem
    )


# 地图
@app.route('/map_t')
def map_t():
    email = session.get('email')

    row, columns = getMapData()
    # print(row, type(row))
    # print(columns, type(columns))
    langRow, langColumns = getLangData()
    return render_template('map_t.html', email=email, row=row, columns=columns, langRow=langRow,
                           langColumns=langColumns, firstItem=firstItem)


# 类型
@app.route('/type_t')
def type_t():
    email = session.get('email')

    typesData = getTypeData()
    return render_template('type_t.html', email=email, typesData=typesData, firstItem=firstItem)


# 导演、演员
@app.route('/actor_t')
def actor_t():
    email = session.get('email')

    row, columns = getDirectorsDataTop20()
    rowCasts, columnsCasts = getCastsDataTop20()
    return render_template('actor_t.html', email=email, row=row, columns=columns, rowCasts=rowCasts,
                           columnsCasts=columnsCasts, firstItem=firstItem)


@app.route('/table/<movieName>')
def table(movieName):
    email = session.get('email')

    tableData = delMovieByMoiveName(movieName)
    # return redirect('/table/0')
    # tableData = getTableDataByTablePage()
    return render_template('table.html', email=email, tableData=tableData, firstItem=firstItem)


# 评论词云图
@app.route('/comments_c', methods=['GET', 'POST'])
def comments_c():
    email = session.get('email')

    resSrc, searchName = '', ''  # 初始化为空字符串

    if request.method == 'POST':
        searchIpt = request.form['searchIpt']
        resSrc, searchName = getCommentsImage(searchIpt)
        # 如果没有找到匹配项，resSrc 应该是空字符串，此时不渲染图片

    return render_template('comments_c.html', email=email, resSrc=resSrc, searchName=searchName, firstItem=firstItem)


# 标题词云图
@app.route('/title_c', methods=['GET', 'POST'])
def title_c():
    email = session.get('email')

    return render_template('title_c.html', email=email, firstItem=firstItem)


# 简介词云图
@app.route('/summary_c', methods=['GET', 'POST'])
def summary_c():
    email = session.get('email')

    return render_template('summary_c.html', email=email, firstItem=firstItem)


# 演员名词云图
@app.route('/casts_c', methods=['GET', 'POST'])
def casts_c():
    email = session.get('email')

    return render_template('casts_c.html', email=email, firstItem=firstItem)


@app.route('/')
def allRequest():
    return redirect('/login')


# 定义了一个 Flask 应用的全局前置请求处理器（before request handler）
# 它会在每次请求到达 Flask 应用之前运行
@app.before_request
def before_requre():
    # 定义一个正则表达式模式，匹配以 '/static' 开头的路径
    pat = re.compile(r'^/static')

    # 如果请求的路径匹配 '/static' 开头，则不进行后续的检查，直接返回
    # 这意味着静态文件的请求不会被后续的认证逻辑所拦截
    if re.search(pat, request.path):
        return

    # 如果请求的路径是 "/login"，同样不进行后续的检查，直接返回
    # 这允许用户直接访问登录页面，而不需要先登录
    if request.path == "/login":
        return

    # 如果请求的路径是 '/register'，同样不进行后续的检查，直接返回
    # 假设 '/register' 是注册页面的路径，允许用户直接访问注册页面
    if request.path == '/register':
        return

    # 尝试从 session 中获取用户的电子邮件地址
    email = session.get('email')

    # 如果 session 中存在电子邮件地址（即用户已登录）
    if email:
        # 则不进行任何操作，返回 None 表示继续处理该请求
        return None

    # 如果 session 中不存在电子邮件地址（即用户未登录）
    # 则重定向用户到登录页面 '/login'
    return redirect('/login')


if __name__ == '__main__':
    app.run()
