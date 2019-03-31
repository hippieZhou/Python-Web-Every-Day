from app import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin, login_user


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    # __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    pwd = db.Column(db.String(120), nullable=False)

    things = db.relationship('Thing', backref='User', lazy='dynamic')

    def __repr__(self):
        return "<User %r>" % self.name

    def generate_password_hash(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password_hash(self, pwd):
        return check_password_hash(self.pwd, pwd)


class Thing(db.Model):
    __tablename__ = 'things'
    # __table_args__ = {"useexisting": True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(20), nullable=False)
    text = db.Column(db.Text, nullable=False)
    add_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<Todo %r>" % self.id
