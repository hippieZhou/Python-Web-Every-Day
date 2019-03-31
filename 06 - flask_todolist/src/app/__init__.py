from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message = '你必须登陆后才能访问该页面'
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    user = User.query.get(int(user_id))
    return user

@app.context_processor
def inject_user():
    from app.models import User
    user = User.query.first()
    return dict(user=user)

from app import views, errors,commands