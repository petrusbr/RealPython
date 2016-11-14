# project/users/forms.py

# Imports

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm(Form):
    name = StringField('Usuario', 
                        validators=[DataRequired(), Length(min=6, max=25)]
                       )
    email = StringField('Email', 
                        validators=[DataRequired(), Email(), Length(min=6, max=40)]
                       )
    password = PasswordField('Senha', 
                        validators=[DataRequired(), Length(min=6, max=40)]
                       )
    confirm = PasswordField('Digite novamente a senha', 
                        validators=[DataRequired(), EqualTo('password', 
                           message='As senhas devem ser iguais')]
                        )

class LoginForm(Form):
    name = StringField( 'Usuario',
                         validators=[DataRequired()] 
                       )
    password = PasswordField( 'Senha',
                         validators=[DataRequired()] 
                       )