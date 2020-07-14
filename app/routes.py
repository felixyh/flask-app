from flask import render_template, flash, request, redirect, url_for
from app import app, bcrypt, db

from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user

from app.forms import LoginForm


from app.forms import RegisterForm
from app.models import User


@app.route('/')
@login_required
def index():
    pragraphs = [
        {
            'user': "Felix",
            'age': 15,
            'role': "engineer",
        },
        {
            'user': "zhanghui",
            'age': 15,
            'role': "UI test",
        }
    ]
    return render_template('index.html', title='home', data=pragraphs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        # print(username, email, password)

        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        flash('congrats, registration success', category='success')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # check if password is matched
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # user existed and password matched
            login_user(user, remember=remember)
            flash('login success', category='info')
            # check if there's already desired next page, other than redirect to default index page
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('User not exists OR password not matched', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
