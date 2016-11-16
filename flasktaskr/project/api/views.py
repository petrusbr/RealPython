# project/api/views.py

from flask import flash, redirect, session, url_for, jsonify, \
           make_response, Blueprint
from functools import wraps

from project import db
from project.models import Task

api_blueprint = Blueprint('api', __name__)

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
                
# Routes

@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'id tarefa': result.task_id,
            'nome tarefa': result.name, 
            'data termino': str(result.due_date), 
            'prioridade': result.priority, 
            'data criacao': str(result.posted_date), 
            'status': result.status, 
            'id usuario': result.user_id
        }
        json_results.append(data)
    return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        json_result = {
            'id tarefa': result.task_id,
            'nome tarefa': result.name, 
            'data termino': str(result.due_date), 
            'prioridade': result.priority, 
            'data criacao': str(result.posted_date), 
            'status': result.status, 
            'id usuario': result.user_id
        }
        code = 200
    else:
        json_result = {"erro": "Elemento inexistente"}
        code = 404
    return make_response(jsonify(items=json_result), code)