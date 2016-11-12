# -*- coding: utf-8 -*-
# project/test.py

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
    
    #########
    # Setup #
    #########
    
    # executado antes de cada teste
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        
    
    # executado após cada teste
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper methods

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), \
                              follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def register(self, name, email, password, confirm):
        return self.app.post('/register/', 
                data=dict(name=name, email=email, password=password, 
                confirm=confirm), follow_redirects=True
        )

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
                name='Ir ao banco',
                due_date='15/11/2016',
                priority='5',
                posted_date='12/11/2016',
                status='1'), follow_redirects=True)
    
    # Test Methods
    
    def test_user_setup(self):
        new_user = User("platao", "platao@caverna.com", "socrates")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        #test = User.query.all()
        for t in test:
            t.name
            assert t.name == "platao"

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Por favor faca o login para acessar a tua lista de tarefas', response.data)
    
    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Usuario ou senha invalidos.', response.data)
    
    def test_users_can_login(self):
        r = self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        #print(db.session.query(User).all())
        response = self.login('Aristoteles', 'poemas')
        self.assertIn(b'Bem-vindo!', response.data)
    
    def test_invalid_form_data(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Usuario ou senha invalidos.', response.data)
    
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Favor efetuar o cadastro para acessar a lista de tarefas', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.assertIn(b'Obrigado por se registrar. Favor efetuar o login', 
                        response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.app.get('register/', follow_redirects=True)
        response = self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.assertIn(b'Usuario/email ja existem', 
                       response.data)

    def test_logged_in_user_can_logout(self):
        self.register("OlavoCarvalho", "odec@gmail.com", "arruinaldo", 
                      "arruinaldo")
        self.login("OlavoCarvalho", "arruinaldo")
        response = self.logout()
        self.assertIn(b'Voce foi deslogado. Au revoir!', 
                        response.data)

    def test_not_logged_in_user_cannot_logout(self):
        response = self.logout()
        self.assertIn(b'Voce precisa se logar primeiro.', response.data)


    def test_logged_in_user_can_access_tasks_page(self):
        self.register("Asfodolo", "fodu@gmail.com", "pitaco", "pitaco")
        self.login("Asfodolo", "pitaco")
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Adicione uma nova tarefa:', response.data)

    def test_not_log_in_user_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Voce precisa se logar primeiro.', response.data)

    def users_can_add_tasks(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'Nova tarefa criada com sucesso!', response.data)

if __name__ == "__main__":
    unittest.main()
        