#project/views.py - Controller
import sqlite3

from flask import Flask, flash, redirect, render_template, \
     request, session, url_for, g

from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

#Configuracao

app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from models import Task, User

# Helper Functions

"""
def connect_db():
	return sqlite3.connect(app.config['DATABASE_PATH'])
"""

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
    session.pop('user_id', None)
    flash('Voce foi deslogado. Au revoir!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['name']).first()
            #user = db.session.query(User).filter_by( \
            #          name=request.form['name']).first()
            if user is not None and user.password == request.form['password']:
                session['logged_in'] = True
                session['user_id'] = user.id
                flash("Bem-vindo!")
                return redirect(url_for('tasks'))
            else:
                error = 'Usuario ou senha invalidos.'
        else:
            error = 'Ambos os campos devem ser preenchidos'
    # If method = 'GET' - Se o metodo eh uma HTTP GET
    return render_template('login.html', form=form, error=error)
    
@app.route('/tasks/')
@login_required
def tasks():
    """  /* SQLite code */
    g.db = connect_db()
    cur = g.db.execute('select name, due_date, priority, task_id from tasks where status=1')
    open_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) 
        for row in cur.fetchall()
    ]
    
    cur = g.db.execute('select name, due_date, priority, task_id from tasks where status=0')
    closed_tasks = [
        dict(name=row[0], due_date=row[1], priority=row[2], task_id=row[3]) 
        for row in cur.fetchall()
    ]
    g.db.close()
    """
    
    return render_template('tasks.html',
                           form = AddTaskForm(request.form),
                           open_tasks=open_tasks(),
                           closed_tasks=closed_tasks())
    
# Add New Tasks
@app.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    
    """ - /* SQLite code */
    g.db = connect_db()
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash("Todos os campos devem ser preenchidos. Por favor, tente de novo")
        return redirect(url_for('tasks'))
    else:
        g.db.execute('insert into tasks (name, due_date, priority, status)' \
             'values (?, ?, ?, 1)', [
                 request.form['name'], 
                 request.form['due_date'], 
                 request.form['priority']
                 ]
        )
        g.db.commit()
        g.db.close()
        flash("Nova tarefa criada com sucesso!")
        return redirect(url_for('tasks'))
    """
    error = None
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task( form.name.data,
                             form.due_date.data,
                             form.priority.data,
                             datetime.utcnow(),
                             '1', 
                             session['user_id']
                            )
            db.session.add(new_task)
            db.session.commit()
            flash("Nova tarefa criada com sucesso!")
            return redirect(url_for('tasks'))
        else:
            flash_errors(form=form)
            #return render_template('tasks.html', form=form, error=error)
    return render_template( 'tasks.html', 
                            form=form, 
                            error=error,
                            open_tasks = open_tasks(), 
                            closed_tasks = closed_tasks()
                           )
        
# Mark tasks as complete
@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    """  /* SQLite code */
    g.db = connect_db()
    g.db.execute('update tasks set status = 0 where task_id=' + str(task_id))
    g.db.commit()
    g.db.close()
    """
    
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
    db.session.commit()
    flash("A tarefa foi marcada como completa.")
    return redirect(url_for('tasks'))

# Delete Tasks
@app.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):
    """  /* SQLite code */
    g.db = connect_db()
    g.db.execute('delete from tasks where task_id=' + str(task_id))
    g.db.commit()
    g.db.close()
    """
    
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash("A tarefa foi removida.")
    return redirect(url_for('tasks'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User( 
                form.name.data,
                form.email.data, 
                form.password.data
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Obrigado por se registrar. Favor efetuar o login.")
                return redirect(url_for('login'))
            except IntegrityError:
                error = "Usuario/email já existem"
                return render_template('register.html', form=form, error=error)
    return render_template('register.html', form=form, error=error)

def open_tasks():
    return db.session.query(Task).filter_by(status='1') \
               .order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0') \
                .order_by(Task.due_date.asc())

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Erro no campo %s - %s" % (
                   getattr(form, field).label.text, 'Erro!'))