from flask_script import Manager
from App.views import blue
from App import create_app

# 通过 App 的 __init__.py 中实例化 app 对象，来帮助 templates 目录的定位
app = create_app()
app.register_blueprint(blueprint=blue)

manager = Manager(app=app)

if __name__ == '__main__':
    manager.run()
