import os
from flask import Flask
from . import db
from . import auth
from . import blog

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 
    #创建Flask 实例 
    #__name__ 是当前模块的名称
    #instance_relative_config=True 表示配置文件只对实例内部有效。
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    #设置一个应用的 缺省配置
    #SECRET_KEY 用于保证数据安全的。这个key 值在发布的时候最好是随机的

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        #通过外部的传入的config.py 文件来重载缺省值
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
        #os.makedirs() 可以确保 app.instance_path 存在。 
        #Flask 不会自动 创建实例文件夹，但是必须确保创建这个文件夹，因为 SQLite 数据库文件会被 保存在里面
    except OSError:
        pass


    # 注册db
    db.init_app(app)
    #   注册用于认证的蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    
    app.add_url_rule('/', endpoint='index')
    # a simple page that says hello
    #@app.route() 创建一个简单的路由
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

    #简单讲就这三代码。在单一的app 中，flask 框架就呢个会正常运行
    #from flask import Flask
    #app = Flask(__name__)
    #@app.route("/")


    #运行设置变量
    #FLASK_APP=flaskr
    #FLASK_ENV=development
