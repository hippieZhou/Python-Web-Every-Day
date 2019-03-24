from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User: %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship(
        'Category', backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return 'Category:%r' % self.name


@app.route('/')
def index():
    users = User.query.all()
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('index.html', users=users, posts=posts, categories=categories)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    u1 = User(username='admin', email='admin@example.com')
    u2 = User(username='guest', email='guest@example.com')
    db.session.add_all([u1, u2])
    db.session.commit()

    py = Category(name='Python')
    p = Post(title='Hello Python!', body='Python is pretty cool', category=py)
    db.session.add_all([py, p])
    db.session.commit()

    app.run(debug=True)
