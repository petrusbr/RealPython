# project/test_main.py

import os
import unittest

from project import app, db
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'

class MainTests(unittest.TestCase):
    
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

    # Helper methods

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), \
                              follow_redirects=True)

    #############
    ### Tests ###
    #############
    
    def test_404_error(self):
        response = self.app.get('/inexistente/')
        self.assertEquals(response.status_code, 404)
        self.assertIn(b'Desculpe. Nada aqui.', response.data)
    
    """
    def test_500_error(self):
        bad_user = User(
            name='Jeremias', 
            email='jeremias@naobatecorner.com', 
            password='python'
        )
        db.session.add(bad_user)
        db.session.commit()
        response = self.login('Jeremias', 'python')
        self.assertEquals(response.status_code, 500)
        self.assertNotIn(b'ValueError: Invalid salt', response.data)
        self.assertIn(b'Oops. Algo errado aconteceu.', response.data)
    """
    
if __name__ == "__main__":
    unittest.main()