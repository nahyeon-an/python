import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '6026f889a75eae515d0f2f94f4e7d227'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login extension
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # function name of route, login_requeired 조건을 만족 못하면 여기에 설정된 route로 이동함
login_manager.login_message_category = 'info'
# mail extension
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_USERNAME'] = 'skgus923@gmail.com'
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_PASSWORD'] = 'Nahyeon9@#'
mail = Mail(app)

from flaskblog import routes