# project/forms.py

from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, \
     PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class AddTaskForm(Form):
    task_id = IntegerField()
    name = StringField('Nome da Tarefa', validators=[DataRequired()])
    due_date = DateField('Data de Término (dd/mm/yyyy)',
                          validators=[DataRequired()], format='%d/%m/%Y'
                         )
    priority = SelectField('Prioridade', validators=[DataRequired()],
                            choices=[('1', '1'), ('2', '2'), ('3', '3'), 
                            ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), 
                            ('8', '8'), ('9', '9'), ('10', '10')]
                           )
    status = IntegerField('Status')


class RegisterForm(Form):
    name = StringField('Usuário', 
                        validators=[DataRequired(), Length(min=6, max=25)]
                       )
    email = StringField('Email', 
                        validators=[DataRequired(), Length(min=6, max=40)]
                       )
    password = PasswordField('Senha', 
                        validators=[DataRequired(), Length(min=6, max=40)]
                       )
    confirm = PasswordField('Digite novamente a senha', 
                        validators=[DataRequired(), EqualTo('password', 
                           message='As senhas devem ser iguais')]
                        )


class LoginForm(Form):
    name = StringField( 'Usuário',
                         validators=[DataRequired()] 
                       )
    password = PasswordField( 'Senha',
                         validators=[DataRequired()] 
                       )
    