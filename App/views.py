from flask import render_template, Blueprint, request, make_response, Response, redirect, url_for, abort, session

blue = Blueprint('blue', __name__)


@blue.route('/', methods=['get', 'post'])
def hello_world():
    if request.remote_addr == '192.168.1.79':
        return '被ban了\n'

    print('*' * 30)
    print('request: ', request)
    print('method: ', request.method)
    print('ip: ', request.remote_addr)
    print('path: ', request.path)
    print('*' * 30)

    return 'Hello!'


@blue.route('/message')
def message():
    return '试试中文'


@blue.route('/surface', methods=['get', 'post'])
def surface():
    # username = request.form.get('name')

    username = session.get('username')
    print(username)
    return render_template('surface_wave.html', name=username)


@blue.route('/para-test', methods=['get', 'post'])
def para_test():
    # # url 中的请求参数
    # args = [(each, request.args.getlist(each)) for each in request.args]

    # 请求体中的请求参数
    args = [(each, request.form.getlist(each)) for each in request.form]

    print(str(args))
    print('path: ', request.path)

    return str(args)


# ****** 返回 Response 对象 ******
@blue.route('/response-test', methods=['get', 'post'])
def response_test():
    res = make_response('返回个 Response')

    print(res)
    print(type(res))

    return res


@blue.route('/response-test2', methods=['get', 'post'])
def response_test2():
    res = Response('返回个 Response')

    print(res)
    print(type(res))

    return res


# ****** 重定向 ******
@blue.route('/redirect-test', methods=['get', 'post'])
def redirect_test():
    a = redirect(url_for('blue.response_test2'))

    print(type(a))

    return redirect(url_for('blue.message'))


# ****** 登录跳转 ******
@blue.route('/welcome', methods=['get', 'post'])
def welcome():
    name = request.form.get('name')
    age = request.form.get('age')

    return render_template('welcome.html', name=name, age=age)


@blue.route('/login', methods=['get', 'post'])
def login():
    username = session.get('username')
    return render_template('login.html', name=username)


# ****** 异常捕获 ******
@blue.route('/error-test-404')
def error_test_404():
    abort(404)

    return '看到这个就坏了'


@blue.errorhandler(404)
def handler_404(exception):
    return '现在是404状态，但是被捕获到了'


# ****** cookie登录 ******
# 登录页面
@blue.route('/cookie-login', methods=['get', 'post'])
def cookie_login():
    username = request.form.get('name')
    return render_template('cookie_login.html', name=username)


# 通过重定向来获取具有客户端请求参数的，response对象，并且将信息存入 cookie
@blue.route('/cookie-redirect', methods=['get', 'post'])
def cookie_redirect():
    # get username fron clien
    username = request.form.get('name')
    password = request.form.get('password')

    # redirect() return a response object
    response = redirect(url_for('blue.cookie_test'))
    response.set_cookie('username', username)
    response.set_cookie('password', password)

    return response


# 重定向的目标网址，该网址从 cookie 中获取用户身份信息，并返回相应权限的数据
@blue.route('/cookie-test', methods=['get', 'post'])
def cookie_test():
    # Registered user in database
    users = {
        'alun': {
            'password': 'zuishuai',
            'age': 18
        }
    }

    username = request.cookies.get('username', '游客')
    password = request.cookies.get('password')

    user = users.get(username, '游客')
    if user == '游客':
        return render_template('welcome.html', name='游客', age='不管多少永远18')

    passwd = user.get('password')

    if password != passwd:
        return '用户名或密码错误'

    age = user.get('age')

    return render_template('welcome.html', name=username, age=age)


# 这里设置了一个主动调用时会清除掉 cookie 的页面
@blue.route('/cookie-clear', methods=['get', 'post'])
def cookie_clear():
    response = redirect(url_for('blue.cookie_test'))
    response.delete_cookie('username')
    response.delete_cookie('password')

    return response


# ****** session登录 ******
# session 登录页面
@blue.route('/session-login', methods=['get', 'post'])
def session_login():
    return render_template('session_login.html')


@blue.route('/session-redirect', methods=['get', 'post'])
def session_redirect():
    user_req = request.form.get('name')
    passwd_req = request.form.get('password')
    print("user_req: ", user_req)
    print("passwd_req: ", passwd_req)

    session['username'] = user_req
    session['password'] = passwd_req

    return redirect(url_for('blue.session_test'))


@blue.route('/session-test', methods=['get', 'post'])
def session_test():
    users = {
        'alun': {
            'password': 'zuishuai',
            'age': 18
        }
    }

    username = session.get('username')
    password = session.get('password')

    user = users.get(username, '游客')
    if user == '游客':
        return render_template('welcome.html', name='游客', age='永远18')

    passwd = user.get('password')

    if password != passwd:
        return '用户名或密码错误！'

    age = user.get('age')

    return render_template('welcome.html', name=username, age=age)


@blue.route('/session-clear')
def session_clear():
    session.pop('username')
    session.pop('password')

    return redirect(url_for('blue.session_test'))
