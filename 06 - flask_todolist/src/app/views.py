from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user, logout_user
from app import app, db
from app.forms import ThingForm, RegisterForm, LoginForm
from app.models import User, Thing


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ThingForm()
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST' and form.validate_on_submit():
        user_id = current_user.id
        title = form.title.data
        text = form.text.data
        thing = Thing(user_id=user_id, title=title, text=text)
        db.session.add(thing)
        db.session.commit()
        flash('添加成功')
    page = request.args.get('page', 1, type=int)
    things = current_user.things.order_by(
        Thing.add_date.desc()).paginate(page, 2, False)
    print(things)
    return render_template('index.html', title="首页", form=form, things=things)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        user = User.query.filter_by(name=name).first()
        if user and user.check_password_hash(pwd):
            login_user(user)
            flash('登陆成功。', category='info')
            return redirect(url_for('index'))
        else:
            flash("密码或账户错误。", category='error')
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('再见！')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        pwd = form.pwd.data
        user = User(name=username, email=email)
        user.generate_password_hash(pwd)
        db.session.add(user)
        db.session.commit()
        flash('注册成功', category='info')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    thing = Thing.query.get(id)
    if thing:
        db.session.delete(thing)
        db.session.commit()
        return redirect(url_for('index'))
