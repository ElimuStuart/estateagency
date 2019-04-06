from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def blog(request):
    return render(request, 'blog-grid.html', {})

def post(request):
    return render(request, 'blog-single.html', {})