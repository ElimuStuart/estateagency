from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Post

def index(request):
    latest = Post.objects.order_by('-timestamp')[:4]
    context = {
        'latest': latest,
    }
    return render(request, 'index.html', context)

def blog(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 6)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'page_request_var': page_request_var,
        'post_list': paginated_queryset,
    }
    return render(request, 'blog-grid.html', context)

def post(request, id):
    return render(request, 'blog-single.html', {})