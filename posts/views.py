from django.shortcuts import render
from .models import Post

def index(request):
    latest = Post.objects.order_by('-timestamp')[:4]
    context = {
        'latest': latest,
    }
    return render(request, 'index.html', context)

def blog(request):
    return render(request, 'blog-grid.html', {})

def post(request):
    return render(request, 'blog-single.html', {})