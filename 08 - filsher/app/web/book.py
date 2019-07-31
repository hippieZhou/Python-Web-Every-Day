from . import web
from flask import request, current_app, url_for, render_template, flash
from flask_login import current_user
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.viewmodels.book import BookViewModel, BookCollection
from app.viewmodels.trade import TradeInfo
from app.models.gift import Gift
from app.models.wish import Wish


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_app.is_authenticated:
        if Gift.query.filter_by(
                uid=current_app.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(
                uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html',
                           book=book,
                           wished=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts)
