# project/users/views.py

# Imports

from flask import Flask, flash, redirect, render_template, \
     request, session, url_for, Blueprint
from functools import wraps
from sqlalchemy.exc import IntegrityError
from flask.ext.sqlalchemy import SQLAlchemy

from .forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User

# Config

users_blueprint = Blueprint('users', __name__)

# Helper Functions

def login_required(test):
    @wraps(test)
    
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Voce precisa se logar primeiro.')
            return redirect(url_for('users.login'))
    
    return wrap

# Routes
@users_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('role', None)
    session.pop('name', None)
    flash('Voce foi deslogado. Au revoir!')
    return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            #user = db.session.query(User).filter_by( \
            #          name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash("Bem-vindo!")
                return redirect(url_for('tasks.tasks'))
            else:
                error = 'Usuario ou senha invalidos.'
        #else: -- Ja cobertos pelo Form
        #    error = 'Ambos os campos devem ser preenchidos'
    # If method = 'GET' - Se o metodo eh uma HTTP GET
    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User( 
                form.name.data,
                form.email.data, 
                bcrypt.generate_password_hash(form.password.data)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Obrigado por se registrar. Favor efetuar o login.")
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = "Usuario/email ja existem"
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)