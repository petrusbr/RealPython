from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

from blog.models import Post

# Create your views here.
def index(request):
	ultimos_posts = Post.objects.all().order_by('-created_at')
	t = loader.get_template('blog/index.html')
	c = Context({'ultimos_posts': ultimos_posts, })
	return HttpResponse(t.render(c))