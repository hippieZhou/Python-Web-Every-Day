from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[
                             DataRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password', validators=[
                            DataRequired(), EqualTo('password')])
    # 用于检测是否是机器人
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        检查函数定义格式：validate__属性名称
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        """
        检查函数定义格式：validate__属性名称
        """
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Emali alreayd taken.")


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[
                           DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Password:', validators=[
                             DataRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit = SubmitField('Send')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email not exists.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:', validators=[
                             DataRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password', validators=[
                            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostTweetForm(FlaskForm):
    text = TextAreaField('Say something...', validators=[
                         DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Post Text')


class UploadPhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')
