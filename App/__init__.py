from flask import Flask


# 为了从当前目录下去寻找 templates 目录，若从 manager.py(app.py) 中实例化 app
# 则其搜索路径为 manager.py 的同级路径，从而造成找不到 templates 的问题
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '110'
    return app
