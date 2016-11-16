# project/test_api.py

import os
import unittest
from datetime import date

from project import app, db
from project._config import basedir
from project.models import Task

TEST_DB = 'test.db'

class APITests(unittest.TestCase):
    
    #########
    # Setup #
    #########
    
    # executado antes de cada teste
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        
    
    # executado após cada teste
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    ##################
    # Helper Methods #
    ##################
    
    def add_tasks(self):
        db.session.add(
            Task(
                "Correr abobalhado em circulo",
                date(2016, 11, 15),
                10,
                date(2016, 11, 14),
                1,
                1
            )
        )
        db.session.commit()
        
        db.session.add(
            Task(
                "Comprar livro na Amazon",
                date(2016, 11, 20),
                10,
                date(2016, 11, 16),
                1,
                1
            )
        )
        db.session.commit()
    
    #########
    # Tests #
    #########
    
    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Correr abobalhado em circulo', response.data)
        self.assertIn(b'Comprar livro na Amazon', response.data)
    
    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertNotIn(b'Correr abobalhado em circulo', response.data)
        self.assertIn(b'Comprar livro na Amazon', response.data)
    
    def test_invalid_resource_endpoint_returns_error(self):
        self.add_tasks()
        response = self.app.get('api/v1/tasks/227', follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Elemento inexistente', response.data)

if __name__ == "__main__":
    unittest.main()