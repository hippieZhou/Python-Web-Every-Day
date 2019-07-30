from app.libs.httper import HTTP
from flask import current_app


class YuShuBook(object):
    root_url = 'http://www.yushu.im/'
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__find_single(result)

    def __find_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __find_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(
            keyword,
            current_app.config['PER_PAGE'],
            self.calculate_start(page))
        result = HTTP.get(url)
        self.__find_collection(result)

    def calculate_start(self, page):
        return (page-1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.tital >= 1 else None
