from flask import g, jsonify
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.book import Book
from app.models.gift import Gift
from app.libs.error_code import DuplicateGift, Success

api = Redprint('gift')


@api.route('/<isbn>', methods=['POST'])
@auth.login_required
def create(isbn):
    uid = g.user.id
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()
        gitf = Gift.query.filter_by(isbn=isbn, uid=uid).first()
        if gitf:
            raise DuplicateGift()
        gift = Gift()
        gitf.isbn = isbn
        gift.uid = uid
        db.session.add(gitf)
    return Success()
