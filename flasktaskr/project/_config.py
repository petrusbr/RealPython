import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'  // Implementado Login - Tabela "users"
#PASSWORD = 'admin'
DEBUG = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'cowabanga'

DATABASE_PATH = os.path.join(basedir, DATABASE)

# database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH