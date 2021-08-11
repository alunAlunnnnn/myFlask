from flask import render_template, Blueprint, request, make_response, Response, redirect, url_for, abort

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
    return render_template('surface_wave.html')


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
    return render_template('login.html')


# ****** 异常捕获 ******
@blue.route('/error-test-404')
def error_test_404():
    abort(404)

    return '看到这个就坏了'


@blue.errorhandler(404)
def handler_404(exception):
    return '现在是404状态，但是被捕获到了'


# ****** cookie登录 ******
@blue.route('/cookie-login', methods=['get', 'post'])
def cookie_login():
    return render_template('cookie_login.html')


@blue.route('/cookie-test', methods=['get', 'post'])
def cookie_test():
    name = request.form.get('name')
    age = request.form.get('age')

    return render_template('welcome.html', name=name, age=age)
