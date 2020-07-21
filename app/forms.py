from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('email already taken!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    remember = BooleanField()
    submit = SubmitField('Login')


class PasswordResetRequestForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('User not existed!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostTweetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=30)])
    text = TextAreaField('Say something...', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Post Text')
