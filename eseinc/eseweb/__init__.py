from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask import flash
from flask import redirect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '2de5a42478640f40a1000b7886e028eca722'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esecon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

bcrpt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

from eseweb import routes