from flask import render_template, flash
from app import app, bcrypt, db

from app.forms import RegisterFrom
from app.models import User


@app.route('/')
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
    form = RegisterFrom()
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
