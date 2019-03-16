
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
from app import db, login
import jwt


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
                     )


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_img = db.Column(
        db.String(120), default='/static/assets/avatar.png', nullable=False)
    posts = db.relationship('Post', backref=db.backref('author', lazy=True))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy=True), lazy=True
    )

    def __repr__(self):
        return "<User %r>" % self.username

    def generate_reset_password_token(self):
        token = jwt.encode(
            {'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token

    @staticmethod
    def check_reset_token(token):
        try:
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithm='HS256')
            user = User.query.filter_by(id=data['id']).first()
            return user
        except:
            return

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.count(user) > 0


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Post:{}>'.format(self.body)
