#project/views.py - Controller
import sqlite3

from flask import Flask, flash, redirect, render_template, \
     request, session, url_for

from functools import wraps

#Configuracao

app = Flask(__name__)
app.config.from_object('_config')

# Helper Functions

def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Voce precisa se logar primeiro.')
            return redirect(url_for('login'))
    
    return wrap

# Route Handlers

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Voce foi deslogado')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
                error = 'Credenciais invalidas. Por favor, tente de novo.'
                return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash("Bem-vindo!")
            return redirect(url_for('tasks'))
    # If method = 'GET'
    return render_template('login.html')
    