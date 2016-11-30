from django.test import TestCase
from blog.models import Post

# Create your tests here.
class PostTests(TestCase):
    
    def test_str(self):
        meu_titulo = Post(title='Este é um título de um caso de teste básico')
        self.assertEquals(str(meu_titulo), 
                          'Este é um título de um caso de teste básico'
        )