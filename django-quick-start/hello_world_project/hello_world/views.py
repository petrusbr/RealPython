from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from datetime import datetime

# Create your views here.
def index(request):
    return HttpResponse("<html><body>Olá, 'Mundo'!</body></html>")

def about(request):
    return HttpResponse("""Esta é a pagina Sobre. Desejar retornar à
           página principal? <a href='/'>Pagina Principal</a>""")

def better(request):
    t = loader.get_template('betterhello.html')
    c = Context({'hora_atual': datetime.now(), })
    return HttpResponse(t.render(c))