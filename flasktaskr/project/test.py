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

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), \
                              follow_redirects=True)
    
    def register(self, name, email, password, confirm):
        return self.app.post('/register/', 
                data=dict(name=name, email=email, password=password, 
                confirm=confirm), follow_redirects=True
        )
    
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

if __name__ == "__main__":
    unittest.main()
        