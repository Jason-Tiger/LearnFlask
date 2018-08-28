import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
# 'sep'.join(seq)  sep 表示分隔符，可以为空格。seq 表示需要连接的元素。可以为字符串、字典、序列，元祖
#  os.path.join() 表示讲多个路径拼接成为一个路径并返回。os.path.join(‘/User/xiaohu/’，‘data.sql’,'name.txt') 
#  表示/User/xiaohu/data.sql/name.txt 

#  os.path.dirname(__file__) 表示获取当前文件夹的绝对路径

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    # tempfile.mkstemp() 表示创建一个临时文件。db_fd 表示临时文件的安全级别。 db_path 表示临时文件的路径。

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)










