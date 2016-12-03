from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import get_object_or_404

from blog.models import Post


def encode_url(url):
    return url.replace(' ', '_')


# Create your views here.
def index(request):
    ultimos_posts = Post.objects.all().order_by('-created_at')
    posts_populares = Post.objects.order_by('-views')[:5]
    t = loader.get_template('blog/index.html')
    context_dict = {
        'ultimos_posts': ultimos_posts,
        'posts_populares': posts_populares,
    }
    for post in ultimos_posts:
        post.url = encode_url(post.title)
    for post in posts_populares:
        post.url = encode_url(post.title)
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def post(request, post_url):
    single_post = get_object_or_404(Post,
                                    title=post_url.replace('_', ' '))
    single_post.views += 1
    single_post.save()
    t = loader.get_template('blog/post.html')
    c = Context({'single_post': single_post, })
    return HttpResponse(t.render(c))
