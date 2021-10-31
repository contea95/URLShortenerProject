from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

# 현재 폴더에 db.sqlite 파일을 생성
basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')
# APP config
# DB URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 로직이 끝날 때 DB에 반영
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항 Track 안함
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# DB Secret key
app.config['SECRET_KEY'] = 'rkskekfkakqktk'

db = SQLAlchemy(app)

db.init_app(app)
db.app = app
db.create_all()
