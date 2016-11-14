# project/tasks/views.py

# Imports

from datetime import datetime
from flask import Flask, flash, redirect, render_template, \
     request, session, url_for, Blueprint
from functools import wraps

from .forms import AddTaskForm
from project import db
from project.models import Task

# Config

tasks_blueprint = Blueprint('tasks', __name__)

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

# Routes

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():

    return render_template('tasks.html',
                           form = AddTaskForm(request.form),
                           open_tasks=open_tasks(),
                           closed_tasks=closed_tasks())

@tasks_blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
def new_task():
    
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
            return redirect(url_for('tasks.tasks'))
        else:
            flash_errors(form=form)
            #return render_template('tasks.html', form=form, error=error)
    return render_template( 'tasks.html', 
                            form=form, 
                            error=error,
                            open_tasks = open_tasks(), 
                            closed_tasks = closed_tasks()
                           )

@tasks_blueprint.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):

    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.update({"status":"0"})
        db.session.commit()
        flash("A tarefa foi marcada como completa.")
        return redirect(url_for('tasks.tasks'))
    else:
        flash('Voce pode atualizar somente as tuas tarefas.')
        return redirect(url_for('tasks.tasks'))
    

# Delete Tasks
@tasks_blueprint.route('/delete/<int:task_id>/')
@login_required
def delete_entry(task_id):

    new_id = task_id
    task = db.session.query(Task).filter_by(task_id=new_id)
    if session['user_id'] == task.first().user_id or session['role'] == "admin":
        task.delete()
        db.session.commit()
        flash("A tarefa foi removida.")
        return redirect(url_for('tasks.tasks'))
    else:
        flash('Voce pode remover somente as tuas tarefas.')
        return redirect(url_for('tasks.tasks'))