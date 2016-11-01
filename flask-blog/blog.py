# blog.py - Controller

from flask import Flask, render_template, request, session, \
     flash, redirect, url_for, g

from functools import wraps

import sqlite3
     
#Configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'dificil_adivinhar'

app = Flask(__name__)

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    

def login_required(test):
    @wraps(test)
    
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Voce precisa se logar primeiro.')
            return redirect(url_for('login'))
    
    return wrap

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
                error = 'Credenciais invalidas. Por favor, tente de novo.'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Voce foi deslogado')
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    curr = g.db.execute('select * from posts')
    posts = [dict(title=row[0], post=row[1]) for row in curr.fetchall()]
    g.db.close()
    return render_template('main.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    title = request.form['titulo']
    post = request.form['post']
    if not title or not post:
        flash("Todos os campos devem ser preenchidos. Tente de novo por favor")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?, ?)',\
             [title, post])
        g.db.commit()
        g.db.close()
        flash('Nova entrada gravada com sucesso!')
        return redirect(url_for('main'))


if __name__ == "__main__":
    app.run("0.0.0.0",8080,debug=True)