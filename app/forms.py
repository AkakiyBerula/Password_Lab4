from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, ValidationError
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp
import email_validator
from app import db, SQLAlchemy
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=
                            [Length(min=4, max=25, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове."),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                            "Ім'я користувача може мати тільки Великі і малі латинські літери, цифри,"
                            "крапки і нижнє підкреслення.")])
    email = StringField('Email', validators=[
                        Email(message="Неправильно вказана електронна пошта."), 
                        DataRequired(message = "Це поле обов'язкове.")])
    password = PasswordField('Password', 
                            validators=[Length(min=6, 
                            message = 'Це поле має бути більше 6 символів.'), 
                            DataRequired(message = "Це поле обов'язкове."),
                            Regexp('(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}', 0,
                            "Пароль повинен включати великі і малі літери, цифру і символ (!@#$%^&*).")
                            ])
    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(message = "Це поле обов'язкове."), 
                EqualTo('password', message = "Паролі не співпадають!")])
    captcha_user = StringField('Captcha', validators=[ 
                                    DataRequired(message = "Це поле обов'язкове."),
                                    EqualTo("captcha_hidden", message = "Captcha validation failed!")])
    captcha_hidden = HiddenField('')
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Електронна пошта уже зареєстрована.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ім'я користувача уже використовується.")

class AuthorizationForm(FlaskForm):
    code = StringField('Verification', validators=[
                                            DataRequired(message = "Це поле обов'язкове")]) 
    submit = SubmitField('Confirm')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                                DataRequired(message = "Це поле обов'язкове"), 
                                Email(message="Неправильно вказана електронна пошта")])
    password = PasswordField('Password', validators=[
                                        DataRequired(message = "Це поле обов'язкове")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')