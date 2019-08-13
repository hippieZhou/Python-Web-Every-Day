from sqlalchemy import Column, Integer, String, Boolean, Float
from app.models.base import Base, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from app.spider.yushu_book import YuShuBook
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.enums import PendingStatus
from math import floor

from flask import current_app


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(128), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_recevice=str(self.send_counter) + '/' +
            str(self.receive_counter)
        )

    def can_send_drift(self):
        if self.beans < 1:
            return False
        sucess_gifts_count = Gift.query.filter_by(
            uid=self.id, launched=True).count()
        success_recevie_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_recevie_count / 2) <= floor(sucess_gifts_count) else False

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 既不在赠送清单，也不再心愿清单才能添加
        gifting = Gift.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()
        return not gifting and not wishing

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True
