from flask import render_template, flash, request, redirect, url_for
from app import app, bcrypt, db

from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user


from app.models import User
from app.email import send_reset_password_mail

from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm, PostTweetForm


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # pragraphs = [
    #     {
    #         'user': "Felix",
    #         'age': 15,
    #         'role': "engineer",
    #     },
    #     {
    #         'user': "zhanghui",
    #         'age': 15,
    #         'role': "UI test",
    #     }
    # ]
    form = PostTweetForm()

    return render_template('index.html', title='home', form=form)


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
        return redirect(url_for('login'))
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


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('Password reset mail already sent, please check your mailbox!', category='info')
    return render_template('send_password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('password reset is done, you can login now', category='info')
            return redirect(url_for('login'))
        else:
            flash('The User is not exist', category='info')
            redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

