# encoding: utf8
from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
import settings

# 生成 Flask 类
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# 设置网站是否为 DEBUG 模式
app.debug = True

# 设置会话密钥
app.secret_key = '\xb7Y\x9a\xbb\xdcH\xb8[\xa7[\xe8:\xfa\xac\t\xf5\x89\xb0\x8e\xc9H\xeb\x08\xd2'

from app import views