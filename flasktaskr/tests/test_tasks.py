# project/test_tasks.py

import os
import unittest

from project import app, db, bcrypt
from project._config import basedir
from project.models import User, Task

TEST_DB = 'test.db'

class UserTests(unittest.TestCase):
    
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

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    
    def register(self, name, email, password, confirm):
        return self.app.post('/register/', 
                data=dict(name=name, email=email, password=password, 
                confirm=confirm), follow_redirects=True
        )

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, 
            password=bcrypt.generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
    
    def create_admin_user(self):
        new_user = User(
            name='Wolverine', 
            email='wolverine@xmen.com', 
            password=bcrypt.generate_password_hash('jeanlove'), 
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
                name='Ir ao banco',
                due_date='15/11/2016',
                priority='5',
                posted_date='12/11/2016',
                status='1'), follow_redirects=True)
    
    
    #############
    ### Tests ###
    #############
    
    def test_logged_in_user_can_access_tasks_page(self):
        self.register("Asfodolo", "fodu@gmail.com", "pitaco", "pitaco")
        self.login("Asfodolo", "pitaco")
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Adicione uma nova tarefa:', response.data)

    def test_not_log_in_user_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'Voce precisa se logar primeiro.', response.data)
    
    def test_users_can_add_tasks(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'Nova tarefa criada com sucesso!', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
                       name='Ir ao banco',
                       due_date='',
                       priority='5',
                       posted_date='12/11/2016',
                       status='1'), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_task(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        response = self.app.get('complete/1', follow_redirects=True)
        self.assertIn(b'A tarefa foi marcada como completa.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        response = self.app.get('delete/1', follow_redirects=True)
        self.assertIn(b'A tarefa foi removida.', response.data)

    def test_users_cannot_complete_tasks_from_other_users(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.logout()
        self.create_user("Pituxo", "turtle@nature.com", "silvas")
        self.login("Pituxo", "silvas")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1', follow_redirects=True)
        self.assertNotIn(b'A tarefa foi marcada como completa.', response.data)
        self.assertIn(b'Voce pode atualizar somente as tuas tarefas.', response.data)
    
    def test_users_cannot_delete_tasks_from_other_users(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.logout()
        self.create_user("Pituxo", "turtle@nature.com", "silvas")
        self.login("Pituxo", "silvas")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1', follow_redirects=True)
        self.assertNotIn(b'A tarefa foi removida.', response.data)
        self.assertIn(b'Voce pode remover somente as tuas tarefas.', response.data)
        
    def test_admin_users_can_complete_tasks_from_other_users(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.logout()
        self.create_admin_user()
        self.login("Wolverine", "jeanlove")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('complete/1', follow_redirects=True)
        self.assertIn(b'A tarefa foi marcada como completa.', response.data)
    
    def test_admin_users_can_delete_tasks_from_other_users(self):
        self.create_user("Pitico", "pit@xuxo.tk", "friend")
        self.login("Pitico", "friend")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.logout()
        self.create_admin_user()
        self.login("Wolverine", "jeanlove")
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get('delete/1', follow_redirects=True)
        self.assertIn(b'A tarefa foi removida.', response.data)
        self.assertNotIn(b'Voce pode remover somente as tuas tarefas.', response.data)
    
    def test_str_representation_of_task_object(self):
        
        from datetime import date
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
        
        tasks = db.session.query(Task).all()
        for task in tasks:
            self.assertEqual(task.name, 'Correr abobalhado em circulo')

    def test_users_cannot_see_task_modify_links_for_tasks_not_created_by_them(self):
        self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.login('Aristoteles', 'poemas')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task();
        self.logout()
        self.register("OlavoCarvalho", "odec@gmail.com", "arruinaldo", 
                      "arruinaldo")
        self.login("OlavoCarvalho", "arruinaldo")
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(b'Marcar como Completa', response.data)

    def test_users_can_see_task_modify_links_for_tasks_created_by_them(self):
        self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.login('Aristoteles', 'poemas')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task();
        self.logout()
        self.register("OlavoCarvalho", "odec@gmail.com", "arruinaldo", 
                      "arruinaldo")
        self.login("OlavoCarvalho", "arruinaldo")
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)

    def test_admin_can_see_task_modify_links_for_all_tasks(self):
        self.register('Aristoteles', 'totinho@hellika.gr', 'poemas', 'poemas')
        self.login('Aristoteles', 'poemas')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task();
        self.logout()
        self.create_admin_user()
        self.login('Wolverine', 'jeanlove')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'complete/1/', response.data)
        self.assertIn(b'delete/1/', response.data)
        self.assertIn(b'complete/2/', response.data)
        self.assertIn(b'delete/2/', response.data)
        
if __name__ == "__main__":
    unittest.main()